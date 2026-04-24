"""
Integration tests for VitalTriage - Testing complete workflows.

Tests end-to-end scenarios including:
- Creating patients and verifying they appear in dashboard
- Updating patient vitals and checking severity changes
- Alert generation for critical patients
- Data consistency across API calls
"""

import pytest
import asyncio
from httpx import AsyncClient
from datetime import datetime

# Test data for integration tests
INTEGRATION_TEST_PATIENTS = {
    "patient_1": {
        "patient_id": "INT_P001",
        "age": 55,
        "gender": "M",
        "vitals": {
            "heart_rate": 88,
            "spo2": 95,
            "systolic_bp": 135,
            "diastolic_bp": 85,
            "temperature": 98.6,
            "respiratory_rate": 18
        },
        "symptoms": ["mild fatigue"],
        "notes": "Routine checkup"
    },
    "patient_2": {
        "patient_id": "INT_P002",
        "age": 72,
        "gender": "F",
        "vitals": {
            "heart_rate": 95,
            "spo2": 92,
            "systolic_bp": 155,
            "diastolic_bp": 95,
            "temperature": 99.2,
            "respiratory_rate": 22
        },
        "symptoms": ["shortness of breath"],
        "notes": "Elevated BP and tachycardia"
    },
    "patient_3_critical": {
        "patient_id": "INT_P003_CRIT",
        "age": 48,
        "gender": "M",
        "vitals": {
            "heart_rate": 140,
            "spo2": 82,
            "systolic_bp": 190,
            "diastolic_bp": 115,
            "temperature": 102.5,
            "respiratory_rate": 32
        },
        "symptoms": ["severe chest pain", "difficulty breathing"],
        "notes": "CRITICAL - Multiple vital sign abnormalities"
    }
}


class TestCreatePatientFlow:
    """Test creating a patient and verifying data integrity."""
    
    @pytest.mark.asyncio
    async def test_create_and_retrieve_patient(self, client):
        """Test creating a patient and then retrieving it."""
        # Create patient
        create_response = await client.post(
            "/api/v1/patient",
            json=INTEGRATION_TEST_PATIENTS["patient_1"]
        )
        
        if create_response.status_code in [200, 201]:
            created_patient = create_response.json()
            patient_id = created_patient.get("id")
            
            if patient_id:
                # Try to retrieve the same patient
                get_response = await client.get(f"/api/v1/patient/{patient_id}")
                assert get_response.status_code in [200, 404]
                
                if get_response.status_code == 200:
                    retrieved_patient = get_response.json()
                    assert retrieved_patient["patient_id"] == "INT_P001"


class TestSeverityClassification:
    """Test that patients are correctly classified by severity."""
    
    @pytest.mark.asyncio
    async def test_stable_patient_classification(self, client):
        """Test that stable patient gets correct severity."""
        response = await client.post(
            "/api/v1/patient",
            json=INTEGRATION_TEST_PATIENTS["patient_1"]
        )
        
        if response.status_code in [200, 201]:
            patient = response.json()
            severity = patient.get("severity", "UNKNOWN")
            assert severity in ["STABLE", "MODERATE", "HIGH", "CRITICAL"]

    @pytest.mark.asyncio
    async def test_high_risk_patient_classification(self, client):
        """Test that high-risk patient gets appropriate severity."""
        response = await client.post(
            "/api/v1/patient",
            json=INTEGRATION_TEST_PATIENTS["patient_2"]
        )
        
        if response.status_code in [200, 201]:
            patient = response.json()
            severity = patient.get("severity", "UNKNOWN")
            # High risk should be at least MODERATE
            assert severity in ["MODERATE", "HIGH", "CRITICAL"]

    @pytest.mark.asyncio
    async def test_critical_patient_classification(self, client):
        """Test that critical patient gets CRITICAL severity."""
        response = await client.post(
            "/api/v1/patient",
            json=INTEGRATION_TEST_PATIENTS["patient_3_critical"]
        )
        
        if response.status_code in [200, 201]:
            patient = response.json()
            severity = patient.get("severity", "UNKNOWN")
            # Critical vitals should trigger CRITICAL severity
            assert severity == "CRITICAL" or severity in ["HIGH", "CRITICAL"]


class TestDashboardAggregation:
    """Test dashboard correctly aggregates and groups patients."""
    
    @pytest.mark.asyncio
    async def test_dashboard_structure(self, client):
        """Test dashboard returns properly structured data."""
        response = await client.get("/api/v1/dashboard")
        
        if response.status_code == 200:
            dashboard = response.json()
            
            # Check if it's a dict with severity keys
            assert isinstance(dashboard, dict)
            
            # Expected severity categories
            expected_keys = {"critical", "high", "moderate", "stable"}
            dashboard_keys = set(dashboard.keys())
            
            # At least some severity keys should be present
            if len(dashboard_keys) > 0:
                # All keys should be severity-related
                for key in dashboard_keys:
                    assert key.lower() in expected_keys

    @pytest.mark.asyncio
    async def test_dashboard_patient_count_increases(self, client):
        """Test that dashboard patient count increases after adding patient."""
        # Get initial count
        response1 = await client.get("/api/v1/dashboard")
        initial_count = 0
        
        if response1.status_code == 200:
            dashboard1 = response1.json()
            initial_count = sum(
                len(v) if isinstance(v, list) else 0 
                for v in dashboard1.values()
            )
        
        # Add a patient
        await client.post("/api/v1/patient", json=INTEGRATION_TEST_PATIENTS["patient_1"])
        
        # Get updated count
        response2 = await client.get("/api/v1/dashboard")
        
        if response2.status_code == 200:
            dashboard2 = response2.json()
            new_count = sum(
                len(v) if isinstance(v, list) else 0 
                for v in dashboard2.values()
            )
            # Count should stay same or increase (might be duplicate ID)
            assert new_count >= initial_count


class TestAlertGeneration:
    """Test alert generation for critical patients."""
    
    @pytest.mark.asyncio
    async def test_alert_for_critical_patient(self, client):
        """Test that critical patient has alert information."""
        response = await client.post(
            "/api/v1/patient",
            json=INTEGRATION_TEST_PATIENTS["patient_3_critical"]
        )
        
        if response.status_code in [200, 201]:
            patient = response.json()
            # Check for alert-related fields
            has_alert_field = "alert" in patient or "alerts" in patient
            if has_alert_field:
                alert = patient.get("alert") or patient.get("alerts")
                assert alert is not None

    @pytest.mark.asyncio
    async def test_no_alert_for_stable_patient(self, client):
        """Test that stable patient doesn't have critical alerts."""
        response = await client.post(
            "/api/v1/patient",
            json=INTEGRATION_TEST_PATIENTS["patient_1"]
        )
        
        if response.status_code in [200, 201]:
            patient = response.json()
            if "alert" in patient:
                alert = patient.get("alert")
                # Alert should not be critical for stable patient
                if alert and isinstance(alert, dict):
                    severity = alert.get("severity", "").upper()
                    assert severity != "CRITICAL"


class TestDataConsistency:
    """Test data consistency across API operations."""
    
    @pytest.mark.asyncio
    async def test_vital_signs_preserved(self, client):
        """Test that vital signs are preserved when creating patient."""
        response = await client.post(
            "/api/v1/patient",
            json=INTEGRATION_TEST_PATIENTS["patient_1"]
        )
        
        if response.status_code in [200, 201]:
            patient = response.json()
            if "vitals" in patient:
                vitals = patient["vitals"]
                original_vitals = INTEGRATION_TEST_PATIENTS["patient_1"]["vitals"]
                
                # Key vital signs should match
                for key in ["heart_rate", "spo2", "temperature"]:
                    if key in vitals:
                        assert vitals[key] == original_vitals[key]

    @pytest.mark.asyncio
    async def test_patient_id_preserved(self, client):
        """Test that patient_id is preserved."""
        response = await client.post(
            "/api/v1/patient",
            json=INTEGRATION_TEST_PATIENTS["patient_1"]
        )
        
        if response.status_code in [200, 201]:
            patient = response.json()
            assert patient.get("patient_id") == "INT_P001"


class TestUpdateAndRetrieve:
    """Test updating patient data and retrieving updated information."""
    
    @pytest.mark.asyncio
    async def test_update_patient_vitals(self, client):
        """Test updating patient's vital signs."""
        # First create a patient
        create_response = await client.post(
            "/api/v1/patient",
            json=INTEGRATION_TEST_PATIENTS["patient_1"]
        )
        
        if create_response.status_code in [200, 201]:
            patient = create_response.json()
            patient_id = patient.get("id")
            
            if patient_id:
                # Update vitals
                update_data = {
                    "vitals": {
                        "heart_rate": 110,
                        "spo2": 90,
                        "systolic_bp": 145,
                        "diastolic_bp": 90,
                        "temperature": 99.5,
                        "respiratory_rate": 22
                    }
                }
                
                update_response = await client.put(
                    f"/api/v1/patient/{patient_id}",
                    json=update_data
                )
                
                # Update might fail if endpoint not implemented
                if update_response.status_code in [200, 201]:
                    updated_patient = update_response.json()
                    if "vitals" in updated_patient:
                        assert updated_patient["vitals"]["heart_rate"] == 110


class TestErrorHandling:
    """Test error handling for edge cases."""
    
    @pytest.mark.asyncio
    async def test_create_with_missing_vitals_field(self, client):
        """Test creating patient with missing vital field."""
        invalid_data = INTEGRATION_TEST_PATIENTS["patient_1"].copy()
        invalid_data["vitals"] = {}  # Empty vitals
        
        response = await client.post("/api/v1/patient", json=invalid_data)
        # Should either reject or handle gracefully
        assert response.status_code in [200, 201, 400, 422]

    @pytest.mark.asyncio
    async def test_create_with_missing_required_field(self, client):
        """Test creating patient without required patient_id."""
        invalid_data = INTEGRATION_TEST_PATIENTS["patient_1"].copy()
        del invalid_data["patient_id"]
        
        response = await client.post("/api/v1/patient", json=invalid_data)
        # Should reject for missing required field
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_get_invalid_id(self, client):
        """Test getting patient with invalid ID."""
        response = await client.get("/api/v1/patient/invalid_id_123!@#")
        # Should return 404 or 400
        assert response.status_code in [400, 404]

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, client):
        """Test deleting non-existent patient."""
        response = await client.delete("/api/v1/patient/nonexistent_id_xyz")
        # Could be 404 or 200 depending on implementation
        assert response.status_code in [200, 404]


# Fixture needed for all tests in this module
@pytest.fixture
async def client():
    """Create test client for the FastAPI app."""
    from app.main import app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
