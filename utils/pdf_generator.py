import weasyprint
import os
from datetime import datetime
from typing import Optional
from config import Config


class PDFGenerator:
    """Handles PDF generation from HTML content using WeasyPrint"""

    def __init__(self):
        self.config = Config()

    def generate_pdf(self, html_content: str, filename: Optional[str] = None) -> str:
        """Generate PDF from HTML content and return the file path"""

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_report_{timestamp}.pdf"

        # Ensure filename has .pdf extension
        if not filename.endswith(".pdf"):
            filename += ".pdf"

        # Create output directory if it doesn't exist
        output_dir = self.config.REPORTS_DIR
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, filename)

        try:
            # Configure WeasyPrint with custom CSS for better PDF rendering
            css_string = self._get_pdf_css()

            # Create WeasyPrint HTML document
            html_doc = weasyprint.HTML(string=html_content, base_url=".")
            css_doc = weasyprint.CSS(string=css_string)

            # Generate PDF with optimized settings
            html_doc.write_pdf(output_path, stylesheets=[css_doc], optimize_images=True)

            return output_path

        except Exception as e:
            raise Exception(f"Error generating PDF: {str(e)}")

    def _get_pdf_css(self) -> str:
        """Get CSS optimized for PDF generation"""
        return """
        @page {
            size: A4;
            margin: 1in;
            @top-center {
                content: "Security Report - " attr(data-report-title);
                font-size: 10pt;
                color: #666;
            }
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 10pt;
                color: #666;
            }
        }
        
        body {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #333;
            margin: 0;
            padding: 0;
        }
        
        .header {
            border-bottom: 2px solid #0080ff;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .logo {
            max-height: 60px;
            max-width: 200px;
        }
        
        h1 {
            color: #0080ff;
            font-size: 24pt;
            margin: 20px 0 10px 0;
            page-break-after: avoid;
        }
        
        h2 {
            color: #0a0a0a;
            font-size: 18pt;
            margin: 25px 0 15px 0;
            page-break-after: avoid;
            border-bottom: 1px solid #0080ff;
            padding-bottom: 5px;
        }
        
        h3 {
            color: #0a0a0a;
            font-size: 14pt;
            margin: 20px 0 10px 0;
            page-break-after: avoid;
        }
        
        .executive-summary {
            background-color: rgba(0, 128, 255, 0.05);
            padding: 20px;
            border-left: 4px solid #0080ff;
            margin: 20px 0;
            page-break-inside: avoid;
        }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .kpi-card {
            background: #fff;
            border: 1px solid #0080ff;
            border-radius: 5px;
            padding: 15px;
            text-align: center;
            page-break-inside: avoid;
        }
        
        .kpi-value {
            font-size: 24pt;
            font-weight: bold;
            color: #0080ff;
            margin: 5px 0;
        }
        
        .kpi-label {
            font-size: 10pt;
            color: #0a0a0a;
            text-transform: uppercase;
        }
        
        .chart-container {
            margin: 20px 0;
            page-break-inside: avoid;
            text-align: center;
            min-height: 300px; /* Ensure space for charts */
        }
        
        .chart-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #0a0a0a;
        }
        
        .chart-explanation {
            margin-top: 10px;
            font-style: italic;
            color: #666;
            font-size: 10pt;
        }
        
        .findings-list {
            background-color: rgba(57, 255, 20, 0.08);
            border: 1px solid #39ff14;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }
        
        .findings-list ul {
            margin: 0;
            padding-left: 20px;
        }
        
        .findings-list li {
            margin: 8px 0;
        }
        
        .recommendations {
            background-color: rgba(0, 128, 255, 0.08);
            border: 1px solid #0080ff;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }
        
        .recommendations ul {
            margin: 0;
            padding-left: 20px;
        }
        
        .recommendations li {
            margin: 8px 0;
        }
        
        .metadata {
            font-size: 9pt;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 15px;
            margin-top: 30px;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        /* Enhanced chart support - ensure Plotly charts render properly */
        .plotly-graph-div {
            page-break-inside: avoid;
            margin: 15px 0;
            min-height: 300px;
            width: 100% !important;
        }
        
        /* Plotly specific styles for PDF */
        .js-plotly-plot .plotly .main-svg {
            background: white !important;
        }
        
        .modebar {
            display: none !important; /* Hide interactive toolbar in PDF */
        }
        
        /* Fallback styles if charts don't render */
        .plotly-notifier {
            display: none;
        }
        
        /* SVG chart styling */
        svg {
            max-width: 100%;
            height: auto;
            background: white;
        }
        
        /* Table styling */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        th {
            background-color: #f8f9fa;
            font-weight: bold;
            color: #0a0a0a;
        }
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        /* Status indicators */
        .status-critical {
            color: #ff4444;
            font-weight: bold;
        }
        
        .status-high {
            color: #0080ff;
            font-weight: bold;
        }
        
        .status-medium {
            color: #39ff14;
        }
        
        .status-low {
            color: #0a0a0a;
        }
        
        .status-resolved {
            color: #39ff14;
            font-weight: bold;
        }
        
        .status-investigating {
            color: #0080ff;
            font-weight: bold;
        }
        """

    def add_watermark(self, pdf_path: str, watermark_text: str = "CONFIDENTIAL") -> str:
        """Add watermark to existing PDF (placeholder for future enhancement)"""
        # This would require additional libraries like PyPDF2 or reportlab
        # For now, we'll return the original path
        return pdf_path

    def optimize_pdf(self, pdf_path: str) -> str:
        """Optimize PDF size (placeholder for future enhancement)"""
        # This could use libraries like PyPDF2 to compress the PDF
        # For now, we'll return the original path
        return pdf_path
