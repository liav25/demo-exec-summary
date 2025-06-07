from functools import lru_cache
from typing import Optional

# Lazy initialization functions to improve startup performance


@lru_cache(maxsize=1)
def get_ai_generator():
    """Get or create AI generator instance (lazy initialization)"""
    try:
        from app.utils.utils.ai_generator import AIGenerator

        return AIGenerator()
    except ValueError as e:
        print(f"Warning: AI Generator initialization failed: {e}")
        return None


@lru_cache(maxsize=1)
def get_email_sender():
    """Get or create email sender instance (lazy initialization)"""
    try:
        from app.utils.utils.email_sender import EmailSender

        return EmailSender()
    except ValueError as e:
        print(f"Warning: Email Sender initialization failed: {e}")
        return None


@lru_cache(maxsize=1)
def get_data_processor():
    """Get or create data processor instance (lazy initialization)"""
    from app.utils.utils.data_processor import DataProcessor

    return DataProcessor()


@lru_cache(maxsize=1)
def get_chart_generator():
    """Get or create chart generator instance (lazy initialization)"""
    from app.utils.utils.chart_generator import ChartGenerator

    return ChartGenerator()


@lru_cache(maxsize=1)
def get_pdf_generator():
    """Get or create PDF generator instance (lazy initialization)"""
    from app.utils.utils.pdf_generator import PDFGenerator

    return PDFGenerator()
