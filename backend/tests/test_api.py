"""
API integration tests for VitalTriage backend.
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient
from app.main import app
from app.db import mongo


@pytest_asyncio.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "VitalTriage API"


@pytest.mark.asyncio
async def test_create_patient_valid(client):
    """Test creating patient with valid data."""
    patient_data = {
        "patient_id": "TEST_P001",
        "age": 50,
        "gender": "M",
        "vitals": {
            "heart_rate": 75,
            "spo2": 97,
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "temperature": 98.6,
            "respiratory_rate": 16
        },
        "symptoms": [],
        "notes": "Test patient"
    }
    
    response = await client.post("/api/v1/patient", json=patient_data)
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == "TEST_P001"
    assert data["severity"] == "STABLE"
    assert data["score"] < 30


@pytest.mark.asyncio
async def test_create_patient_invalid_spo2(client):
    """Test creating patient with invalid SpO2."""
    patient_data = {
        "patient_id": "TEST_P002",
        "age": 50,
        "gender": "M",
        "vitals": {
            "heart_rate": 75,
            "spo2": 150,  # Invalid
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "temperature": 98.6,
            "respiratory_rate": 16
        },
        "symptoms": [],
        "notes": "Test patient"
    }
    
    response = await client.post("/api/v1/patient", json=patient_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_critical_patient(client):
    """Test creating critical patient."""
    patient_data = {
        "patient_id": "TEST_CRITICAL",
        "age": 60,
        "gender": "F",
        "vitals": {
            "heart_rate": 150,
            "spo2": 82,
            "systolic_bp": 85,
            "diastolic_bp": 50,
            "temperature": 105,
            "respiratory_rate": 35
        },
        "symptoms": ["breathlessness"],
        "notes": "Critical case"
    }
    
    response = await client.post("/api/v1/patient", json=patient_data)
    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "CRITICAL"
    assert data["score"] >= 80


@pytest.mark.asyncio
async def test_get_patient(client):
    """Test getting patient details."""
    # First create a patient
    patient_data = {
        "patient_id": "TEST_GET",
        "age": 45,
        "gender": "M",
        "vitals": {
            "heart_rate": 75,
            "spo2": 97,
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "temperature": 98.6,
            "respiratory_rate": 16
        },
        "symptoms": [],
        "notes": "Test"
    }
    
    await client.post("/api/v1/patient", json=patient_data)
    
    # Get patient
    response = await client.get("/api/v1/patient/TEST_GET")
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == "TEST_GET"
    assert data["age"] == 45


@pytest.mark.asyncio
async def test_get_nonexistent_patient(client):
    """Test getting nonexistent patient."""
    response = await client.get("/api/v1/patient/NONEXISTENT")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_patient(client):
    """Test updating patient."""
    # First create a patient
    patient_data = {
        "patient_id": "TEST_UPDATE",
        "age": 50,
        "gender": "M",
        "vitals": {
            "heart_rate": 75,
            "spo2": 97,
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "temperature": 98.6,
            "respiratory_rate": 16
        },
        "symptoms": [],
        "notes": "Original"
    }
    
    await client.post("/api/v1/patient", json=patient_data)
    
    # Update patient
    update_data = {
        "vitals": {
            "heart_rate": 85,
            "spo2": 95,
            "systolic_bp": 130,
            "diastolic_bp": 85,
            "temperature": 99.0,
            "respiratory_rate": 18
        },
        "notes": "Updated"
    }
    
    response = await client.put("/api/v1/patient/TEST_UPDATE", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["vitals"]["heart_rate"] == 85
    assert data["notes"] == "Updated"


@pytest.mark.asyncio
async def test_dashboard(client):
    """Test dashboard endpoint."""
    # Create patients with different severities
    patients = [
        {
            "patient_id": "DASH_STABLE",
            "age": 40,
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
            "notes": "Stable"
        },
        {
            "patient_id": "DASH_CRITICAL",
            "age": 70,
            "gender": "F",
            "vitals": {
                "heart_rate": 145,
                "spo2": 82,
                "systolic_bp": 85,
                "diastolic_bp": 50,
                "temperature": 105,
                "respiratory_rate": 32
            },
            "symptoms": ["breathlessness"],
            "notes": "Critical"
        }
    ]
    
    for patient in patients:
        await client.post("/api/v1/patient", json=patient)
    
    # Get dashboard
    response = await client.get("/api/v1/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "critical" in data
    assert "high" in data
    assert "moderate" in data
    assert "stable" in data
    assert len(data["critical"]) > 0
    assert len(data["stable"]) > 0
