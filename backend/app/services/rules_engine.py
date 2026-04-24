"""
Critical override rules engine for determining severity.
"""
from typing import Tuple, List


class RulesEngine:
    """Engine for evaluating critical override rules."""
    
    # Critical thresholds
    SPO2_CRITICAL_THRESHOLD = 85
    BP_SYSTOLIC_CRITICAL_THRESHOLD = 90
    HR_CRITICAL_THRESHOLD = 140
    TEMP_CRITICAL_THRESHOLD = 104  # Fahrenheit
    RR_CRITICAL_THRESHOLD = 30
    
    # High-risk thresholds (escalate to HIGH even if score is MODERATE)
    SPO2_HIGH_THRESHOLD = 88
    BP_SYSTOLIC_HIGH_THRESHOLD = 160
    HR_HIGH_THRESHOLD = 110
    TEMP_HIGH_THRESHOLD = 101.5
    RR_HIGH_THRESHOLD = 25
    
    # Moderate thresholds (escalate to MODERATE even if score suggests STABLE)
    SPO2_MODERATE_THRESHOLD = 94
    BP_SYSTOLIC_MODERATE_THRESHOLD = 135
    HR_MODERATE_THRESHOLD = 100
    TEMP_MODERATE_THRESHOLD = 100.4
    RR_MODERATE_THRESHOLD = 20
    
    @staticmethod
    def evaluate_critical_rules(
        heart_rate: float,
        spo2: float,
        systolic_bp: float,
        temperature: float,
        respiratory_rate: float
    ) -> Tuple[bool, List[str]]:
        """
        Evaluate critical override rules.
        
        If any condition is met, patient is CRITICAL.
        
        Args:
            heart_rate: HR in bpm
            spo2: SpO2 percentage
            systolic_bp: Systolic BP
            temperature: Temperature in Fahrenheit
            respiratory_rate: RR in breaths/min
            
        Returns:
            Tuple of (is_critical: bool, triggered_rules: List[str])
        """
        is_critical = False
        triggered_rules = []
        
        if spo2 < RulesEngine.SPO2_CRITICAL_THRESHOLD:
            is_critical = True
            triggered_rules.append(f"SpO2 < {RulesEngine.SPO2_CRITICAL_THRESHOLD}%")
        
        if systolic_bp < RulesEngine.BP_SYSTOLIC_CRITICAL_THRESHOLD:
            is_critical = True
            triggered_rules.append(f"Systolic BP < {RulesEngine.BP_SYSTOLIC_CRITICAL_THRESHOLD}")
        
        if heart_rate > RulesEngine.HR_CRITICAL_THRESHOLD:
            is_critical = True
            triggered_rules.append(f"HR > {RulesEngine.HR_CRITICAL_THRESHOLD} bpm")
        
        if temperature > RulesEngine.TEMP_CRITICAL_THRESHOLD:
            is_critical = True
            triggered_rules.append(f"Temperature > {RulesEngine.TEMP_CRITICAL_THRESHOLD}°F")
        
        if respiratory_rate > RulesEngine.RR_CRITICAL_THRESHOLD:
            is_critical = True
            triggered_rules.append(f"RR > {RulesEngine.RR_CRITICAL_THRESHOLD}")
        
        return is_critical, triggered_rules
    
    @staticmethod
    def evaluate_high_risk_rules(
        heart_rate: float,
        spo2: float,
        systolic_bp: float,
        temperature: float,
        respiratory_rate: float
    ) -> Tuple[bool, List[str]]:
        """
        Evaluate HIGH-risk override rules.
        
        If 2+ conditions are met, patient is HIGH (even if score is MODERATE).
        
        Args:
            heart_rate: HR in bpm
            spo2: SpO2 percentage
            systolic_bp: Systolic BP
            temperature: Temperature in Fahrenheit
            respiratory_rate: RR in breaths/min
            
        Returns:
            Tuple of (is_high_risk: bool, triggered_rules: List[str])
        """
        is_high_risk = False
        triggered_rules = []
        abnormal_count = 0
        
        if spo2 < RulesEngine.SPO2_HIGH_THRESHOLD:
            abnormal_count += 1
            triggered_rules.append(f"SpO2 < {RulesEngine.SPO2_HIGH_THRESHOLD}%")
        
        if systolic_bp > RulesEngine.BP_SYSTOLIC_HIGH_THRESHOLD:
            abnormal_count += 1
            triggered_rules.append(f"Systolic BP > {RulesEngine.BP_SYSTOLIC_HIGH_THRESHOLD}")
        
        if heart_rate > RulesEngine.HR_HIGH_THRESHOLD:
            abnormal_count += 1
            triggered_rules.append(f"HR > {RulesEngine.HR_HIGH_THRESHOLD} bpm")
        
        if temperature > RulesEngine.TEMP_HIGH_THRESHOLD:
            abnormal_count += 1
            triggered_rules.append(f"Temperature > {RulesEngine.TEMP_HIGH_THRESHOLD}°F")
        
        if respiratory_rate > RulesEngine.RR_HIGH_THRESHOLD:
            abnormal_count += 1
            triggered_rules.append(f"RR > {RulesEngine.RR_HIGH_THRESHOLD}")
        
        # Escalate to HIGH if 2+ vitals are abnormal
        if abnormal_count >= 2:
            is_high_risk = True
        
        return is_high_risk, triggered_rules
    
    @staticmethod
    def evaluate_moderate_rules(
        heart_rate: float,
        spo2: float,
        systolic_bp: float,
        temperature: float,
        respiratory_rate: float
    ) -> Tuple[bool, List[str]]:
        """
        Evaluate MODERATE rule overrides.
        
        If any condition is met, patient is at least MODERATE
        (escalates STABLE → MODERATE, preserves MODERATE and above).
        
        Args:
            heart_rate: HR in bpm
            spo2: SpO2 percentage
            systolic_bp: Systolic BP
            temperature: Temperature in Fahrenheit
            respiratory_rate: RR in breaths/min
            
        Returns:
            Tuple of (is_moderate: bool, triggered_rules: List[str])
        """
        is_moderate = False
        triggered_rules = []
        abnormal_count = 0
        
        if spo2 < RulesEngine.SPO2_MODERATE_THRESHOLD:
            abnormal_count += 1
            triggered_rules.append(f"SpO2 < {RulesEngine.SPO2_MODERATE_THRESHOLD}%")
        
        if systolic_bp > RulesEngine.BP_SYSTOLIC_MODERATE_THRESHOLD:
            abnormal_count += 1
            triggered_rules.append(f"Systolic BP > {RulesEngine.BP_SYSTOLIC_MODERATE_THRESHOLD}")
        
        if heart_rate > RulesEngine.HR_MODERATE_THRESHOLD:
            abnormal_count += 1
            triggered_rules.append(f"HR > {RulesEngine.HR_MODERATE_THRESHOLD} bpm")
        
        if temperature > RulesEngine.TEMP_MODERATE_THRESHOLD:
            abnormal_count += 1
            triggered_rules.append(f"Temperature > {RulesEngine.TEMP_MODERATE_THRESHOLD}°F")
        
        if respiratory_rate > RulesEngine.RR_MODERATE_THRESHOLD:
            abnormal_count += 1
            triggered_rules.append(f"RR > {RulesEngine.RR_MODERATE_THRESHOLD}")
        
        # Escalate to MODERATE if any vital is abnormal by moderate threshold
        if abnormal_count >= 1:
            is_moderate = True
        
        return is_moderate, triggered_rules
