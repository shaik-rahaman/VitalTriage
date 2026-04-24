import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { ArrowLeft, Edit, Trash2, AlertTriangle, Heart, Thermometer, TrendingUp } from 'lucide-react';
import { useState } from 'react';
import Header from '@components/Layout/Header';
import Footer from '@components/Layout/Footer';
import UpdatePatientForm from '@components/Forms/UpdatePatientForm';
import { apiClient } from '@services/api';
import { getSeverityIcon, formatVital } from '@utils/formatters';
import type { UpdatePatientRequest } from '../types/patient';

export const PatientDetailsPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { data: patient, isLoading: dataLoading, refetch } = useQuery(
    ['patient', id],
    () => apiClient.getPatient(id!),
    { 
      enabled: !!id,
      // Force fresh data every 5 seconds for healthcare safety
      refetchInterval: 5000,
      staleTime: 2000,
    }
  );

  const handleUpdate = async (data: UpdatePatientRequest) => {
    if (!id) return;
    setIsLoading(true);
    try {
      console.log('📤 CRITICAL: Patient details update initiated:', { patient_id: id });
      const response = await apiClient.updatePatient(id, data);
      
      console.log('✅ CRITICAL: Patient updated, refetching fresh data:', {
        severity: response.severity,
        alert: response.alert ? response.alert.substring(0, 50) : 'NONE',
        score: response.score
      });
      
      // CRITICAL: Refetch immediately to show fresh assessment
      await refetch();
      setShowUpdateForm(false);
      
      console.log('✅ CRITICAL: Patient details page refreshed with latest assessment');
    } catch (err) {
      console.error('❌ CRITICAL: Failed to update patient:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!id || !window.confirm('Are you sure you want to delete this patient?')) return;
    setIsLoading(true);
    try {
      await apiClient.deletePatient(id);
      navigate('/');
    } catch (err) {
      console.error('Failed to delete patient:', err);
      setIsLoading(false);
    }
  };

  if (dataLoading) {
    return (
      <div className="flex flex-col min-h-screen bg-slate-50">
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <p className="text-slate-600">Loading patient details...</p>
        </main>
        <Footer />
      </div>
    );
  }

  if (!patient) {
    return (
      <div className="flex flex-col min-h-screen bg-slate-50">
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <p className="text-slate-600 mb-4">Patient not found</p>
            <button
              onClick={() => navigate('/')}
              className="text-blue-600 hover:underline"
            >
              Go back to dashboard
            </button>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-slate-50">
      <Header />

      <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-blue-600 hover:text-blue-800 mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </button>
          <div className="flex gap-2">
            <button
              onClick={() => setShowUpdateForm(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              <Edit className="w-4 h-4" />
              Edit
            </button>
            <button
              onClick={handleDelete}
              disabled={isLoading}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition disabled:opacity-50"
            >
              <Trash2 className="w-4 h-4" />
              Delete
            </button>
          </div>
        </div>

        {/* Patient Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="text-4xl">{getSeverityIcon(patient.severity)}</span>
                <h1 className="text-3xl font-bold text-slate-900">{patient.patient_id}</h1>
              </div>
              <p className="text-slate-600">Patient ID: {patient.patient_id}</p>
            </div>
            <span className={`px-4 py-2 rounded-lg font-semibold text-white ${
              patient.severity === 'critical' ? 'bg-red-600' :
              patient.severity === 'high' ? 'bg-orange-600' :
              patient.severity === 'moderate' ? 'bg-yellow-600' :
              'bg-green-600'
            }`}>
              {patient.severity.toUpperCase()}
            </span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-slate-600">Age</p>
              <p className="text-lg font-semibold text-slate-900">{patient.age}</p>
            </div>
            <div>
              <p className="text-sm text-slate-600">Gender</p>
              <p className="text-lg font-semibold text-slate-900">{patient.gender}</p>
            </div>
            <div>
              <p className="text-sm text-slate-600">Ward</p>
              <p className="text-lg font-semibold text-slate-900">{patient.ward}</p>
            </div>
            <div>
              <p className="text-sm text-slate-600">Room</p>
              <p className="text-lg font-semibold text-slate-900">{patient.room}</p>
            </div>
          </div>
        </div>

        {/* Vitals */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 className="text-xl font-bold text-slate-900 mb-4">Vital Signs</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {patient.vitals.heart_rate && (
              <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg">
                <Heart className="w-8 h-8 text-red-500" />
                <div>
                  <p className="text-sm text-slate-600">Heart Rate</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {formatVital('heart_rate', patient.vitals.heart_rate)}
                  </p>
                </div>
              </div>
            )}
            {patient.vitals.spo2 && (
              <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg">
                <TrendingUp className="w-8 h-8 text-blue-500" />
                <div>
                  <p className="text-sm text-slate-600">SpO₂</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {formatVital('spo2', patient.vitals.spo2)}
                  </p>
                </div>
              </div>
            )}
            {patient.vitals.temperature && (
              <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg">
                <Thermometer className="w-8 h-8 text-orange-500" />
                <div>
                  <p className="text-sm text-slate-600">Temperature</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {formatVital('temperature', patient.vitals.temperature)}
                  </p>
                </div>
              </div>
            )}
            {patient.vitals.respiratory_rate && (
              <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg">
                <span className="text-2xl">🫁</span>
                <div>
                  <p className="text-sm text-slate-600">Respiratory Rate</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {formatVital('respiratory_rate', patient.vitals.respiratory_rate)}
                  </p>
                </div>
              </div>
            )}
            {patient.vitals.systolic_bp && patient.vitals.diastolic_bp && (
              <div className="flex items-center gap-4 p-4 bg-slate-50 rounded-lg col-span-1 md:col-span-2">
                <span className="text-2xl">🩺</span>
                <div>
                  <p className="text-sm text-slate-600">Blood Pressure</p>
                  <p className="text-lg font-semibold text-slate-900">
                    {patient.vitals.systolic_bp}/{patient.vitals.diastolic_bp} mmHg
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Alerts */}
        {patient.alert && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6">
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="w-5 h-5 text-yellow-700" />
              <h2 className="text-lg font-bold text-yellow-900">Alert</h2>
            </div>
            <p className="text-yellow-800">{patient.alert}</p>
            <p className="text-xs text-yellow-700 mt-2">
              ✅ Fresh data - Last updated: {patient.timestamp ? new Date(patient.timestamp).toLocaleTimeString() : 'unknown'}
            </p>
          </div>
        )}

        {/* LLM Output Section - CRITICAL FOR HEALTHCARE */}
        {patient.llm_output && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
            <h2 className="text-lg font-bold text-blue-900 mb-4">Clinical Assessment (AI Insight)</h2>
            
            {/* Explanation */}
            <div className="mb-4">
              <h3 className="text-sm font-semibold text-blue-800 mb-2">Explanation</h3>
              <p className="text-blue-700 leading-relaxed">
                {patient.llm_output.explanation || 'No explanation available'}
              </p>
              {!patient.llm_output.explanation && (
                <p className="text-red-600 font-semibold">🔴 WARNING: LLM explanation is missing!</p>
              )}
            </div>
            
            {/* Suggested Actions */}
            <div>
              <h3 className="text-sm font-semibold text-blue-800 mb-2">Recommended Actions</h3>
              {patient.llm_output.suggested_actions && patient.llm_output.suggested_actions.length > 0 ? (
                <ul className="list-disc list-inside space-y-1">
                  {patient.llm_output.suggested_actions.map((action, idx) => (
                    <li key={idx} className="text-blue-700">{action}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-red-600 font-semibold">🔴 WARNING: No recommended actions found!</p>
              )}
            </div>
            
            {/* Data freshness indicator */}
            <p className="text-xs text-blue-700 mt-4 pt-4 border-t border-blue-200">
              ✅ Fresh assessment data - Computed at {patient.timestamp ? new Date(patient.timestamp).toLocaleTimeString() : 'unknown'}
            </p>
          </div>
        )}

        {/* Notes */}
        {patient.notes && (
          <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
            <h2 className="text-lg font-bold text-slate-900 mb-4">Notes</h2>
            <p className="text-slate-700 italic">"{patient.notes}"</p>
          </div>
        )}

        {/* Metadata */}
        <div className="bg-slate-200 rounded-lg p-4 text-sm text-slate-600">
          {patient.timestamp && (
            <p>Last Updated: {patient.timestamp}</p>
          )}
        </div>
      </main>

      {showUpdateForm && (
        <UpdatePatientForm
          patient={patient}
          onSubmit={handleUpdate}
          onClose={() => setShowUpdateForm(false)}
          isLoading={isLoading}
        />
      )}

      <Footer />
    </div>
  );
};

export default PatientDetailsPage;
