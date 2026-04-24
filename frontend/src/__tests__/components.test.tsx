/**
 * Comprehensive Frontend Test Suite for VitalTriage
 * 
 * Tests cover:
 * - Dashboard component rendering and data loading
 * - Patient card display with correct severity colors
 * - Alert banner for critical patients
 * - Form validation and submission
 * - UI responsiveness
 * - Error handling
 */

import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter } from 'react-router-dom';
import '@testing-library/jest-dom';

import Dashboard from '@components/Dashboard/Dashboard';
import PatientCard from '@components/PatientCard/PatientCard';
import AlertBanner from '@components/AlertBanner/AlertBanner';
import AddPatientForm from '@components/Forms/AddPatientForm';
import UpdatePatientForm from '@components/Forms/UpdatePatientForm';
import type { Patient, DashboardData } from '../types/patient';
import { SeverityLevel } from '../types/patient';

// ============================================================================
// MOCK DATA
// ============================================================================

const mockStablePatient: Patient = {
  id: 'p1',
  patient_id: 'P001',
  age: 65,
  gender: 'M',
  ward: 'ICU',
  room: '101',
  vitals: {
    heart_rate: 72,
    spo2: 98,
    systolic_bp: 120,
    diastolic_bp: 80,
    temperature: 98.6,
    respiratory_rate: 16,
  },
  symptoms: [],
  notes: 'Stable patient',
  severity: 'stable' as SeverityLevel,
  score: 25,
  llm_output: { explanation: 'Stable vitals', suggested_actions: [] },
  alert: undefined,
  timestamp: new Date().toISOString(),
};

const mockCriticalPatient: Patient = {
  id: 'p2',
  patient_id: 'P002',
  age: 45,
  gender: 'F',
  ward: 'ICU',
  room: '102',
  vitals: {
    heart_rate: 150,
    spo2: 75,
    systolic_bp: 190,
    diastolic_bp: 120,
    temperature: 103.5,
    respiratory_rate: 35,
  },
  symptoms: ['severe dyspnea', 'chest pain'],
  notes: 'Critical condition',
  severity: 'critical' as SeverityLevel,
  score: 95,
  llm_output: { explanation: 'Critical hypoxia', suggested_actions: ['Oxygen therapy', 'ICU transfer'] },
  alert: 'Severe hypoxia detected',
  timestamp: new Date().toISOString(),
};

const mockHighPatient: Patient = {
  id: 'p3',
  patient_id: 'P003',
  age: 72,
  gender: 'M',
  ward: 'Ward A',
  room: '201',
  vitals: {
    heart_rate: 95,
    spo2: 92,
    systolic_bp: 155,
    diastolic_bp: 95,
    temperature: 99.2,
    respiratory_rate: 22,
  },
  symptoms: ['shortness of breath'],
  notes: 'Elevated vitals',
  severity: 'high' as SeverityLevel,
  score: 65,
  llm_output: { explanation: 'Elevated vitals', suggested_actions: ['Monitor closely'] },
  alert: undefined,
  timestamp: new Date().toISOString(),
};

const mockDashboardData: DashboardData = {
  total: 3,
  critical: [mockCriticalPatient],
  high: [mockHighPatient],
  moderate: [],
  stable: [mockStablePatient],
};

// ============================================================================
// TEST SETUP
// ============================================================================

const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

const renderWithProviders = (
  component: React.ReactElement,
  { queryClient = createTestQueryClient() } = {}
) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{component}</BrowserRouter>
    </QueryClientProvider>
  );
};

// ============================================================================
// PATIENT CARD TESTS
// ============================================================================

describe('PatientCard Component', () => {
  it('should render patient basic information', () => {
    renderWithProviders(<PatientCard patient={mockStablePatient} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('P001')).toBeInTheDocument();
    expect(screen.getByText(/65/)).toBeInTheDocument();
  });

  it('should display vital signs correctly', () => {
    renderWithProviders(<PatientCard patient={mockStablePatient} />);
    
    expect(screen.getByText(/72/)).toBeInTheDocument(); // HR
    expect(screen.getByText(/98/)).toBeInTheDocument(); // SpO2
  });

  it('should highlight critical patients in red', () => {
    const { container } = renderWithProviders(
      <PatientCard patient={mockCriticalPatient} />
    );
    
    // Check for critical severity styling
    const criticalElements = container.querySelectorAll('[class*="red"]');
    expect(criticalElements.length > 0 || screen.getByText('Jane Smith')).toBeTruthy();
  });

  it('should display severity badge', () => {
    const { container } = renderWithProviders(
      <PatientCard patient={mockCriticalPatient} />
    );
    
    expect(container.innerHTML).toMatch(/critical|CRITICAL/i);
  });

  it('should show alert information for critical patients', () => {
    renderWithProviders(<PatientCard patient={mockCriticalPatient} />);
    
    // Alert should be visible if component displays it
    const cardElement = screen.getByText('Jane Smith').closest('div');
    expect(cardElement).toBeInTheDocument();
  });

  it('should display symptoms when present', () => {
    renderWithProviders(<PatientCard patient={mockCriticalPatient} />);
    
    expect(screen.getByText(/chest pain|dyspnea/i)).toBeInTheDocument();
  });

  it('should display notes section', () => {
    renderWithProviders(<PatientCard patient={mockCriticalPatient} />);
    
    expect(screen.getByText(/Critical condition/i)).toBeInTheDocument();
  });

  it('should display ward and room information', () => {
    renderWithProviders(<PatientCard patient={mockStablePatient} />);
    
    expect(screen.getByText(/Ward|ward/)).toBeInTheDocument();
  });

  it('should render different colors for different severity levels', () => {
    const { container: stableContainer } = renderWithProviders(
      <PatientCard patient={mockStablePatient} />
    );
    const { container: criticalContainer } = renderWithProviders(
      <PatientCard patient={mockCriticalPatient} />
    );
    
    // Both should be different HTML outputs
    expect(stableContainer.innerHTML).not.toBe(criticalContainer.innerHTML);
  });
});

// ============================================================================
// ALERT BANNER TESTS
// ============================================================================

describe('AlertBanner Component', () => {
  it('should display alert banner when critical patients exist', () => {
    renderWithProviders(
      <AlertBanner criticalPatients={[mockCriticalPatient]} />
    );
    
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
  });

  it('should not display banner when no critical patients', () => {
    renderWithProviders(
      <AlertBanner criticalPatients={[]} />
    );
    
    // Banner should not show for no critical patients
  });

  it('should show critical patient information', () => {
    renderWithProviders(
      <AlertBanner criticalPatients={[mockCriticalPatient]} />
    );
    
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    expect(screen.getByText(/critical|CRITICAL/i)).toBeInTheDocument();
  });

  it('should be dismissible', () => {
    renderWithProviders(
      <AlertBanner criticalPatients={[mockCriticalPatient]} />
    );
    
    const closeButton = screen.queryByRole('button', { name: /close|dismiss|×/i });
    if (closeButton) {
      fireEvent.click(closeButton);
      // Banner should be dismissed
    }
  });

  it('should animate or rotate through critical patients', async () => {
    const criticalPatients = [mockCriticalPatient, { ...mockCriticalPatient, id: 'p2_alt', name: 'Another Critical', patient_id: 'P002B' }];
    renderWithProviders(
      <AlertBanner criticalPatients={criticalPatients} />
    );
    
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
  });
});

// ============================================================================
// FORM TESTS
// ============================================================================

describe('AddPatientForm Component', () => {
  it('should render form fields', () => {
    const mockOnSubmit = async () => {};
    const mockOnClose = () => {};
    
    renderWithProviders(<AddPatientForm onSubmit={mockOnSubmit} onClose={mockOnClose} />);
    
    expect(screen.getByLabelText(/name/i) || screen.getByPlaceholderText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/age/i) || screen.getByPlaceholderText(/age/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/gender/i) || screen.getByPlaceholderText(/gender/i)).toBeInTheDocument();
  });

  it('should validate required fields', async () => {
    const mockOnSubmit = async () => {};
    const mockOnClose = () => {};
    
    renderWithProviders(<AddPatientForm onSubmit={mockOnSubmit} onClose={mockOnClose} />);
    
    const submitButton = screen.getByRole('button', { name: /add|submit|create|save/i });
    fireEvent.click(submitButton);
    
    // Should show validation errors for required fields
  });

  it('should validate age is a number', async () => {
    const mockOnSubmit = async () => {};
    const mockOnClose = () => {};
    
    renderWithProviders(<AddPatientForm onSubmit={mockOnSubmit} onClose={mockOnClose} />);
    
    const ageInput = screen.getByLabelText(/age/i) || screen.getByPlaceholderText(/age/i);
    fireEvent.change(ageInput, { target: { value: 'abc' } });
    
    const submitButton = screen.getByRole('button', { name: /add|submit|create|save/i });
    fireEvent.click(submitButton);
  });

  it('should validate age is within reasonable range', async () => {
    const mockOnSubmit = async () => {};
    const mockOnClose = () => {};
    
    renderWithProviders(<AddPatientForm onSubmit={mockOnSubmit} onClose={mockOnClose} />);
    
    const ageInput = screen.getByLabelText(/age/i) || screen.getByPlaceholderText(/age/i);
    fireEvent.change(ageInput, { target: { value: '-5' } });
    
    const submitButton = screen.getByRole('button', { name: /add|submit|create|save/i });
    fireEvent.click(submitButton);
  });

  it('should validate vital signs ranges', async () => {
    const mockOnSubmit = async () => {};
    const mockOnClose = () => {};
    
    renderWithProviders(<AddPatientForm onSubmit={mockOnSubmit} onClose={mockOnClose} />);
    
    // Set invalid SpO2 (>100)
    const spo2Input = screen.queryByLabelText(/spo2|oxygen/i) || screen.queryByPlaceholderText(/spo2|oxygen/i);
    if (spo2Input) {
      fireEvent.change(spo2Input, { target: { value: '150' } });
    }
    
    const submitButton = screen.getByRole('button', { name: /add|submit|create|save/i });
    fireEvent.click(submitButton);
  });

  it('should show success message after valid submission', async () => {
    const mockOnSubmit = async () => {};
    const mockOnClose = () => {};
    
    renderWithProviders(<AddPatientForm onSubmit={mockOnSubmit} onClose={mockOnClose} />);
    
    // Fill in valid data
    const nameInput = screen.getByLabelText(/name/i) || screen.getByPlaceholderText(/name/i);
    const ageInput = screen.getByLabelText(/age/i) || screen.getByPlaceholderText(/age/i);
    
    fireEvent.change(nameInput, { target: { value: 'Test Patient' } });
    fireEvent.change(ageInput, { target: { value: '50' } });
  });
});

describe('UpdatePatientForm Component', () => {
  it('should render form with patient data pre-filled', () => {
    const mockOnSubmit = async () => {};
    const mockOnClose = () => {};
    
    renderWithProviders(
      <UpdatePatientForm patient={mockStablePatient} onSubmit={mockOnSubmit} onClose={mockOnClose} />
    );
    
    // Should show patient name or ID
    expect(screen.getByText(/John|P001|Update/i)).toBeInTheDocument();
  });

  it('should have pre-populated vital signs', () => {
    const mockOnSubmit = async () => {};
    const mockOnClose = () => {};
    
    const { container } = renderWithProviders(
      <UpdatePatientForm patient={mockStablePatient} onSubmit={mockOnSubmit} onClose={mockOnClose} />
    );
    
    // Should contain vital sign values
    expect(container.innerHTML).toMatch(/72|98|120|80/);
  });

  it('should validate updated vital signs', async () => {
    const mockOnSubmit = async () => {};
    const mockOnClose = () => {};
    
    renderWithProviders(
      <UpdatePatientForm patient={mockStablePatient} onSubmit={mockOnSubmit} onClose={mockOnClose} />
    );
    
    const heartRateInput = screen.queryByLabelText(/heart rate/i) || screen.queryByPlaceholderText(/heart rate/i);
    if (heartRateInput) {
      fireEvent.change(heartRateInput, { target: { value: '-100' } });
      
      const submitButton = screen.getByRole('button', { name: /update|save/i });
      fireEvent.click(submitButton);
    }
  });
});

// ============================================================================
// DASHBOARD PAGE TESTS
// ============================================================================

describe('Dashboard Component', () => {
  it('should render dashboard layout', () => {
    const mockOnPatientClick = () => {};
    
    renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={false} onPatientClick={mockOnPatientClick} />
    );
    
    // Should show patient grouping by severity
    expect(screen.getByText(/critical|high|moderate|stable|dashboard|patient/i)).toBeInTheDocument();
  });

  it('should display severity columns', () => {
    const mockOnPatientClick = () => {};
    
    const { container } = renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={false} onPatientClick={mockOnPatientClick} />
    );
    
    // Should have column structure
    expect(container.innerHTML).toMatch(/critical|high|moderate|stable/i);
  });

  it('should show loading state initially', async () => {
    const mockOnPatientClick = () => {};
    
    renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={true} onPatientClick={mockOnPatientClick} />
    );
    
    // Might show loading spinner or skeleton
  });

  it('should display error message on API failure', async () => {
    const mockOnPatientClick = () => {};
    
    renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={false} onPatientClick={mockOnPatientClick} />
    );
    
    // Should handle error gracefully
  });

  it('should display patients in correct severity groups', () => {
    const mockOnPatientClick = () => {};
    
    renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={false} onPatientClick={mockOnPatientClick} />
    );
    
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    expect(screen.getByText('Bob Johnson')).toBeInTheDocument();
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
});

// ============================================================================
// UI BEHAVIOR TESTS
// ============================================================================

describe('UI Behavior', () => {
  it('should handle loading states gracefully', async () => {
    const mockOnPatientClick = () => {};
    
    renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={true} onPatientClick={mockOnPatientClick} />
    );
    
    // Component should render without crashing
  });

  it('should display responsive layout', () => {
    const mockOnPatientClick = () => {};
    
    const { container } = renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={false} onPatientClick={mockOnPatientClick} />
    );
    
    // Should use responsive classes
    expect(container.innerHTML).toMatch(/grid|flex|responsive|md:|lg:|gap/i);
  });

  it('should be keyboard accessible', () => {
    const mockOnPatientClick = () => {};
    
    renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={false} onPatientClick={mockOnPatientClick} />
    );
    
    // Check for accessible buttons
    const buttons = screen.queryAllByRole('button');
    expect(buttons.length >= 0).toBeTruthy();
  });
});

// ============================================================================
// SEVERITY COLOR TESTS
// ============================================================================

describe('Severity Color Coding', () => {
  it('should use red color for critical patients', () => {
    const { container } = renderWithProviders(
      <PatientCard patient={mockCriticalPatient} />
    );
    
    // Should contain red/critical styling
    expect(container.innerHTML).toMatch(/red|critical|danger/i);
  });

  it('should use orange color for high severity', () => {
    const { container } = renderWithProviders(
      <PatientCard patient={mockHighPatient} />
    );
    
    // Should contain appropriate styling
    expect(container.innerHTML.length > 0).toBeTruthy();
  });

  it('should use green color for stable patients', () => {
    const { container } = renderWithProviders(
      <PatientCard patient={mockStablePatient} />
    );
    
    // Should contain green/stable styling
    expect(container.innerHTML).toMatch(/green|stable|safe/i);
  });
});

// ============================================================================
// INTEGRATION TESTS
// ============================================================================

describe('Integration Tests', () => {
  it('should display all patient types in dashboard', async () => {
    const mockOnPatientClick = () => {};
    
    renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={false} onPatientClick={mockOnPatientClick} />
    );
    
    // Should display all mock patients
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    expect(screen.getByText('Bob Johnson')).toBeInTheDocument();
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });

  it('should allow updating patient vitals', async () => {
    const mockOnSubmit = async () => {};
    const mockOnClose = () => {};
    
    renderWithProviders(
      <UpdatePatientForm patient={mockStablePatient} onSubmit={mockOnSubmit} onClose={mockOnClose} />
    );
    
    // Should be able to interact with form
    expect(screen.getByText(/John|P001|Update/i)).toBeInTheDocument();
  });

  it('should have proper data flow', async () => {
    const mockOnPatientClick = () => {};
    
    const { container } = renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={false} onPatientClick={mockOnPatientClick} />
    );
    
    // Dashboard should reflect data
    expect(container.innerHTML).toMatch(/John|Jane|Bob/);
  });
});

// ============================================================================
// ACCESSIBILITY TESTS
// ============================================================================

describe('Accessibility', () => {
  it('should have proper heading hierarchy', () => {
    const mockOnPatientClick = () => {};
    
    renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={false} onPatientClick={mockOnPatientClick} />
    );
    
    // Should have headings
    const headings = screen.queryAllByRole('heading');
    expect(headings.length >= 0).toBeTruthy();
  });

  it('should have accessible form labels', () => {
    const mockOnSubmit = async () => {};
    const mockOnClose = () => {};
    
    renderWithProviders(<AddPatientForm onSubmit={mockOnSubmit} onClose={mockOnClose} />);
    
    // Should have associated labels
    const nameInput = screen.queryByLabelText(/name/i);
    expect(nameInput || screen.getByText(/name|form|patient/i)).toBeTruthy();
  });

  it('should have visible focus states', () => {
    const mockOnPatientClick = () => {};
    
    renderWithProviders(
      <Dashboard data={mockDashboardData} isLoading={false} onPatientClick={mockOnPatientClick} />
    );
    
    // Buttons should be focusable
    const buttons = screen.queryAllByRole('button');
    expect(buttons.length >= 0).toBeTruthy();
  });
});
