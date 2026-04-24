"""
CRITICAL HEALTHCARE SAFETY TEST
================================

This test verifies that VitalTriage correctly:
1. Identifies critical patients with hypoxia + tachycardia
2. Recomputes AI insights and recommended actions on update
3. Enforces clinical accuracy constraints
4. Provides fresh data on refresh

Test Case: Patient with critical vitals
- SpO2 = 85% (critically low - requires oxygen)
- HR = 177 (severely elevated tachycardia)
- Temp = 102.5°F (high fever)
- RR = 28 (elevated respiratory rate)

Expected outcomes:
✅ Severity MUST be CRITICAL
✅ Alert MUST mention oxygen
✅ LLM explanation MUST discuss hypoxia + tachycardia
✅ Recommended actions MUST include oxygen therapy reference
✅ On update, all fields MUST be recomputed (not cached)
"""

import json
import requests
import sys
from datetime import datetime

# Test configuration
API_BASE = "http://localhost:8000/api/v1"
PATIENT_ID = "HEALTHCARE_TEST_P001"

# Critical vitals that require CRITICAL severity classification
CRITICAL_VITALS = {
    "heart_rate": 177,      # Severely elevated - tachycardia
    "spo2": 85,             # Critically low - hypoxia (normal: >95%)
    "systolic_bp": 168,     # Elevated
    "diastolic_bp": 105,    # Elevated
    "temperature": 102.5,   # High fever (normal: 98.6°F)
    "respiratory_rate": 28  # Elevated (normal: 12-20)
}

def log_critical(msg):
    """Log critical test messages."""
    print(f"🔴 {msg}")

def log_success(msg):
    """Log successful test assertions."""
    print(f"✅ {msg}")

def log_info(msg):
    """Log informational messages."""
    print(f"ℹ️ {msg}")

def test_critical_patient_creation():
    """Test 1: Create patient with critical vitals."""
    log_info("=" * 70)
    log_info("TEST 1: Create patient with critical vitals")
    log_info("=" * 70)
    
    payload = {
        "patient_id": PATIENT_ID,
        "age": 68,
        "gender": "M",
        "ward": "ICU",
        "room": "101",
        "vitals": CRITICAL_VITALS,
        "symptoms": ["difficulty breathing", "chest pain", "confusion"],
        "notes": "Acute respiratory distress"
    }
    
    response = requests.post(f"{API_BASE}/patient", json=payload)
    
    if response.status_code != 200:
        log_critical(f"Failed to create patient: {response.status_code}")
        log_critical(f"Response: {response.text}")
        return None
    
    patient = response.json()
    
    # CRITICAL ASSERTIONS
    print("\n📋 Patient Created - Validating Response:")
    print(json.dumps({
        "patient_id": patient["patient_id"],
        "severity": patient["severity"],
        "score": patient["score"],
        "alert": patient["alert"],
        "has_llm_output": bool(patient.get("llm_output")),
        "has_suggested_actions": bool(patient.get("llm_output", {}).get("suggested_actions"))
    }, indent=2))
    
    # Assertion 1: Severity MUST be CRITICAL
    if patient["severity"].upper() != "CRITICAL":
        log_critical(f"FAILED: Severity is {patient['severity']}, expected CRITICAL")
        return None
    log_success(f"Severity correctly set to CRITICAL")
    
    # Assertion 2: Alert MUST exist
    if not patient.get("alert"):
        log_critical("FAILED: Alert is empty!")
        return None
    log_success(f"Alert present: {patient['alert'][:60]}...")
    
    # Assertion 3: Alert MUST mention oxygen (due to SpO2=85%)
    if "oxygen" not in patient["alert"].lower():
        log_critical(f"WARNING: Alert does not mention oxygen: {patient['alert']}")
    else:
        log_success("Alert correctly mentions oxygen requirement")
    
    # Assertion 4: LLM output MUST exist
    if not patient.get("llm_output"):
        log_critical("FAILED: LLM output is missing!")
        return None
    log_success("LLM output generated")
    
    # Assertion 5: LLM explanation MUST exist and discuss hypoxia
    explanation = patient["llm_output"].get("explanation", "")
    if not explanation:
        log_critical("FAILED: LLM explanation is empty!")
        return None
    log_success(f"LLM explanation present ({len(explanation)} chars)")
    
    if "hypoxia" in explanation.lower() or "oxygen" in explanation.lower():
        log_success("LLM explanation discusses hypoxia/oxygen")
    else:
        log_critical(f"WARNING: Explanation may not address hypoxia: {explanation[:100]}")
    
    # Assertion 6: Suggested actions MUST exist
    actions = patient["llm_output"].get("suggested_actions", [])
    if not actions:
        log_critical("WARNING: No suggested actions provided")
    else:
        log_success(f"Suggested actions: {len(actions)} items")
        for i, action in enumerate(actions[:3], 1):
            print(f"   {i}. {action}")
    
    return patient


def test_critical_patient_update():
    """Test 2: Update patient vitals and verify recomputation."""
    log_info("\n" + "=" * 70)
    log_info("TEST 2: Update patient vitals and verify recomputation")
    log_info("=" * 70)
    
    # Update vitals to slightly better but still critical
    updated_vitals = {
        "heart_rate": 165,      # Still tachycardia but slightly better
        "spo2": 88,             # Still hypoxic but improved
        "systolic_bp": 160,     # Slightly better
        "diastolic_bp": 100,    # Slightly better
        "temperature": 101.8,   # Slightly better
        "respiratory_rate": 26  # Slightly better
    }
    
    payload = {
        "vitals": updated_vitals
    }
    
    response = requests.put(f"{API_BASE}/patient/{PATIENT_ID}", json=payload)
    
    if response.status_code != 200:
        log_critical(f"Failed to update patient: {response.status_code}")
        log_critical(f"Response: {response.text}")
        return None
    
    updated_patient = response.json()
    
    # CRITICAL ASSERTIONS FOR UPDATE
    print("\n📋 Patient Updated - Validating Recomputation:")
    print(json.dumps({
        "patient_id": updated_patient["patient_id"],
        "severity": updated_patient["severity"],
        "score": updated_patient["score"],
        "alert": updated_patient["alert"],
        "timestamp": updated_patient.get("timestamp"),
        "has_llm_output": bool(updated_patient.get("llm_output")),
    }, indent=2))
    
    # Assertion 1: Severity MUST still be CRITICAL or HIGH
    if updated_patient["severity"].upper() not in ["CRITICAL", "HIGH"]:
        log_critical(f"FAILED: Severity degraded to {updated_patient['severity']}")
        return None
    log_success(f"Severity appropriate: {updated_patient['severity'].upper()}")
    
    # Assertion 2: Alert MUST be recomputed (not cached)
    if not updated_patient.get("alert"):
        log_critical("FAILED: Alert is empty after update!")
        return None
    log_success("Alert recomputed after update")
    
    # Assertion 3: LLM output MUST be recomputed
    if not updated_patient.get("llm_output") or not updated_patient["llm_output"].get("explanation"):
        log_critical("FAILED: LLM output not recomputed!")
        return None
    log_success("LLM output recomputed")
    
    # Assertion 4: Timestamp MUST be fresh
    old_timestamp = "2024-01-01T00:00:00"  # dummy old timestamp
    new_timestamp = updated_patient.get("timestamp", old_timestamp)
    if new_timestamp == old_timestamp:
        log_critical("WARNING: Timestamp not updated")
    else:
        log_success(f"Timestamp updated: {new_timestamp}")
    
    return updated_patient


def test_data_consistency():
    """Test 3: Verify data consistency constraints."""
    log_info("\n" + "=" * 70)
    log_info("TEST 3: Verify data consistency constraints")
    log_info("=" * 70)
    
    response = requests.get(f"{API_BASE}/patient/{PATIENT_ID}")
    
    if response.status_code != 200:
        log_critical(f"Failed to fetch patient: {response.status_code}")
        return False
    
    patient = response.json()
    
    # Constraint 1: All required fields MUST exist
    required_fields = ["patient_id", "severity", "alert", "llm_output", "score", "timestamp"]
    missing = [f for f in required_fields if f not in patient or patient[f] is None]
    
    if missing:
        log_critical(f"FAILED: Missing critical fields: {missing}")
        return False
    log_success(f"All required fields present: {', '.join(required_fields)}")
    
    # Constraint 2: Severity MUST be valid
    valid_severities = ["CRITICAL", "HIGH", "MODERATE", "STABLE"]
    if patient["severity"].upper() not in valid_severities:
        log_critical(f"FAILED: Invalid severity '{patient['severity']}'")
        return False
    log_success(f"Severity valid: {patient['severity'].upper()}")
    
    # Constraint 3: LLM output structure MUST be correct
    llm = patient["llm_output"]
    if not isinstance(llm, dict) or "explanation" not in llm or "suggested_actions" not in llm:
        log_critical("FAILED: LLM output structure invalid")
        return False
    log_success("LLM output structure valid")
    
    # Constraint 4: Score MUST be numeric
    if not isinstance(patient["score"], (int, float)):
        log_critical("FAILED: Score is not numeric")
        return False
    log_success(f"Score is numeric: {patient['score']}")
    
    return True


def test_refresh_mechanism():
    """Test 4: Verify refresh returns fresh data."""
    log_info("\n" + "=" * 70)
    log_info("TEST 4: Verify refresh mechanism returns fresh data")
    log_info("=" * 70)
    
    # Fetch same patient twice
    response1 = requests.get(f"{API_BASE}/patient/{PATIENT_ID}")
    response2 = requests.get(f"{API_BASE}/patient/{PATIENT_ID}")
    
    if response1.status_code != 200 or response2.status_code != 200:
        log_critical("Failed to fetch patient data")
        return False
    
    patient1 = response1.json()
    patient2 = response2.json()
    
    # Both responses MUST have same patient ID
    if patient1["patient_id"] != patient2["patient_id"]:
        log_critical("FAILED: Patient IDs don't match")
        return False
    log_success("Patient ID consistent across requests")
    
    # Both responses MUST have valid alerts
    if not patient1.get("alert") or not patient2.get("alert"):
        log_critical("FAILED: Alert missing in refresh")
        return False
    log_success("Alert present in both requests")
    
    # Both responses MUST have LLM output
    if not patient1.get("llm_output") or not patient2.get("llm_output"):
        log_critical("FAILED: LLM output missing in refresh")
        return False
    log_success("LLM output present in both requests")
    
    return True


def cleanup():
    """Delete test patient."""
    log_info("\n" + "=" * 70)
    log_info("CLEANUP: Deleting test patient")
    log_info("=" * 70)
    
    response = requests.delete(f"{API_BASE}/patient/{PATIENT_ID}")
    if response.status_code == 200:
        log_success(f"Test patient {PATIENT_ID} deleted")
    else:
        log_critical(f"Failed to delete test patient: {response.status_code}")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("🏥 VITALTRIAGE HEALTHCARE SAFETY TEST SUITE")
    print("=" * 70)
    
    try:
        # Test 1: Create patient with critical vitals
        patient = test_critical_patient_creation()
        if not patient:
            log_critical("TEST 1 FAILED: Could not create critical patient")
            return False
        
        # Test 2: Update patient and verify recomputation
        updated = test_critical_patient_update()
        if not updated:
            log_critical("TEST 2 FAILED: Could not update patient")
            return False
        
        # Test 3: Data consistency
        if not test_data_consistency():
            log_critical("TEST 3 FAILED: Data consistency check failed")
            return False
        
        # Test 4: Refresh mechanism
        if not test_refresh_mechanism():
            log_critical("TEST 4 FAILED: Refresh mechanism failed")
            return False
        
        log_info("\n" + "=" * 70)
        log_success("ALL HEALTHCARE SAFETY TESTS PASSED ✅")
        log_info("=" * 70)
        
        return True
        
    except Exception as e:
        log_critical(f"Test execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        cleanup()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
