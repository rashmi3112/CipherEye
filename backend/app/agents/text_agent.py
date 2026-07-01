import json
import logging
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class TextAgent(BaseAgent):
    """
    Analyzes raw text content (emails, messages, documents) for threats.
    """
    def __init__(self):
        system_instruction = (
            "You are an elite cyber investigation AI. Your task is to analyze the following text "
            "for potential threats such as phishing, social engineering, scams, and misinformation. "
            "Respond strictly in JSON format with the following keys: "
            "'findings' (list of specific suspicious elements), "
            "'threat_categories' (list of categories like phishing, scam, safe), "
            "'risk_level' (low, medium, high, critical), "
            "and 'confidence' (float between 0.0 and 1.0)."
        )
        super().__init__(system_instruction=system_instruction)

    def analyze(self, content: str) -> dict:
        logger.info("TextAgent analyzing content...")
        
        # We define a basic schema to enforce JSON structure
        schema = {
            "type": "OBJECT",
            "properties": {
                "findings": {"type": "ARRAY", "items": {"type": "STRING"}},
                "threat_categories": {"type": "ARRAY", "items": {"type": "STRING"}},
                "risk_level": {"type": "STRING"},
                "confidence": {"type": "NUMBER"}
            },
            "required": ["findings", "threat_categories", "risk_level", "confidence"]
        }
        
        prompt = f"Analyze the following text content for threats:\n\n{content}"
        
        response_text = self.call_llm(prompt=prompt, response_schema=schema)
        
        if response_text:
            try:
                return json.loads(response_text)
            except Exception as e:
                logger.error(f"Failed to parse TextAgent JSON: {e}")
        
        return {
            "findings": ["Failed to analyze text content."],
            "threat_categories": ["unknown"],
            "risk_level": "unknown",
            "confidence": 0.0
        }
