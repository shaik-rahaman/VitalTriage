# VitalTriage Frontend - Complete Setup Guide

## 📋 Overview

A complete React + TypeScript + Tailwind CSS frontend for the VitalTriage hospital patient monitoring system. Built with modern tools and best practices.

## 🏗️ Project Architecture

### Directory Structure
```
frontend/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── AlertBanner/      # Critical alerts notification
│   │   ├── Dashboard/        # Main dashboard grid view
│   │   ├── PatientCard/      # Individual patient card
│   │   ├── Forms/            # Add/Update patient forms
│   │   │   ├── AddPatientForm.tsx
│   │   │   └── UpdatePatientForm.tsx
│   │   └── Layout/           # Page layout components
│   │       ├── Header.tsx
│   │       └── Footer.tsx
│   │
│   ├── pages/                # Page components (for future routing)
│   │   ├── DashboardPage.tsx
│   │   ├── AddPatientPage.tsx
│   │   └── PatientDetailsPage.tsx
│   │
│   ├── services/             # API & external services
│   │   └── api.ts            # Axios-based API client
│   │
│   ├── store/                # State management (Zustand)
│   │   └── useStore.ts       # Global app store
│   │
│   ├── types/                # TypeScript type definitions
│   │   └── patient.ts        # Patient-related types
│   │
│   ├── utils/                # Helper functions
│   │   └── formatters.ts     # Data formatting utilities
│   │
│   ├── styles/               # CSS & Tailwind setup
│   │   └── index.css         # Main stylesheet
│   │
│   ├── App.tsx               # Root component with routing
│   └── main.tsx              # React entry point
│
├── index.html                # HTML entry point
├── package.json              # Dependencies & scripts
├── tsconfig.json             # TypeScript config
├── vite.config.ts            # Vite build config
├── tailwind.config.ts        # Tailwind CSS config
├── postcss.config.js         # PostCSS config (for Tailwind)
├── .eslintrc.json            # ESLint config
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ (recommended: 18 LTS)
- npm 7+ or yarn
- Backend API running on `http://localhost:8000`

### Installation Steps

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```
   
   This will install all required packages:
   - React 18.2.0
   - TypeScript 5.0.2
   - Tailwind CSS 3.3.2
   - React Query 3.39.3
   - Zustand 4.4.0
   - Axios 1.6.2
   - Lucide React (icons)
   - Vite 4.4.5

3. **Create environment file**
   ```bash
   cp .env.example .env
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```
   
   The app will be available at `http://localhost:5174`

### Build for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` directory.

## 🔧 Configuration

### Environment Variables (.env)
```env
# Backend API configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=10000  # milliseconds
```

### Tailwind CSS Customization
Edit `tailwind.config.ts` to customize:
- Colors (critical: red, high: orange, moderate: yellow, stable: green)
- Animations (pulse, flash)
- Theme extensions

### Vite Configuration
The `vite.config.ts` includes:
- React plugin
- Path aliases (@components, @pages, @services, etc.)
- Proxy for API calls to `/api/*`

## 📦 Core Components

### 1. Dashboard Component
**Location**: `src/components/Dashboard/Dashboard.tsx`

Displays patients in four columns based on severity:
- Critical (Red)
- High (Orange)
- Moderate (Yellow)
- Stable (Green)

**Props**:
```typescript
interface DashboardProps {
  data: DashboardData;
  isLoading: boolean;
  onPatientClick: (patient: Patient) => void;
}
```

### 2. Patient Card Component
**Location**: `src/components/PatientCard/PatientCard.tsx`

Shows individual patient information with vitals and alerts.

**Features**:
- Color-coded severity indicator
- Vital signs display
- Alert messages
- Animated pulse for critical patients
- Click handler for patient selection

### 3. Alert Banner Component
**Location**: `src/components/AlertBanner/AlertBanner.tsx`

Sticky banner at top showing critical alerts.

**Features**:
- Auto-rotating through critical patients
- Dismissible
- Flashing animation
- Sticky positioning

### 4. Add Patient Form
**Location**: `src/components/Forms/AddPatientForm.tsx`

Modal form for adding new patients.

**Form Fields**:
- Patient Name (required)
- Age (required, 0-150)
- Gender (required: Male, Female, Other)
- Ward (required)
- Room (required)
- Heart Rate (bpm)
- Oxygen Saturation (%)
- Blood Pressure
- Temperature (°C)
- Respiratory Rate
- Notes

**Validation**: Client-side validation with error messages

### 5. Update Patient Form
**Location**: `src/components/Forms/UpdatePatientForm.tsx`

Similar to Add form but pre-populated with patient data.

## 💾 State Management (Zustand)

**Location**: `src/store/useStore.ts`

Global store with the following state:
```typescript
{
  selectedPatient: Patient | null;
  showAddPatientModal: boolean;
  showUpdatePatientModal: boolean;
  isLoading: boolean;
  error: string | null;
  autoRefreshEnabled: boolean;
  refreshInterval: number; // milliseconds
}
```

**Usage**:
```typescript
const store = useStore();
store.setSelectedPatient(patient);
store.setShowAddPatientModal(true);
```

## 🔌 API Integration

**Location**: `src/services/api.ts`

Axios-based API client with endpoints:

### Methods
- `getDashboard()` - Get patients grouped by severity
- `getPatient(id: string)` - Get single patient details
- `getAllPatients()` - Get all patients
- `createPatient(data: CreatePatientRequest)` - Add new patient
- `updatePatient(id: string, data: UpdatePatientRequest)` - Update patient
- `deletePatient(id: string)` - Delete patient
- `healthCheck()` - Verify backend connectivity

### Error Handling
- Automatic error logging
- Throws errors for component handling
- Configurable timeout

## 📊 Data Fetching (React Query)

**Location**: `src/pages/DashboardPage.tsx`

Uses React Query for:
- Dashboard data caching
- Auto-refresh every 5 seconds
- Stale time management
- Automatic refetching on focus

**Configuration**:
```typescript
const { data, isLoading, refetch } = useQuery(
  'dashboard',
  () => apiClient.getDashboard(),
  {
    refetchInterval: 5000,
    staleTime: 5000,
  }
);
```

## 🎨 Styling with Tailwind CSS

### Custom Utilities (in `src/styles/index.css`):
- `.status-critical` - Red status badge
- `.status-high` - Orange status badge
- `.status-moderate` - Yellow status badge
- `.status-stable` - Green status badge
- `.glass` - Glass-morphism effect

### Color Palette
- Critical: `#dc2626` (red-600)
- High: `#f97316` (orange-600)
- Moderate: `#eab308` (yellow-600)
- Stable: `#16a34a` (green-600)

### Animations
- `pulse` - Gentle opacity pulse
- `flash` - Rapid flash for alerts

## 🔄 Data Flow

```
DashboardPage (Main Component)
├── useQuery() → API → getDashboard()
├── useStore() → Global state
└── Renders:
    ├── Header
    ├── AlertBanner (if critical patients exist)
    ├── Dashboard
    │   ├── Summary Cards (stats)
    │   └── Patient Columns
    │       └── PatientCard × N
    ├── AddPatientForm (if modal visible)
    ├── UpdatePatientForm (if modal visible)
    └── Footer
```

## 🧪 Component Usage Examples

### Using Dashboard
```tsx
import Dashboard from '@components/Dashboard/Dashboard';

<Dashboard
  data={dashboardData}
  isLoading={isLoading}
  onPatientClick={(patient) => store.setSelectedPatient(patient)}
/>
```

### Using PatientCard
```tsx
import PatientCard from '@components/PatientCard/PatientCard';

<PatientCard
  patient={patient}
  onClick={() => handlePatientClick(patient)}
/>
```

### Using AddPatientForm
```tsx
import AddPatientForm from '@components/Forms/AddPatientForm';

<AddPatientForm
  onSubmit={handleAddPatient}
  onClose={() => store.setShowAddPatientModal(false)}
  isLoading={store.isLoading}
/>
```

## 📝 Type Definitions

**Location**: `src/types/patient.ts`

```typescript
enum SeverityLevel {
  CRITICAL = 'critical',
  HIGH = 'high',
  MODERATE = 'moderate',
  STABLE = 'stable',
}

interface Patient {
  id: string;
  patient_id: string;
  name: string;
  age: number;
  gender: string;
  ward: string;
  room: string;
  vitals: Vitals;
  symptoms?: string[];
  notes?: string;
  severity: SeverityLevel;
  alerts?: string[];
  created_at?: string;
  updated_at?: string;
}

interface DashboardData {
  critical: Patient[];
  high: Patient[];
  moderate: Patient[];
  stable: Patient[];
}
```

## 🛠️ Development Scripts

```bash
# Start development server with HMR
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run ESLint (when eslint packages are added)
npm run lint
```

## 📱 Responsive Design

The frontend is responsive with breakpoints:
- **Mobile**: < 640px (sm)
- **Tablet**: 640px - 1024px (md)
- **Desktop**: > 1024px (lg)

Dashboard uses:
- 1 column on mobile
- 2 columns on tablet
- 4 columns on desktop

## ⚡ Performance Optimizations

1. **Code Splitting**: Vite handles automatic chunks
2. **CSS Optimization**: Tailwind purges unused styles
3. **Data Caching**: React Query caches responses
4. **State Updates**: Zustand for minimal re-renders
5. **Asset Optimization**: Vite bundles optimally

## 🔍 Debugging

### Browser DevTools
1. **React DevTools**: Inspect components
2. **Network Tab**: Monitor API calls
3. **Console**: Check for errors
4. **Lighthouse**: Performance audit

### React Query DevTools (optional)
Install for advanced debugging:
```bash
npm install @tanstack/react-query-devtools
```

### TypeScript Checking
```bash
npx tsc --noEmit
```

## 📚 Utility Functions

**Location**: `src/utils/formatters.ts`

Available functions:
- `getSeverityColor(severity)` - Get color name
- `getSeverityBgClass(severity)` - Get Tailwind bg class
- `getSeverityTextClass(severity)` - Get Tailwind text class
- `getSeverityIcon(severity)` - Get emoji icon
- `formatDate(dateString)` - Format date/time
- `formatVital(key, value)` - Format vital sign with unit
- `getAlertIcon(severity)` - Get alert emoji

## 🚀 Deployment

### Build
```bash
npm run build
```

### Serve
The `dist/` folder contains static files ready for:
- Nginx
- Apache
- Vercel
- Netlify
- Any static host

### Environment
Update `.env` for production API URL:
```env
VITE_API_BASE_URL=https://your-api-domain.com
```

## 🔒 Security Considerations

1. **API Security**: Use HTTPS in production
2. **CORS**: Configure on backend
3. **Environment Secrets**: Never commit `.env`
4. **Input Validation**: Implemented in forms
5. **XSS Protection**: React handles by default

## 🐛 Troubleshooting

### Issue: Cannot connect to API
**Solution**: 
- Verify backend is running
- Check API URL in `.env`
- Ensure CORS is enabled on backend

### Issue: Form submission fails
**Solution**:
- Check browser console for errors
- Verify all required fields are filled
- Check Network tab for API response

### Issue: Styling looks broken
**Solution**:
- Rebuild with `npm run build`
- Clear browser cache
- Verify Tailwind config is correct

### Issue: Hot reload not working
**Solution**:
- Restart dev server: `npm run dev`
- Check Vite configuration
- Clear `.vite` cache

## 📞 Support & Contributing

For issues or improvements:
1. Check the README.md
2. Review browser console errors
3. Check React Query DevTools
4. Review API responses in Network tab

## 📄 Additional Resources

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [React Query Docs](https://tanstack.com/query/latest)
- [Zustand Docs](https://github.com/pmndrs/zustand)
- [Vite Docs](https://vitejs.dev)

## ✅ Checklist for Running Frontend

- [ ] Node.js 16+ installed
- [ ] Dependencies installed: `npm install`
- [ ] Backend API running on `:8000`
- [ ] Environment file created: `.env`
- [ ] Dev server started: `npm run dev`
- [ ] Frontend accessible at `http://localhost:5174`
- [ ] Can see dashboard with patient data
- [ ] Can add new patient
- [ ] Can see critical alerts in banner

## 🎉 You're Ready!

The VitalTriage frontend is now fully set up and ready for development. Start building amazing features!
