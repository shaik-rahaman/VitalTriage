import { SeverityLevel } from '../types/patient';

export const getSeverityColor = (severity: SeverityLevel): string => {
  const colors: Record<SeverityLevel, string> = {
    [SeverityLevel.CRITICAL]: 'red',
    [SeverityLevel.HIGH]: 'orange',
    [SeverityLevel.MODERATE]: 'yellow',
    [SeverityLevel.STABLE]: 'green',
  };
  return colors[severity];
};

export const getSeverityBgClass = (severity: SeverityLevel): string => {
  const classes: Record<SeverityLevel, string> = {
    [SeverityLevel.CRITICAL]: 'bg-red-50 border-red-200',
    [SeverityLevel.HIGH]: 'bg-orange-50 border-orange-200',
    [SeverityLevel.MODERATE]: 'bg-yellow-50 border-yellow-200',
    [SeverityLevel.STABLE]: 'bg-green-50 border-green-200',
  };
  return classes[severity];
};

export const getSeverityTextClass = (severity: SeverityLevel): string => {
  const classes: Record<SeverityLevel, string> = {
    [SeverityLevel.CRITICAL]: 'text-red-800',
    [SeverityLevel.HIGH]: 'text-orange-800',
    [SeverityLevel.MODERATE]: 'text-yellow-800',
    [SeverityLevel.STABLE]: 'text-green-800',
  };
  return classes[severity];
};

export const getSeverityIcon = (severity: SeverityLevel): string => {
  const icons: Record<SeverityLevel, string> = {
    [SeverityLevel.CRITICAL]: '🔴',
    [SeverityLevel.HIGH]: '🟠',
    [SeverityLevel.MODERATE]: '🟡',
    [SeverityLevel.STABLE]: '🟢',
  };
  return icons[severity];
};

export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const formatVital = (key: string, value: number | string | undefined): string => {
  if (value === undefined || value === null) return 'N/A';
  
  const vitalFormats: Record<string, string> = {
    heart_rate: `${value} bpm`,
    spo2: `${value}%`,
    oxygen_saturation: `${value}%`,
    temperature: `${value}°F`,
    respiratory_rate: `${value} breaths/min`,
    systolic_bp: `${value} mmHg`,
    diastolic_bp: `${value} mmHg`,
  };
  
  return vitalFormats[key] || String(value);
};

export const isVitalAbnormal = (key: string, value: number): boolean => {
  // Define critical and high thresholds for each vital
  const abnormalRanges: Record<string, { critical: [number, number]; high: [number, number] }> = {
    heart_rate: { critical: [0, 50], high: [0, 60] },
    spo2: { critical: [0, 88], high: [0, 92] },
    temperature: { critical: [95, 103], high: [98, 101] },
    respiratory_rate: { critical: [0, 12], high: [0, 14] },
    systolic_bp: { critical: [0, 90], high: [0, 100] },
    diastolic_bp: { critical: [0, 60], high: [0, 70] },
  };
  
  const range = abnormalRanges[key];
  if (!range) return false;
  
  // Check if value is in critical range
  if (value <= range.critical[0] || value >= range.critical[1]) {
    return true;
  }
  return false;
};

export const getVitalStatus = (key: string, value: number): 'critical' | 'high' | 'normal' => {
  const abnormalRanges: Record<string, { critical: [number, number]; high: [number, number] }> = {
    heart_rate: { critical: [0, 50], high: [0, 60] },
    spo2: { critical: [0, 88], high: [0, 92] },
    temperature: { critical: [95, 103], high: [98, 101] },
    respiratory_rate: { critical: [0, 12], high: [0, 14] },
    systolic_bp: { critical: [0, 90], high: [0, 100] },
    diastolic_bp: { critical: [0, 60], high: [0, 70] },
  };
  
  const range = abnormalRanges[key];
  if (!range) return 'normal';
  
  if (value <= range.critical[0] || value >= range.critical[1]) {
    return 'critical';
  }
  if (value <= range.high[0] || value >= range.high[1]) {
    return 'high';
  }
  return 'normal';
};

export const formatTimeAgo = (dateString: string | undefined): string => {
  if (!dateString) return 'N/A';
  
  const now = new Date();
  const date = new Date(dateString);
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  
  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `${diffHours}h ago`;
  
  const diffDays = Math.floor(diffHours / 24);
  if (diffDays < 7) return `${diffDays}d ago`;
  
  return formatDate(dateString);
};

export const getAlertIcon = (severity: SeverityLevel): string => {
  const icons: Record<SeverityLevel, string> = {
    [SeverityLevel.CRITICAL]: '🚨',
    [SeverityLevel.HIGH]: '⚠️',
    [SeverityLevel.MODERATE]: '⚡',
    [SeverityLevel.STABLE]: 'ℹ️',
  };
  return icons[severity];
};
