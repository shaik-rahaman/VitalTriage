"""
Scoring engine for computing patient risk score.
"""
from typing import Dict, Tuple
from .rules_engine import RulesEngine


class ScoringEngine:
    """Engine for computing patient risk score based on vitals and symptoms."""
    
    # Weight distribution (must sum to 100)
    WEIGHT_SPO2 = 0.40  # 40%
    WEIGHT_BP = 0.20    # 20%
    WEIGHT_HR = 0.15    # 15%
    WEIGHT_RR = 0.10    # 10%
    WEIGHT_TEMP = 0.10  # 10%
    WEIGHT_SYMPTOMS = 0.05  # 5%
    
    # Severity thresholds
    CRITICAL_THRESHOLD = 80
    HIGH_THRESHOLD = 60
    MODERATE_THRESHOLD = 30
    
    # Symptom keyword scoring
    SYMPTOM_SCORES = {
        "breathlessness": 20,
        "shortness of breath": 20,
        "chest pain": 25,
        "chest discomfort": 25,
        "fever": 10,
        "high fever": 15,
        "difficulty breathing": 20,
        "confusion": 20,
        "dizziness": 15,
        "fainting": 25,
        "severe headache": 20,
        "persistent cough": 15,
        "severe cough": 20,
        "abdominal pain": 15,
        "nausea": 10,
        "vomiting": 15
    }
    
    @staticmethod
    def score_spo2(spo2: float) -> float:
        """
        Score SpO2 on 0-100 scale.
        ≥95: 0, 90-94: 30, 85-89: 70, <85: 100
        """
        if spo2 >= 95:
            return 0
        elif spo2 >= 90:
            return 30
        elif spo2 >= 85:
            return 70
        else:
            return 100
    
    @staticmethod
    def score_blood_pressure(systolic: float, diastolic: float) -> float:
        """
        Score blood pressure on 0-100 scale.
        Considers systolic and diastolic.
        """
        systolic_score = 0
        diastolic_score = 0
        
        # Systolic scoring
        if systolic < 90:
            systolic_score = 100
        elif systolic < 100:
            systolic_score = 80
        elif systolic < 120:
            systolic_score = 0
        elif systolic < 140:
            systolic_score = 20
        elif systolic < 160:
            systolic_score = 50
        else:
            systolic_score = 80
        
        # Diastolic scoring
        if diastolic < 60:
            diastolic_score = 70
        elif diastolic < 80:
            diastolic_score = 10
        elif diastolic < 100:
            diastolic_score = 30
        else:
            diastolic_score = 70
        
        return (systolic_score + diastolic_score) / 2
    
    @staticmethod
    def score_heart_rate(hr: float) -> float:
        """
        Score heart rate on 0-100 scale.
        Optimal 60-100 bpm.
        """
        if 60 <= hr <= 100:
            return 0
        elif 50 <= hr < 60:
            return 20
        elif 100 < hr <= 120:
            return 20
        elif 40 <= hr < 50:
            return 50
        elif 120 < hr <= 140:
            return 50
        else:
            return 100
    
    @staticmethod
    def score_respiratory_rate(rr: float) -> float:
        """
        Score respiratory rate on 0-100 scale.
        Normal 12-20 breaths/min.
        """
        if 12 <= rr <= 20:
            return 0
        elif 10 <= rr < 12:
            return 20
        elif 20 < rr <= 25:
            return 20
        elif 25 < rr <= 30:
            return 60
        else:
            return 100
    
    @staticmethod
    def score_temperature(temp: float) -> float:
        """
        Score temperature on 0-100 scale.
        Normal ~98.6°F.
        """
        if 97 <= temp <= 100:
            return 0
        elif 95 <= temp < 97:
            return 30
        elif 100 < temp <= 102:
            return 20
        elif 102 < temp <= 104:
            return 60
        else:
            return 100
    
    @staticmethod
    def score_symptoms(symptoms: list) -> float:
        """
        Score symptoms on 0-100 scale.
        Based on keyword matching.
        """
        if not symptoms:
            return 0
        
        total_score = 0
        matched_symptoms = set()
        
        for symptom in symptoms:
            symptom_lower = symptom.lower().strip()
            
            # Direct match
            if symptom_lower in ScoringEngine.SYMPTOM_SCORES:
                total_score += ScoringEngine.SYMPTOM_SCORES[symptom_lower]
                matched_symptoms.add(symptom_lower)
            else:
                # Partial match
                for key, value in ScoringEngine.SYMPTOM_SCORES.items():
                    if key in symptom_lower:
                        total_score += value
                        matched_symptoms.add(key)
                        break
        
        # Cap at 100
        return min(total_score, 100)
    
    @staticmethod
    def compute_score(
        heart_rate: float,
        spo2: float,
        systolic_bp: float,
        diastolic_bp: float,
        temperature: float,
        respiratory_rate: float,
        symptoms: list
    ) -> Tuple[float, Dict[str, float]]:
        """
        Compute final risk score using weighted average.
        
        Returns:
            Tuple of (final_score, score_breakdown)
        """
        # Compute individual scores
        spo2_score = ScoringEngine.score_spo2(spo2)
        bp_score = ScoringEngine.score_blood_pressure(systolic_bp, diastolic_bp)
        hr_score = ScoringEngine.score_heart_rate(heart_rate)
        rr_score = ScoringEngine.score_respiratory_rate(respiratory_rate)
        temp_score = ScoringEngine.score_temperature(temperature)
        symptom_score = ScoringEngine.score_symptoms(symptoms)
        
        # Compute weighted final score
        final_score = (
            spo2_score * ScoringEngine.WEIGHT_SPO2 +
            bp_score * ScoringEngine.WEIGHT_BP +
            hr_score * ScoringEngine.WEIGHT_HR +
            rr_score * ScoringEngine.WEIGHT_RR +
            temp_score * ScoringEngine.WEIGHT_TEMP +
            symptom_score * ScoringEngine.WEIGHT_SYMPTOMS
        )
        
        score_breakdown = {
            "spo2": spo2_score,
            "bp": bp_score,
            "hr": hr_score,
            "rr": rr_score,
            "temperature": temp_score,
            "symptoms": symptom_score,
            "final_score": round(final_score, 2)
        }
        
        return round(final_score, 2), score_breakdown
    
    @staticmethod
    def map_severity(score: float) -> str:
        """
        Map score to severity level.
        
        ≥80: CRITICAL
        60-79: HIGH
        30-59: MODERATE
        <30: STABLE
        """
        if score >= ScoringEngine.CRITICAL_THRESHOLD:
            return "CRITICAL"
        elif score >= ScoringEngine.HIGH_THRESHOLD:
            return "HIGH"
        elif score >= ScoringEngine.MODERATE_THRESHOLD:
            return "MODERATE"
        else:
            return "STABLE"
