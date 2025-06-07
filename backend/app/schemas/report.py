from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict


# Pydantic models for request/response
class ReportRequest(BaseModel):
    recipient_email: EmailStr
    report_type: str
    time_period: str
    focus_areas: List[str] = []
    specific_questions: Optional[str] = ""


class ReportResponse(BaseModel):
    status: str
    message: str
    report_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    components: Dict[str, str]


class EmailTestResponse(BaseModel):
    status: str
    message: str
