"""FastAPI application for Security+ exam preparation."""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
from schemas import AnalysisRequest, AnalysisResponse
from services import text_analysis_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Security+ Learning API",
    description="AI-powered backend for Security+ exam preparation with Azerbaijani translation",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Serve the frontend."""
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")


@app.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_text(request: AnalysisRequest):
    """
    Analyze Security+ technical text and return structured learning format.
    
    - Translates text to Azerbaijani
    - Identifies unknown technical words
    - Provides A2-level English definitions
    - Generates mini notes in Azerbaijani
    """
    try:
        logger.info(f"Analyzing text: {request.text[:50]}...")
        
        # Process text through analysis service
        result = text_analysis_service.analyze_text(request.text)
        
        logger.info(f"Analysis completed. Unknown words: {result['unknown_words_count']}")
        
        return AnalysisResponse(**result)
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Detailed health check with service status."""
    import os
    
    return {
        "status": "healthy",
        "gemini_api_configured": bool(os.getenv("GEMINI_API_KEY")),
        "services": {
            "translation": "operational",
            "ai_analysis": "operational"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
