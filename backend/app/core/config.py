import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class AppConfig(BaseSettings):
    """Simple application configuration"""

    # Environment
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(False, env="DEBUG")
    flask_debug: Optional[bool] = Field(None, env="FLASK_DEBUG")  # Legacy Flask setting

    # App metadata
    app_name: str = Field("AI Security Analyst", env="APP_NAME")
    app_version: str = Field("1.0.0", env="APP_VERSION")
    company_name: str = Field("SecureCorp Inc.", env="COMPANY_NAME")
    company_logo: str = Field("static/images/logo.png", env="COMPANY_LOGO")

    # File paths
    data_dir: str = Field("data", env="DATA_DIR")
    templates_dir: str = Field("templates", env="TEMPLATES_DIR")
    static_dir: str = Field("static", env="STATIC_DIR")
    reports_dir: str = Field("generated_reports", env="REPORTS_DIR")

    # Database configuration
    database_url: Optional[str] = Field(None, env="DATABASE_URL")
    redis_url: Optional[str] = Field(None, env="REDIS_URL")

    # AI service configuration
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL")
    openai_max_tokens: int = Field(4000, env="OPENAI_MAX_TOKENS")
    openai_temperature: float = Field(0.7, env="OPENAI_TEMPERATURE")

    # Email service configuration
    smtp_server: str = Field("smtp.gmail.com", env="SMTP_SERVER")
    smtp_port: int = Field(587, env="SMTP_PORT")
    email_address: Optional[str] = Field(None, env="EMAIL_ADDRESS")
    email_password: Optional[str] = Field(None, env="EMAIL_PASSWORD")
    resend_api_key: Optional[str] = Field(None, env="RESEND_API_KEY")

    # Security configuration
    secret_key: str = Field("dev-secret-key-change-in-production", env="SECRET_KEY")
    cors_origins: List[str] = Field(
        ["http://localhost:3000", "http://localhost:5173"], env="CORS_ORIGINS"
    )
    rate_limit_per_minute: int = Field(60, env="RATE_LIMIT_PER_MINUTE")
    jwt_expiry_hours: int = Field(24, env="JWT_EXPIRY_HOURS")

    @field_validator("openai_api_key")
    @classmethod
    def validate_api_key(cls, v):
        if v and not v.startswith(("sk-", "sk-proj-")):
            raise ValueError("Invalid OpenAI API key format")
        return v

    @field_validator("smtp_port")
    @classmethod
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError("SMTP port must be between 1 and 65535")
        return v

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        return self.environment.lower() == "development"

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",  # Ignore extra fields from environment
    }


# Global configuration instance
config = AppConfig()

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
        "required_focus_areas": ["Network Security", "Endpoint Compliance"],
        "estimated_generation_time": 180,  # seconds
    },
    "monthly_threat": {
        "name": "Monthly Threat Overview",
        "description": "Monthly threat landscape and incident summary",
        "data_sources": ["security_events.csv", "phishing_data.csv"],
        "required_focus_areas": ["Phishing Statistics", "Malware Incidents"],
        "estimated_generation_time": 120,
    },
    "phishing_deep_dive": {
        "name": "Phishing Deep Dive",
        "description": "Detailed analysis of phishing attacks and trends",
        "data_sources": ["phishing_data.csv"],
        "required_focus_areas": ["Phishing Statistics", "Security Training"],
        "estimated_generation_time": 90,
    },
    "compliance_status": {
        "name": "Compliance Status Report",
        "description": "Current compliance posture and requirements status",
        "data_sources": ["compliance_data.csv"],
        "required_focus_areas": ["Endpoint Compliance", "Data Protection"],
        "estimated_generation_time": 100,
    },
    "incident_response": {
        "name": "Incident Response Summary",
        "description": "Summary of security incidents and response activities",
        "data_sources": ["security_events.csv"],
        "required_focus_areas": ["Network Security", "Access Management"],
        "estimated_generation_time": 110,
    },
}

# Focus areas configuration with metadata
FOCUS_AREAS = [
    {
        "id": "phishing_stats",
        "name": "Phishing Statistics",
        "description": "Email security and phishing attack metrics",
        "color": "#FF6B6B",
        "icon": "mail",
    },
    {
        "id": "malware_incidents",
        "name": "Malware Incidents",
        "description": "Malware detection and response metrics",
        "color": "#4ECDC4",
        "icon": "shield-alert",
    },
    {
        "id": "endpoint_compliance",
        "name": "Endpoint Compliance",
        "description": "Device compliance and policy adherence",
        "color": "#45B7D1",
        "icon": "monitor",
    },
    {
        "id": "network_security",
        "name": "Network Security",
        "description": "Network infrastructure security status",
        "color": "#96CEB4",
        "icon": "network",
    },
    {
        "id": "data_protection",
        "name": "Data Protection",
        "description": "Data security and privacy measures",
        "color": "#FECA57",
        "icon": "database",
    },
    {
        "id": "access_management",
        "name": "Access Management",
        "description": "Identity and access control systems",
        "color": "#FF9FF3",
        "icon": "key",
    },
    {
        "id": "vulnerability_management",
        "name": "Vulnerability Management",
        "description": "Vulnerability assessment and remediation",
        "color": "#54A0FF",
        "icon": "search",
    },
    {
        "id": "security_training",
        "name": "Security Training",
        "description": "Employee security awareness and training",
        "color": "#5F27CD",
        "icon": "graduation-cap",
    },
]
