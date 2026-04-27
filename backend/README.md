# VitalTriage - AI Patient Monitoring System Backend

A production-ready FastAPI backend for the VitalTriage AI Patient Monitoring System. This system accepts patient vitals, computes risk scores, applies clinical decision rules, and uses LLM for patient condition explanations.

## 🎯 Features

- **Risk Scoring Engine**: Deterministic, transparent scoring based on vital signs
- **Critical Override Rules**: Immediate identification of critical patients
- **LLM Integration**: AI-powered explanations and suggested actions
- **Dashboard API**: Real-time patient grouping by severity
- **MongoDB Storage**: Persistent patient data with audit trails
- **Async/Await**: Full async implementation using Motor
- **Comprehensive Validation**: Input validation with meaningful error messages
- **Clean Architecture**: Modular, maintainable code structure

## 🛠️ Technology Stack

- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and serialization
- **Motor**: Async MongoDB driver
- **OpenAI**: LLM integration for explanations
- **Uvicorn**: ASGI server

## 📋 Requirements

- Python 3.9+
- MongoDB 4.0+
- OpenAI API key (optional - fallback to defaults if not provided)

## 🚀 Quick Start

### 1. Setup MongoDB

**Option A: Local Installation**
```bash
# macOS with Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

# Or pull Docker image
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**Option B: MongoDB Atlas Cloud**
- Create account at https://www.mongodb.com/cloud/atlas
- Get connection string: `mongodb+srv://user:password@cluster.mongodb.net/vitaltriage_db?retryWrites=true`

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set:
```
MONGO_URI=mongodb://localhost:27017  # or your MongoDB Atlas connection
MONGO_DB_NAME=vitaltriage_db
OPENAI_API_KEY=sk_...               # Optional: Get from https://platform.openai.com/api-keys
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

The API will be available at: `http://localhost:8002`

- **API Docs**: http://localhost:8002/docs
- **ReDoc**: http://localhost:8002/redoc
- **Health Check**: http://localhost:8002/api/v1/health

## 📡 API Endpoints

### 1. Create Patient
```http
POST /api/v1/patient
Content-Type: application/json

{
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
```

**Response:**
```json
{
  "patient_id": "P001",
  "age": 65,
  "gender": "M",
  "vitals": {...},
  "symptoms": ["fever", "chest pain"],
  "notes": "Patient reports mild discomfort",
  "score": 55,
  "severity": "MODERATE",
  "alert": "ℹ️ MODERATE: Standard monitoring - Patient stable but requires attention",
  "llm_output": {
    "explanation": "Patient shows elevated vitals...",
    "suggested_actions": ["Monitor closely", "Administer fluids", "Continue observation"]
  },
  "audit_log": {
    "rules_triggered": [],
    "score_breakdown": {
      "spo2": 30,
      "bp": 20,
      "hr": 0,
      "rr": 20,
      "temperature": 20,
      "symptoms": 25,
      "final_score": 55.0
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 2. Update Patient
```http
PUT /api/v1/patient/{patient_id}
Content-Type: application/json

{
  "vitals": {
    "heart_rate": 85,
    "spo2": 95,
    "systolic_bp": 130,
    "diastolic_bp": 85,
    "temperature": 98.6,
    "respiratory_rate": 18
  },
  "symptoms": ["fever"],
  "notes": "Patient improving"
}
```

### 3. Get Patient Details
```http
GET /api/v1/patient/{patient_id}
```

### 4. Get Dashboard (Grouped by Severity)
```http
GET /api/v1/dashboard
```

**Response:**
```json
{
  "critical": [
    {
      "patient_id": "P003",
      "score": 92,
      "severity": "CRITICAL",
      "alert": "🚨 CRITICAL: Critical condition – immediate attention required",
      ...
    }
  ],
  "high": [...],
  "moderate": [...],
  "stable": [...]
}
```

## 📊 Scoring Algorithm

### Critical Override Rules
If ANY condition is met → CRITICAL severity

- SpO2 < 85%
- Systolic BP < 90
- Heart Rate > 140 bpm
- Temperature > 104°F
- Respiratory Rate > 30

### Range-Based Scoring (0-100)

| Vital | Range | Score |
|-------|-------|-------|
| SpO2 | ≥95% | 0 |
| SpO2 | 90-94% | 30 |
| SpO2 | 85-89% | 70 |
| SpO2 | <85% | 100 |

Similar logic applied to HR, BP, Temperature, RR

### Weight Distribution

- SpO2: 40%
- BP: 20%
- HR: 15%
- RR: 10%
- Temperature: 10%
- Symptoms: 5%

### Severity Mapping

| Score | Severity |
|-------|----------|
| ≥80 | CRITICAL |
| 60-79 | HIGH |
| 30-59 | MODERATE |
| <30 | STABLE |

## 🧪 Example Requests

### Example 1: Critical Patient
```bash
curl -X POST "http://localhost:8002/api/v1/patient" \
  -H "Content-Type: application/json" \
  -d '{
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
    "symptoms": ["breathlessness", "chest pain"],
    "notes": "Severe respiratory distress"
  }'
```

### Example 2: Stable Patient
```bash
curl -X POST "http://localhost:8002/api/v1/patient" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P_STABLE_001",
    "age": 45,
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
    "notes": "Routine checkup"
  }'
```

### Example 3: Get Dashboard
```bash
curl -X GET "http://localhost:8002/api/v1/dashboard" \
  -H "Content-Type: application/json"
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── routes/
│   │   ├── __init__.py
│   │   └── patient_routes.py  # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── scoring_service.py # Risk scoring logic
│   │   ├── rules_engine.py    # Critical rules
│   │   ├── llm_service.py     # LLM integration
│   │   └── alert_service.py   # Alert generation
│   ├── models/
│   │   ├── __init__.py
│   │   └── patient_model.py   # Pydantic models
│   ├── db/
│   │   ├── __init__.py
│   │   └── mongo.py           # MongoDB operations
│   └── utils/
│       ├── __init__.py
│       └── validators.py      # Input validation
├── requirements.txt
├── .env.example
└── README.md
```

## 🔑 Environment Variables

```env
# MongoDB
MONGO_URI              # MongoDB connection string
MONGO_DB_NAME          # Database name (default: vitaltriage_db)

# OpenAI
OPENAI_API_KEY         # OpenAI API key (optional)

# Application
ENVIRONMENT            # development/production
DEBUG                  # True/False
```

## 📝 Logging

The application logs to stdout with the following format:
```
2024-01-15 10:30:00,123 - app.routes.patient_routes - INFO - Patient created: P001 - Severity: MODERATE
```

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## 🚨 Error Handling

The API returns standardized error responses:

```json
{
  "detail": "SpO2 must be between 0 and 100"
}
```

**HTTP Status Codes:**
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error

## ⚙️ Performance Considerations

- **Async Operations**: All database and API calls are non-blocking
- **Connection Pooling**: Motor handles connection pooling automatically
- **Indexing**: MongoDB indexes created on:
  - `patient_id` (unique)
  - `severity`
  - `timestamp`
  - `score`
- **Validation**: Input validation at the API layer

## 🔒 Security Notes

For production:
1. Set `CORS` origins to specific domains
2. Use HTTPS
3. Implement authentication/authorization
4. Use secrets manager for API keys
5. Enable MongoDB authentication
6. Add rate limiting
7. Implement request logging

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Motor Documentation](https://motor.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📞 Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review logs for error details
3. Verify MongoDB connection
4. Check environment variables

---

**Version**: 1.0.0  
**Last Updated**: January 2024
