import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class"""

    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

    # OpenAI settings
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    # Email settings
    SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

    RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

    # File paths
    DATA_DIR = "data"
    TEMPLATES_DIR = "templates"
    STATIC_DIR = "static"
    REPORTS_DIR = "generated_reports"

    # Report settings
    COMPANY_NAME = os.environ.get("COMPANY_NAME", "SecureCorp Inc.")
    COMPANY_LOGO = os.environ.get("COMPANY_LOGO", "static/images/logo.png")

    # Report types configuration
    REPORT_TYPES = {
        "quarterly_review": {
            "name": "Quarterly Security Review",
            "description": "Comprehensive quarterly security posture assessment",
            "data_sources": [
                "security_events.csv",
                "compliance_data.csv",
                "phishing_data.csv",
            ],
        },
        "monthly_threat": {
            "name": "Monthly Threat Overview",
            "description": "Monthly threat landscape and incident summary",
            "data_sources": ["security_events.csv", "phishing_data.csv"],
        },
        "phishing_deep_dive": {
            "name": "Phishing Deep Dive",
            "description": "Detailed analysis of phishing attacks and trends",
            "data_sources": ["phishing_data.csv"],
        },
        "compliance_status": {
            "name": "Compliance Status Report",
            "description": "Current compliance posture and requirements status",
            "data_sources": ["compliance_data.csv"],
        },
        "incident_response": {
            "name": "Incident Response Summary",
            "description": "Summary of security incidents and response activities",
            "data_sources": ["security_events.csv"],
        },
    }

    # Focus areas configuration
    FOCUS_AREAS = [
        "Phishing Statistics",
        "Malware Incidents",
        "Endpoint Compliance",
        "Network Security",
        "Data Protection",
        "Access Management",
        "Vulnerability Management",
        "Security Training",
    ]
