import axios, { AxiosInstance } from 'axios';
import type { Patient, DashboardData, CreatePatientRequest, UpdatePatientRequest } from '../types/patient';

// Type assertion for Vite env variables
const env = (import.meta as any).env as any;
const API_BASE_URL = (env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
const API_TIMEOUT = parseInt((env.VITE_API_TIMEOUT as string) || '10000', 10);

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: API_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error);
        throw error;
      }
    );
  }

  // Dashboard endpoints
  async getDashboard(): Promise<DashboardData> {
    const response = await this.client.get<DashboardData>('/api/v1/dashboard');
    const data = response.data;
    
    // Calculate what the total SHOULD be
    const groupSum = data.critical.length + data.high.length + data.moderate.length + data.stable.length;
    
    // Log detailed response for debugging
    console.log('📊 Dashboard API Response:', {
      apiTotal: data.total,
      groupSum,
      critical: data.critical.length,
      high: data.high.length,
      moderate: data.moderate.length,
      stable: data.stable.length,
      match: data.total === groupSum
    });
    
    // Normalize data
    const normalizePatient = (patient: Patient) => ({
      ...patient,
      severity: (patient.severity as string).toLowerCase() as any,
    });
    
    const normalizedData: DashboardData = {
      total: data.total,
      critical: data.critical.map(normalizePatient).sort((a, b) => b.score - a.score),
      high: data.high.map(normalizePatient).sort((a, b) => b.score - a.score),
      moderate: data.moderate.map(normalizePatient).sort((a, b) => b.score - a.score),
      stable: data.stable.map(normalizePatient).sort((a, b) => b.score - a.score),
    };
    
    // CRITICAL VALIDATION: Ensure total always matches sum
    const recalculatedSum = normalizedData.critical.length + normalizedData.high.length + normalizedData.moderate.length + normalizedData.stable.length;
    
    if (normalizedData.total !== recalculatedSum) {
      console.error(
        '🔴 CRITICAL: API total does not match group sum!',
        { apiTotal: normalizedData.total, recalculatedSum }
      );
      // Force correct total
      normalizedData.total = recalculatedSum;
    }
    
    return normalizedData;
  }

  // Patient endpoints
  async getPatient(id: string): Promise<Patient> {
    console.log(`📥 Fetching patient details: ${id}`);
    const response = await this.client.get<Patient>(`/api/v1/patient/${id}`);
    const patient = response.data;
    
    // CRITICAL: Validate patient data integrity
    console.log('✅ CRITICAL: Patient data received:', {
      patient_id: patient.patient_id,
      severity: patient.severity,
      score: patient.score,
      alert: patient.alert ? patient.alert.substring(0, 50) : 'NONE',
      llm_output: patient.llm_output ? 'Present' : 'MISSING',
      timestamp: patient.timestamp
    });
    
    // Validate critical fields
    if (!patient.alert) {
      console.warn('⚠️ WARNING: Patient alert is empty');
    }
    if (!patient.llm_output || !patient.llm_output.explanation) {
      console.warn('⚠️ WARNING: Patient LLM output is missing');
    }
    if (!['critical', 'high', 'moderate', 'stable'].includes(patient.severity.toLowerCase())) {
      console.error(`🔴 CRITICAL: Invalid severity "${patient.severity}"`);
    }
    
    return {
      ...patient,
      severity: (patient.severity as string).toLowerCase() as any,
    };
  }

  async getAllPatients(): Promise<Patient[]> {
    const response = await this.client.get<Patient[]>('/api/v1/patients');
    return response.data;
  }

  async createPatient(data: CreatePatientRequest): Promise<Patient> {
    const response = await this.client.post<Patient>('/api/v1/patient', data);
    return response.data;
  }

  async updatePatient(patientId: string, data: UpdatePatientRequest): Promise<Patient> {
    console.log(`📡 CRITICAL: PUT /api/v1/patient/${patientId}`, {
      vitals: data.vitals,
      timestamp: new Date().toISOString()
    });
    
    try {
      const response = await this.client.put<Patient>(`/api/v1/patient/${patientId}`, data);
      const updatedPatient = response.data;
      
      // CRITICAL: Validate backend recomputed fields
      console.log('📥 CRITICAL: Update response received:', {
        patient_id: updatedPatient.patient_id,
        severity: updatedPatient.severity,
        score: updatedPatient.score,
        alert: updatedPatient.alert ? updatedPatient.alert.substring(0, 60) : 'MISSING',
        llm_explanation: updatedPatient.llm_output?.explanation ? 'Present' : 'MISSING',
        suggested_actions: updatedPatient.llm_output?.suggested_actions?.length || 0,
        timestamp: updatedPatient.timestamp
      });
      
      // CRITICAL VALIDATION: Ensure all safety-critical fields are present
      if (!updatedPatient.alert) {
        console.error('🔴 CRITICAL: Backend did not return alert!');
      }
      
      if (!updatedPatient.llm_output || !updatedPatient.llm_output.explanation) {
        console.error('🔴 CRITICAL: Backend did not recompute LLM explanation!');
      }
      
      if (!['critical', 'high', 'moderate', 'stable'].includes(updatedPatient.severity.toLowerCase())) {
        console.error(`🔴 CRITICAL: Backend returned invalid severity: ${updatedPatient.severity}`);
      }
      
      console.log('✅ CRITICAL: Update response validation passed');
      
      return {
        ...updatedPatient,
        severity: (updatedPatient.severity as string).toLowerCase() as any,
      };
    } catch (error) {
      console.error(`❌ CRITICAL: Update failed for patient ${patientId}:`, error);
      throw error;
    }
  }

  async deletePatient(id: string): Promise<void> {
    await this.client.delete(`/api/v1/patient/${id}`);
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await this.client.get<{ status: string }>('/api/v1/health');
    return response.data;
  }
}

export const apiClient = new APIClient();
