import { Users, Activity, AlertTriangle, Heart, AlertCircle } from 'lucide-react';
import type { DashboardData, Patient } from '../../types/patient';
import PatientCard from '@components/PatientCard/PatientCard';

interface DashboardProps {
  data: DashboardData;
  isLoading: boolean;
  onPatientClick: (patient: Patient) => void;
}

export const Dashboard = ({ data, isLoading, onPatientClick }: DashboardProps) => {
  const columns = [
    { title: 'Critical', patients: data.critical, color: 'red', icon: '🔴', count: data.critical.length },
    { title: 'High', patients: data.high, color: 'orange', icon: '🟠', count: data.high.length },
    { title: 'Moderate', patients: data.moderate, color: 'yellow', icon: '🟡', count: data.moderate.length },
    { title: 'Stable', patients: data.stable, color: 'green', icon: '🟢', count: data.stable.length },
  ];

  // CRITICAL: Calculate total from groups (this is the source of truth)
  const calculatedTotal = data.critical.length + data.high.length + data.moderate.length + data.stable.length;
  
  // Use API total if provided, otherwise use calculated
  let displayTotal = data.total ?? calculatedTotal;
  
  // VALIDATION: Verify API total matches calculated (safety check)
  if (data.total !== undefined && data.total !== calculatedTotal) {
    console.error(
      `🔴 CRITICAL BUG: Dashboard total mismatch!`,
      {
        apiTotal: data.total,
        calculatedTotal,
        critical: data.critical.length,
        high: data.high.length,
        moderate: data.moderate.length,
        stable: data.stable.length,
        difference: data.total - calculatedTotal
      }
    );
    // Use calculated value as fallback
    displayTotal = calculatedTotal;
  } else if (data.total !== undefined) {
    console.log(
      `✅ Dashboard total verified:`,
      {
        total: displayTotal,
        critical: data.critical.length,
        high: data.high.length,
        moderate: data.moderate.length,
        stable: data.stable.length
      }
    );
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin">
            <Activity className="w-12 h-12 text-blue-600 mx-auto" />
          </div>
          <p className="mt-4 text-slate-600">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  // Debug Log - Log data to console
  console.log('📊 Dashboard Summary - Data:', {
    total: displayTotal,
    critical: data.critical?.length || 0,
    high: data.high?.length || 0,
    moderate: data.moderate?.length || 0,
    stable: data.stable?.length || 0
  });

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Total Patients Card */}
        <div className="bg-white rounded-lg p-4 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-600 mb-1">Total Patients</p>
              <p className="text-2xl font-bold text-slate-900">{displayTotal}</p>
            </div>
            <Users className="w-10 h-10 text-blue-500 opacity-20" />
          </div>
        </div>

        {/* Critical Card */}
        <div className="bg-white rounded-lg p-4 border border-red-200 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-red-600 mb-1 font-semibold">Critical</p>
              <p className="text-2xl font-bold text-red-600">{data.critical?.length || 0}</p>
            </div>
            <AlertTriangle className="w-10 h-10 text-red-500 opacity-20" />
          </div>
        </div>

        {/* High Risk Card */}
        <div className="bg-white rounded-lg p-4 border border-orange-200 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-orange-600 mb-1 font-semibold">High Risk</p>
              <p className="text-2xl font-bold text-orange-600">{data.high?.length || 0}</p>
            </div>
            <Heart className="w-10 h-10 text-orange-500 opacity-20" />
          </div>
        </div>

        {/* Moderate Card (PREVIOUSLY MISSING) */}
        <div className="bg-white rounded-lg p-4 border border-yellow-200 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-yellow-700 mb-1 font-semibold">Moderate</p>
              <p className="text-2xl font-bold text-yellow-700">{data.moderate?.length || 0}</p>
            </div>
            <AlertCircle className="w-10 h-10 text-yellow-600 opacity-20" />
          </div>
        </div>

        {/* Stable Card */}
        <div className="bg-white rounded-lg p-4 border border-green-200 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-600 mb-1 font-semibold">Stable</p>
              <p className="text-2xl font-bold text-green-600">{data.stable?.length || 0}</p>
            </div>
            <Activity className="w-10 h-10 text-green-500 opacity-20" />
          </div>
        </div>
      </div>

      {/* Patient Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        {columns.map((column) => (
          <div key={column.title} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
            <div className="mb-4 pb-3 border-b border-slate-300">
              <h2 className="text-lg font-bold text-slate-900">
                {column.icon} {column.title}
              </h2>
              <p className="text-xs text-slate-600 mt-1">
                {column.count} patient{column.count !== 1 ? 's' : ''}
              </p>
            </div>

            {column.patients.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-sm text-slate-500">No patients</p>
              </div>
            ) : (
              <div className="space-y-3 max-h-[calc(100vh-300px)] overflow-y-auto">
                {column.patients.map((patient: Patient) => (
                  <div key={patient.id} onClick={() => onPatientClick(patient)}>
                    <PatientCard patient={patient} onClick={() => onPatientClick(patient)} />
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
