"""
LLM service for generating patient condition explanations and suggested actions.
Supports both OpenAI and GROQ as LLM providers.
"""
import logging
from typing import Dict, Any
import os
from openai import AsyncOpenAI, APIError, APIConnectionError
from groq import Groq

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM-based patient condition explanations."""
    
    def __init__(self, api_key: str = None, provider: str = None, model: str = None):
        """
        Initialize LLM service with configurable provider.
        
        Args:
            api_key: API key (defaults to env var based on provider)
            provider: LLM provider - 'openai' or 'groq' (defaults to env var LLM_PROVIDER)
            model: Model name (defaults to env var LLM_MODEL or provider default)
        """
        # Determine provider
        self.provider = provider or os.getenv("LLM_PROVIDER", "openai").lower()
        
        # Initialize based on provider
        if self.provider == "groq":
            self.api_key = api_key or os.getenv("GROQ_API_KEY")
            self.model = model or os.getenv("LLM_MODEL", "mixtral-8x7b-32768")
            self.client = Groq(api_key=self.api_key) if self.api_key else None
            logger.info(f"Initialized GROQ LLM service with model: {self.model}")
        else:  # Default to OpenAI
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.model = model or os.getenv("LLM_MODEL", "gpt-3.5-turbo")
            self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None
            logger.info(f"Initialized OpenAI LLM service with model: {self.model}")
    
    async def generate_explanation(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate LLM-based explanation and suggested actions.
        
        Args:
            patient_data: Dictionary containing patient vitals and info
                {
                    'spo2': float,
                    'hr': float,
                    'bp': str,
                    'temp': float,
                    'rr': float,
                    'symptoms': list,
                    'notes': str,
                    'severity': str,
                    'score': float
                }
        
        Returns:
            Dictionary with explanation and suggested_actions
            Falls back to default explanation if LLM fails
        """
        try:
            if not self.client:
                logger.warning(f"{self.provider.upper()} API key not configured, using default explanation")
                return self._get_default_explanation(patient_data)
            
            prompt = self._build_prompt(patient_data)
            system_message = "You are a clinical decision support AI assistant. Provide clear, concise explanations of patient conditions based on vital signs. Focus on immediate clinical concerns. DO NOT prescribe medications. Only suggest monitoring, positioning, oxygen therapy, hydration, or referral to specialists when appropriate."
            
            if self.provider == "groq":
                # GROQ uses synchronous client
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                response_text = response.choices[0].message.content
            else:
                # OpenAI uses async client
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500,
                    timeout=10.0
                )
                response_text = response.choices[0].message.content
            
            # Extract explanation and suggested actions
            result = self._parse_llm_response(response_text, patient_data)
            logger.info(f"Generated {self.provider.upper()} LLM explanation for patient")
            return result
            
        except (APIError, APIConnectionError) as e:
            logger.error(f"{self.provider.upper()} API error: {str(e)}")
            return self._get_default_explanation(patient_data)
        except Exception as e:
            logger.error(f"Unexpected error in LLM service: {str(e)}")
            return self._get_default_explanation(patient_data)
    
    def _build_prompt(self, patient_data: Dict[str, Any]) -> str:
        """Build the prompt for LLM."""
        bp = f"{patient_data.get('systolic_bp')}/{patient_data.get('diastolic_bp')}"
        
        prompt = f"""
Patient Assessment:
- SpO2: {patient_data.get('spo2')}%
- Heart Rate: {patient_data.get('hr')} bpm
- Blood Pressure: {bp} mmHg
- Temperature: {patient_data.get('temperature')}°F
- Respiratory Rate: {patient_data.get('rr')} breaths/min
- Reported Symptoms: {', '.join(patient_data.get('symptoms', [])) or 'None'}
- Clinical Notes: {patient_data.get('notes') or 'None'}
- Risk Score: {patient_data.get('score')}/100
- Severity Level: {patient_data.get('severity')}

Please provide:
1. A brief (2-3 sentence) clinical explanation of this patient's current condition
2. A JSON array with 2-4 immediate suggested actions (each as a concise string, e.g., "Monitor oxygen saturation every 15 minutes", "Position patient upright", "Ensure IV access", "Contact specialist if condition worsens")

Format your response as:
EXPLANATION: [explanation here]
ACTIONS: [["action1", "action2", "action3"]]

DO NOT recommend any medications or invasive procedures.
"""
        return prompt.strip()
    
    def _parse_llm_response(self, response_text: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse LLM response to extract explanation and actions."""
        try:
            lines = response_text.split('\n')
            explanation = ""
            actions = []
            
            for i, line in enumerate(lines):
                if line.startswith("EXPLANATION:"):
                    explanation = line.replace("EXPLANATION:", "").strip()
                elif line.startswith("ACTIONS:"):
                    actions_text = line.replace("ACTIONS:", "").strip()
                    # Try to extract JSON array
                    import json
                    try:
                        # Handle multiple formats
                        if actions_text.startswith('["'):
                            actions = json.loads(actions_text)
                        else:
                            # Try to parse as plain text list
                            actions_text = actions_text.strip('[]')
                            actions = [a.strip().strip('"') for a in actions_text.split(',')]
                    except:
                        actions = [a.strip().strip('"') for a in actions_text.split(',')]
            
            if not explanation:
                explanation = response_text[:200]  # Fallback to first part of response
            
            if not actions:
                actions = self._get_default_actions(patient_data)
            
            return {
                "explanation": explanation,
                "suggested_actions": actions[:4]  # Limit to 4 actions
            }
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {str(e)}")
            return self._get_default_explanation(patient_data)
    
    def _get_default_explanation(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate default explanation when LLM is unavailable."""
        severity = patient_data.get('severity', 'UNKNOWN')
        
        explanations = {
            "CRITICAL": {
                "explanation": "Patient is in a CRITICAL condition with one or more vital signs at dangerous levels requiring immediate medical intervention.",
                "suggested_actions": [
                    "Ensure continuous pulse oximetry and cardiac monitoring",
                    "Prepare for potential emergency procedures",
                    "Contact critical care team immediately"
                ]
            },
            "HIGH": {
                "explanation": "Patient presents HIGH risk with multiple abnormal vital signs requiring urgent clinical attention and close monitoring.",
                "suggested_actions": [
                    "Increase monitoring frequency to every 15-30 minutes",
                    "Ensure IV access is available",
                    "Notify clinical team of status changes"
                ]
            },
            "MODERATE": {
                "explanation": "Patient shows MODERATE risk level with some abnormal vitals. Requires standard clinical monitoring and reassessment.",
                "suggested_actions": [
                    "Continue routine vital sign monitoring",
                    "Assess patient comfort and position",
                    "Document any symptom changes"
                ]
            },
            "STABLE": {
                "explanation": "Patient vitals are STABLE with no immediate concerns. Continue routine monitoring and care.",
                "suggested_actions": [
                    "Maintain current care protocol",
                    "Continue regular vital sign monitoring",
                    "Encourage hydration and rest"
                ]
            }
        }
        
        return explanations.get(severity, explanations["MODERATE"])
    
    def _get_default_actions(self, patient_data: Dict[str, Any]) -> list:
        """Get default suggested actions based on severity."""
        severity = patient_data.get('severity', 'MODERATE')
        
        if severity == "CRITICAL":
            return [
                "Ensure continuous monitoring",
                "Prepare emergency response",
                "Contact critical care team"
            ]
        elif severity == "HIGH":
            return [
                "Increase monitoring frequency",
                "Ensure IV access",
                "Notify clinical team"
            ]
        elif severity == "MODERATE":
            return [
                "Continue routine monitoring",
                "Reassess patient regularly",
                "Document observations"
            ]
        else:
            return [
                "Maintain current care",
                "Regular monitoring",
                "Encourage hydration"
            ]
