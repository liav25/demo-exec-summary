from fastapi import APIRouter, Depends, HTTPException
from app.schemas.report import ReportRequest, ReportResponse, EmailTestResponse
from app.services import report_service
from app.utils.utils.email_sender import EmailSender
from app.core.dependencies import get_email_sender, get_pdf_generator
import traceback
import os
from datetime import datetime

router = APIRouter()


@router.post("/generate-report", response_model=ReportResponse, tags=["Reports"])
async def generate_report(
    request: ReportRequest,
    email_sender: EmailSender = Depends(get_email_sender),
    pdf_generator=Depends(get_pdf_generator),
):
    """Generate and send security report based on request data"""
    try:
        # Validate required fields
        if not all([request.recipient_email, request.report_type, request.time_period]):
            raise HTTPException(
                status_code=400, detail="Please fill in all required fields."
            )

        # Generate the report
        report_data = report_service.generate_report_data(
            request.report_type,
            request.time_period,
            request.focus_areas,
            request.specific_questions,
        )

        # Create HTML report
        html_content = report_service.render_report_html(report_data)

        # Generate PDF
        pdf_path = pdf_generator.generate_pdf(
            html_content,
            f"{request.report_type}_{request.time_period}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        )

        # Send email
        if email_sender:
            success = email_sender.send_report(
                recipient_email=str(request.recipient_email),
                pdf_path=pdf_path,
                report_type=request.report_type,
                period=request.time_period,
            )

            if success:
                return ReportResponse(
                    status="success",
                    message=f"Report successfully generated and sent to {request.recipient_email}!",
                    report_id=os.path.basename(pdf_path),
                )
            else:
                return ReportResponse(
                    status="warning",
                    message="Report generated but email delivery failed. Please check email configuration.",
                    report_id=os.path.basename(pdf_path),
                )
        else:
            return ReportResponse(
                status="info",
                message="Report generated successfully, but email functionality is not configured.",
                report_id=os.path.basename(pdf_path),
            )

    except Exception as e:
        print(f"Error generating report: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Error generating report: {str(e)}"
        )


@router.get("/test-email", response_model=EmailTestResponse, tags=["Reports"])
async def test_email(email_sender: EmailSender = Depends(get_email_sender)):
    """Test email configuration"""
    if email_sender:
        success = email_sender.test_connection()
        if success:
            return EmailTestResponse(
                status="success", message="Email configuration is working"
            )
        else:
            return EmailTestResponse(
                status="error", message="Email configuration failed"
            )
    else:
        return EmailTestResponse(status="error", message="Email sender not configured")
