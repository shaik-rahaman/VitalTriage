"""
Input validation utilities for vital signs and patient data.
"""
from fastapi import HTTPException, status


class VitalsValidator:
    """Validator for patient vital signs."""
    
    # Valid ranges for each vital
    SPO2_MIN = 0
    SPO2_MAX = 100
    HR_MIN = 30
    HR_MAX = 200
    BP_MIN = 70
    BP_MAX = 200
    TEMP_MIN = 95
    TEMP_MAX = 110
    RR_MIN = 10
    RR_MAX = 40
    
    @staticmethod
    def validate_spo2(spo2: float) -> bool:
        """Validate SpO2 value."""
        return VitalsValidator.SPO2_MIN <= spo2 <= VitalsValidator.SPO2_MAX
    
    @staticmethod
    def validate_heart_rate(hr: float) -> bool:
        """Validate heart rate."""
        return VitalsValidator.HR_MIN <= hr <= VitalsValidator.HR_MAX
    
    @staticmethod
    def validate_blood_pressure(systolic: float, diastolic: float) -> bool:
        """Validate blood pressure."""
        systolic_valid = VitalsValidator.BP_MIN <= systolic <= VitalsValidator.BP_MAX
        diastolic_valid = 40 <= diastolic <= 130
        return systolic_valid and diastolic_valid
    
    @staticmethod
    def validate_temperature(temp: float) -> bool:
        """Validate temperature."""
        return VitalsValidator.TEMP_MIN <= temp <= VitalsValidator.TEMP_MAX
    
    @staticmethod
    def validate_respiratory_rate(rr: float) -> bool:
        """Validate respiratory rate."""
        return VitalsValidator.RR_MIN <= rr <= VitalsValidator.RR_MAX
    
    @staticmethod
    def validate_all_vitals(heart_rate: float, spo2: float, systolic_bp: float,
                           diastolic_bp: float, temperature: float, respiratory_rate: float) -> None:
        """
        Validate all vital signs.
        
        Raises HTTPException if any vital is out of range.
        """
        if not VitalsValidator.validate_heart_rate(heart_rate):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Heart rate must be between {VitalsValidator.HR_MIN} and {VitalsValidator.HR_MAX}"
            )
        
        if not VitalsValidator.validate_spo2(spo2):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"SpO2 must be between {VitalsValidator.SPO2_MIN} and {VitalsValidator.SPO2_MAX}"
            )
        
        if not VitalsValidator.validate_blood_pressure(systolic_bp, diastolic_bp):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Systolic BP must be 70-200, Diastolic must be 40-130"
            )
        
        if not VitalsValidator.validate_temperature(temperature):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Temperature must be between {VitalsValidator.TEMP_MIN} and {VitalsValidator.TEMP_MAX}°F"
            )
        
        if not VitalsValidator.validate_respiratory_rate(respiratory_rate):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Respiratory rate must be between {VitalsValidator.RR_MIN} and {VitalsValidator.RR_MAX}"
            )


def validate_patient_input(vitals) -> None:
    """
    Validate patient input data.
    
    Args:
        vitals: VitalsModel object
        
    Raises:
        HTTPException if validation fails
    """
    VitalsValidator.validate_all_vitals(
        heart_rate=vitals.heart_rate,
        spo2=vitals.spo2,
        systolic_bp=vitals.systolic_bp,
        diastolic_bp=vitals.diastolic_bp,
        temperature=vitals.temperature,
        respiratory_rate=vitals.respiratory_rate
    )
