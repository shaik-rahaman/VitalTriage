# 🏥 VitalTriage Frontend Architecture

## 🎯 Objective
Build a modern, intuitive, hospital-grade dashboard for doctors and nurses to:
- View patient criticality in real-time
- Receive alerts for critical patients
- Add/update patient data
- Quickly take action based on insights

---

## 🧭 High-Level UI Flow

Dashboard → Alerts Panel → Patient Cards  
→ Add Patient Form → Update Patient → View Details

---

## 🧱 Tech Stack

- React (with Vite) ⚡
- TypeScript
- Tailwind CSS (for fast, clean UI)
- ShadCN UI (professional components)
- Axios (API calls)
- React Query (data fetching + caching)
- Zustand (lightweight state management)

---

## 📁 Project Structure

frontend/
 ├── src/
 │   ├── components/
 │   │   ├── Dashboard/
 │   │   ├── PatientCard/
 │   │   ├── AlertBanner/
 │   │   ├── Forms/
 │   │   ├── Layout/
 │   ├── pages/
 │   │   ├── DashboardPage.tsx
 │   │   ├── AddPatientPage.tsx
 │   │   ├── PatientDetailsPage.tsx
 │   ├── services/
 │   │   └── api.ts
 │   ├── store/
 │   │   └── useStore.ts
 │   ├── types/
 │   │   └── patient.ts
 │   ├── App.tsx
 │   └── main.tsx

---

## 🧑‍⚕️ Core UI Components

### 1. Dashboard

- Four columns:
  - 🔴 Critical
  - 🟠 High
  - 🟡 Moderate
  - 🟢 Stable

Each column shows:
- Patient cards
- Count of patients
- Color-coded alerts

---

### 2. Patient Card

Shows:
- Patient Name / ID
- Ward / Room
- Severity Badge
- Key vitals (SpO2, HR)
- Alert message

Critical card:
- Red background
- Flash/pulse animation

---

### 3. Alert Banner

Top of screen:
- “🚨 CRITICAL ALERT: Patient P123 needs oxygen immediately”
- Auto-refresh every few seconds

---

### 4. Add / Update Patient Form

Fields:
- Patient ID
- Name
- Age
- Gender
- Ward / Room
- Vitals (HR, SpO2, BP, Temp, RR)
- Symptoms
- Notes

Validation:
- Numeric ranges enforced
- Required fields

---

## 🔌 API Integration

Base URL:
http://localhost:8002

### Endpoints:

- POST /patient → create
- PUT /patient/{id} → update
- GET /dashboard → grouped data
- GET /patient/{id} → details

---

## 📊 State Management

Use React Query:
- Fetch dashboard data
- Auto-refresh every 5–10 seconds

Use Zustand:
- Store selected patient
- UI state (modals, forms)

---

## 🎨 UI Design Principles

- Minimal cognitive load
- Large readable fonts
- High contrast colors
- Immediate visual alerts

---

## 🚨 Critical UX Features

- Flashing red cards for CRITICAL patients
- Sticky alert banner
- Real-time updates
- One-click navigation to patient details

---

## 🧪 Demo Enhancements

- Preload sample patients
- Simulate live updates
- Add loading skeletons

---

## 🚀 Future Enhancements

- WebSocket real-time updates
- Mobile responsive layout
- Dark mode
- Voice alerts

---

## ✅ Key Principles

- Speed > complexity
- Clarity > features
- Alerts must be unmissable
- Designed for real doctors, not demos
