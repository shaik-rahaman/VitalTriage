# 🏥 AI Patient Monitoring System — Backend Architecture

## 🎯 Objective
Build a backend system that:
- Accepts patient vitals from UI
- Computes risk score and severity
- Applies critical override rules
- Uses LLM for explanation + suggested actions
- Stores results in MongoDB
- Exposes APIs for dashboard (grouped by severity)

---

# 🧭 High-Level Flow

UI Form → FastAPI → Validation → Rules Engine → Scoring Engine  
→ LLM (Explain + Suggest) → MongoDB → Alerts → Dashboard API

---

# 🗄️ Database Design (MongoDB)

## Collection: `patients`

```json
{
  "_id": "ObjectId",
  "patient_id": "string",
  "age": "number",
  "gender": "string",

  "vitals": {
    "heart_rate": "number",
    "spo2": "number",
    "systolic_bp": "number",
    "diastolic_bp": "number",
    "temperature": "number",
    "respiratory_rate": "number"
  },

  "symptoms": ["string"],
  "notes": "string",

  "score": "number",
  "severity": "CRITICAL | HIGH | MODERATE | STABLE",

  "alert": "string",

  "llm_output": {
    "explanation": "string",
    "suggested_actions": ["string"]
  },

  "audit_log": {
    "rules_triggered": ["string"],
    "score_breakdown": {
      "spo2": "number",
      "bp": "number",
      "hr": "number",
      "rr": "number",
      "temp": "number"
    }
  },

  "timestamp": "ISODate"
}
```

---

# ⚙️ Tech Stack

- FastAPI (Backend)
- MongoDB (Database)
- OpenAI / Azure OpenAI (LLM)
- Pydantic (Validation)

---

# 📁 Project Structure

app/
 ├── main.py
 ├── routes/
 │    └── patient_routes.py
 ├── services/
 │    ├── scoring_service.py
 │    ├── rules_engine.py
 │    ├── llm_service.py
 │    ├── alert_service.py
 ├── models/
 │    └── patient_model.py
 ├── db/
 │    └── mongo.py
 ├── utils/
 │    └── validators.py

---

# 🧠 Core Logic

## 1. Critical Override Rules

If any condition is met → severity = CRITICAL

- SpO2 < 85
- Systolic BP < 90
- HR > 140
- Temperature > 104°F
- Respiratory Rate > 30

---

## 2. Range-Based Scoring

### SpO2
| Range | Score |
|------|------|
| ≥ 95 | 0 |
| 90–94 | 30 |
| 85–89 | 70 |
| < 85 | 100 |

Apply similar logic for:
- BP
- HR
- Temperature
- Respiratory Rate

---

## 3. Weight Distribution

- SpO2 → 40%
- BP → 20%
- HR → 15%
- RR → 10%
- Temp → 10%
- Symptoms → 5%

---

## 4. Final Score Calculation

final_score = weighted sum of all parameters

---

## 5. Severity Mapping

| Score | Severity |
|------|--------|
| ≥ 80 | CRITICAL |
| 60–79 | HIGH |
| 30–59 | MODERATE |
| < 30 | STABLE |

---

## 6. Symptoms Scoring

Keyword-based:

breathlessness → +20  
chest pain → +25  
fever → +10  

---

# 🤖 LLM Integration

## Purpose
- Explain condition
- Suggest immediate actions
- DO NOT prescribe medication

## Prompt Template

Patient vitals:
SpO2: {spo2}, HR: {hr}, BP: {bp}, Temp: {temp}, RR: {rr}

Symptoms: {symptoms}
Notes: {notes}

Explain the patient's condition and suggest immediate actions.  
Do NOT prescribe medication.

---

## Expected Output

```json
{
  "explanation": "string",
  "suggested_actions": ["string"]
}
```

---

# 🚨 Alert Generation Logic

- If CRITICAL:
  - SpO2 < 90 → "Immediate oxygen required"
  - Else → "Critical condition – immediate attention required"

- If HIGH:
  - "Close monitoring needed"

- Else:
  - "Stable"

---

# 🌐 API Design

## 1. Create Patient
POST /patient

## 2. Update Patient
PUT /patient/{id}

## 3. Get Dashboard (Grouped)
GET /dashboard

### Response:
```json
{
  "critical": [],
  "high": [],
  "moderate": [],
  "stable": []
}
```

## 4. Get Patient Details
GET /patient/{id}

---

# 🧪 Validation Rules

- SpO2: 0–100
- HR: 30–200
- BP: 70–200 systolic
- Temp: 95–110°F
- RR: 10–40

Reject invalid inputs.

---

# 🧾 Audit Trail

Store:
- Triggered rules
- Score breakdown
- Final decision

---

# ⚡ Processing Mode

- Synchronous (on API call)
- No background jobs

---

# 🎯 Demo Requirements

- Preload 5–8 patients
- Ensure:
  - 2 Critical
  - 2 High
  - 2 Moderate

---

# 🚀 Future Enhancements (Optional)

- Trend analysis
- Multi-hospital support
- Real-time streaming
- Notifications (SMS/Email)

---

# ✅ Key Principles

- Deterministic scoring first
- LLM only for explanation
- No black-box decisions
- Always human-in-the-loop
