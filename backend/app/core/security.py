import re
import logging

logger = logging.getLogger(__name__)

# Basic heuristic patterns for detecting common prompt injection attempts
PROMPT_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous\s+)?instructions", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?(previous\s+)?instructions", re.IGNORECASE),
    re.compile(r"system\s+prompt", re.IGNORECASE),
    re.compile(r"you\s+are\s+now", re.IGNORECASE),
    re.compile(r"forget\s+everything", re.IGNORECASE),
]

def check_prompt_injection(content: str) -> bool:
    """
    Checks the input content against known prompt injection heuristics.
    Returns True if a potential injection is detected, False otherwise.
    
    Note: This is a basic layer of defense. The LLM prompts themselves 
    must also be robust against injections.
    """
    if not content:
        return False
        
    for pattern in PROMPT_INJECTION_PATTERNS:
        if pattern.search(content):
            logger.warning(f"Potential prompt injection detected matching pattern: {pattern.pattern}")
            return True
            
    return False

def sanitize_input(content: str) -> str:
    """
    Basic input sanitization to prevent rudimentary issues before it hits the LLM.
    """
    # In a real-world scenario, we might strip harmful HTML/Scripts here if analyzing web pages,
    # but since the LLM will parse it, we mainly want to ensure it's valid UTF-8 and strip excessive whitespace.
    if not isinstance(content, str):
        return str(content)
    return content.strip()
