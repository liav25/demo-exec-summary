from fastapi import APIRouter, Depends
from datetime import datetime
from app.schemas.report import HealthResponse
from app.utils.utils.ai_generator import AIGenerator
from app.utils.utils.email_sender import EmailSender
from app.core.dependencies import get_ai_generator, get_email_sender

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(
    ai_generator: AIGenerator = Depends(get_ai_generator),
    email_sender: EmailSender = Depends(get_email_sender),
):
    """Health check endpoint"""
    status = HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        components={
            "data_processor": "ok",
            "chart_generator": "ok",
            "pdf_generator": "ok",
            "ai_generator": "ok" if ai_generator else "not_configured",
            "email_sender": "ok" if email_sender else "not_configured",
        },
    )
    return status
