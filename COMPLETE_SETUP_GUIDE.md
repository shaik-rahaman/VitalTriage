# 🏥 VitalTriage - Complete Setup & Run Guide

A full-stack hospital patient monitoring system with AI-powered risk assessment.

---

## 📋 What You Have

### Backend (Python FastAPI)
- Risk scoring engine
- MongoDB integration
- OpenAI LLM integration
- RESTful API
- Async operations

### Frontend (React + TypeScript)
- Real-time dashboard
- Patient management
- Alert system
- Tailwind CSS styling

---

## 🚀 Quick Start (2 Steps)

### Step 1: Start Backend (Terminal 1)
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

### Step 2: Start Frontend (Terminal 2)
```bash
cd frontend
npm install  # First time only
npm run dev
```

**Done!** Open `http://localhost:5174` in your browser.

---

## 🔧 Detailed Setup

### Prerequisites

```bash
# Check Python version (need 3.9+)
python3 --version

# Check Node version (need 16+)
node --version

# Check npm version (need 7+)
npm --version

# Check if MongoDB is available
# Option 1: Local MongoDB
brew services list | grep mongodb

# Option 2: Docker MongoDB
docker ps | grep mongo
```

---

## 📦 Backend Setup (Python FastAPI)

### 1. Create Virtual Environment
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Dependencies included:
- FastAPI 0.104.1
- Uvicorn 0.24.0
- Motor 3.3.2 (Async MongoDB)
- Pydantic 2.13.3
- OpenAI 2.32.0
- Python-dotenv 1.0.0

### 3. Configure Environment

Copy template:
```bash
cp .env.example .env
```

Edit `.env` file:
```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=vitaltriage_db

# OpenAI Configuration (Optional)
OPENAI_API_KEY=sk_your_key_here

# Server Configuration
PORT=8002
HOST=0.0.0.0
ENVIRONMENT=development
```

### 4. Setup MongoDB

**Option A: Local MongoDB (macOS)**
```bash
# Install
brew tap mongodb/brew
brew install mongodb-community

# Start service
brew services start mongodb-community

# Verify connection
mongosh  # Should connect to localhost:27017
```

**Option B: Docker**
```bash
docker run -d -p 27017:27017 --name vitaltriage-mongo mongo:latest
```

**Option C: MongoDB Atlas (Cloud)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Update `MONGO_URI` in `.env`

### 5. Run Backend Server

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

**Success indicators:**
- Terminal shows: `Uvicorn running on http://0.0.0.0:8002`
- Can access http://localhost:8002/docs (API documentation)
- Can access http://localhost:8002/api/v1/health (health check)

### Backend File Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── db/
│   │   └── mongo.py         # MongoDB connection
│   ├── models/
│   │   └── patient_model.py # Data models
│   ├── routes/
│   │   └── patient_routes.py # API endpoints
│   ├── services/
│   │   ├── alert_service.py
│   │   ├── llm_service.py
│   │   ├── rules_engine.py
│   │   └── scoring_service.py
│   └── utils/
│       └── validators.py     # Input validation
├── tests/
│   └── test_api.py          # API tests
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── Makefile                 # Useful commands
└── README.md               # Backend docs
```

---

## 📱 Frontend Setup (React + TypeScript)

### 1. Install Dependencies
```bash
cd frontend
npm install
```

Installs:
- React 18.2.0
- TypeScript 5.0.2
- Tailwind CSS 3.3.2
- React Query 3.39.3
- Zustand 4.4.0
- Axios 1.6.2
- Vite 4.4.5

### 2. Configure Environment

Copy template:
```bash
cp .env.example .env
```

Edit `.env` file:
```env
# Backend API Configuration
VITE_API_BASE_URL=http://localhost:8002
VITE_API_TIMEOUT=10000
```

### 3. Run Development Server

```bash
npm run dev
```

**Success indicators:**
- Terminal shows: `Local: http://localhost:5174/`
- Can access http://localhost:5174 in browser
- Dashboard loads with patient data

### 4. Production Build (Optional)

```bash
npm run build
```

Creates optimized `dist/` folder ready for deployment.

### Frontend File Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── AlertBanner/
│   │   ├── Dashboard/
│   │   ├── PatientCard/
│   │   ├── Forms/
│   │   │   ├── AddPatientForm.tsx
│   │   │   └── UpdatePatientForm.tsx
│   │   └── Layout/
│   ├── pages/
│   │   ├── DashboardPage.tsx
│   │   ├── AddPatientPage.tsx
│   │   └── PatientDetailsPage.tsx
│   ├── services/
│   │   └── api.ts          # API client
│   ├── store/
│   │   └── useStore.ts     # State management
│   ├── types/
│   │   └── patient.ts      # TypeScript types
│   ├── utils/
│   │   └── formatters.ts   # Helper functions
│   ├── styles/
│   │   └── index.css       # Tailwind CSS
│   ├── App.tsx             # Root component
│   └── main.tsx            # Entry point
├── index.html              # HTML template
├── package.json            # NPM dependencies
├── tsconfig.json           # TypeScript config
├── vite.config.ts          # Vite config
├── tailwind.config.ts      # Tailwind config
└── README.md              # Frontend docs
```

---

## ✅ Verification Checklist

### Backend Running?
```bash
# Test backend is running
curl http://localhost:8002/api/v1/health

# Expected response:
# {"status":"healthy","timestamp":"2024-04-23T12:34:56"}
```

### Frontend Running?
```bash
# Check frontend is accessible
curl http://localhost:5173

# Open browser
open http://localhost:5173
```

### Can Create Patient?
```bash
curl -X POST http://localhost:8002/api/v1/patient \
  -H "Content-Type: application/json" \
  -d '{
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
    }
  }'
```

---

## 🔌 API Endpoints

All endpoints are prefixed with `/api/v1`

### Dashboard
- `GET /dashboard` - Get all patients grouped by severity

### Patients
- `POST /patient` - Create new patient
- `GET /patient/{id}` - Get patient details
- `GET /patients` - Get all patients
- `PUT /patient/{id}` - Update patient
- `DELETE /patient/{id}` - Delete patient

### Health
- `GET /health` - Server health check

### Documentation
- `GET /docs` - Interactive API docs (Swagger UI)
- `GET /redoc` - Alternative API docs (ReDoc)

---

## 🐛 Troubleshooting

### Backend Issues

#### "No module named 'fastapi'"
```bash
# Activate virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### "Connection refused" (MongoDB)
```bash
# Start MongoDB
brew services start mongodb-community

# Or with Docker
docker run -d -p 27017:27017 --name vitaltriage-mongo mongo:latest

# Verify connection
mongosh
```

#### Port 8002 already in use
```bash
# Find process using port 8002
lsof -i :8002

# Kill process (if needed)
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### Frontend Issues

#### "npm: command not found"
```bash
# Install Node.js from https://nodejs.org
# Or with Homebrew
brew install node
```

#### "VITE_API_BASE_URL not found"
```bash
# Create .env file
cp .env.example .env

# Update with correct API URL
VITE_API_BASE_URL=http://localhost:8002
```

#### Port 5173 already in use
```bash
# Find process
lsof -i :5173

# Kill process
kill -9 <PID>

# Vite will auto-increment port, or specify:
npm run dev -- --port 5174
```

#### API calls failing
```bash
# Verify backend is running
curl http://localhost:8002/api/v1/health

# Check browser console for errors
# Open DevTools: F12
# Check Network tab for API calls
```

---

## 🚀 Common Tasks

### Add Demo Data
```bash
cd backend
source .venv/bin/activate
python demo_data.py
```

### Run Backend Tests
```bash
cd backend
source .venv/bin/activate
pytest tests/
```

### Build Frontend for Deployment
```bash
cd frontend
npm run build

# Output in dist/ directory
ls dist/
```

### View API Documentation
Open browser to: http://localhost:8002/docs

### Clear Node Modules (if issues)
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Reset MongoDB
```bash
# Stop MongoDB
brew services stop mongodb-community

# Remove data
rm -rf /usr/local/var/mongodb

# Start again
brew services start mongodb-community
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────┐
│              Browser (localhost:5174)               │
│  ┌─────────────────────────────────────────────┐   │
│  │           React Dashboard                    │   │
│  │  - Real-time patient monitoring             │   │
│  │  - Alert system                             │   │
│  │  - Patient management forms                 │   │
│  └─────────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP (Axios)
                   │ Port 8002
                   ▼
┌─────────────────────────────────────────────────────┐
│         FastAPI Backend (localhost:8002)            │
│  ┌─────────────────────────────────────────────┐   │
│  │      REST API Endpoints                      │   │
│  │  - /api/v1/dashboard (patient grouping)     │   │
│  │  - /api/v1/patient (CRUD operations)        │   │
│  │  - /api/v1/health (health check)            │   │
│  └─────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────┐   │
│  │      Business Logic                          │   │
│  │  - Risk Scoring Engine                      │   │
│  │  - Clinical Decision Rules                  │   │
│  │  - LLM Integration (OpenAI)                 │   │
│  └─────────────────────────────────────────────┘   │
└──────────────┬──────────────────────┬───────────────┘
               │                      │
      Port 27017 (TCP)    Optional API Keys
               │                      │
               ▼                      ▼
    ┌──────────────────┐     ┌─────────────────┐
    │   MongoDB        │     │  OpenAI API     │
    │  (Patient Data)  │     │  (Explanations) │
    └──────────────────┘     └─────────────────┘
```

---

## 📝 Next Steps

1. **Verify Setup**
   - Start backend: `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload`
   - Start frontend: `cd frontend && npm run dev`
   - Open http://localhost:5174

2. **Add Sample Patients**
   - Use frontend UI: Click "Add Patient" button
   - Or run: `python backend/demo_data.py`

3. **Test Dashboard**
   - See patients grouped by severity
   - Add new patients
   - Update patient vitals
   - See alerts for critical patients

4. **Explore API**
   - Visit http://localhost:8002/docs
   - Try different endpoints
   - Read API documentation

5. **Production Deployment**
   - Build frontend: `npm run build`
   - Deploy to hosting (Vercel, Netlify, etc.)
   - Deploy backend: Use docker, heroku, or cloud platform

---

## 🆘 Getting Help

### Check Logs
```bash
# Backend: Check terminal output
# Frontend: Open DevTools (F12) → Console tab

# View backend errors
tail -f ~/.npm/_logs/*
```

### Review Documentation
- Backend: `backend/README.md`
- Frontend: `frontend/README.md`
- API Docs: http://localhost:8002/docs
- Setup Details: `frontend/FRONTEND_SETUP.md`

### Common Fixes
1. Kill port processes
2. Restart services
3. Clear caches (rm node_modules, pip cache)
4. Check environment variables
5. Verify MongoDB is running

---

## ✨ Key Features

### Backend
✅ Risk scoring algorithm
✅ MongoDB data persistence
✅ OpenAI LLM integration
✅ Async/await performance
✅ Input validation
✅ Error handling

### Frontend
✅ Real-time dashboard
✅ Patient CRUD operations
✅ Alert system
✅ Responsive design
✅ TypeScript type safety
✅ React Query caching

---

**You're all set! Start building.** 🚀
