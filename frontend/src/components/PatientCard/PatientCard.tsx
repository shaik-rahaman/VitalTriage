import { Heart, AlertTriangle, TrendingUp, Thermometer, Clock, AlertCircle, CheckCircle2, Phone, Zap, Check } from 'lucide-react';
import { useState } from 'react';
import type { Patient } from '../../types/patient';
import { SeverityLevel } from '../../types/patient';
import { getSeverityBgClass, getSeverityTextClass, formatVital, getVitalStatus, formatTimeAgo } from '@utils/formatters';

interface PatientCardProps {
  patient: Patient;
  onClick?: () => void;
}

export const PatientCard = ({ patient, onClick }: PatientCardProps) => {
  const [actionTaken, setActionTaken] = useState<string | null>(null);
  const isCritical = patient.severity === SeverityLevel.CRITICAL;
  const bgClass = getSeverityBgClass(patient.severity);
  const textClass = getSeverityTextClass(patient.severity);

  const handleQuickAction = (action: string) => {
    setActionTaken(action);
    console.log(`Quick action taken for ${patient.patient_id}: ${action}`);
    setTimeout(() => setActionTaken(null), 2000);
  };

  const getSeverityBadgeClass = () => {
    switch (patient.severity) {
      case SeverityLevel.CRITICAL:
        return 'bg-red-500 text-white animate-pulse';
      case SeverityLevel.HIGH:
        return 'bg-orange-500 text-white';
      case SeverityLevel.MODERATE:
        return 'bg-yellow-500 text-white';
      case SeverityLevel.STABLE:
        return 'bg-green-500 text-white';
      default:
        return 'bg-slate-500 text-white';
    }
  };

  const getSeverityIcon = () => {
    switch (patient.severity) {
      case SeverityLevel.CRITICAL:
        return '🔴';
      case SeverityLevel.HIGH:
        return '🟠';
      case SeverityLevel.MODERATE:
        return '🟡';
      case SeverityLevel.STABLE:
        return '🟢';
      default:
        return '⚪';
    }
  };

  const getVitalColor = (key: string, value: number | undefined) => {
    if (value === undefined) return '';
    const status = getVitalStatus(key, value);
    if (status === 'critical') return 'text-red-600 font-bold';
    if (status === 'high') return 'text-orange-600 font-semibold';
    return 'text-green-700';
  };

  const getAbnormalVitals = () => {
    const abnormal = [];
    if (patient.vitals.heart_rate && getVitalStatus('heart_rate', patient.vitals.heart_rate) !== 'normal') {
      abnormal.push(`HR ${patient.vitals.heart_rate} bpm`);
    }
    if (patient.vitals.spo2 && getVitalStatus('spo2', patient.vitals.spo2) !== 'normal') {
      abnormal.push(`SpO₂ ${patient.vitals.spo2}%`);
    }
    if (patient.vitals.temperature && getVitalStatus('temperature', patient.vitals.temperature) !== 'normal') {
      abnormal.push(`Temp ${patient.vitals.temperature}°F`);
    }
    if (patient.vitals.respiratory_rate && getVitalStatus('respiratory_rate', patient.vitals.respiratory_rate) !== 'normal') {
      abnormal.push(`RR ${patient.vitals.respiratory_rate}`);
    }
    return abnormal;
  };

  const abnormalVitals = getAbnormalVitals();
  const scoreColor = patient.score > 70 ? 'text-red-600 font-bold' : patient.score > 40 ? 'text-orange-600 font-semibold' : 'text-green-700';

  return (
    <div
      onClick={onClick}
      className={`${bgClass} border-2 rounded-lg p-4 cursor-pointer transition-all duration-300 hover:shadow-lg hover:scale-[1.02] ${
        isCritical ? 'border-red-500 shadow-lg' : 'border-slate-200'
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-2xl">{getSeverityIcon()}</span>
            <div>
              <h3 className={`font-bold text-lg ${textClass}`}>{patient.patient_id}</h3>
              <p className={`text-xs font-medium ${scoreColor}`}>Score: {patient.score.toFixed(1)}/100</p>
            </div>
          </div>
        </div>
        <span className={`${getSeverityBadgeClass()} px-3 py-1 rounded-full text-sm font-semibold whitespace-nowrap`}>
          {patient.severity.toUpperCase()}
        </span>
      </div>

      {/* Location & Demographics */}
      <div className="space-y-1 mb-3 text-sm border-b border-slate-200 pb-3">
        <div className="flex justify-between text-slate-700">
          <span>
            <span className="font-semibold">Ward:</span> {patient.ward || 'N/A'} • <span className="font-semibold">Room:</span> {patient.room || 'N/A'}
          </span>
          <span className="text-xs text-slate-500 flex items-center gap-1">
            <Clock className="w-3 h-3" />
            {formatTimeAgo(patient.timestamp)}
          </span>
        </div>
        <p className="text-slate-600 text-xs">
          <span className="font-semibold">Age:</span> {patient.age} • <span className="font-semibold">Gender:</span> {patient.gender}
        </p>
      </div>

      {/* Critical Issues (Abnormal Vitals) */}
      {abnormalVitals.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded p-2 mb-3">
          <div className="flex items-start gap-2">
            <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" />
            <div className="text-xs text-red-700">
              <p className="font-semibold mb-1">🔴 Issues:</p>
              {abnormalVitals.map((vital, idx) => (
                <p key={idx}>• {vital}</p>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Vitals Grid */}
      <div className="bg-white bg-opacity-60 rounded p-3 mb-3">
        <p className="text-xs font-semibold text-slate-600 mb-2">VITALS</p>
        <div className="grid grid-cols-2 gap-2 text-sm">
          {patient.vitals.heart_rate !== undefined && (
            <div className={`flex items-center gap-1 ${getVitalColor('heart_rate', patient.vitals.heart_rate)}`}>
              <Heart className="w-4 h-4" />
              <span>{formatVital('heart_rate', patient.vitals.heart_rate)}</span>
            </div>
          )}
          {patient.vitals.spo2 !== undefined && (
            <div className={`flex items-center gap-1 ${getVitalColor('spo2', patient.vitals.spo2)}`}>
              <TrendingUp className="w-4 h-4" />
              <span>{formatVital('spo2', patient.vitals.spo2)}</span>
            </div>
          )}
          {patient.vitals.temperature !== undefined && (
            <div className={`flex items-center gap-1 ${getVitalColor('temperature', patient.vitals.temperature)}`}>
              <Thermometer className="w-4 h-4" />
              <span>{formatVital('temperature', patient.vitals.temperature)}</span>
            </div>
          )}
          {patient.vitals.respiratory_rate !== undefined && (
            <div className={`flex items-center gap-1 ${getVitalColor('respiratory_rate', patient.vitals.respiratory_rate)}`}>
              <span className="font-semibold">RR:</span>
              <span>{formatVital('respiratory_rate', patient.vitals.respiratory_rate)}</span>
            </div>
          )}
        </div>
        {patient.vitals.systolic_bp !== undefined && patient.vitals.diastolic_bp !== undefined && (
          <p className={`text-sm mt-2 font-semibold ${getVitalColor('systolic_bp', patient.vitals.systolic_bp)}`}>
            BP: {patient.vitals.systolic_bp}/{patient.vitals.diastolic_bp} mmHg
          </p>
        )}
      </div>

      {/* AI Insight */}
      {patient.llm_output?.explanation && (
        <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-3">
          <p className="text-xs font-semibold text-blue-900 mb-1">🧠 AI Insight</p>
          <p className="text-xs text-blue-800 leading-relaxed">{patient.llm_output.explanation}</p>
        </div>
      )}

      {/* Recommended Actions */}
      {patient.llm_output?.suggested_actions && patient.llm_output.suggested_actions.length > 0 && (
        <div className="bg-green-50 border border-green-200 rounded p-3 mb-3">
          <p className="text-xs font-semibold text-green-900 mb-2 flex items-center gap-1">
            <CheckCircle2 className="w-4 h-4" /> ⚡ Recommended Actions
          </p>
          <ul className="space-y-1">
            {patient.llm_output.suggested_actions.map((action, idx) => (
              <li key={idx} className="text-xs text-green-800 flex gap-2">
                <span className="flex-shrink-0">→</span>
                <span>{action}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Alert Message */}
      {patient.alert && (
        <div className="bg-yellow-50 border border-yellow-200 rounded p-2 mb-3">
          <div className="flex items-start gap-2">
            <AlertTriangle className="w-4 h-4 text-yellow-700 flex-shrink-0 mt-0.5" />
            <p className="text-xs text-yellow-800">{patient.alert}</p>
          </div>
        </div>
      )}

      {/* Symptoms/Notes */}
      {(patient.symptoms && patient.symptoms.length > 0) || patient.notes ? (
        <div className="bg-slate-50 rounded p-2 text-xs text-slate-700 space-y-1 mb-3">
          {patient.symptoms && patient.symptoms.length > 0 && (
            <div>
              <span className="font-semibold">Symptoms:</span> {patient.symptoms.join(', ')}
            </div>
          )}
          {patient.notes && (
            <div>
              <span className="font-semibold">Notes:</span> <span className="italic">"{patient.notes}"</span>
            </div>
          )}
        </div>
      ) : null}

      {/* Quick Action Buttons */}
      <div className="grid grid-cols-3 gap-2 mb-3">
        <button
          onClick={() => handleQuickAction('nurse_called')}
          className={`flex items-center justify-center gap-1 px-2 py-2 rounded text-xs font-semibold transition ${
            actionTaken === 'nurse_called'
              ? 'bg-green-500 text-white'
              : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
          }`}
          title="Call Nurse"
        >
          <Phone className="w-3 h-3" />
          <span className="hidden sm:inline">Call</span>
        </button>
        <button
          onClick={() => handleQuickAction('escalated')}
          className={`flex items-center justify-center gap-1 px-2 py-2 rounded text-xs font-semibold transition ${
            actionTaken === 'escalated'
              ? 'bg-green-500 text-white'
              : 'bg-orange-100 text-orange-700 hover:bg-orange-200'
          }`}
          title="Escalate"
        >
          <Zap className="w-3 h-3" />
          <span className="hidden sm:inline">Escalate</span>
        </button>
        <button
          onClick={() => handleQuickAction('reviewed')}
          className={`flex items-center justify-center gap-1 px-2 py-2 rounded text-xs font-semibold transition ${
            actionTaken === 'reviewed'
              ? 'bg-green-500 text-white'
              : 'bg-green-100 text-green-700 hover:bg-green-200'
          }`}
          title="Mark Reviewed"
        >
          <Check className="w-3 h-3" />
          <span className="hidden sm:inline">Reviewed</span>
        </button>
      </div>

      <div className="text-right">
        <button className="text-xs font-semibold text-blue-600 hover:text-blue-800 underline">
          View Details →
        </button>
      </div>
    </div>
  );
};

export default PatientCard;
