export enum SeverityLevel {
  CRITICAL = 'critical',
  HIGH = 'high',
  MODERATE = 'moderate',
  STABLE = 'stable',
}

export interface Vitals {
  heart_rate?: number;
  spo2?: number;
  systolic_bp?: number;
  diastolic_bp?: number;
  temperature?: number;
  respiratory_rate?: number;
}

export interface LLMOutput {
  explanation: string;
  suggested_actions: string[];
}

export interface AuditLog {
  rules_triggered: string[];
  score_breakdown: Record<string, number>;
  final_score: number;
}

export interface Patient {
  id?: string;
  patient_id: string;
  age: number;
  gender: string;
  ward?: string;
  room?: string;
  vitals: Vitals;
  symptoms?: string[];
  notes?: string;
  score: number;
  severity: SeverityLevel;
  alert?: string;
  llm_output: LLMOutput;
  audit_log?: AuditLog;
  timestamp?: string;
}

export interface DashboardData {
  total: number;
  critical: Patient[];
  high: Patient[];
  moderate: Patient[];
  stable: Patient[];
}

export interface Alert {
  id: string;
  patient_id: string;
  patient_name: string;
  message: string;
  severity: SeverityLevel;
  timestamp: string;
}

export interface CreatePatientRequest {
  patient_id: string;
  age: number;
  gender: string;
  ward?: string;
  room?: string;
  vitals: Vitals;
  symptoms?: string[];
  notes?: string;
}

export interface UpdatePatientRequest extends Partial<CreatePatientRequest> {}
