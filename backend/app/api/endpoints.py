from fastapi import APIRouter, HTTPException, Depends
import logging
from app.models.schemas import AnalyzeRequest, InvestigationReport
from app.agents.orchestrator import orchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Analysis"])

@router.post("/analyze", response_model=InvestigationReport)
async def analyze_content(request: AnalyzeRequest):
    """
    Main endpoint for CipherEye.
    Accepts various content types (URL, Text, Base64 Image) and orchestrates 
    the Multi-Agent system to investigate and return a structured report.
    """
    logger.info(f"Received analysis request for type: {request.content_type}")
    try:
        report = await orchestrator.process_request(request)
        return report
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during investigation.")
