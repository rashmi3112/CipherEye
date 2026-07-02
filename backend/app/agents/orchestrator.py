import logging
import asyncio
from app.models.schemas import AnalyzeRequest, InvestigationReport, ContentType
from app.core.security import check_prompt_injection, sanitize_input
from app.agents.pii_agent import PIIAgent
from app.agents.text_agent import TextAgent
from app.agents.url_agent import URLAgent
from app.agents.image_agent import ImageAgent
from app.agents.threat_agent import ThreatAgent
from app.agents.report_agent import ReportAgent

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Coordinates the flow of data through the Multi-Agent system.
    """
    def __init__(self):
        logger.info("Initializing Agent Orchestrator and specialized agents...")
        self.pii_agent = PIIAgent()
        self.text_agent = TextAgent()
        self.url_agent = URLAgent()
        self.image_agent = ImageAgent()
        self.threat_agent = ThreatAgent()
        self.report_agent = ReportAgent()

    async def process_request(self, request: AnalyzeRequest) -> InvestigationReport:
        # 1. Security Check
        sanitized_content = sanitize_input(request.content)
        if check_prompt_injection(sanitized_content):
            return self._create_error_report("Security Alert: Potential prompt injection detected. Request blocked.")

        # 2. PII Detection (Skip for images unless we do OCR first, but for this scope we apply to text/url)
        detected_pii = []
        safe_content = sanitized_content
        
        if request.content_type in [ContentType.TEXT, ContentType.EMAIL]:
            pii_result = self.pii_agent.analyze_and_mask(sanitized_content)
            safe_content = pii_result.get("masked_text", sanitized_content)
            detected_pii = pii_result.get("detected_pii", [])

        # 3. Delegate to Specialized Content Agent
        raw_findings = {}
        if request.content_type in [ContentType.TEXT, ContentType.EMAIL]:
            raw_findings = await asyncio.to_thread(self.text_agent.analyze, safe_content)
        elif request.content_type == ContentType.URL:
            raw_findings = await self.url_agent.analyze(safe_content)
        elif request.content_type == ContentType.IMAGE:
            raw_findings = await asyncio.to_thread(self.image_agent.analyze, sanitized_content) # Base64 string
        else:
            return self._create_error_report(f"Unsupported content type: {request.content_type}")

        # 4. Threat Assessment
        threat_assessment = await asyncio.to_thread(self.threat_agent.analyze, raw_findings)

        # 5. Report Generation
        final_report = await asyncio.to_thread(self.report_agent.generate_report, raw_findings, threat_assessment)

        # 6. Construct Final Response Model
        return InvestigationReport(
            trust_score=threat_assessment.get("trust_score", 0),
            risk_level=threat_assessment.get("final_risk_level", "unknown"),
            threat_categories=threat_assessment.get("consolidated_threats", ["unknown"]),
            summary=final_report.get("summary", "No summary provided."),
            findings=raw_findings.get("findings", []),
            confidence=raw_findings.get("confidence", 0.0),
            recommendations=final_report.get("recommendations", []),
            detected_pii=detected_pii
        )

    def _create_error_report(self, message: str) -> InvestigationReport:
        return InvestigationReport(
            trust_score=0,
            risk_level="critical",
            threat_categories=["safe"], # Safe because we blocked it
            summary=message,
            findings=["Request terminated early due to security policies or unsupported type."],
            confidence=1.0,
            recommendations=["Review the input content.", "Ensure no malicious patterns are present."],
            detected_pii=[]
        )

# Global orchestrator instance
orchestrator = AgentOrchestrator()
