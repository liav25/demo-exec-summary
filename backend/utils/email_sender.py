import smtplib
import os

import resend
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import List, Optional, Dict
from config import Config


class EmailSender:
    """Handles sending email reports with PDF attachments"""

    def __init__(self):
        self.config = Config()

        # Validate email configuration
        if not all([self.config.EMAIL_ADDRESS, self.config.EMAIL_PASSWORD]):
            raise ValueError(
                "Email configuration incomplete. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in your .env file."
            )

    def send_report(
        self,
        recipient_email: str,
        pdf_path: str,
        report_type: str,
        period: str,
        subject: Optional[str] = None,
        custom_message: Optional[str] = None,
    ) -> bool:
        """Send security report via email with PDF attachment"""

        try:
            f: bytes = open(pdf_path, "rb").read()
            attachment: resend.Attachment = {
                "content": list(f),
                "filename": "summary.pdf",
            }

            params: resend.Emails.SendParams = {
                "from": "Acme <onboarding@resend.dev>",
                "to": recipient_email,
                "subject": subject or self._generate_subject(report_type, period),
                "html": custom_message
                or self._generate_email_body(report_type, period),
                "attachments": [attachment],
            }

            # Send email
            email = resend.Emails.send(params)
            print(email)

            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def send_bulk_reports(
        self, recipients: List[str], pdf_path: str, report_type: str, period: str
    ) -> Dict[str, bool]:
        """Send reports to multiple recipients"""

        results = {}

        for recipient in recipients:
            try:
                success = self.send_report(recipient, pdf_path, report_type, period)
                results[recipient] = success
            except Exception as e:
                print(f"Failed to send to {recipient}: {str(e)}")
                results[recipient] = False

        return results

    def _generate_subject(self, report_type: str, period: str) -> str:
        """Generate email subject line"""
        report_name = self.config.REPORT_TYPES.get(report_type, {}).get(
            "name", report_type.replace("_", " ").title()
        )
        company_name = self.config.COMPANY_NAME

        return f"{company_name} - {report_name} ({period.replace('_', ' ').title()})"

    def _generate_email_body(self, report_type: str, period: str) -> str:
        """Generate HTML email body"""

        report_name = self.config.REPORT_TYPES.get(report_type, {}).get(
            "name", report_type.replace("_", " ").title()
        )
        company_name = self.config.COMPANY_NAME
        current_date = datetime.now().strftime("%B %d, %Y")

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #1f77b4;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f8f9fa;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .highlight {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #666;
                }}
                .button {{
                    display: inline-block;
                    background-color: #1f77b4;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{company_name}</h1>
                <h2>Security Report Delivery</h2>
            </div>
            
            <div class="content">
                <p>Dear Executive,</p>
                
                <p>Please find attached your requested <strong>{report_name}</strong> for the <strong>{period.replace('_', ' ')}</strong> period.</p>
                
                <div class="highlight">
                    <h3>📊 Report Summary</h3>
                    <ul>
                        <li><strong>Report Type:</strong> {report_name}</li>
                        <li><strong>Period:</strong> {period.replace('_', ' ').title()}</li>
                        <li><strong>Generated:</strong> {current_date}</li>
                        <li><strong>Format:</strong> PDF</li>
                    </ul>
                </div>
                
                <p>This report contains:</p>
                <ul>
                    <li>Executive summary of security posture</li>
                    <li>Key performance indicators and metrics</li>
                    <li>Interactive data visualizations</li>
                    <li>AI-generated insights and analysis</li>
                    <li>Actionable recommendations</li>
                </ul>
                
                <p>The report has been automatically generated using our AI-powered security analytics platform, providing you with the most current and relevant security insights for informed decision-making.</p>
                
                <div class="highlight">
                    <p><strong>📋 Next Steps:</strong></p>
                    <ul>
                        <li>Review the executive summary for key findings</li>
                        <li>Examine the recommendations section for actionable items</li>
                        <li>Share relevant sections with your security team</li>
                        <li>Schedule follow-up discussions as needed</li>
                    </ul>
                </div>
                
                <p>If you have any questions about this report or need additional analysis, please don't hesitate to reach out to our security team.</p>
                
                <p>Best regards,<br>
                <strong>{company_name} Security Team</strong></p>
            </div>
            
            <div class="footer">
                <p><strong>Confidentiality Notice:</strong> This email and its attachments contain confidential and proprietary information. If you are not the intended recipient, please delete this email and notify the sender immediately.</p>
                
                <p><strong>Generated by:</strong> Gen AI Security Report Generator<br>
                <strong>Date:</strong> {current_date}</p>
            </div>
        </body>
        </html>
        """

        return html_body

    def _attach_pdf(self, msg: MIMEMultipart, pdf_path: str) -> None:
        """Attach PDF file to email message"""

        filename = os.path.basename(pdf_path)

        with open(pdf_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header("Content-Disposition", f"attachment; filename= {filename}")

        msg.attach(part)

    def send_notification(
        self,
        recipient_email: str,
        message: str,
        subject: str = "Security Report Notification",
    ) -> bool:
        """Send a simple notification email without attachments"""

        try:
            msg = MIMEMultipart()
            msg["From"] = self.config.EMAIL_ADDRESS
            msg["To"] = recipient_email
            msg["Subject"] = subject

            msg.attach(MIMEText(message, "plain"))

            server = smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT)
            server.starttls()
            server.login(self.config.EMAIL_ADDRESS, self.config.EMAIL_PASSWORD)

            text = msg.as_string()
            server.sendmail(self.config.EMAIL_ADDRESS, recipient_email, text)
            server.quit()

            return True

        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            return False

    def test_connection(self) -> bool:
        """Test SMTP connection and authentication"""

        try:
            server = smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT)
            server.starttls()
            server.login(self.config.EMAIL_ADDRESS, self.config.EMAIL_PASSWORD)
            server.quit()
            return True

        except Exception as e:
            print(f"Email connection test failed: {str(e)}")
            return False
