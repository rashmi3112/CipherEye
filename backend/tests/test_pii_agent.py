import pytest
from app.agents.pii_agent import PIIAgent

def test_pii_agent_redacts_properly():
    agent = PIIAgent()
    text_with_pii = "My email is test@example.com and phone is 123-456-7890."
    
    result = agent.analyze_and_mask(text_with_pii)
    
    assert "masked_text" in result
    assert "detected_pii" in result
    
    if agent.enabled:
        # Check that it masked the email and/or phone
        assert "test@example.com" not in result["masked_text"]
        assert len(result["detected_pii"]) > 0
    else:
        # If disabled (e.g. no spaCy model download), it should safely return the original text
        assert result["masked_text"] == text_with_pii
        assert len(result["detected_pii"]) == 0

def test_pii_agent_empty_text():
    agent = PIIAgent()
    result = agent.analyze_and_mask("")
    assert result["masked_text"] == ""
    assert len(result["detected_pii"]) == 0
