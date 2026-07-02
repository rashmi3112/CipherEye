import pytest
from app.models.schemas import InvestigationReport, ThreatCategory, RiskLevel, DetectedPII

def test_coerce_threat_categories_valid():
    report_data = {
        "trust_score": 90,
        "risk_level": "low",
        "threat_categories": ["safe"],
        "summary": "This is a safe text.",
        "findings": ["No threats found."],
        "confidence": 0.95,
        "recommendations": ["No actions required."],
        "detected_pii": []
    }
    report = InvestigationReport(**report_data)
    assert report.threat_categories == [ThreatCategory.SAFE]

def test_coerce_threat_categories_invalid_and_fallback():
    report_data = {
        "trust_score": 10,
        "risk_level": "critical",
        "threat_categories": ["phishing", "invalid-category-name", "scam"],
        "summary": "Phishing detection.",
        "findings": ["Phishing domain."],
        "confidence": 0.95,
        "recommendations": ["Do not click."],
        "detected_pii": []
    }
    report = InvestigationReport(**report_data)
    # The invalid category name should be coerced to 'unknown'
    assert report.threat_categories == [ThreatCategory.PHISHING, ThreatCategory.UNKNOWN, ThreatCategory.SCAM]

def test_coerce_risk_level_invalid():
    report_data = {
        "trust_score": 50,
        "risk_level": "ultra-high-danger-level", # invalid
        "threat_categories": ["scam"],
        "summary": "Scam alert.",
        "findings": ["Scam pattern."],
        "confidence": 0.8,
        "recommendations": ["Be careful."],
        "detected_pii": []
    }
    report = InvestigationReport(**report_data)
    assert report.risk_level == RiskLevel.UNKNOWN
