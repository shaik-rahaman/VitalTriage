import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Test data with high-risk vitals
patient_data = {
    "patient_id": "P_HIGH_FIXED_011",
    "age": 60,
    "gender": "M",
    "ward": "ICU",
    "room": "105",
    "vitals": {
        "heart_rate": 115,
        "spo2": 89,
        "systolic_bp": 165,
        "diastolic_bp": 100,
        "temperature": 102.0,
        "respiratory_rate": 28
    },
    "symptoms": ["chest_discomfort", "shortness_of_breath"],
    "notes": "Patient with multiple high-risk vital signs"
}

print("=" * 70)
print("TESTING HIGH-RISK SEVERITY FIX")
print("=" * 70)

response = requests.post(f"{BASE_URL}/patient", json=patient_data)
patient = response.json()

print(f"\nPatient ID: {patient.get('patient_id')}")
print(f"Score: {patient.get('score')}")
print(f"Severity: {patient.get('severity')} {'✓ FIXED!' if patient.get('severity') == 'HIGH' else '✗ STILL WRONG'}")
print(f"\nScore Breakdown:")
print(f"  - SpO2: {patient['audit_log']['score_breakdown'].get('spo2')}")
print(f"  - BP: {patient['audit_log']['score_breakdown'].get('bp')}")
print(f"  - HR: {patient['audit_log']['score_breakdown'].get('hr')}")
print(f"  - RR: {patient['audit_log']['score_breakdown'].get('rr')}")
print(f"  - Temp: {patient['audit_log']['score_breakdown'].get('temperature')}")
print(f"\nTriggered Rules:")
for rule in patient['audit_log']['rules_triggered']:
    print(f"  - {rule}")

print(f"\nAlert: {patient.get('alert')}")
print(f"\nLLM Recommendation: {patient['llm_output']['explanation'][:80]}...")

# Verify it's in HIGH group
dashboard_response = requests.get(f"{BASE_URL}/dashboard")
dashboard = dashboard_response.json()

print("\n" + "=" * 70)
print("DASHBOARD STATUS")
print("=" * 70)
print(f"Critical: {len(dashboard.get('critical', []))}")
print(f"High Risk: {len(dashboard.get('high', []))} patients")
print(f"Moderate: {len(dashboard.get('moderate', []))}")
print(f"Stable: {len(dashboard.get('stable', []))}")

# Check if our patient is in HIGH
for patient in dashboard.get('high', []):
    if patient['patient_id'] == 'P_HIGH_FIXED_011':
        print(f"\n✓ Patient {patient['patient_id']} FOUND in HIGH Risk column!")
        break
