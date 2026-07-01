import json
import logging
from app.agents.base_agent import BaseAgent
from app.mcp.client_manager import mcp_manager

logger = logging.getLogger(__name__)

class URLAgent(BaseAgent):
    """
    Analyzes URLs for malicious patterns (typosquatting, strange TLDs, phishing params).
    Optionally utilizes MCP to fetch additional domain intelligence if a tool is available.
    """
    def __init__(self):
        system_instruction = (
            "You are a cyber security expert specializing in URL analysis. "
            "Analyze the given URL for malicious intent such as typosquatting, phishing, "
            "suspicious parameters, or dangerous TLDs. "
            "Respond strictly in JSON format with keys: 'findings' (list), "
            "'threat_categories' (list), 'risk_level' (low, medium, high, critical), "
            "and 'confidence' (float)."
        )
        super().__init__(system_instruction=system_instruction)

    async def analyze(self, content: str) -> dict:
        logger.info(f"URLAgent analyzing URL: {content}")
        
        # Optional: Ask MCP manager if we have a reputation lookup tool
        # mcp_context = ""
        # result = await mcp_manager.call_tool("search", "domain_reputation", {"url": content})
        # if result:
        #    mcp_context = f"\nExternal Intelligence:\n{result}"
        
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
        
        prompt = f"Analyze this URL for threats: {content}"
        
        response_text = self.call_llm(prompt=prompt, response_schema=schema)
        
        if response_text:
            try:
                return json.loads(response_text)
            except Exception as e:
                logger.error(f"Failed to parse URLAgent JSON: {e}")
        
        return {
            "findings": ["Failed to analyze URL."],
            "threat_categories": ["unknown"],
            "risk_level": "unknown",
            "confidence": 0.0
        }
