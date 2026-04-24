"""
Pydantic models for patient data validation and serialization.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class VitalsModel(BaseModel):
    """Patient vital signs."""
    heart_rate: Optional[float] = Field(None, ge=30, le=200, description="Heart rate in bpm")
    spo2: Optional[float] = Field(None, ge=0, le=100, description="Oxygen saturation percentage")
    systolic_bp: Optional[float] = Field(None, ge=70, le=200, description="Systolic blood pressure")
    diastolic_bp: Optional[float] = Field(None, ge=40, le=130, description="Diastolic blood pressure")
    temperature: Optional[float] = Field(None, ge=95, le=110, description="Temperature in Fahrenheit")
    respiratory_rate: Optional[float] = Field(None, ge=10, le=40, description="Respiratory rate in breaths/min")

    class Config:
        json_schema_extra = {
            "example": {
                "heart_rate": 78,
                "spo2": 96,
                "systolic_bp": 120,
                "diastolic_bp": 80,
                "temperature": 98.6,
                "respiratory_rate": 18
            }
        }


class LLMOutputModel(BaseModel):
    """LLM-generated explanation and suggestions."""
    explanation: str = Field(..., description="Explanation of patient's condition")
    suggested_actions: List[str] = Field(default_factory=list, description="Suggested immediate actions")

    class Config:
        json_schema_extra = {
            "example": {
                "explanation": "Patient has stable vitals with normal oxygen saturation.",
                "suggested_actions": ["Continue monitoring", "Ensure hydration"]
            }
        }


class AuditLogModel(BaseModel):
    """Audit trail for patient assessment."""
    rules_triggered: List[str] = Field(default_factory=list, description="List of triggered critical rules")
    score_breakdown: dict = Field(default_factory=dict, description="Score contribution by each vital")
    final_score: float = Field(default=0, description="Final computed risk score")


class PatientCreateRequest(BaseModel):
    """Request model for creating a patient."""
    patient_id: str = Field(..., description="Unique patient identifier")
    age: int = Field(..., ge=0, le=150, description="Patient age in years")
    gender: str = Field(..., description="Patient gender")
    ward: str = Field(default="", description="Hospital ward")
    room: str = Field(default="", description="Room number")
    vitals: VitalsModel
    symptoms: List[str] = Field(default_factory=list, description="List of reported symptoms")
    notes: str = Field(default="", description="Additional clinical notes")

    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "P001",
                "age": 65,
                "gender": "M",
                "vitals": {
                    "heart_rate": 88,
                    "spo2": 94,
                    "systolic_bp": 140,
                    "diastolic_bp": 90,
                    "temperature": 99.5,
                    "respiratory_rate": 20
                },
                "symptoms": ["fever", "chest pain"],
                "notes": "Patient reports mild discomfort"
            }
        }


class PatientUpdateRequest(BaseModel):
    """Request model for updating a patient."""
    vitals: VitalsModel
    symptoms: Optional[List[str]] = None
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "vitals": {
                    "heart_rate": 85,
                    "spo2": 95,
                    "systolic_bp": 130,
                    "diastolic_bp": 85,
                    "temperature": 98.6,
                    "respiratory_rate": 18
                }
            }
        }


class PatientResponse(BaseModel):
    """Response model for patient data."""
    patient_id: str
    age: int
    gender: str
    ward: str = Field(default="", description="Hospital ward")
    room: str = Field(default="", description="Room number")
    vitals: VitalsModel
    symptoms: List[str]
    notes: str
    score: float
    severity: str  # CRITICAL, HIGH, MODERATE, STABLE
    alert: str
    llm_output: LLMOutputModel
    audit_log: AuditLogModel
    timestamp: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "patient_id": "P001",
                "age": 65,
                "gender": "M",
                "vitals": {
                    "heart_rate": 88,
                    "spo2": 94,
                    "systolic_bp": 140,
                    "diastolic_bp": 90,
                    "temperature": 99.5,
                    "respiratory_rate": 20
                },
                "symptoms": ["fever"],
                "notes": "Initial assessment",
                "score": 55,
                "severity": "MODERATE",
                "alert": "Close monitoring needed",
                "llm_output": {
                    "explanation": "Patient shows elevated vitals.",
                    "suggested_actions": ["Monitor closely", "Administer fluids"]
                },
                "audit_log": {
                    "rules_triggered": [],
                    "score_breakdown": {"spo2": 30, "bp": 20},
                    "final_score": 55
                },
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class DashboardResponse(BaseModel):
    """Dashboard response grouped by severity."""
    total: int = Field(default=0, description="Total count of all patients")
    critical: List[PatientResponse] = Field(default_factory=list)
    high: List[PatientResponse] = Field(default_factory=list)
    moderate: List[PatientResponse] = Field(default_factory=list)
    stable: List[PatientResponse] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "total": 0,
                "critical": [],
                "high": [],
                "moderate": [],
                "stable": []
            }
        }
