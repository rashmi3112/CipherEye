import json
import logging
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ThreatAgent(BaseAgent):
    """
    Acts as a secondary reviewer. It takes the raw findings from the specialized agents
    (Text, URL, Image) and assesses the overall risk, ensuring consistency.
    """
    def __init__(self):
        system_instruction = (
            "You are the Lead Threat Assessor. Review the raw findings from specialized analysis agents. "
            "Determine the final objective risk level, calculate a trust score (0=completely malicious, 100=perfectly safe), "
            "and consolidate the threat categories. "
            "Respond strictly in JSON format with keys: 'trust_score' (int), 'final_risk_level' (low, medium, high, critical), "
            "'consolidated_threats' (list)."
        )
        super().__init__(system_instruction=system_instruction)

    def analyze(self, raw_findings: dict) -> dict:
        logger.info("ThreatAgent aggregating findings...")
        
        schema = {
            "type": "OBJECT",
            "properties": {
                "trust_score": {"type": "INTEGER"},
                "final_risk_level": {"type": "STRING"},
                "consolidated_threats": {"type": "ARRAY", "items": {"type": "STRING"}}
            },
            "required": ["trust_score", "final_risk_level", "consolidated_threats"]
        }
        
        prompt = f"Assess the following raw findings and determine the final threat metrics:\n{json.dumps(raw_findings)}"
        
        response_text = self.call_llm(prompt=prompt, response_schema=schema)
        
        if response_text:
            try:
                return json.loads(response_text)
            except Exception as e:
                logger.error(f"Failed to parse ThreatAgent JSON: {e}")
        
        return {
            "trust_score": 50,
            "final_risk_level": "medium",
            "consolidated_threats": ["unknown"]
        }
