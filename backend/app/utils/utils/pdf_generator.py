from weasyprint import HTML, CSS
import os
from datetime import datetime
from typing import Optional
from app.core.config import config


class PDFGenerator:
    """Handles PDF generation from HTML content using WeasyPrint"""

    def __init__(self):
        self.config = config
        # Ensure reports directory exists
        self.reports_dir = config.reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_pdf(self, html_content: str, filename: Optional[str] = None) -> str:
        """Generate PDF from HTML content and return the file path"""

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_report_{timestamp}.pdf"

        # Ensure filename has .pdf extension
        if not filename.endswith(".pdf"):
            filename += ".pdf"

        # Create output directory if it doesn't exist
        output_dir = self.reports_dir
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, filename)

        try:
            # Configure WeasyPrint with custom CSS for better PDF rendering
            css_string = self._get_pdf_css()

            # Create WeasyPrint HTML document
            html_doc = HTML(string=html_content, base_url=".")
            css_doc = CSS(string=css_string)

            # Generate PDF with optimized settings
            html_doc.write_pdf(output_path, stylesheets=[css_doc])

            return output_path

        except Exception as e:
            raise Exception(f"Error generating PDF: {str(e)}")

    def _get_pdf_css(self) -> str:
        """Get CSS optimized for PDF generation with web form color palette"""
        return """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* CSS Variables matching web form */
        :root {
            --rich-black: #0D1117;
            --white: #FFFFFF;
            --electric-blue: #0066CC;
            --cyber-green: #00FF41;
            --glass-bg: rgba(13, 17, 23, 0.05);
            --glass-border: rgba(13, 17, 23, 0.1);
            --error-red: #dc3545;
            --warning-orange: #fd7e14;
            --success-green: #28a745;
        }
        
        @page {
            size: A4;
            margin: 0.8in;
            @top-center {
                content: "Security Report - " attr(data-report-title);
                font-size: 10pt;
                color: var(--rich-black);
                opacity: 0.7;
                font-family: 'Inter', sans-serif;
            }
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 10pt;
                color: var(--rich-black);
                opacity: 0.7;
                font-family: 'Inter', sans-serif;
            }
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: var(--rich-black);
            background: var(--white);
            margin: 0;
            padding: 0;
            font-weight: 400;
        }
        
        .header {
            background: linear-gradient(135deg, var(--electric-blue) 0%, var(--cyber-green) 100%);
            color: var(--white);
            padding: 40px 30px;
            margin: -20px -20px 40px -20px;
            border-radius: 0 0 20px 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 102, 204, 0.3);
        }
        
        .company-name {
            font-family: 'Inter', sans-serif;
            font-size: 28pt;
            font-weight: 700;
            margin: 0 0 10px 0;
            letter-spacing: -0.5px;
        }
        
        .report-title {
            font-size: 24pt;
            font-weight: 600;
            margin: 15px 0;
            opacity: 0.95;
        }
        
        .report-subtitle {
            font-size: 14pt;
            font-weight: 400;
            margin-bottom: 15px;
            opacity: 0.9;
        }
        
        .metadata {
            font-size: 11pt;
            font-weight: 300;
            opacity: 0.85;
        }
        
        h1 {
            font-family: 'Inter', sans-serif;
            color: var(--rich-black);
            font-size: 22pt;
            font-weight: 700;
            margin: 40px 0 20px 0;
            page-break-after: avoid;
            letter-spacing: -0.3px;
            line-height: 1.2;
        }
        
        h2 {
            color: var(--rich-black);
            font-size: 18pt;
            font-weight: 600;
            margin: 30px 0 15px 0;
            page-break-after: avoid;
            border-bottom: 2px solid var(--electric-blue);
            padding-bottom: 8px;
            letter-spacing: -0.2px;
        }
        
        h3 {
            color: var(--rich-black);
            font-size: 15pt;
            font-weight: 500;
            margin: 25px 0 12px 0;
            page-break-after: avoid;
        }
        
        .executive-summary {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
            page-break-inside: avoid;
            border-left: 6px solid var(--electric-blue);
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
            position: relative;
        }
        
        .executive-summary::before {
            content: "📊";
            position: absolute;
            top: 15px;
            right: 20px;
            font-size: 24pt;
            opacity: 0.6;
        }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .kpi-card {
            background: var(--white);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 25px 20px;
            text-align: center;
            page-break-inside: avoid;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
        }
        
        .kpi-value {
            font-family: 'Inter', sans-serif;
            font-size: 28pt;
            font-weight: 700;
            color: var(--electric-blue);
            margin: 8px 0 12px 0;
            line-height: 1;
        }
        
        .kpi-label {
            font-size: 11pt;
            color: var(--rich-black);
            text-transform: uppercase;
            font-weight: 500;
            letter-spacing: 0.5px;
            opacity: 0.7;
        }
        
        .chart-container {
            margin: 35px 0;
            page-break-inside: avoid;
            text-align: center;
            background: var(--white);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.06);
        }
        
        .chart-title {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--rich-black);
            font-size: 16pt;
        }
        
        .chart-explanation {
            margin-top: 20px;
            font-style: italic;
            color: var(--rich-black);
            opacity: 0.7;
            font-size: 10pt;
            text-align: left;
            padding: 15px 20px;
            background: var(--glass-bg);
            border-radius: 8px;
            border-left: 3px solid var(--electric-blue);
        }
        
        .findings-list {
            background: rgba(0, 255, 65, 0.1);
            border: 1px solid var(--cyber-green);
            border-radius: 12px;
            padding: 25px;
            margin: 25px 0;
            border-left: 6px solid var(--cyber-green);
        }
        
        .findings-list h3 {
            color: var(--rich-black);
            margin-top: 0;
            font-weight: 600;
        }
        
        .findings-list ul {
            margin: 15px 0 0 0;
            padding-left: 25px;
        }
        
        .findings-list li {
            margin: 12px 0;
            line-height: 1.5;
        }
        
        .recommendations {
            background: rgba(0, 102, 204, 0.1);
            border: 1px solid var(--electric-blue);
            border-radius: 12px;
            padding: 25px;
            margin: 25px 0;
            border-left: 6px solid var(--electric-blue);
        }
        
        .recommendations h3 {
            color: var(--rich-black);
            margin-top: 0;
            font-weight: 600;
        }
        
        .recommendations ul {
            margin: 15px 0 0 0;
            padding-left: 25px;
        }
        
        .recommendations li {
            margin: 12px 0;
            line-height: 1.5;
        }
        
        .section {
            margin: 40px 0;
            page-break-inside: avoid;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        .footer-metadata {
            font-size: 9pt;
            color: var(--rich-black);
            opacity: 0.7;
            border-top: 2px solid var(--glass-border);
            padding-top: 20px;
            margin-top: 50px;
            text-align: center;
            font-style: italic;
        }
        
        /* Enhanced chart support */
        .plotly-graph-div {
            page-break-inside: avoid;
            margin: 20px 0;
            min-height: 350px;
            width: 100% !important;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .js-plotly-plot .plotly .main-svg {
            background: var(--white) !important;
            border-radius: 8px;
        }
        
        .modebar {
            display: none !important;
        }
        
        .plotly-notifier {
            display: none;
        }
        
        svg {
            max-width: 100%;
            height: auto;
            background: var(--white);
            border-radius: 8px;
        }
        
        /* Beautiful table styling */
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 25px 0;
            font-size: 10pt;
            background: var(--white);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
            border: 1px solid var(--glass-border);
        }
        
        th {
            background: linear-gradient(135deg, var(--rich-black) 0%, var(--electric-blue) 100%);
            color: var(--white);
            font-weight: 600;
            padding: 15px 12px;
            text-align: left;
            font-size: 11pt;
        }
        
        td {
            padding: 12px;
            border-bottom: 1px solid var(--glass-border);
        }
        
        tr:nth-child(even) td {
            background-color: var(--glass-bg);
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        /* Enhanced status indicators with web form colors */
        .status-critical {
            color: var(--error-red);
            font-weight: 600;
            background: rgba(220, 53, 69, 0.1);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        .status-high {
            color: var(--electric-blue);
            font-weight: 600;
            background: rgba(0, 102, 204, 0.1);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        .status-medium {
            color: var(--warning-orange);
            font-weight: 500;
            background: rgba(253, 126, 20, 0.1);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        .status-low {
            color: var(--rich-black);
            font-weight: 500;
            background: var(--glass-bg);
            padding: 4px 8px;
            border-radius: 6px;
            opacity: 0.7;
        }
        
        .status-resolved {
            color: var(--success-green);
            font-weight: 600;
            background: rgba(40, 167, 69, 0.1);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        .status-investigating {
            color: var(--cyber-green);
            font-weight: 600;
            background: rgba(0, 255, 65, 0.1);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        /* Soft accent elements */
        .accent-box {
            background: rgba(0, 102, 204, 0.1);
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid var(--electric-blue);
        }
        
        /* Enhanced readability */
        p {
            margin: 15px 0;
            line-height: 1.6;
        }
        
        ul, ol {
            margin: 15px 0;
            padding-left: 25px;
        }
        
        li {
            margin: 8px 0;
            line-height: 1.5;
        }
        
        /* Print optimization */
        @media print {
            .header {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            
            .executive-summary,
            .kpi-card,
            .chart-container,
            .findings-list,
            .recommendations {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
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
