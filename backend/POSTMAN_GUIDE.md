# 📮 VitalTriage Postman Collection Guide

## 📥 Import Instructions

### Step 1: Import the Collection
1. Open **Postman**
2. Click on **Import** (top-left corner)
3. Click **Upload Files** tab
4. Select: `VitalTriage_API.postman_collection.json`
5. Click **Import**

### Step 2: Import the Environment
1. Click **Environments** (left sidebar)
2. Click **Import** (top-right)
3. Select: `VitalTriage_Environment.postman_environment.json`
4. Click **Import**

### Step 3: Select the Environment
1. Top-right corner, select dropdown
2. Choose **VitalTriage Environment**

---

## 🌐 Collection Overview

### Base URL
```
http://localhost:8000
```

### Available Endpoints

#### 1. **Create Patient** 
- **Method:** `POST`
- **URL:** `/api/v1/patient`
- **Purpose:** Create a new patient record with vital signs
- **Test Cases Included:** CRITICAL, HIGH, MODERATE, STABLE patients

#### 2. **Get Patient by ID**
- **Method:** `GET`
- **URL:** `/api/v1/patient/{patient_id}`
- **Purpose:** Retrieve patient details
- **Example:** `/api/v1/patient/P001`

#### 3. **Update Patient Vitals**
- **Method:** `PUT`
- **URL:** `/api/v1/patient/{patient_id}`
- **Purpose:** Update patient vital signs and symptoms
- **Example:** `/api/v1/patient/P001`

#### 4. **Get Dashboard**
- **Method:** `GET`
- **URL:** `/api/v1/dashboard`
- **Purpose:** Get all patients grouped by severity level

---

## 📋 Collection Structure

### 1. Patient Management
- Create Patient (basic template)
- Get Patient by ID
- Update Patient Vitals
- Get Dashboard

### 2. Test Scenarios
Pre-configured requests for testing different severity levels:
- **CRITICAL Patient:** All critical thresholds exceeded (score ≥80)
- **STABLE Patient:** All normal vitals (score <30)
- **HIGH RISK Patient:** Multiple elevated vitals (score 60-79)

### 3. Bulk Testing
Templates for quick repeated testing:
- Template 1: Mild symptoms
- Template 2: Elevated vitals

---

## 🧪 Testing Guide

### Quick Start Test (5 minutes)

1. **Create a Moderate Patient**
   - Request: `Create Patient` (Patient Management)
   - Expected Status: `201 Created`
   - Check Response: `severity: "MODERATE"`, `score: 45`

2. **Retrieve Patient**
   - Request: `Get Patient by ID`
   - Change `patient_id` variable to: `P001`
   - Expected Status: `200 OK`

3. **Update Patient Vitals**
   - Request: `Update Patient Vitals`
   - Update vitals to show deterioration
   - Expected Status: `200 OK`
   - Check: `severity` changed to `"HIGH"`, `score` increased

4. **View Dashboard**
   - Request: `Get Dashboard`
   - Expected Status: `200 OK`
   - Check: Patients grouped by severity

---

## 🎯 Test Scenarios to Try

### Scenario 1: Normal Patient
Run: `Create STABLE Patient`
- Expected severity: `STABLE`
- Expected score: ~15-25

### Scenario 2: Concerning Vitals
Run: `Create HIGH RISK Patient`
- Expected severity: `HIGH`
- Expected score: 60-79

### Scenario 3: Emergency Case
Run: `Create CRITICAL Patient`
- Expected severity: `CRITICAL`
- Expected score: 80-100
- Alert: 🚨 CRITICAL

### Scenario 4: Deteriorating Patient
1. Run: `Create Patient` (basic)
2. Run: `Update Patient Vitals` with worse values
3. Check how severity increases

---

## 📊 Example Request/Response

### Request: Create Patient
```json
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
  "symptoms": ["fever", "cough"],
  "notes": "Initial assessment"
}
```

### Response: 201 Created
```json
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
  "symptoms": ["fever", "cough"],
  "score": 45,
  "severity": "MODERATE",
  "alert": "⚠️ Moderate risk - Monitor closely",
  "explanation": "Patient shows moderate vital sign abnormalities...",
  "timestamp": "2026-04-23T12:00:00Z",
  "_id": "507f1f77bcf86cd799439011"
}
```

---

## ⚙️ Using Environment Variables

### Available Variables:
- `{{baseUrl}}` → `http://localhost:8000`
- `{{patientId}}` → `P001` (change as needed)
- `{{contentType}}` → `application/json`

### How to Use:
In any request, use: `{{baseUrl}}/api/v1/patient/{{patientId}}`

### Change Variable:
1. Click **VitalTriage Environment** dropdown
2. Click the eye icon (👁️)
3. Edit values directly

---

## 🔍 Validation Checks

### When creating a patient, the API validates:

| Field | Valid Range | Example |
|-------|------------|---------|
| **SpO2** | 0-100 | 94 ✓ |
| **Heart Rate** | 30-200 | 88 ✓ |
| **Systolic BP** | 70-200 | 140 ✓ |
| **Temperature** | 95-110°F | 99.5 ✓ |
| **Respiratory Rate** | 10-40 | 20 ✓ |

Invalid values will return `400 Bad Request`

---

## 🚨 Severity Scoring

| Score | Severity | Action |
|-------|----------|--------|
| ≥80 | **CRITICAL** | 🚨 Emergency intervention |
| 60-79 | **HIGH** | 🔴 Immediate attention |
| 30-59 | **MODERATE** | ⚠️ Monitor closely |
| <30 | **STABLE** | ✅ Routine monitoring |

---

## 💡 Tips & Tricks

### 1. Modify Patient ID
- Click any `patient_id` in request body
- Change value before sending

### 2. Run Multiple Requests
- Select requests in collection
- Right-click → **Run**

### 3. Save Responses
- Send request
- Click **Save** button
- Create a custom name

### 4. View Response Headers
- After sending request
- Click **Headers** tab to see metadata

### 5. Set Up Pre-request Script
- Click request → **Pre-request Script**
- Add dynamic ID: `pm.environment.set("patientId", "P" + Math.random())`

---

## 🐛 Troubleshooting

### Error: `Connection Refused`
- ✅ Backend server not running
- **Fix:** Start server: `python3 -m uvicorn app.main:app --reload`

### Error: `404 Not Found`
- ✅ Incorrect endpoint URL
- **Fix:** Check URL matches `/api/v1/...`

### Error: `400 Bad Request`
- ✅ Invalid vital signs values
- **Fix:** Check values are within valid ranges

### Error: `MongoDB Connection Error`
- ✅ Expected if MongoDB Atlas unreachable
- **Fix:** API still works, operations queue when MongoDB available

---

## 🔗 Related Files

- **Collection:** `VitalTriage_API.postman_collection.json`
- **Environment:** `VitalTriage_Environment.postman_environment.json`
- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **API Code:** `app/routes/patient_routes.py`

---

## 📞 Support

For issues or questions:
1. Check API logs: See server terminal output
2. Test in Swagger UI: http://localhost:8000/docs
3. Review backend code: `backend/app/routes/`

---

**Happy Testing! 🎉**
