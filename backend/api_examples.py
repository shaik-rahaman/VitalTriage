#!/usr/bin/env python3
"""
API Usage Examples
This script demonstrates how to use the VitalTriage API.
"""
import asyncio
import httpx
import json

BASE_URL = "http://localhost:8002/api/v1"


async def example_1_create_stable_patient():
    """Example 1: Create a stable patient."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Create Stable Patient")
    print("="*60)
    
    patient_data = {
        "patient_id": "P_STABLE_EXAMPLE",
        "age": 45,
        "gender": "M",
        "vitals": {
            "heart_rate": 72,
            "spo2": 98,
            "systolic_bp": 120,
            "diastolic_bp": 78,
            "temperature": 98.6,
            "respiratory_rate": 16
        },
        "symptoms": [],
        "notes": "Regular check-up, all vitals normal"
    }
    
    print("\nRequest:")
    print(f"POST {BASE_URL}/patient")
    print(json.dumps(patient_data, indent=2))
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/patient", json=patient_data)
        
        print("\nResponse:")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps({
            "patient_id": data["patient_id"],
            "score": data["score"],
            "severity": data["severity"],
            "alert": data["alert"],
            "llm_output": data["llm_output"]
        }, indent=2))


async def example_2_create_critical_patient():
    """Example 2: Create a critical patient."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Create Critical Patient")
    print("="*60)
    
    patient_data = {
        "patient_id": "P_CRITICAL_EXAMPLE",
        "age": 72,
        "gender": "F",
        "vitals": {
            "heart_rate": 145,
            "spo2": 82,
            "systolic_bp": 85,
            "diastolic_bp": 50,
            "temperature": 105,
            "respiratory_rate": 32
        },
        "symptoms": ["breathlessness", "chest pain"],
        "notes": "Severe respiratory distress, admitted from ER"
    }
    
    print("\nRequest:")
    print(f"POST {BASE_URL}/patient")
    print(json.dumps(patient_data, indent=2))
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/patient", json=patient_data)
        
        print("\nResponse:")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps({
            "patient_id": data["patient_id"],
            "score": data["score"],
            "severity": data["severity"],
            "alert": data["alert"],
            "audit_log": data["audit_log"]
        }, indent=2))


async def example_3_update_patient():
    """Example 3: Update patient vitals."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Update Patient Vitals")
    print("="*60)
    
    patient_id = "P_UPDATE_EXAMPLE"
    
    # First create a patient
    print("\nStep 1: Create initial patient...")
    initial_data = {
        "patient_id": patient_id,
        "age": 60,
        "gender": "M",
        "vitals": {
            "heart_rate": 110,
            "spo2": 91,
            "systolic_bp": 145,
            "diastolic_bp": 90,
            "temperature": 101,
            "respiratory_rate": 24
        },
        "symptoms": ["fever"],
        "notes": "Initial assessment"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/patient", json=initial_data)
        print(f"Created patient - Severity: {response.json()['severity']}")
        
        # Update the patient
        print("\nStep 2: Update patient vitals...")
        update_data = {
            "vitals": {
                "heart_rate": 78,
                "spo2": 96,
                "systolic_bp": 125,
                "diastolic_bp": 80,
                "temperature": 98.8,
                "respiratory_rate": 18
            },
            "notes": "Patient responding to treatment"
        }
        
        print(f"PUT {BASE_URL}/patient/{patient_id}")
        print(json.dumps(update_data, indent=2))
        
        response = await client.put(f"{BASE_URL}/patient/{patient_id}", json=update_data)
        data = response.json()
        print(f"\nUpdated patient - Severity: {data['severity']} (improved from MODERATE)")


async def example_4_get_patient():
    """Example 4: Get patient details."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Get Patient Details")
    print("="*60)
    
    patient_id = "P_STABLE_EXAMPLE"
    
    print(f"\nRequest:")
    print(f"GET {BASE_URL}/patient/{patient_id}")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/patient/{patient_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nResponse:")
            print(json.dumps({
                "patient_id": data["patient_id"],
                "age": data["age"],
                "gender": data["gender"],
                "score": data["score"],
                "severity": data["severity"],
                "vitals": data["vitals"]
            }, indent=2))
        else:
            print(f"Patient not found (Status: {response.status_code})")


async def example_5_get_dashboard():
    """Example 5: Get dashboard with all patients grouped by severity."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Get Dashboard")
    print("="*60)
    
    print(f"\nRequest:")
    print(f"GET {BASE_URL}/dashboard")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/dashboard")
        data = response.json()
        
        print(f"\nResponse - Patient Summary by Severity:")
        print(f"  🚨 Critical: {len(data['critical'])} patients")
        if data['critical']:
            for p in data['critical'][:2]:  # Show first 2
                print(f"     - {p['patient_id']} (Score: {p['score']})")
        
        print(f"  ⚠️  High: {len(data['high'])} patients")
        if data['high']:
            for p in data['high'][:2]:
                print(f"     - {p['patient_id']} (Score: {p['score']})")
        
        print(f"  ℹ️  Moderate: {len(data['moderate'])} patients")
        if data['moderate']:
            for p in data['moderate'][:2]:
                print(f"     - {p['patient_id']} (Score: {p['score']})")
        
        print(f"  ✓ Stable: {len(data['stable'])} patients")
        if data['stable']:
            for p in data['stable'][:2]:
                print(f"     - {p['patient_id']} (Score: {p['score']})")


async def example_6_error_handling():
    """Example 6: Error handling for invalid data."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Error Handling")
    print("="*60)
    
    invalid_patient = {
        "patient_id": "P_INVALID",
        "age": 50,
        "gender": "M",
        "vitals": {
            "heart_rate": 75,
            "spo2": 150,  # Invalid - must be 0-100
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "temperature": 98.6,
            "respiratory_rate": 16
        },
        "symptoms": [],
        "notes": "This request should fail"
    }
    
    print(f"\nRequest with invalid SpO2:")
    print(f"POST {BASE_URL}/patient")
    print(json.dumps(invalid_patient, indent=2))
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/patient", json=invalid_patient)
        
        print(f"\nResponse:")
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            error_data = response.json()
            print(f"Error: {error_data.get('detail', 'Unknown error')}")


async def main():
    """Run all examples."""
    print("🏥 VitalTriage API - Usage Examples")
    print("====================================")
    print(f"\nBase URL: {BASE_URL}")
    print("Make sure the API server is running: uvicorn app.main:app --reload")
    
    try:
        # Check if server is running
        async with httpx.AsyncClient() as client:
            await client.get(f"{BASE_URL}/health", timeout=2.0)
    except Exception as e:
        print(f"\n❌ Error: Could not connect to server at {BASE_URL}")
        print("Please start the server with: uvicorn app.main:app --reload")
        return
    
    try:
        await example_1_create_stable_patient()
        await example_2_create_critical_patient()
        await example_3_update_patient()
        await example_4_get_patient()
        await example_5_get_dashboard()
        await example_6_error_handling()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
