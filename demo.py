#!/usr/bin/env python3
"""
Demo Script for Gen AI Security Report Generator
This script generates sample reports for demonstration purposes without requiring email setup.
Perfect for hackathon demos and testing.
"""

import os
import sys
from datetime import datetime
from flask import Flask

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from utils.data_processor import DataProcessor
from utils.chart_generator import ChartGenerator
from utils.pdf_generator import PDFGenerator

# Import the report generation functions from app.py
from app import generate_report_data, render_report_html


def setup_demo_environment():
    """Set up minimal environment for demo"""
    # Set minimal config for demo
    os.environ["SECRET_KEY"] = "demo-secret-key"
    os.environ["FLASK_DEBUG"] = "false"
    os.environ["COMPANY_NAME"] = "DemoSecure Corp"

    # Create necessary directories
    os.makedirs("generated_reports", exist_ok=True)
    os.makedirs("static/images", exist_ok=True)


def generate_demo_report(
    report_type, time_period, focus_areas=None, output_dir="generated_reports"
):
    """Generate a demo report and save it as PDF"""

    if focus_areas is None:
        focus_areas = ["Phishing Statistics", "Malware Incidents", "Network Security"]

    print(f"🔄 Generating {report_type} report for {time_period}...")

    try:
        # Generate report data
        report_data = generate_report_data(
            report_type=report_type,
            time_period=time_period,
            focus_areas=focus_areas,
            specific_questions="Please focus on executive-level insights and actionable recommendations.",
        )

        # Create HTML content
        app = Flask(__name__)
        app.config.from_object(Config)

        with app.app_context():
            html_content = render_report_html(report_data)

        # Generate PDF
        pdf_generator = PDFGenerator()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"demo_{report_type}_{time_period}_{timestamp}.pdf"
        pdf_path = pdf_generator.generate_pdf(html_content, filename)

        print(f"✅ Report generated successfully: {pdf_path}")
        return pdf_path

    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def generate_all_demo_reports():
    """Generate all types of demo reports"""

    print("🎯 Gen AI Security Report Generator - Demo Mode")
    print("=" * 60)
    print("Generating sample reports for demonstration...\n")

    # Define demo scenarios
    demo_scenarios = [
        {
            "report_type": "quarterly_review",
            "time_period": "last_quarter",
            "focus_areas": [
                "Phishing Statistics",
                "Malware Incidents",
                "Compliance Status",
            ],
            "description": "Comprehensive quarterly security review",
        },
        {
            "report_type": "monthly_threat",
            "time_period": "last_month",
            "focus_areas": ["Network Security", "Endpoint Compliance"],
            "description": "Monthly threat landscape overview",
        },
        {
            "report_type": "phishing_deep_dive",
            "time_period": "last_6_months",
            "focus_areas": ["Phishing Statistics", "Security Training"],
            "description": "Deep dive into phishing attack trends",
        },
        {
            "report_type": "compliance_status",
            "time_period": "year_to_date",
            "focus_areas": ["Compliance Status", "Data Protection"],
            "description": "Current compliance posture assessment",
        },
    ]

    generated_reports = []

    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"📊 Demo {i}/4: {scenario['description']}")

        pdf_path = generate_demo_report(
            report_type=scenario["report_type"],
            time_period=scenario["time_period"],
            focus_areas=scenario["focus_areas"],
        )

        if pdf_path:
            generated_reports.append(pdf_path)

        print()  # Add spacing between reports

    # Summary
    print("📋 Demo Summary:")
    print("=" * 40)
    print(f"✅ Successfully generated {len(generated_reports)} demo reports")

    if generated_reports:
        print("\n📁 Generated files:")
        for report in generated_reports:
            print(f"   • {report}")

        print(f"\n📂 All reports saved in: {os.path.abspath('generated_reports')}")
        print("\n💡 Demo Tips:")
        print("   • Open the PDF files to see the generated reports")
        print("   • Each report contains AI-generated insights and visualizations")
        print("   • Reports include executive summaries, KPIs, and recommendations")
        print("   • Charts are embedded as images in the PDF")

    return generated_reports


def interactive_demo():
    """Interactive demo mode for custom report generation"""

    print("🎯 Interactive Demo Mode")
    print("=" * 30)

    # Get user preferences
    print("\nAvailable report types:")
    report_types = {
        "1": "quarterly_review",
        "2": "monthly_threat",
        "3": "phishing_deep_dive",
        "4": "compliance_status",
        "5": "incident_response",
    }

    for key, value in report_types.items():
        print(f"   {key}. {value.replace('_', ' ').title()}")

    choice = input("\nSelect report type (1-5): ").strip()
    report_type = report_types.get(choice, "quarterly_review")

    print("\nAvailable time periods:")
    time_periods = {
        "1": "last_month",
        "2": "last_quarter",
        "3": "last_6_months",
        "4": "year_to_date",
    }

    for key, value in time_periods.items():
        print(f"   {key}. {value.replace('_', ' ').title()}")

    choice = input("\nSelect time period (1-4): ").strip()
    time_period = time_periods.get(choice, "last_quarter")

    # Generate the custom report
    print(f"\n🔄 Generating custom {report_type} report...")
    pdf_path = generate_demo_report(report_type, time_period)

    if pdf_path:
        print(f"\n✅ Custom report generated: {pdf_path}")
    else:
        print("\n❌ Failed to generate custom report")


def main():
    """Main demo function"""

    # Setup demo environment
    setup_demo_environment()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive":
            interactive_demo()
        elif sys.argv[1] == "--help":
            print("Gen AI Security Report Generator - Demo Script")
            print("\nUsage:")
            print("  python demo.py                 # Generate all demo reports")
            print("  python demo.py --interactive   # Interactive demo mode")
            print("  python demo.py --help          # Show this help")
        else:
            print("Unknown option. Use --help for usage information.")
    else:
        # Generate all demo reports
        generate_all_demo_reports()


if __name__ == "__main__":
    main()
