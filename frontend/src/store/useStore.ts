import { create } from 'zustand';
import type { Patient } from '../types/patient';

interface StoreState {
  selectedPatient: Patient | null;
  setSelectedPatient: (patient: Patient | null) => void;
  
  showAddPatientModal: boolean;
  setShowAddPatientModal: (show: boolean) => void;
  
  showUpdatePatientModal: boolean;
  setShowUpdatePatientModal: (show: boolean) => void;
  
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  
  error: string | null;
  setError: (error: string | null) => void;
  
  autoRefreshEnabled: boolean;
  setAutoRefreshEnabled: (enabled: boolean) => void;
  
  refreshInterval: number;
  setRefreshInterval: (interval: number) => void;
}

export const useStore = create<StoreState>((set) => ({
  selectedPatient: null,
  setSelectedPatient: (patient) => set({ selectedPatient: patient }),
  
  showAddPatientModal: false,
  setShowAddPatientModal: (show) => set({ showAddPatientModal: show }),
  
  showUpdatePatientModal: false,
  setShowUpdatePatientModal: (show) => set({ showUpdatePatientModal: show }),
  
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
  
  error: null,
  setError: (error) => set({ error }),
  
  autoRefreshEnabled: true,
  setAutoRefreshEnabled: (enabled) => set({ autoRefreshEnabled: enabled }),
  
  refreshInterval: 5000, // 5 seconds
  setRefreshInterval: (interval) => set({ refreshInterval: interval }),
}));
