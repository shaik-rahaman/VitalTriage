"""
Demo data generation script.
Preloads sample patients with different severity levels.
"""
import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import mongo
from app.routes.patient_routes import process_patient_vitals
from app.models.patient_model import VitalsModel

load_dotenv()


async def create_demo_patients():
    """Create demo patients with various severity levels."""
    
    # Demo patients data
    demo_patients = [
        {
            "patient_id": "P_CRITICAL_001",
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
            "symptoms": ["breathlessness", "chest pain", "confusion"],
            "notes": "Severe respiratory distress, admitted from ER"
        },
        {
            "patient_id": "P_CRITICAL_002",
            "age": 58,
            "gender": "M",
            "vitals": {
                "heart_rate": 150,
                "spo2": 83,
                "systolic_bp": 88,
                "diastolic_bp": 48,
                "temperature": 103.5,
                "respiratory_rate": 35
            },
            "symptoms": ["severe fever", "difficulty breathing"],
            "notes": "Post-operative patient, sepsis suspected"
        },
        {
            "patient_id": "P_HIGH_001",
            "age": 68,
            "gender": "M",
            "vitals": {
                "heart_rate": 125,
                "spo2": 91,
                "systolic_bp": 155,
                "diastolic_bp": 95,
                "temperature": 101.2,
                "respiratory_rate": 28
            },
            "symptoms": ["fever", "chest discomfort"],
            "notes": "Hypertensive crisis, fever ongoing"
        },
        {
            "patient_id": "P_HIGH_002",
            "age": 55,
            "gender": "F",
            "vitals": {
                "heart_rate": 118,
                "spo2": 92,
                "systolic_bp": 148,
                "diastolic_bp": 92,
                "temperature": 100.8,
                "respiratory_rate": 26
            },
            "symptoms": ["persistent cough", "fever"],
            "notes": "Possible pneumonia, awaiting X-ray results"
        },
        {
            "patient_id": "P_MODERATE_001",
            "age": 45,
            "gender": "M",
            "vitals": {
                "heart_rate": 95,
                "spo2": 94,
                "systolic_bp": 132,
                "diastolic_bp": 85,
                "temperature": 99.8,
                "respiratory_rate": 22
            },
            "symptoms": ["mild fever"],
            "notes": "Common cold, supportive care"
        },
        {
            "patient_id": "P_MODERATE_002",
            "age": 62,
            "gender": "F",
            "vitals": {
                "heart_rate": 88,
                "spo2": 93,
                "systolic_bp": 138,
                "diastolic_bp": 88,
                "temperature": 99.5,
                "respiratory_rate": 21
            },
            "symptoms": ["mild cough"],
            "notes": "Recovering from flu"
        },
        {
            "patient_id": "P_STABLE_001",
            "age": 40,
            "gender": "M",
            "vitals": {
                "heart_rate": 72,
                "spo2": 98,
                "systolic_bp": 118,
                "diastolic_bp": 76,
                "temperature": 98.6,
                "respiratory_rate": 16
            },
            "symptoms": [],
            "notes": "Routine checkup, all vitals normal"
        },
        {
            "patient_id": "P_STABLE_002",
            "age": 35,
            "gender": "F",
            "vitals": {
                "heart_rate": 68,
                "spo2": 99,
                "systolic_bp": 115,
                "diastolic_bp": 74,
                "temperature": 98.4,
                "respiratory_rate": 15
            },
            "symptoms": [],
            "notes": "Pre-operative assessment, cleared for surgery"
        }
    ]
    
    print("🏥 VitalTriage - Demo Data Generator\n")
    print(f"Creating {len(demo_patients)} demo patients...")
    print("-" * 60)
    
    created_count = 0
    
    for patient_data in demo_patients:
        try:
            # Create vitals model
            vitals = VitalsModel(**patient_data["vitals"])
            
            # Process vitals through pipeline
            score, severity, alert, llm_output, audit_log = await process_patient_vitals(
                vitals=vitals,
                symptoms=patient_data["symptoms"],
                notes=patient_data["notes"]
            )
            
            # Create document
            timestamp = datetime.utcnow()
            patient_doc = {
                "patient_id": patient_data["patient_id"],
                "age": patient_data["age"],
                "gender": patient_data["gender"],
                "vitals": patient_data["vitals"],
                "symptoms": patient_data["symptoms"],
                "notes": patient_data["notes"],
                "score": score,
                "severity": severity,
                "alert": alert,
                "llm_output": llm_output.model_dump(),
                "audit_log": audit_log.model_dump(),
                "timestamp": timestamp
            }
            
            # Insert into MongoDB
            await mongo.insert_patient(patient_doc)
            created_count += 1
            
            print(f"✓ {patient_data['patient_id']:20} | Score: {score:5.1f} | Severity: {severity:10}")
            
        except Exception as e:
            print(f"✗ {patient_data['patient_id']:20} | Error: {str(e)}")
    
    print("-" * 60)
    print(f"\n✅ Successfully created {created_count}/{len(demo_patients)} demo patients\n")
    
    # Print summary
    all_patients = await mongo.get_all_patients()
    critical = await mongo.get_patients_by_severity("CRITICAL")
    high = await mongo.get_patients_by_severity("HIGH")
    moderate = await mongo.get_patients_by_severity("MODERATE")
    stable = await mongo.get_patients_by_severity("STABLE")
    
    print("📊 Dashboard Summary:")
    print(f"  Total Patients: {len(all_patients)}")
    print(f"  🚨 Critical: {len(critical)}")
    print(f"  ⚠️  High: {len(high)}")
    print(f"  ℹ️  Moderate: {len(moderate)}")
    print(f"  ✓ Stable: {len(stable)}")


async def clear_database():
    """Clear all patients from database."""
    print("\n⚠️  Clearing all patients from database...")
    await mongo.clear_all_patients()
    print("✓ Database cleared\n")


async def main():
    """Main function."""
    try:
        # Connect to MongoDB
        print("🔌 Connecting to MongoDB...")
        await mongo.connect_to_mongo()
        print("✓ Connected\n")
        
        # Clear existing data
        await clear_database()
        
        # Create demo patients
        await create_demo_patients()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    finally:
        # Close connection
        await mongo.close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
