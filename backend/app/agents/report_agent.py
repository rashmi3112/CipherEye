import json
import logging
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ReportAgent(BaseAgent):
    """
    The final agent in the pipeline. Responsible for taking all accumulated data
    and writing a clear, explainable, and actionable report for the end user.
    """
    def __init__(self):
        system_instruction = (
            "You are an expert Cyber Security Communicator. Your job is to take technical threat findings "
            "and translate them into a clear, concise, and actionable security report for a non-technical user. "
            "You must respond strictly in JSON format with keys: 'summary' (string), "
            "and 'recommendations' (list of strings representing actionable advice)."
        )
        super().__init__(system_instruction=system_instruction)

    def generate_report(self, raw_findings: dict, threat_assessment: dict) -> dict:
        logger.info("ReportAgent generating final report...")
        
        schema = {
            "type": "OBJECT",
            "properties": {
                "summary": {"type": "STRING"},
                "recommendations": {"type": "ARRAY", "items": {"type": "STRING"}}
            },
            "required": ["summary", "recommendations"]
        }
        
        context = {
            "raw_findings": raw_findings,
            "threat_assessment": threat_assessment
        }
        
        prompt = f"Write the final report summary and recommendations based on these findings:\n{json.dumps(context)}"
        
        response_text = self.call_llm(prompt=prompt, response_schema=schema)
        
        if response_text:
            try:
                return json.loads(response_text)
            except Exception as e:
                logger.error(f"Failed to parse ReportAgent JSON: {e}")
        
        return {
            "summary": "An error occurred while generating the report summary.",
            "recommendations": ["Exercise caution as the analysis could not be fully completed."]
        }
