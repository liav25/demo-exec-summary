#!/usr/bin/env python3
"""
Test script to generate a PDF report with all areas of focus, YTD time frame, and quarterly report type
"""

import sys
import os
import asyncio
from datetime import datetime

# Get the directory where this script is located (backend directory)
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Change working directory to backend directory
os.chdir(BACKEND_DIR)
print(f"📁 Changed working directory to: {os.getcwd()}")

# Add the backend directory to the Python path
sys.path.insert(0, BACKEND_DIR)

from app.services import report_service
from app.utils.utils.pdf_generator import PDFGenerator
from app.core.config import config, FOCUS_AREAS


def test_generate_comprehensive_pdf():
    """Generate a comprehensive PDF report with all options selected"""

    print("🚀 Starting comprehensive PDF report generation test...")
    print("=" * 60)

    # Prepare test parameters
    report_type = "quarterly_review"
    time_period = "ytd"

    # Get all focus areas
    all_focus_areas = [area["name"] for area in FOCUS_AREAS]

    specific_questions = """
    Please provide comprehensive analysis covering:
    1. Overall security posture assessment
    2. Critical vulnerabilities and remediation progress
    3. Compliance status across all frameworks
    4. Employee security awareness metrics
    5. Incident response effectiveness
    6. Strategic recommendations for improvement
    """

    print(f"📋 Report Configuration:")
    print(f"   - Report Type: Quarterly Security Review")
    print(f"   - Time Period: Year to Date (YTD)")
    print(f"   - Focus Areas: All {len(all_focus_areas)} areas")
    for area in all_focus_areas:
        print(f"     • {area}")
    print(f"   - Specific Questions: Yes (comprehensive analysis)")
    print()

    try:
        # Generate report data
        print("📊 Generating report data...")
        report_data = report_service.generate_report_data(
            report_type=report_type,
            time_period=time_period,
            focus_areas=all_focus_areas,
            specific_questions=specific_questions,
        )
        print("✅ Report data generated successfully")

        # Create HTML report
        print("\n📝 Rendering HTML report...")
        html_content = report_service.render_report_html(report_data)
        print("✅ HTML report rendered successfully")

        # Generate PDF
        print("\n📄 Generating PDF...")
        pdf_generator = PDFGenerator()

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"TEST_comprehensive_{report_type}_{time_period}_{timestamp}.pdf"

        pdf_path = pdf_generator.generate_pdf(html_content, filename)
        print(f"✅ PDF generated successfully: {pdf_path}")

        # Display report summary
        print("\n📊 Report Summary:")
        print(
            f"   - Total Security Events: {report_data['metrics']['security_metrics'].get('total_events', 0)}"
        )
        print(
            f"   - Critical Events: {report_data['metrics']['security_metrics'].get('critical_events', 0)}"
        )
        print(
            f"   - Resolution Rate: {report_data['metrics']['security_metrics'].get('resolution_rate', 0):.1f}%"
        )
        print(
            f"   - Phishing Campaigns: {report_data['metrics']['phishing_metrics'].get('total_campaigns', 0)}"
        )
        print(
            f"   - Compliance Rate: {report_data['metrics']['compliance_metrics'].get('compliance_rate', 0):.1f}%"
        )

        # Display AI content preview
        print("\n🤖 AI-Generated Content Preview:")
        exec_summary = report_data.get("ai_content", {}).get(
            "executive_summary", "No summary available"
        )
        print(f"   Executive Summary (first 200 chars):")
        print(
            f"   {exec_summary[:200]}..."
            if len(exec_summary) > 200
            else f"   {exec_summary}"
        )

        print("\n" + "=" * 60)
        print(f"✅ Test completed successfully!")
        print(f"📁 PDF saved to: {pdf_path}")
        print(f"💡 You can find the report in the '{config.reports_dir}' directory")

        # Return the path for verification
        return pdf_path

    except Exception as e:
        print(f"\n❌ Error generating report: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def test_generate_minimal_pdf():
    """Generate a minimal PDF report for comparison"""

    print("\n\n🚀 Starting minimal PDF report generation test...")
    print("=" * 60)

    # Prepare minimal test parameters
    report_type = "quarterly_review"
    time_period = "last_week"
    focus_areas = ["Network Security", "Phishing Statistics"]  # Just 2 areas
    specific_questions = "What are the top 3 security concerns?"

    print(f"📋 Minimal Report Configuration:")
    print(f"   - Report Type: Quarterly Security Review")
    print(f"   - Time Period: Last Week")
    print(f"   - Focus Areas: {len(focus_areas)} areas")
    for area in focus_areas:
        print(f"     • {area}")
    print(f"   - Specific Questions: {specific_questions}")
    print()

    try:
        # Generate report data
        print("📊 Generating minimal report data...")
        report_data = report_service.generate_report_data(
            report_type=report_type,
            time_period=time_period,
            focus_areas=focus_areas,
            specific_questions=specific_questions,
        )

        # Create HTML report
        html_content = report_service.render_report_html(report_data)

        # Generate PDF
        pdf_generator = PDFGenerator()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"TEST_minimal_{report_type}_{time_period}_{timestamp}.pdf"

        pdf_path = pdf_generator.generate_pdf(html_content, filename)
        print(f"✅ Minimal PDF generated: {pdf_path}")

        return pdf_path

    except Exception as e:
        print(f"\n❌ Error generating minimal report: {str(e)}")
        return None


if __name__ == "__main__":
    print("🧪 PDF Generation Test Suite")
    print("============================\n")

    # Test 1: Comprehensive report with all options
    comprehensive_pdf = test_generate_comprehensive_pdf()

    # Test 2: Minimal report for comparison
    minimal_pdf = test_generate_minimal_pdf()

    # Summary
    print("\n\n📋 Test Summary:")
    print("=" * 60)
    if comprehensive_pdf:
        print(f"✅ Comprehensive Report: {os.path.basename(comprehensive_pdf)}")
        print(f"   Size: {os.path.getsize(comprehensive_pdf) / 1024:.1f} KB")
    else:
        print("❌ Comprehensive Report: Failed")

    if minimal_pdf:
        print(f"✅ Minimal Report: {os.path.basename(minimal_pdf)}")
        print(f"   Size: {os.path.getsize(minimal_pdf) / 1024:.1f} KB")
    else:
        print("❌ Minimal Report: Failed")

    print("\n✨ Test suite completed!")
