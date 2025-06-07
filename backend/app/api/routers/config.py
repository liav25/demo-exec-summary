from fastapi import APIRouter
from app.core.config import config, REPORT_TYPES, FOCUS_AREAS

router = APIRouter()


@router.get("/config", tags=["Configuration"])
async def get_config():
    """Get configuration data for frontend"""
    return {
        "report_types": REPORT_TYPES,
        "focus_areas": FOCUS_AREAS,
        "company_name": config.company_name,
    }
