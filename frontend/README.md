# VitalTriage Frontend

A modern, hospital-grade real-time patient monitoring dashboard built with React, TypeScript, and Tailwind CSS.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn
- Backend API running on `http://localhost:8002`

### Installation

```bash
# Install dependencies
npm install

# Create .env file from template
cp .env.example .env

# Start development server
npm run dev
```

The application will be available at `http://localhost:5173`

## 📁 Project Structure

```
src/
├── components/
│   ├── AlertBanner/        # Critical alerts banner
│   ├── Dashboard/          # Main dashboard view with patient columns
│   ├── PatientCard/        # Individual patient card component
│   ├── Forms/              # Add/Update patient forms
│   └── Layout/             # Header and Footer
├── pages/
│   ├── DashboardPage.tsx   # Dashboard page (main view)
│   ├── AddPatientPage.tsx  # Add patient page
│   └── PatientDetailsPage.tsx # Patient details view
├── services/
│   └── api.ts              # API client with axios
├── store/
│   └── useStore.ts         # Zustand state management
├── types/
│   └── patient.ts          # TypeScript interfaces and types
├── utils/
│   └── formatters.ts       # Helper functions for formatting
├── styles/
│   └── index.css           # Tailwind CSS setup
├── App.tsx                 # Main app component
└── main.tsx                # React entry point
```

## 🎨 Key Features

### Dashboard
- **Four-Column Layout**: Critical, High, Moderate, Stable patients
- **Real-time Updates**: Auto-refresh every 5 seconds
- **Patient Summary**: Quick stats on patient counts and severity
- **Responsive Design**: Works on desktop and mobile

### Patient Cards
- **Color-coded Severity**: Visual indicators for patient criticality
- **Key Vitals Display**: Heart rate, oxygen saturation, temperature, etc.
- **Alert Messages**: Active alerts displayed on patient cards
- **Pulse Animation**: Critical patients pulse to grab attention

### Alert Banner
- **Sticky Top Position**: Always visible for critical alerts
- **Auto-rotating**: Cycles through critical patients
- **Dismissible**: Can be closed by users
- **Color-coded**: Red for maximum visibility

### Forms
- **Add Patient**: Create new patient records with vitals
- **Update Patient**: Edit existing patient information
- **Form Validation**: Client-side validation for data integrity
- **Loading States**: Visual feedback during API calls

## 🔧 Configuration

### Environment Variables
```env
VITE_API_BASE_URL=http://localhost:8002
VITE_API_TIMEOUT=10000
```

### API Integration
The frontend connects to the backend API at endpoints:
- `GET /dashboard` - Get all patients grouped by severity
- `GET /patient/{id}` - Get individual patient details
- `POST /patient` - Create new patient
- `PUT /patient/{id}` - Update patient
- `DELETE /patient/{id}` - Delete patient

## 📦 Dependencies

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Query** - Data fetching and caching
- **Zustand** - State management
- **Axios** - HTTP client
- **Lucide React** - Icons
- **React Router DOM** - Routing (optional for future pages)

## 🏗️ Building

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 🧪 Development Features

- **Hot Module Replacement (HMR)**: Fast refresh during development
- **Type Checking**: Full TypeScript support
- **Tailwind CSS**: Utility-first CSS framework
- **React Query DevTools**: Debug data fetching

## 🎯 UI/UX Principles

- **Speed > Complexity**: Fast, intuitive interface
- **Clarity > Features**: Clear visual hierarchy
- **Alerts Must Be Unmissable**: Critical patients stand out
- **Hospital-Grade Design**: Professional and reliable

## 📊 State Management

### Zustand Store (`useStore`)
- Selected patient
- Modal visibility (add/update patient)
- Loading states
- Error messages
- Auto-refresh settings

### React Query Cache
- Dashboard data with 5-second auto-refresh
- Individual patient queries
- Automatic cache invalidation

## 🔄 Real-time Updates

The dashboard automatically refreshes every 5 seconds when `autoRefreshEnabled` is true. You can control this via:

```typescript
const store = useStore();
store.setAutoRefreshEnabled(false); // Disable auto-refresh
store.setRefreshInterval(10000);    // Change interval to 10 seconds
```

## 📝 Component Examples

### Using the Dashboard
```tsx
<Dashboard
  data={dashboardData}
  isLoading={isLoading}
  onPatientClick={handlePatientClick}
/>
```

### Using Patient Card
```tsx
<PatientCard
  patient={patient}
  onClick={() => store.setSelectedPatient(patient)}
/>
```

### Using Forms
```tsx
<AddPatientForm
  onSubmit={handleAddPatient}
  onClose={() => setShowModal(false)}
  isLoading={isLoading}
/>
```

## 🚀 Future Enhancements

- [ ] WebSocket real-time updates
- [ ] Mobile responsive layout optimization
- [ ] Dark mode support
- [ ] Voice alerts
- [ ] Patient search and filtering
- [ ] Data export (PDF, CSV)
- [ ] User authentication
- [ ] Audit logs

## 🐛 Troubleshooting

### API Connection Issues
1. Ensure backend is running on `http://localhost:8002`
2. Check `VITE_API_BASE_URL` in `.env`
3. Verify CORS is enabled on backend

### Form Submission Issues
1. Check browser console for errors
2. Verify all required fields are filled
3. Check API response in Network tab

### Performance Issues
1. Disable auto-refresh if not needed
2. Clear React Query cache
3. Check for memory leaks in DevTools

## 📞 Support

For issues or questions:
1. Check the backend logs
2. Review TypeScript errors
3. Inspect React Query DevTools
4. Check browser console for errors

## 📄 License

Part of the VitalTriage project.
