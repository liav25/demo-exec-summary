from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from datetime import datetime
import os
import traceback
from typing import Dict, List

# Import our custom modules
from config import Config
from utils.data_processor import DataProcessor
from utils.ai_generator import AIGenerator
from utils.chart_generator import ChartGenerator
from utils.pdf_generator import PDFGenerator
from utils.email_sender import EmailSender

app = Flask(__name__)
app.config.from_object(Config)

# Initialize components
data_processor = DataProcessor()
chart_generator = ChartGenerator()
pdf_generator = PDFGenerator()

# Initialize AI generator and email sender with error handling
try:
    ai_generator = AIGenerator()
except ValueError as e:
    print(f"Warning: AI Generator initialization failed: {e}")
    ai_generator = None

try:
    email_sender = EmailSender()
except ValueError as e:
    print(f"Warning: Email Sender initialization failed: {e}")
    email_sender = None


@app.route("/")
def index():
    """Main page with report request form"""
    return render_template("index.html")


@app.route("/generate_report", methods=["POST"])
def generate_report():
    """Generate and send security report based on form data"""
    try:
        # Extract form data
        recipient_email = request.form.get("recipient_email")
        report_type = request.form.get("report_type")
        time_period = request.form.get("time_period")
        focus_areas = request.form.getlist("focus_areas")
        specific_questions = request.form.get("specific_questions", "")

        # Validate required fields
        if not all([recipient_email, report_type, time_period]):
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("index"))

        # Generate the report
        report_data = generate_report_data(
            report_type, time_period, focus_areas, specific_questions
        )

        # Create HTML report
        html_content = render_report_html(report_data)

        # Generate PDF
        pdf_path = pdf_generator.generate_pdf(
            html_content,
            f"{report_type}_{time_period}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        )

        # Send email
        if email_sender:
            success = email_sender.send_report(
                recipient_email=recipient_email,
                pdf_path=pdf_path,
                report_type=report_type,
                period=time_period,
            )

            if success:
                flash(
                    f"Report successfully generated and sent to {recipient_email}!",
                    "success",
                )
            else:
                flash(
                    "Report generated but email delivery failed. Please check email configuration.",
                    "warning",
                )
        else:
            flash(
                "Report generated successfully, but email functionality is not configured.",
                "info",
            )

        return redirect(url_for("index"))

    except Exception as e:
        print(f"Error generating report: {str(e)}")
        print(traceback.format_exc())
        flash(f"Error generating report: {str(e)}", "error")
        return redirect(url_for("index"))


def generate_report_data(
    report_type: str, time_period: str, focus_areas: List[str], specific_questions: str
) -> Dict:
    """Generate all data needed for the report"""

    # Load and process data
    events_df = data_processor.get_security_events_data(
        report_type, time_period, focus_areas
    )
    phishing_df = data_processor.get_phishing_data(time_period)
    compliance_df = data_processor.get_compliance_data(time_period)

    # Calculate metrics
    security_metrics = data_processor.calculate_security_metrics(events_df)
    phishing_metrics = data_processor.calculate_phishing_metrics(phishing_df)
    compliance_metrics = data_processor.calculate_compliance_metrics(compliance_df)

    # Combine all metrics
    all_metrics = {
        "security_metrics": security_metrics,
        "phishing_metrics": phishing_metrics,
        "compliance_metrics": compliance_metrics,
    }

    # Generate AI content
    ai_content = generate_ai_content(
        report_type, time_period, all_metrics, focus_areas, specific_questions
    )

    # Generate charts optimized for PDF
    charts = generate_charts(
        events_df, phishing_df, compliance_df, all_metrics, report_type, for_pdf=True
    )

    # Prepare KPI data
    kpi_data = prepare_kpi_data(all_metrics)

    # Get report configuration
    report_config = Config.REPORT_TYPES.get(report_type, {})

    return {
        "report_title": report_config.get(
            "name", report_type.replace("_", " ").title()
        ),
        "report_type": report_type,
        "time_period": time_period,
        "period_description": time_period.replace("_", " ").title(),
        "company_name": Config.COMPANY_NAME,
        "generation_date": datetime.now().strftime("%B %d, %Y"),
        "report_period": f"{time_period.replace('_', ' ').title()}",
        "focus_areas": focus_areas,
        "specific_questions": specific_questions,
        "metrics": all_metrics,
        "ai_content": ai_content,
        "charts": charts,
        "kpi_data": kpi_data,
        "events_data": events_df,
        "phishing_data": phishing_df,
        "compliance_data": compliance_df,
    }


def generate_ai_content(
    report_type: str,
    time_period: str,
    metrics: Dict,
    focus_areas: List[str],
    specific_questions: str,
) -> Dict:
    """Generate AI-powered content for the report"""

    if not ai_generator:
        return {
            "executive_summary": "AI content generation is not available. Please configure OpenAI API key.",
            "key_findings": ["AI analysis not available"],
            "recommendations": [
                "Please configure AI integration for detailed recommendations"
            ],
        }

    try:
        # Generate executive summary
        executive_summary = ai_generator.generate_executive_summary(
            report_type=report_type,
            period=time_period,
            metrics=metrics,
            focus_areas=focus_areas,
        )

        # Generate key findings
        key_findings = ai_generator.generate_key_findings(metrics, report_type)

        # Generate recommendations
        recommendations = ai_generator.generate_recommendations(metrics, focus_areas)

        return {
            "executive_summary": executive_summary,
            "key_findings": key_findings,
            "recommendations": recommendations,
        }

    except Exception as e:
        print(f"Error generating AI content: {str(e)}")
        return {
            "executive_summary": f"Error generating AI summary: {str(e)}",
            "key_findings": ["AI analysis temporarily unavailable"],
            "recommendations": ["Please try again later"],
        }


def generate_charts(
    events_df,
    phishing_df,
    compliance_df,
    metrics: Dict,
    report_type: str,
    for_pdf: bool = True,
) -> List[Dict]:
    """Generate all charts for the report"""

    charts = []

    try:
        # Pass the for_pdf parameter to chart generator
        if hasattr(chart_generator, "set_pdf_mode"):
            chart_generator.set_pdf_mode(for_pdf)

        # Security events overview
        if not events_df.empty:
            charts.append(
                {
                    "title": "Security Events Overview",
                    "html": chart_generator.create_security_events_overview(events_df),
                    "explanation": "This chart shows the distribution of security events by type and severity level.",
                }
            )

            # Events timeline
            charts.append(
                {
                    "title": "Security Events Timeline",
                    "html": chart_generator.create_events_timeline(events_df),
                    "explanation": "Timeline showing security events over the reporting period, categorized by severity.",
                }
            )

        # Phishing analysis
        if not phishing_df.empty and (
            "phishing" in report_type.lower() or "Phishing Statistics" in str(metrics)
        ):
            charts.append(
                {
                    "title": "Phishing Campaign Analysis",
                    "html": chart_generator.create_phishing_analysis(phishing_df),
                    "explanation": "Comprehensive analysis of phishing campaigns including success rates and trends.",
                }
            )

        # Compliance dashboard
        if not compliance_df.empty and (
            "compliance" in report_type.lower() or len(compliance_df) > 0
        ):
            charts.append(
                {
                    "title": "Compliance Status Dashboard",
                    "html": chart_generator.create_compliance_dashboard(compliance_df),
                    "explanation": "Current compliance status across different frameworks and controls.",
                }
            )

        # KPI visualization
        charts.append(
            {
                "title": "Key Performance Indicators",
                "html": chart_generator.create_kpi_cards(metrics),
                "explanation": "Key security metrics and performance indicators for the reporting period.",
            }
        )

        # Trend analysis
        if not events_df.empty:
            charts.append(
                {
                    "title": "Security Trends Analysis",
                    "html": chart_generator.create_trend_analysis(events_df),
                    "explanation": "Trend analysis showing security event patterns and impact scores over time.",
                }
            )

    except Exception as e:
        print(f"Error generating charts: {str(e)}")
        charts.append(
            {
                "title": "Chart Generation Error",
                "html": f"<p>Error generating charts: {str(e)}</p>",
                "explanation": "There was an error generating the visualizations.",
            }
        )

    return charts


def prepare_kpi_data(metrics: Dict) -> List[Dict]:
    """Prepare KPI data for display"""

    kpis = []

    # Security metrics KPIs
    if "security_metrics" in metrics:
        sec_metrics = metrics["security_metrics"]
        kpis.extend(
            [
                {
                    "value": sec_metrics.get("total_events", 0),
                    "label": "Total Security Events",
                },
                {
                    "value": sec_metrics.get("critical_events", 0),
                    "label": "Critical Events",
                },
                {
                    "value": f"{sec_metrics.get('resolution_rate', 0):.1f}%",
                    "label": "Resolution Rate",
                },
                {
                    "value": f"{sec_metrics.get('avg_impact_score', 0):.1f}",
                    "label": "Avg Impact Score",
                },
            ]
        )

    # Phishing metrics KPIs
    if "phishing_metrics" in metrics:
        phish_metrics = metrics["phishing_metrics"]
        kpis.extend(
            [
                {
                    "value": phish_metrics.get("total_campaigns", 0),
                    "label": "Phishing Campaigns",
                },
                {
                    "value": f"{phish_metrics.get('avg_success_rate', 0):.1f}%",
                    "label": "Avg Success Rate",
                },
                {
                    "value": phish_metrics.get("total_blocked", 0),
                    "label": "Emails Blocked",
                },
            ]
        )

    # Compliance metrics KPIs
    if "compliance_metrics" in metrics:
        comp_metrics = metrics["compliance_metrics"]
        kpis.extend(
            [
                {
                    "value": f"{comp_metrics.get('compliance_rate', 0):.1f}%",
                    "label": "Compliance Rate",
                },
                {
                    "value": comp_metrics.get("total_controls", 0),
                    "label": "Total Controls",
                },
                {
                    "value": f"{comp_metrics.get('avg_compliance_score', 0):.1f}",
                    "label": "Avg Compliance Score",
                },
            ]
        )

    return kpis


def render_report_html(report_data: Dict) -> str:
    """Render the report HTML using the template"""

    return render_template(
        "report_template.html",
        report_title=report_data["report_title"],
        company_name=report_data["company_name"],
        period_description=report_data["period_description"],
        generation_date=report_data["generation_date"],
        report_period=report_data["report_period"],
        executive_summary=report_data["ai_content"]["executive_summary"],
        key_findings=report_data["ai_content"]["key_findings"],
        recommendations=report_data["ai_content"]["recommendations"],
        charts=report_data["charts"],
        kpi_data=report_data["kpi_data"],
    )


@app.route("/test_email")
def test_email():
    """Test email configuration"""
    if email_sender:
        success = email_sender.test_connection()
        if success:
            return jsonify(
                {"status": "success", "message": "Email configuration is working"}
            )
        else:
            return jsonify({"status": "error", "message": "Email configuration failed"})
    else:
        return jsonify({"status": "error", "message": "Email sender not configured"})


@app.route("/health")
def health_check():
    """Health check endpoint"""
    status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "data_processor": "ok",
            "chart_generator": "ok",
            "pdf_generator": "ok",
            "ai_generator": "ok" if ai_generator else "not_configured",
            "email_sender": "ok" if email_sender else "not_configured",
        },
    }
    return jsonify(status)


@app.errorhandler(404)
def not_found_error(error):
    return render_template("base.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("base.html"), 500


if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("generated_reports", exist_ok=True)
    os.makedirs("static/images", exist_ok=True)

    # Run the application
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=5555)
