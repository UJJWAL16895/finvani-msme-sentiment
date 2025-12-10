from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.models.infer import SentimentAnalyzer
import logging

# Configure Logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/analyze",
    tags=["analyze"]
)

# Instantiate the analyzer once at module level to keep model in memory
try:
    # Instantiate the analyzer using the default model (XLM-RoBERTa)
    ANALYZER = SentimentAnalyzer()
    logger.info("SentimentAnalyzer initialized successfully with default model (XLM-RoBERTa).")
except Exception as e:
    logger.error(f"Failed to initialize SentimentAnalyzer: {e}")
    ANALYZER = None

class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    label: str
    score: float

@router.post("/", response_model=AnalysisResponse)
async def analyze_headline(request: AnalysisRequest):
    if ANALYZER is None:
        raise HTTPException(status_code=503, detail="Sentiment model is not initialized.")
    
    try:
        result = ANALYZER.predict(request.text)
        return AnalysisResponse(label=result["label"], score=result["score"])
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
