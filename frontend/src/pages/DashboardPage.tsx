import { useState } from 'react';
import { useQuery, useQueryClient } from 'react-query';
import { Plus, RefreshCw } from 'lucide-react';
import Header from '@components/Layout/Header';
import Footer from '@components/Layout/Footer';
import AlertBanner from '@components/AlertBanner/AlertBanner';
import Dashboard from '@components/Dashboard/Dashboard';
import AddPatientForm from '@components/Forms/AddPatientForm';
import UpdatePatientForm from '@components/Forms/UpdatePatientForm';
import { apiClient } from '@services/api';
import { useStore } from '@store/useStore';
import type { Patient, CreatePatientRequest, UpdatePatientRequest } from '../types/patient';

export const DashboardPage = () => {
  const store = useStore();
  const queryClient = useQueryClient();
  const [error, setError] = useState<string | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Fetch dashboard data
  const { data: dashboardData, isLoading, refetch } = useQuery(
    'dashboard',
    () => apiClient.getDashboard(),
    {
      refetchInterval: store.autoRefreshEnabled ? store.refreshInterval : false,
      staleTime: 5000,
    }
  );

  // Handle refresh button - CRITICAL for real-time data updates
  const handleRefresh = async () => {
    if (isRefreshing) {
      console.warn('⚠️ Refresh already in progress');
      return;
    }
    
    setIsRefreshing(true);
    console.log('🔄 CRITICAL: Manual refresh triggered by user');
    
    try {
      // Force immediate refetch (ignore cache)
      const result = await refetch();
      
      if (result.data) {
        console.log('✅ CRITICAL: Fresh dashboard data received:', {
          total: result.data.total,
          critical: result.data.critical.length,
          high: result.data.high.length,
          moderate: result.data.moderate.length,
          stable: result.data.stable.length,
          timestamp: new Date().toISOString()
        });
      } else {
        console.error('❌ CRITICAL: Refetch returned no data');
        setError('Failed to refresh data');
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Refresh failed';
      console.error('❌ CRITICAL: Refresh error:', errorMsg);
      setError(errorMsg);
    } finally {
      setIsRefreshing(false);
    }
  };

  // Handle add patient
  const handleAddPatient = async (data: CreatePatientRequest) => {
    store.setIsLoading(true);
    try {
      console.log('➕ Adding patient:', data);
      const response = await apiClient.createPatient(data);
      console.log('✅ Patient added:', response);
      
      // CRITICAL: Invalidate dashboard cache to force refetch
      console.log('🔄 CRITICAL: Invalidating dashboard cache after patient add');
      await queryClient.invalidateQueries('dashboard');
      
      // Wait a bit and then explicitly refetch to ensure fresh data
      await new Promise(resolve => setTimeout(resolve, 300));
      await refetch();
      console.log('✅ CRITICAL: Dashboard refreshed after add');
      
      store.setShowAddPatientModal(false);
      setError(null);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to add patient';
      console.error('❌ Add error:', errorMsg);
      setError(errorMsg);
      store.setError(errorMsg);
    } finally {
      store.setIsLoading(false);
    }
  };

  // Handle update patient - CRITICAL for real-time accuracy
  const handleUpdatePatient = async (data: UpdatePatientRequest) => {
    if (!store.selectedPatient?.patient_id) {
      console.error('❌ No patient_id available for update');
      setError('No patient selected');
      return;
    }

    console.log('📤 CRITICAL: Update request for patient:', {
      patient_id: store.selectedPatient.patient_id,
      vitals: data.vitals
    });

    store.setIsLoading(true);
    try {
      const response = await apiClient.updatePatient(store.selectedPatient.patient_id, data);
      console.log('✅ Update successful, received response:', {
        patient_id: response.patient_id,
        severity: response.severity,
        score: response.score,
        alert: response.alert
      });
      
      // CRITICAL: Invalidate dashboard cache to force refetch with fresh data
      console.log('🔄 CRITICAL: Invalidating dashboard cache after patient update');
      await queryClient.invalidateQueries('dashboard');
      
      // Wait a bit and then explicitly refetch to ensure latest data
      await new Promise(resolve => setTimeout(resolve, 300));
      await refetch();
      console.log('✅ CRITICAL: Dashboard refreshed after update with latest patient severity and alerts');
      
      store.setShowUpdatePatientModal(false);
      store.setSelectedPatient(null);
      setError(null);
      
      // Show success message
      alert(`✅ Patient ${store.selectedPatient.patient_id} updated successfully with latest assessment!`);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to update patient';
      console.error('❌ Update error:', errorMsg);
      setError(errorMsg);
      store.setError(errorMsg);
    } finally {
      store.setIsLoading(false);
    }
  };

  // Handle patient click
  const handlePatientClick = (patient: Patient) => {
    store.setSelectedPatient(patient);
    store.setShowUpdatePatientModal(true);
  };

  const defaultDashboardData = {
    total: 0,
    critical: [],
    high: [],
    moderate: [],
    stable: [],
  };

  return (
    <div className="flex flex-col min-h-screen bg-slate-50">
      <Header />

      {dashboardData && dashboardData.critical.length > 0 && (
        <AlertBanner criticalPatients={dashboardData.critical} />
      )}

      {error && (
        <div className="bg-red-50 border-b border-red-200 text-red-800 px-4 sm:px-6 lg:px-8 py-4">
          <p className="font-semibold">Error: {error}</p>
          <button
            onClick={() => setError(null)}
            className="text-sm mt-2 underline hover:no-underline"
          >
            Dismiss
          </button>
        </div>
      )}

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold text-slate-900">Patient Dashboard</h2>
            <p className="text-slate-600 mt-1">Real-time monitoring and alerts</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={handleRefresh}
              disabled={isRefreshing || isLoading}
              className="flex items-center gap-2 px-4 py-2 bg-slate-200 text-slate-900 rounded-lg hover:bg-slate-300 transition disabled:opacity-50 disabled:cursor-not-allowed"
              title="Refresh dashboard with latest patient data"
            >
              <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
              {isRefreshing ? 'Refreshing...' : 'Refresh'}
            </button>
            <button
              onClick={() => store.setShowAddPatientModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              <Plus className="w-4 h-4" />
              Add Patient
            </button>
          </div>
        </div>

        <Dashboard
          data={dashboardData || defaultDashboardData}
          isLoading={isLoading}
          onPatientClick={handlePatientClick}
        />
      </main>

      {store.showAddPatientModal && (
        <AddPatientForm
          onSubmit={handleAddPatient}
          onClose={() => store.setShowAddPatientModal(false)}
          isLoading={store.isLoading}
        />
      )}

      {store.showUpdatePatientModal && store.selectedPatient && (
        <UpdatePatientForm
          patient={store.selectedPatient}
          onSubmit={handleUpdatePatient}
          onClose={() => {
            store.setShowUpdatePatientModal(false);
            store.setSelectedPatient(null);
          }}
          isLoading={store.isLoading}
        />
      )}

      <Footer />
    </div>
  );
};

export default DashboardPage;
