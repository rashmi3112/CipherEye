import json
import logging
import base64
from typing import Dict
from google.genai import types
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ImageAgent(BaseAgent):
    """
    Analyzes images (e.g., screenshots of emails, QR codes, deepfakes) using Gemini's vision capabilities.
    """
    def __init__(self):
        system_instruction = (
            "You are a cyber security vision expert. Analyze the provided image for threats "
            "such as malicious QR codes, fake login screens, deepfake artifacts, or embedded text (OCR). "
            "Respond strictly in JSON format with keys: 'findings', 'threat_categories', "
            "'risk_level', and 'confidence'."
        )
        super().__init__(system_instruction=system_instruction)

    def analyze(self, content: str) -> dict:
        """
        Expects `content` to be a base64 encoded string of the image.
        """
        logger.info("ImageAgent analyzing image content...")
        
        try:
            # Basic validation: check if it's base64
            if "," in content:
                # Strip out data URI prefix like data:image/png;base64,
                content = content.split(",")[1]
            
            image_bytes = base64.b64decode(content)
            
            # Use Google GenAI types.Part for image bytes
            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg' # Defaulting to jpeg, in prod we'd sniff the mime type
            )
            
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
            
            config_dict = {
                "system_instruction": self.system_instruction,
                "response_mime_type": "application/json",
                "response_schema": schema
            }
            config = types.GenerateContentConfig(**config_dict)

            # Note: The BaseAgent.call_llm expects a string prompt. 
            # For multimodal, we call the client directly here.
            if not self.client:
                raise Exception("GenAI client not initialized.")
                
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=["Analyze this image for cyber threats.", image_part],
                config=config
            )
            
            if response.text:
                return json.loads(response.text)
                
        except Exception as e:
            logger.error(f"ImageAgent failed: {e}")
            
        return {
            "findings": ["Failed to process image. Ensure it is a valid base64 string."],
            "threat_categories": ["unknown"],
            "risk_level": "unknown",
            "confidence": 0.0
        }
