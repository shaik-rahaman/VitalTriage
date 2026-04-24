import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Test data with all required fields
patient_data = {
    "patient_id": "TEST_P001",
    "age": 65,
    "gender": "M",
    "ward": "ICU",
    "room": "102",
    "vitals": {
        "heart_rate": 95,
        "spo2": 88,
        "systolic_bp": 140,
        "diastolic_bp": 95,
        "temperature": 99.5,
        "respiratory_rate": 22
    },
    "symptoms": ["chest pain", "shortness of breath"],
    "notes": "Patient presented with acute symptoms"
}

print("=" * 60)
print("CREATING PATIENT...")
print("=" * 60)

response = requests.post(f"{BASE_URL}/patient", json=patient_data)
print(f"Status Code: {response.status_code}")
print(f"Response:\n{json.dumps(response.json(), indent=2, default=str)}")

if response.status_code == 200:
    print("\n" + "=" * 60)
    print("FETCHING DASHBOARD...")
    print("=" * 60)
    
    dashboard_response = requests.get(f"{BASE_URL}/dashboard")
    dashboard = dashboard_response.json()
    
    print(f"Critical Patients: {len(dashboard.get('critical', []))}")
    print(f"High Risk Patients: {len(dashboard.get('high', []))}")
    print(f"Moderate Patients: {len(dashboard.get('moderate', []))}")
    print(f"Stable Patients: {len(dashboard.get('stable', []))}")
    
    # Check if the patient appears in the dashboard
    all_patients = dashboard.get('critical', []) + dashboard.get('high', []) + dashboard.get('moderate', []) + dashboard.get('stable', [])
    
    for patient in all_patients:
        if patient.get('patient_id') == 'TEST_P001':
            print(f"\n✓ Patient found in dashboard!")
            print(f"  Ward: {patient.get('ward')}")
            print(f"  Room: {patient.get('room')}")
            print(f"  Severity: {patient.get('severity')}")
            print(f"  Score: {patient.get('score')}")
            print(f"  LLM Output:")
            print(f"    - Explanation: {patient.get('llm_output', {}).get('explanation', 'N/A')[:100]}...")
            print(f"    - Suggested Actions: {patient.get('llm_output', {}).get('suggested_actions', [])}")
            print(f"  Timestamp: {patient.get('timestamp')}")
            break
