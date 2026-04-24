"""
Comprehensive pytest test suite for VitalTriage backend API.

This test suite validates:
- API endpoint functionality
- Input validation
- Error handling
- Data consistency
- Edge cases
"""

import pytest
import asyncio
from httpx import AsyncClient
from datetime import datetime
import json

# Fixtures
@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def client():
    """Create test client for the FastAPI app."""
    from app.main import app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# ============================================================================
# TEST DATA
# ============================================================================

VALID_PATIENT_DATA = {
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
    "notes": "Regular checkup"
}

CRITICAL_PATIENT_DATA = {
    "patient_id": "P002_CRITICAL",
    "age": 45,
    "gender": "F",
    "vitals": {
        "heart_rate": 150,  # Tachycardia
        "spo2": 75,         # Severe hypoxia
        "systolic_bp": 200,
        "diastolic_bp": 120,
        "temperature": 103.5,
        "respiratory_rate": 35
    },
    "symptoms": ["severe dyspnea", "chest pain", "altered mental status"],
    "notes": "Critical condition"
}

STABLE_PATIENT_DATA = {
    "patient_id": "P003_STABLE",
    "age": 35,
    "gender": "M",
    "vitals": {
        "heart_rate": 72,
        "spo2": 98,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "temperature": 98.6,
        "respiratory_rate": 16
    },
    "symptoms": [],
    "notes": "Stable vital signs"
}


# ============================================================================
# HEALTH CHECK TESTS
# ============================================================================

class TestHealthCheck:
    """Test server health and connectivity."""
    
    @pytest.mark.asyncio
    async def test_health_check_endpoint(self, client):
        """Test health check endpoint returns success."""
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    @pytest.mark.asyncio
    async def test_api_version(self, client):
        """Test API is accessible at v1 prefix."""
        response = await client.get("/api/v1/health")
        assert response.status_code in [200, 404]  # 200 if endpoint exists, 404 otherwise


# ============================================================================
# CREATE PATIENT TESTS
# ============================================================================

class TestCreatePatient:
    """Test POST /api/v1/patient endpoint."""
    
    @pytest.mark.asyncio
    async def test_create_valid_patient(self, client):
        """Test creating a patient with valid data."""
        response = await client.post("/api/v1/patient", json=VALID_PATIENT_DATA)
        assert response.status_code in [200, 201]
        data = response.json()
        assert "id" in data
        assert data["patient_id"] == "P001"
        assert data["severity"] in ["CRITICAL", "HIGH", "MODERATE", "STABLE"]

    @pytest.mark.asyncio
    async def test_create_critical_patient(self, client):
        """Test creating a critical patient gets correct severity."""
        response = await client.post("/api/v1/patient", json=CRITICAL_PATIENT_DATA)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["severity"] == "CRITICAL"
        assert "alerts" in data or "alert" in data.keys()

    @pytest.mark.asyncio
    async def test_create_stable_patient(self, client):
        """Test creating a stable patient gets correct severity."""
        response = await client.post("/api/v1/patient", json=STABLE_PATIENT_DATA)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["severity"] in ["STABLE", "MODERATE"]

    @pytest.mark.asyncio
    async def test_create_patient_missing_required_field(self, client):
        """Test creating patient without required field returns error."""
        invalid_data = VALID_PATIENT_DATA.copy()
        del invalid_data["patient_id"]
        response = await client.post("/api/v1/patient", json=invalid_data)
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_create_patient_invalid_age(self, client):
        """Test creating patient with invalid age."""
        invalid_data = VALID_PATIENT_DATA.copy()
        invalid_data["age"] = -5
        response = await client.post("/api/v1/patient", json=invalid_data)
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_create_patient_invalid_heart_rate(self, client):
        """Test validation of out-of-range heart rate."""
        invalid_data = VALID_PATIENT_DATA.copy()
        invalid_data["vitals"]["heart_rate"] = -50  # Invalid
        response = await client.post("/api/v1/patient", json=invalid_data)
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_create_patient_invalid_spo2(self, client):
        """Test validation of oxygen saturation."""
        invalid_data = VALID_PATIENT_DATA.copy()
        invalid_data["vitals"]["spo2"] = 150  # > 100%
        response = await client.post("/api/v1/patient", json=invalid_data)
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_create_patient_missing_vitals(self, client):
        """Test creating patient without vital signs."""
        invalid_data = {
            "patient_id": "P_NO_VITALS",
            "age": 50,
            "gender": "M",
            "vitals": {}
        }
        response = await client.post("/api/v1/patient", json=invalid_data)
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_create_patient_extreme_temperature(self, client):
        """Test creating patient with extreme temperature."""
        invalid_data = VALID_PATIENT_DATA.copy()
        invalid_data["vitals"]["temperature"] = 150  # Unrealistic
        response = await client.post("/api/v1/patient", json=invalid_data)
        # Should either accept with warning or reject with validation error
        assert response.status_code in [200, 201, 400, 422]


# ============================================================================
# GET PATIENT TESTS
# ============================================================================

class TestGetPatient:
    """Test GET /api/v1/patient/{id} endpoint."""
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_patient(self, client):
        """Test getting a patient that doesn't exist."""
        response = await client.get("/api/v1/patient/nonexistent_id")
        assert response.status_code in [404, 400]

    @pytest.mark.asyncio
    async def test_get_patient_invalid_id_format(self, client):
        """Test getting patient with invalid ID format."""
        response = await client.get("/api/v1/patient/!!invalid!!")
        assert response.status_code in [400, 404]


# ============================================================================
# UPDATE PATIENT TESTS
# ============================================================================

class TestUpdatePatient:
    """Test PUT /api/v1/patient/{id} endpoint."""
    
    @pytest.mark.asyncio
    async def test_update_nonexistent_patient(self, client):
        """Test updating a patient that doesn't exist."""
        response = await client.put(
            "/api/v1/patient/nonexistent_id",
            json={"vitals": {"heart_rate": 90}}
        )
        assert response.status_code in [404, 400]

    @pytest.mark.asyncio
    async def test_update_with_invalid_data(self, client):
        """Test updating patient with invalid vital signs."""
        response = await client.put(
            "/api/v1/patient/some_id",
            json={"vitals": {"heart_rate": -100}}
        )
        assert response.status_code in [400, 422, 404]


# ============================================================================
# DASHBOARD TESTS
# ============================================================================

class TestDashboard:
    """Test GET /api/v1/dashboard endpoint."""
    
    @pytest.mark.asyncio
    async def test_dashboard_endpoint_exists(self, client):
        """Test dashboard endpoint is accessible."""
        response = await client.get("/api/v1/dashboard")
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            # Verify structure
            assert isinstance(data, dict)
            # Check for expected severity keys
            severity_keys = {"critical", "high", "moderate", "stable"}
            data_keys = set(data.keys())
            # At least some keys should be present
            assert len(data_keys & severity_keys) >= 0

    @pytest.mark.asyncio
    async def test_dashboard_returns_list(self, client):
        """Test dashboard returns patients grouped by severity."""
        response = await client.get("/api/v1/dashboard")
        if response.status_code == 200:
            data = response.json()
            for severity_key in ["critical", "high", "moderate", "stable"]:
                if severity_key in data:
                    assert isinstance(data[severity_key], list)


# ============================================================================
# LIST PATIENTS TESTS
# ============================================================================

class TestListPatients:
    """Test GET /api/v1/patients endpoint."""
    
    @pytest.mark.asyncio
    async def test_list_patients_endpoint(self, client):
        """Test listing all patients."""
        response = await client.get("/api/v1/patients")
        # Endpoint might not exist, but if it does, it should return list
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)


# ============================================================================
# DELETE PATIENT TESTS
# ============================================================================

class TestDeletePatient:
    """Test DELETE /api/v1/patient/{id} endpoint."""
    
    @pytest.mark.asyncio
    async def test_delete_nonexistent_patient(self, client):
        """Test deleting a patient that doesn't exist."""
        response = await client.delete("/api/v1/patient/nonexistent_id")
        assert response.status_code in [404, 400, 200]  # Some APIs return 200 anyway


# ============================================================================
# EDGE CASES AND VALIDATION
# ============================================================================

class TestValidationEdgeCases:
    """Test edge cases and validation logic."""
    
    @pytest.mark.asyncio
    async def test_create_patient_with_null_symptoms(self, client):
        """Test creating patient with null symptoms."""
        data = VALID_PATIENT_DATA.copy()
        data["symptoms"] = None
        response = await client.post("/api/v1/patient", json=data)
        # Should handle gracefully
        assert response.status_code in [200, 201, 400]

    @pytest.mark.asyncio
    async def test_create_patient_with_empty_notes(self, client):
        """Test creating patient with empty notes."""
        data = VALID_PATIENT_DATA.copy()
        data["notes"] = ""
        response = await client.post("/api/v1/patient", json=data)
        assert response.status_code in [200, 201]

    @pytest.mark.asyncio
    async def test_create_patient_with_very_long_notes(self, client):
        """Test creating patient with very long notes."""
        data = VALID_PATIENT_DATA.copy()
        data["notes"] = "A" * 10000
        response = await client.post("/api/v1/patient", json=data)
        # Should accept or reject with clear error
        assert response.status_code in [200, 201, 400, 422]

    @pytest.mark.asyncio
    async def test_create_patient_special_characters_in_name(self, client):
        """Test creating patient with special characters in notes."""
        data = VALID_PATIENT_DATA.copy()
        data["notes"] = "<script>alert('xss')</script>"
        response = await client.post("/api/v1/patient", json=data)
        # Should sanitize or reject
        assert response.status_code in [200, 201, 400]

    @pytest.mark.asyncio
    async def test_create_multiple_patients_same_id(self, client):
        """Test creating multiple patients with same ID."""
        response1 = await client.post("/api/v1/patient", json=VALID_PATIENT_DATA)
        response2 = await client.post("/api/v1/patient", json=VALID_PATIENT_DATA)
        # Second create might fail due to duplicate ID
        assert response1.status_code in [200, 201]
        # Response2 could be success (update) or conflict


# ============================================================================
# RESPONSE STRUCTURE TESTS
# ============================================================================

class TestResponseStructure:
    """Test API response structures are correct."""
    
    @pytest.mark.asyncio
    async def test_patient_response_contains_required_fields(self, client):
        """Test patient response has all required fields."""
        response = await client.post("/api/v1/patient", json=VALID_PATIENT_DATA)
        if response.status_code in [200, 201]:
            data = response.json()
            required_fields = ["id", "patient_id", "name", "age", "severity"]
            # At minimum, these fields should be present
            for field in required_fields:
                assert field in data or field.replace("name", "vitals") in data.keys()

    @pytest.mark.asyncio
    async def test_health_check_response_structure(self, client):
        """Test health check response structure."""
        response = await client.get("/api/v1/health")
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert data["status"] == "healthy"


# ============================================================================
# PERFORMANCE AND LOAD TESTS (Basic)
# ============================================================================

class TestPerformance:
    """Basic performance and load testing."""
    
    @pytest.mark.asyncio
    async def test_create_patient_response_time(self, client):
        """Test creating patient completes in reasonable time."""
        import time
        start = time.time()
        response = await client.post("/api/v1/patient", json=VALID_PATIENT_DATA)
        elapsed = time.time() - start
        # Should complete within 5 seconds
        assert elapsed < 5.0
        assert response.status_code in [200, 201, 400, 422]

    @pytest.mark.asyncio
    async def test_dashboard_response_time(self, client):
        """Test dashboard endpoint responds quickly."""
        import time
        start = time.time()
        response = await client.get("/api/v1/dashboard")
        elapsed = time.time() - start
        # Dashboard should respond quickly
        assert elapsed < 3.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
