from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from enum import Enum

class ContentType(str, Enum):
    URL = "url"
    TEXT = "text"
    EMAIL = "email"
    IMAGE = "image"
    PDF = "pdf"
    AUDIO = "audio"
    VIDEO = "video"

class AnalyzeRequest(BaseModel):
    content_type: ContentType = Field(..., description="The type of content being submitted for analysis.")
    content: str = Field(..., description="The actual content. For URLs or Text, it's the string. For files, it should be a base64 encoded string or a URL to the file.")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata about the content.")

class ThreatCategory(str, Enum):
    PHISHING = "phishing"
    MALWARE = "malware"
    SCAM = "scam"
    SPAM = "spam"
    DISINFORMATION = "disinformation"
    SOCIAL_ENGINEERING = "social engineering"  # FIX: was missing, LLM returns this
    IMPERSONATION = "impersonation"             # added: LLM commonly returns this too
    FRAUD = "fraud"                             # added: LLM commonly returns this too
    SAFE = "safe"
    UNKNOWN = "unknown"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

class DetectedPII(BaseModel):
    entity_type: str = Field(..., description="The type of PII detected (e.g., EMAIL_ADDRESS, PHONE_NUMBER).")
    start: int = Field(..., description="Start index in the text.")
    end: int = Field(..., description="End index in the text.")
    replacement: str = Field(..., description="The string used to mask the PII.")

class InvestigationReport(BaseModel):
    trust_score: int = Field(..., ge=0, le=100, description="A score from 0 (completely untrustworthy) to 100 (completely trustworthy).")
    risk_level: RiskLevel = Field(..., description="The overall risk level.")
    threat_categories: List[ThreatCategory] = Field(..., description="Identified threat categories.")
    summary: str = Field(..., description="A high-level human-readable summary of the findings.")
    findings: List[str] = Field(..., description="Specific details and evidence discovered during analysis.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="The confidence level of the report.")
    recommendations: List[str] = Field(..., description="Actionable advice for the user based on the findings.")
    detected_pii: Optional[List[DetectedPII]] = Field(default=None, description="A list of PII detected and masked during analysis.")

    @field_validator("threat_categories", mode="before")
    @classmethod
    def coerce_threat_categories(cls, values: list) -> list:
        """
        Sanitizes the LLM's threat_categories output before Pydantic validates it.
        Any value the LLM returns that isn't a known ThreatCategory is silently
        replaced with 'unknown' instead of crashing the whole request.
        """
        known = {e.value for e in ThreatCategory}
        sanitized = []
        for v in values:
            if isinstance(v, str) and v.lower() in known:
                sanitized.append(v.lower())
            else:
                import logging
                logging.getLogger(__name__).warning(
                    f"Unknown threat category from LLM: '{v}' — replacing with 'unknown'"
                )
                sanitized.append("unknown")
        # Deduplicate while preserving order
        seen = set()
        return [x for x in sanitized if not (x in seen or seen.add(x))]

    @field_validator("risk_level", mode="before")
    @classmethod
    def coerce_risk_level(cls, v: str) -> str:
        """Same safety net for risk_level — maps anything unexpected to 'unknown'."""
        known = {e.value for e in RiskLevel}
        if isinstance(v, str) and v.lower() in known:
            return v.lower()
        import logging
        logging.getLogger(__name__).warning(f"Unknown risk_level from LLM: '{v}' — replacing with 'unknown'")
        return "unknown"

    class Config:
        json_schema_extra = {
            "example": {
                "trust_score": 10,
                "risk_level": "critical",
                "threat_categories": ["phishing", "scam"],
                "summary": "This URL strongly resembles a known phishing attack attempting to steal credentials.",
                "findings": ["The domain is recently registered.", "The login form posts to an external IP."],
                "confidence": 0.95,
                "recommendations": ["Do not enter any credentials.", "Block this domain on your network."],
                "detected_pii": []
            }
        }