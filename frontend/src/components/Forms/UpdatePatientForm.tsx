import { FormEvent, useState } from 'react';
import { X, Save } from 'lucide-react';
import type { Patient, UpdatePatientRequest, Vitals } from '../../types/patient';

interface UpdatePatientFormProps {
  patient: Patient;
  onSubmit: (data: UpdatePatientRequest) => Promise<void>;
  onClose: () => void;
  isLoading?: boolean;
}

export const UpdatePatientForm = ({ patient, onSubmit, onClose, isLoading = false }: UpdatePatientFormProps) => {
  const [formData, setFormData] = useState<UpdatePatientRequest>({
    vitals: patient.vitals,
    symptoms: patient.symptoms || [],
    notes: patient.notes || '',
  });

  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!formData.vitals?.heart_rate || !formData.vitals?.spo2) {
      const errMsg = 'Please provide at least heart rate and SpO2';
      setError(errMsg);
      console.warn('⚠️ Form validation failed:', errMsg);
      return;
    }

    console.log('📋 Form submitted with data:', formData);
    try {
      await onSubmit(formData);
      console.log('✅ Form submission successful');
      onClose();
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : 'Failed to update patient';
      console.error('❌ Form submission error:', errMsg);
      setError(errMsg);
    }
  };

  const handleVitalChange = (key: keyof Vitals, value: any) => {
    setFormData((prev: UpdatePatientRequest) => ({
      ...prev,
      vitals: {
        ...prev.vitals,
        [key]: value === '' ? undefined : value,
      },
    }));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-slate-200 p-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-slate-900">Update Patient - {patient.patient_id}</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-100 rounded transition"
            aria-label="Close form"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {/* Vitals */}
          <fieldset className="space-y-4">
            <legend className="text-lg font-semibold text-slate-900 mb-4">Update Vitals</legend>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Heart Rate (bpm) *
                </label>
                <input
                  type="number"
                  required
                  min="30"
                  max="200"
                  value={formData.vitals?.heart_rate || ''}
                  onChange={(e) => handleVitalChange('heart_rate', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="72"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  SpO₂ (%) *
                </label>
                <input
                  type="number"
                  required
                  min="0"
                  max="100"
                  value={formData.vitals?.spo2 || ''}
                  onChange={(e) => handleVitalChange('spo2', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="98"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Systolic BP (mmHg)
                </label>
                <input
                  type="number"
                  min="70"
                  max="200"
                  value={formData.vitals?.systolic_bp || ''}
                  onChange={(e) => handleVitalChange('systolic_bp', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="120"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Diastolic BP (mmHg)
                </label>
                <input
                  type="number"
                  min="40"
                  max="130"
                  value={formData.vitals?.diastolic_bp || ''}
                  onChange={(e) => handleVitalChange('diastolic_bp', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="80"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Temperature (°F)
                </label>
                <input
                  type="number"
                  step="0.1"
                  min="95"
                  max="110"
                  value={formData.vitals?.temperature || ''}
                  onChange={(e) => handleVitalChange('temperature', parseFloat(e.target.value))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="98.6"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Respiratory Rate (breaths/min)
                </label>
                <input
                  type="number"
                  min="10"
                  max="40"
                  value={formData.vitals?.respiratory_rate || ''}
                  onChange={(e) => handleVitalChange('respiratory_rate', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="16"
                />
              </div>
            </div>
          </fieldset>

          {/* Symptoms */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Symptoms (comma-separated)
            </label>
            <input
              type="text"
              value={formData.symptoms?.join(', ') || ''}
              onChange={(e) => setFormData({ ...formData, symptoms: e.target.value.split(',').map(s => s.trim()).filter(s => s) })}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., fever, cough"
            />
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Clinical Notes
            </label>
            <textarea
              value={formData.notes || ''}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="Any additional clinical notes..."
            />
          </div>

          {/* Buttons */}
          <div className="flex gap-3 justify-end pt-4 border-t border-slate-200">
            <button
              type="button"
              onClick={onClose}
              disabled={isLoading}
              className="px-4 py-2 border border-slate-300 rounded-lg text-slate-700 hover:bg-slate-50 transition disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center gap-2 disabled:opacity-50"
            >
              <Save className="w-4 h-4" />
              {isLoading ? 'Updating...' : 'Update Patient'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UpdatePatientForm;
