"""
Patient API routes.
"""
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from app.models.patient_model import (
    PatientCreateRequest,
    PatientUpdateRequest,
    PatientResponse,
    DashboardResponse,
    LLMOutputModel,
    AuditLogModel,
    VitalsModel
)
from app.utils.validators import validate_patient_input
from app.services.rules_engine import RulesEngine
from app.services.scoring_service import ScoringEngine
from app.services.alert_service import AlertService
from app.services.llm_service import LLMService
from app.db import mongo

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["patients"],
    responses={404: {"description": "Not found"}}
)

# Initialize LLM service
llm_service = LLMService()


async def process_patient_vitals(
    vitals: VitalsModel,
    symptoms: list = None,
    notes: str = ""
) -> tuple:
    """
    Process patient vitals through scoring pipeline.
    
    Returns:
        (score, severity, alert, llm_output, audit_log)
    """
    # Validate vitals
    validate_patient_input(vitals)
    
    # Step 1: Run critical rules engine
    is_critical, triggered_rules = RulesEngine.evaluate_critical_rules(
        heart_rate=vitals.heart_rate,
        spo2=vitals.spo2,
        systolic_bp=vitals.systolic_bp,
        temperature=vitals.temperature,
        respiratory_rate=vitals.respiratory_rate
    )
    
    # Step 1b: Check HIGH-risk rules if not critical
    is_high_risk = False
    high_risk_rules = []
    if not is_critical:
        is_high_risk, high_risk_rules = RulesEngine.evaluate_high_risk_rules(
            heart_rate=vitals.heart_rate,
            spo2=vitals.spo2,
            systolic_bp=vitals.systolic_bp,
            temperature=vitals.temperature,
            respiratory_rate=vitals.respiratory_rate
        )
    
    # Step 1c: Check MODERATE rules if not critical or high-risk
    is_moderate = False
    moderate_rules = []
    if not is_critical and not is_high_risk:
        is_moderate, moderate_rules = RulesEngine.evaluate_moderate_rules(
            heart_rate=vitals.heart_rate,
            spo2=vitals.spo2,
            systolic_bp=vitals.systolic_bp,
            temperature=vitals.temperature,
            respiratory_rate=vitals.respiratory_rate
        )
    
    # Step 2: Run scoring engine
    final_score, score_breakdown = ScoringEngine.compute_score(
        heart_rate=vitals.heart_rate,
        spo2=vitals.spo2,
        systolic_bp=vitals.systolic_bp,
        diastolic_bp=vitals.diastolic_bp,
        temperature=vitals.temperature,
        respiratory_rate=vitals.respiratory_rate,
        symptoms=symptoms or []
    )
    
    # Step 3: Apply rule-based override logic (rules take precedence over score)
    if is_critical:
        severity = "CRITICAL"
        triggered_rules.extend(high_risk_rules)  # Include high-risk rules for reference
    elif is_high_risk:
        severity = "HIGH"
        triggered_rules = high_risk_rules
    elif is_moderate:
        # Escalate to MODERATE if score would be STABLE, but preserve if score is already MODERATE or higher
        score_severity = ScoringEngine.map_severity(final_score)
        if score_severity == "STABLE":
            severity = "MODERATE"
        else:
            severity = score_severity
        triggered_rules = moderate_rules
    else:
        # Use score-based severity if no rules triggered
        severity = ScoringEngine.map_severity(final_score)
    
    # Step 4: Generate alert
    alert = AlertService.generate_alert(severity, vitals.spo2)
    
    # Step 5: Call LLM
    patient_data = {
        "spo2": vitals.spo2,
        "hr": vitals.heart_rate,
        "systolic_bp": vitals.systolic_bp,
        "diastolic_bp": vitals.diastolic_bp,
        "temperature": vitals.temperature,
        "rr": vitals.respiratory_rate,
        "symptoms": symptoms or [],
        "notes": notes,
        "severity": severity,
        "score": final_score
    }
    
    llm_output = await llm_service.generate_explanation(patient_data)
    llm_output_model = LLMOutputModel(**llm_output)
    
    # Step 6: Create audit log
    audit_log = AuditLogModel(
        rules_triggered=triggered_rules,
        score_breakdown=score_breakdown,
        final_score=final_score
    )
    
    # CRITICAL SAFETY CHECKS - Healthcare System Integrity
    assert alert is not None, "🔴 CRITICAL: Alert cannot be None"
    assert llm_output_model is not None, "🔴 CRITICAL: LLM output cannot be None"
    assert severity in ["CRITICAL", "HIGH", "MODERATE", "STABLE"], f"🔴 CRITICAL: Invalid severity '{severity}'"
    assert llm_output_model.explanation, "🔴 CRITICAL: LLM explanation cannot be empty"
    assert llm_output_model.suggested_actions is not None, "🔴 CRITICAL: Suggested actions cannot be None"
    
    logger.info(f"✅ SAFETY CHECKS PASSED: Severity={severity}, Alert set, LLM output valid")
    
    return final_score, severity, alert, llm_output_model, audit_log


@router.post("/patient", response_model=PatientResponse)
async def create_patient(request: PatientCreateRequest):
    """
    Create a new patient record.
    
    Processing flow:
    1. Validate input
    2. Run rules engine
    3. Run scoring engine
    4. Apply override logic
    5. Generate alert
    6. Call LLM
    7. Store in MongoDB
    8. Return response
    """
    try:
        # Process vitals
        score, severity, alert, llm_output, audit_log = await process_patient_vitals(
            vitals=request.vitals,
            symptoms=request.symptoms,
            notes=request.notes
        )
        
        # Create patient document
        timestamp = datetime.utcnow()
        patient_doc = {
            "patient_id": request.patient_id,
            "age": request.age,
            "gender": request.gender,
            "ward": request.ward,
            "room": request.room,
            "vitals": request.vitals.model_dump(),
            "symptoms": request.symptoms,
            "notes": request.notes,
            "score": score,
            "severity": severity,
            "alert": alert,
            "llm_output": llm_output.model_dump(),
            "audit_log": audit_log.model_dump(),
            "timestamp": timestamp
        }
        
        # Store in MongoDB
        await mongo.insert_patient(patient_doc)
        
        # Return response
        response = PatientResponse(
            patient_id=request.patient_id,
            age=request.age,
            gender=request.gender,
            ward=request.ward,
            room=request.room,
            vitals=request.vitals,
            symptoms=request.symptoms,
            notes=request.notes,
            score=score,
            severity=severity,
            alert=alert,
            llm_output=llm_output,
            audit_log=audit_log,
            timestamp=timestamp
        )
        
        logger.info(f"Patient created: {request.patient_id} - Severity: {severity}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating patient: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating patient: {str(e)}"
        )


@router.put("/patient/{patient_id}", response_model=PatientResponse)
async def update_patient(patient_id: str, request: PatientUpdateRequest):
    """
    Update patient vitals and recompute assessment.
    """
    try:
        logger.info(f"🔄 Update request for patient: {patient_id}")
        logger.debug(f"📊 Update payload: {request.model_dump()}")
        
        # Get existing patient
        existing_patient = await mongo.get_patient_by_id(patient_id)
        if not existing_patient:
            logger.error(f"❌ Patient not found: {patient_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient {patient_id} not found"
            )
        
        logger.info(f"✓ Found existing patient: {patient_id}")
        
        # Process vitals
        score, severity, alert, llm_output, audit_log = await process_patient_vitals(
            vitals=request.vitals,
            symptoms=request.symptoms or existing_patient.get("symptoms", []),
            notes=request.notes or existing_patient.get("notes", "")
        )
        
        logger.info(f"✓ Processed vitals - Score: {score}, Severity: {severity}")
        
        # Update document
        timestamp = datetime.utcnow()
        update_doc = {
            "vitals": request.vitals.model_dump(),
            "score": score,
            "severity": severity,
            "alert": alert,
            "llm_output": llm_output.model_dump(),
            "audit_log": audit_log.model_dump(),
            "timestamp": timestamp
        }
        
        if request.symptoms is not None:
            update_doc["symptoms"] = request.symptoms
        
        if request.notes is not None:
            update_doc["notes"] = request.notes
        
        result = await mongo.update_patient(patient_id, update_doc)
        logger.info(f"✓ Database update result - matched: {result.matched_count}, modified: {result.modified_count}")
        
        if result.matched_count == 0:
            logger.error(f"❌ No patient matched for update: {patient_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient {patient_id} not found in database"
            )
        
        # Return updated response
        response = PatientResponse(
            patient_id=existing_patient["patient_id"],
            age=existing_patient["age"],
            gender=existing_patient["gender"],
            ward=existing_patient.get("ward", ""),
            room=existing_patient.get("room", ""),
            vitals=request.vitals,
            symptoms=request.symptoms or existing_patient.get("symptoms", []),
            notes=request.notes or existing_patient.get("notes", ""),
            score=score,
            severity=severity,
            alert=alert,
            llm_output=llm_output,
            audit_log=audit_log,
            timestamp=timestamp
        )
        
        logger.info(f"✅ Patient updated successfully: {patient_id} - Severity: {severity}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating patient: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating patient: {str(e)}"
        )


@router.get("/patient/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str):
    """
    Get patient details by ID.
    """
    try:
        patient = await mongo.get_patient_by_id(patient_id)
        
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient {patient_id} not found"
            )
        
        # Convert MongoDB document to response
        response = PatientResponse(
            patient_id=patient["patient_id"],
            age=patient["age"],
            gender=patient["gender"],
            ward=patient.get("ward", ""),
            room=patient.get("room", ""),
            vitals=VitalsModel(**patient["vitals"]),
            symptoms=patient.get("symptoms", []),
            notes=patient.get("notes", ""),
            score=patient["score"],
            severity=patient["severity"],
            alert=patient["alert"],
            llm_output=LLMOutputModel(**patient["llm_output"]),
            audit_log=AuditLogModel(**patient["audit_log"]),
            timestamp=patient["timestamp"]
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving patient: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving patient: {str(e)}"
        )


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard():
    """
    Get dashboard with patients grouped by severity.
    """
    try:
        # Step 1: Fetch all patients from database (single query)
        patients = await mongo.get_all_patients()
        
        # Handle None or empty response
        if patients is None:
            patients = []
        
        logger.info(f"🔍 Dashboard: Retrieved {len(patients)} patients from database")
        
        # Step 2: Initialize groups
        critical = []
        high = []
        moderate = []
        stable = []
        
        # Step 3: Group patients by severity (normalize to lowercase)
        skipped_patients = 0
        for idx, patient in enumerate(patients):
            try:
                # Normalize severity to lowercase (critical safety check)
                severity_raw = patient.get("severity", "STABLE")
                severity_lower = str(severity_raw).lower()
                
                logger.debug(f"Processing patient {idx+1}/{len(patients)}: {patient.get('patient_id')} -> severity={severity_lower}")
                
                response = PatientResponse(
                    patient_id=patient["patient_id"],
                    age=patient["age"],
                    gender=patient["gender"],
                    ward=patient.get("ward", ""),
                    room=patient.get("room", ""),
                    vitals=VitalsModel(**patient["vitals"]),
                    symptoms=patient.get("symptoms", []),
                    notes=patient.get("notes", ""),
                    score=patient["score"],
                    severity=severity_lower,  # Return lowercase severity
                    alert=patient["alert"],
                    llm_output=LLMOutputModel(**patient["llm_output"]),
                    audit_log=AuditLogModel(**patient["audit_log"]),
                    timestamp=patient["timestamp"]
                )
                
                # Group by lowercase severity - CRITICAL LOGIC
                if severity_lower == "critical":
                    critical.append(response)
                elif severity_lower == "high":
                    high.append(response)
                elif severity_lower == "moderate":
                    moderate.append(response)
                else:  # Default to stable for any other severity
                    stable.append(response)
                    
            except Exception as e:
                logger.error(f"❌ Error processing patient {patient.get('patient_id', 'UNKNOWN')}: {str(e)}")
                skipped_patients += 1
                continue
        
        # Step 4: Sort each group by score descending
        critical.sort(key=lambda x: x.score, reverse=True)
        high.sort(key=lambda x: x.score, reverse=True)
        moderate.sort(key=lambda x: x.score, reverse=True)
        stable.sort(key=lambda x: x.score, reverse=True)
        
        # Step 5: Calculate total from grouped data (SINGLE SOURCE OF TRUTH)
        total = len(critical) + len(high) + len(moderate) + len(stable)
        
        # Step 6: Validate total calculation
        expected_total = len(patients) - skipped_patients
        if total != expected_total:
            logger.warning(f"⚠️  Total mismatch! Calculated={total}, Expected={expected_total}, Skipped={skipped_patients}")
        
        # Step 7: Log final state
        logger.info(
            f"✅ Dashboard: Total={total} (Critical={len(critical)}, High={len(high)}, "
            f"Moderate={len(moderate)}, Stable={len(stable)}) | Skipped={skipped_patients}"
        )
        
        # Step 8: Assert total always equals sum
        assert total == (len(critical) + len(high) + len(moderate) + len(stable)), \
            f"CRITICAL BUG: Total={total} does NOT match sum of groups!"
        
        # Step 9: Return response
        return DashboardResponse(
            total=total,
            critical=critical,
            high=high,
            moderate=moderate,
            stable=stable
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"❌ Error retrieving dashboard: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving dashboard: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "VitalTriage API",
        "version": "1.0.0"
    }
