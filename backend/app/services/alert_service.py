"""
Alert generation service based on severity and vitals.
"""


class AlertService:
    """Service for generating alerts based on patient condition."""
    
    @staticmethod
    def generate_alert(severity: str, spo2: float) -> str:
        """
        Generate alert message based on severity and vitals.
        
        Args:
            severity: Severity level (CRITICAL, HIGH, MODERATE, STABLE)
            spo2: SpO2 value
            
        Returns:
            Alert message string
        """
        if severity == "CRITICAL":
            if spo2 < 90:
                return "⚠️ CRITICAL: Immediate oxygen required - SpO2 critically low"
            else:
                return "🚨 CRITICAL: Critical condition – immediate attention required"
        
        elif severity == "HIGH":
            return "⚠️ HIGH: Close monitoring needed - Patient requires frequent vitals check"
        
        elif severity == "MODERATE":
            return "ℹ️ MODERATE: Standard monitoring - Patient stable but requires attention"
        
        else:  # STABLE
            return "✓ STABLE: Patient vitals stable - Continue routine monitoring"
    
    @staticmethod
    def get_alert_priority(severity: str) -> int:
        """
        Get priority level for alert (higher = more urgent).
        
        Args:
            severity: Severity level
            
        Returns:
            Priority level (1-4)
        """
        priority_map = {
            "CRITICAL": 4,
            "HIGH": 3,
            "MODERATE": 2,
            "STABLE": 1
        }
        return priority_map.get(severity, 1)
