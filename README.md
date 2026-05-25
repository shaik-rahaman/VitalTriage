# 🚑 VitalTriage

AI-powered Clinical Decision & Triage Intelligence Platform designed for real-time patient risk assessment, intelligent triage workflows, and AI-assisted clinical decision support.

Built using FastAPI, MongoDB, LLM orchestration, retrieval workflows, and production-oriented cloud deployment architecture.

---

# 🌐 Live Demo

Live Application:
https://vitaltriage.ddns.net

Note:
This platform is intended for demonstration, engineering evaluation, and AI workflow showcase purposes only.

---

# 🔥 Highlights

* 🏥 AI-powered patient triage and monitoring platform
* 🚨 Real-time severity classification and critical patient detection
* 📊 Transparent risk scoring engine with auditability
* 🤖 LLM-powered clinical explanations and suggested actions
* 🧠 Hybrid AI + deterministic rule-based architecture
* 📡 Real-time dashboard APIs grouped by patient severity
* ☁️ Production deployment using Azure VM, Nginx, PM2, and HTTPS
* 🔐 Secure backend architecture with environment-based configuration

---

# 🎯 Use Case

Designed for healthcare and clinical operations scenarios to:

* Monitor patient vitals in real time
* Prioritize patients based on severity
* Generate AI-assisted clinical insights
* Improve triage decision workflows
* Support healthcare operational visibility
* Enable intelligent patient monitoring systems

This project demonstrates a real-world AI-assisted clinical decision-support architecture with human-in-the-loop workflows.

---

# 📸 Screenshots

## Dashboard

Real-time patient monitoring dashboard with severity grouping and operational visibility.

![Dashboard](./screenshots/dashboard.png)

---

## Patient Risk Analysis

AI-assisted patient severity scoring and clinical workflow insights.

![Risk Analysis](./screenshots/risk-analysis.png)

---

## AI Clinical Assistant

LLM-powered clinical reasoning and suggested action workflows.

![AI Assistant](./screenshots/ai-assistant.png)

---

# 🧠 AI Capabilities

* AI-assisted clinical triage workflows
* LLM-powered patient condition explanations
* Intelligent severity classification
* Rule-engine-driven risk scoring
* Conversational AI integration
* Retrieval-enhanced clinical workflows
* Real-time decision-support orchestration
* Transparent and auditable scoring system

---

# 🏗️ Architecture

Frontend:

* React
* TypeScript
* Dashboard UI

Backend:

* FastAPI
* Python
* Async APIs
* Pydantic validation

AI Layer:

* LLM orchestration
* Clinical reasoning workflows
* Retrieval-enhanced AI pipelines
* Prompt-driven explanation generation

Database:

* MongoDB Atlas
* Async Motor driver

Infrastructure:

* Azure VM
* Nginx reverse proxy
* PM2 process management
* HTTPS / Let's Encrypt

---

# 🛠️ Technology Stack

| Layer      | Technologies                          |
| ---------- | ------------------------------------- |
| Frontend   | React, TypeScript                     |
| Backend    | FastAPI, Python, AsyncIO              |
| Database   | MongoDB Atlas, Motor                  |
| AI/ML      | OpenAI / LLM APIs, Prompt Engineering |
| Validation | Pydantic                              |
| DevOps     | Azure VM, PM2, Nginx, HTTPS           |
| APIs       | REST APIs                             |

---

# 📊 Clinical Scoring Engine

## Critical Override Rules

Patients are immediately classified as CRITICAL if any condition is met:

* SpO2 < 85%
* Systolic BP < 90
* Heart Rate > 140 bpm
* Temperature > 104°F
* Respiratory Rate > 30

---

## Severity Mapping

| Score | Severity |
| ----- | -------- |
| ≥80   | CRITICAL |
| 60-79 | HIGH     |
| 30-59 | MODERATE |
| <30   | STABLE   |

---

# 🚀 Quick Start

## Prerequisites

* Python 3.9+
* MongoDB
* OpenAI API Key (optional)

---

## Local Development

### Install Dependencies

```bash id="vtread1"
cd backend
pip install -r requirements.txt
```

---

## Configure Environment

```bash id="vtread2"
cp .env.example .env
```

---

## Backend Environment Variables

```env id="vtread3"
MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=vitaltriage_db
OPENAI_API_KEY=your_openai_api_key
ENVIRONMENT=development
DEBUG=True
```

---

## Run Application

```bash id="vtread4"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

---

## Access

API:
http://localhost:8002

API Docs:
http://localhost:8002/docs

ReDoc:
http://localhost:8002/redoc

Health Check:
http://localhost:8002/api/v1/health

---

# 📡 API Endpoints

| Endpoint                 | Description                   |
| ------------------------ | ----------------------------- |
| POST /api/v1/patient     | Create patient                |
| PUT /api/v1/patient/{id} | Update patient                |
| GET /api/v1/patient/{id} | Get patient details           |
| GET /api/v1/dashboard    | Dashboard grouped by severity |
| GET /api/v1/health       | Health check                  |

---

# 🐳 Deployment

Supports deployment using:

* Azure VM
* Docker
* PM2
* Nginx reverse proxy
* HTTPS / Let's Encrypt

---

# ☁️ Production Infrastructure

* Azure VM deployment
* Nginx reverse proxy
* PM2 process management
* HTTPS-enabled deployment
* MongoDB Atlas
* Environment-based configuration
* Async backend processing

---

# 🔐 Security

* Environment-variable-based secret management
* HTTPS-enabled deployment
* Request validation using Pydantic
* Secure API configuration
* MongoDB Atlas authentication
* Production-ready deployment practices

---

# 📂 Project Structure

```bash id="vtread5"
backend/
├── app/
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── db/
│   └── utils/
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙️ Performance & Scalability

* Async/Await implementation
* Non-blocking database operations
* MongoDB indexing support
* Modular service architecture
* Production-oriented API design
* Scalable AI workflow integration

---

# 🧪 Testing

Run tests:

```bash id="vtread6"
pytest tests/ -v
```

Run coverage:

```bash id="vtread7"
pytest tests/ --cov=app --cov-report=html
```

---

# 🚢 Cloud Readiness

Supports deployment to:

* Azure VM
* Docker-based infrastructure
* AWS
* Render
* Railway
* Kubernetes-compatible environments

---

# 👨‍💻 Author

Shaik Rahaman

LinkedIn:
https://www.linkedin.com/in/shaikrahaman

GitHub:
https://github.com/shaik-rahaman

---

# 📝 License

© 2026 VitalTriage
