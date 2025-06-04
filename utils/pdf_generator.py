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
        """Get CSS optimized for PDF generation with beautiful, soft color palette"""
        return """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Serif+Pro:wght@400;600&display=swap');
        
        @page {
            size: A4;
            margin: 0.8in;
            @top-center {
                content: "Security Report - " attr(data-report-title);
                font-size: 10pt;
                color: #7E909A;
                font-family: 'Inter', sans-serif;
            }
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 10pt;
                color: #7E909A;
                font-family: 'Inter', sans-serif;
            }
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #202020;
            margin: 0;
            padding: 0;
            font-weight: 400;
        }
        
        .header {
            background: linear-gradient(135deg, #A5D8DD 0%, #4CB5F5 100%);
            color: #FFFFFF;
            padding: 40px 30px;
            margin: -20px -20px 40px -20px;
            border-radius: 0 0 20px 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(165, 216, 221, 0.3);
        }
        
        .company-name {
            font-family: 'Source Serif Pro', serif;
            font-size: 28pt;
            font-weight: 600;
            margin: 0 0 10px 0;
            letter-spacing: -0.5px;
        }
        
        .report-title {
            font-size: 24pt;
            font-weight: 500;
            margin: 15px 0;
            opacity: 0.95;
        }
        
        .report-subtitle {
            font-size: 14pt;
            font-weight: 300;
            margin-bottom: 15px;
            opacity: 0.9;
        }
        
        .metadata {
            font-size: 11pt;
            font-weight: 300;
            opacity: 0.85;
        }
        
        h1 {
            font-family: 'Source Serif Pro', serif;
            color: #23282D;
            font-size: 22pt;
            font-weight: 600;
            margin: 40px 0 20px 0;
            page-break-after: avoid;
            letter-spacing: -0.3px;
            line-height: 1.2;
        }
        
        h2 {
            color: #484848;
            font-size: 18pt;
            font-weight: 500;
            margin: 30px 0 15px 0;
            page-break-after: avoid;
            border-bottom: 2px solid #CED2CC;
            padding-bottom: 8px;
            letter-spacing: -0.2px;
        }
        
        h3 {
            color: #484848;
            font-size: 15pt;
            font-weight: 500;
            margin: 25px 0 12px 0;
            page-break-after: avoid;
        }
        
        .executive-summary {
            background: linear-gradient(135deg, #F1F1F1 0%, #DADADA 100%);
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
            page-break-inside: avoid;
            border-left: 6px solid #DBAE58;
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
            background: linear-gradient(135deg, #FFFFFF 0%, #F1F1F1 100%);
            border: 1px solid #CED2CC;
            border-radius: 12px;
            padding: 25px 20px;
            text-align: center;
            page-break-inside: avoid;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
        }
        
        .kpi-value {
            font-family: 'Source Serif Pro', serif;
            font-size: 28pt;
            font-weight: 600;
            color: #1C4E80;
            margin: 8px 0 12px 0;
            line-height: 1;
        }
        
        .kpi-label {
            font-size: 11pt;
            color: #7E909A;
            text-transform: uppercase;
            font-weight: 500;
            letter-spacing: 0.5px;
        }
        
        .chart-container {
            margin: 35px 0;
            page-break-inside: avoid;
            text-align: center;
            background: #FFFFFF;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.06);
        }
        
        .chart-title {
            font-family: 'Source Serif Pro', serif;
            font-weight: 600;
            margin-bottom: 20px;
            color: #23282D;
            font-size: 16pt;
        }
        
        .chart-explanation {
            margin-top: 20px;
            font-style: italic;
            color: #7E909A;
            font-size: 10pt;
            text-align: left;
            padding: 15px 20px;
            background: linear-gradient(135deg, #A5D8DD 0%, rgba(165, 216, 221, 0.1) 100%);
            border-radius: 8px;
            border-left: 3px solid #4CB5F5;
        }
        
        .findings-list {
            background: linear-gradient(135deg, #6AB187 0%, rgba(106, 177, 135, 0.1) 100%);
            border: 1px solid #6AB187;
            border-radius: 12px;
            padding: 25px;
            margin: 25px 0;
            border-left: 6px solid #6AB187;
        }
        
        .findings-list h3 {
            color: #488A99;
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
            background: linear-gradient(135deg, #DBAE58 0%, rgba(219, 174, 88, 0.1) 100%);
            border: 1px solid #DBAE58;
            border-radius: 12px;
            padding: 25px;
            margin: 25px 0;
            border-left: 6px solid #DBAE58;
        }
        
        .recommendations h3 {
            color: #AC3E31;
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
            color: #7E909A;
            border-top: 2px solid #CED2CC;
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
            background: white !important;
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
            background: white;
            border-radius: 8px;
        }
        
        /* Beautiful table styling */
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 25px 0;
            font-size: 10pt;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        }
        
        th {
            background: linear-gradient(135deg, #23282D 0%, #484848 100%);
            color: white;
            font-weight: 600;
            padding: 15px 12px;
            text-align: left;
            font-size: 11pt;
        }
        
        td {
            padding: 12px;
            border-bottom: 1px solid #CED2CC;
        }
        
        tr:nth-child(even) td {
            background-color: #F1F1F1;
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        /* Enhanced status indicators with soft colors */
        .status-critical {
            color: #AC3E31;
            font-weight: 600;
            background: rgba(172, 62, 49, 0.1);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        .status-high {
            color: #1C4E80;
            font-weight: 600;
            background: rgba(28, 78, 128, 0.1);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        .status-medium {
            color: #6AB187;
            font-weight: 500;
            background: rgba(106, 177, 135, 0.1);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        .status-low {
            color: #7E909A;
            font-weight: 500;
            background: rgba(126, 144, 154, 0.1);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        .status-resolved {
            color: #6AB187;
            font-weight: 600;
            background: rgba(106, 177, 135, 0.15);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        .status-investigating {
            color: #DBAE58;
            font-weight: 600;
            background: rgba(219, 174, 88, 0.15);
            padding: 4px 8px;
            border-radius: 6px;
        }
        
        /* Soft accent elements */
        .accent-box {
            background: linear-gradient(135deg, #4CB5F5 0%, rgba(76, 181, 245, 0.1) 100%);
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #4CB5F5;
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
