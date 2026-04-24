import { FormEvent, useState } from 'react';
import { X, Save } from 'lucide-react';
import type { CreatePatientRequest, Vitals } from '../../types/patient';

interface AddPatientFormProps {
  onSubmit: (data: CreatePatientRequest) => Promise<void>;
  onClose: () => void;
  isLoading?: boolean;
}

export const AddPatientForm = ({ onSubmit, onClose, isLoading = false }: AddPatientFormProps) => {
  const [formData, setFormData] = useState<CreatePatientRequest>({
    patient_id: '',
    age: 0,
    gender: '',
    ward: '',
    room: '',
    vitals: {
      heart_rate: undefined,
      spo2: undefined,
      systolic_bp: undefined,
      diastolic_bp: undefined,
      temperature: undefined,
      respiratory_rate: undefined,
    },
    symptoms: [],
    notes: '',
  });

  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (!formData.patient_id || !formData.age || !formData.gender) {
      setError('Please fill in patient ID, age, and gender');
      return;
    }

    if (formData.age < 0 || formData.age > 150) {
      setError('Please enter a valid age');
      return;
    }

    try {
      await onSubmit(formData);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add patient');
    }
  };

  const handleVitalChange = (key: keyof Vitals, value: any) => {
    setFormData((prev: CreatePatientRequest) => ({
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
          <h2 className="text-2xl font-bold text-slate-900">Add New Patient</h2>
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

          {/* Personal Information */}
          <fieldset className="space-y-4">
            <legend className="text-lg font-semibold text-slate-900 mb-4">Personal Information</legend>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Patient ID *
                </label>
                <input
                  type="text"
                  required
                  value={formData.patient_id}
                  onChange={(e) => setFormData({ ...formData, patient_id: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="P001"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Age *
                </label>
                <input
                  type="number"
                  required
                  min="0"
                  max="150"
                  value={formData.age || ''}
                  onChange={(e) => setFormData({ ...formData, age: parseInt(e.target.value) || 0 })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="45"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Gender *
                </label>
                <select
                  required
                  value={formData.gender}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select Gender</option>
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                  <option value="O">Other</option>
                </select>
              </div>
            </div>
          </fieldset>

          {/* Location Information */}
          <fieldset className="space-y-4">
            <legend className="text-lg font-semibold text-slate-900 mb-4">Location</legend>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Ward (optional)
                </label>
                <input
                  type="text"
                  value={formData.ward}
                  onChange={(e) => setFormData({ ...formData, ward: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="ICU"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Room (optional)
                </label>
                <input
                  type="text"
                  value={formData.room}
                  onChange={(e) => setFormData({ ...formData, room: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="101"
                />
              </div>
            </div>
          </fieldset>

          {/* Vitals */}
          <fieldset className="space-y-4">
            <legend className="text-lg font-semibold text-slate-900 mb-4">Vitals</legend>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Heart Rate (bpm)
                </label>
                <input
                  type="number"
                  min="30"
                  max="200"
                  value={formData.vitals.heart_rate || ''}
                  onChange={(e) => handleVitalChange('heart_rate', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="72"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  SpO₂ (%)
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={formData.vitals.spo2 || ''}
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
                  value={formData.vitals.systolic_bp || ''}
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
                  value={formData.vitals.diastolic_bp || ''}
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
                  value={formData.vitals.temperature || ''}
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
                  value={formData.vitals.respiratory_rate || ''}
                  onChange={(e) => handleVitalChange('respiratory_rate', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="16"
                />
              </div>
            </div>
          </fieldset>

          {/* Symptoms & Notes */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Symptoms (comma-separated)
            </label>
            <input
              type="text"
              value={formData.symptoms?.join(', ') || ''}
              onChange={(e) => setFormData({ ...formData, symptoms: e.target.value.split(',').map(s => s.trim()).filter(s => s) })}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., fever, cough, fatigue"
            />
          </div>

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
              {isLoading ? 'Adding...' : 'Add Patient'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddPatientForm;
