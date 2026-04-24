import { AlertCircle, X, Zap } from 'lucide-react';
import { useState, useEffect } from 'react';
import type { Patient } from '../../types/patient';

interface AlertBannerProps {
  criticalPatients: Patient[];
}

export const AlertBanner = ({ criticalPatients }: AlertBannerProps) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (criticalPatients.length === 0) {
      setIsVisible(false);
      return;
    }

    setIsVisible(true);
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % criticalPatients.length);
    }, 5000);

    return () => clearInterval(interval);
  }, [criticalPatients.length]);

  if (!isVisible || criticalPatients.length === 0) {
    return null;
  }

  const currentPatient = criticalPatients[currentIndex];
  const firstAction = currentPatient.llm_output?.suggested_actions?.[0];

  return (
    <div className="bg-red-600 text-white py-4 animate-flash">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between">
        <div className="flex items-center gap-3 flex-1">
          <AlertCircle className="w-6 h-6 animate-pulse flex-shrink-0" />
          <div className="flex-1">
            <p className="font-bold text-lg">
              🚨 CRITICAL: Patient {currentPatient.patient_id}
            </p>
            <p className="text-sm text-red-100 mt-1">
              Ward: {currentPatient.ward || 'N/A'} | Room: {currentPatient.room || 'N/A'} | Risk Score: {currentPatient.score.toFixed(1)}/100
            </p>
            {currentPatient.llm_output?.explanation && (
              <p className="text-sm text-red-100 mt-1 font-medium">
                Issue: {currentPatient.llm_output.explanation.substring(0, 80)}...
              </p>
            )}
            {firstAction && (
              <p className="text-sm text-yellow-100 mt-1 flex items-center gap-2">
                <Zap className="w-3 h-3" />
                <span className="font-semibold">Action: {firstAction}</span>
              </p>
            )}
          </div>
          <div className="text-xs text-red-100 text-right">
            {currentIndex + 1} / {criticalPatients.length}
          </div>
        </div>
        <button
          onClick={() => setIsVisible(false)}
          className="ml-4 p-2 hover:bg-red-700 rounded transition flex-shrink-0"
          aria-label="Close alert"
        >
          <X className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default AlertBanner;
