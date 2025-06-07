from typing import List, Dict
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

from app.core.dependencies import (
    get_data_processor,
    get_ai_generator,
    get_chart_generator,
    get_pdf_generator,
)
from app.core.config import config, REPORT_TYPES

data_processor = get_data_processor()
ai_generator = get_ai_generator()
chart_generator = get_chart_generator()
pdf_generator = get_pdf_generator()


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
    report_config = REPORT_TYPES.get(report_type, {})

    return {
        "report_title": report_config.get(
            "name", report_type.replace("_", " ").title()
        ),
        "report_type": report_type,
        "time_period": time_period,
        "period_description": time_period.replace("_", " ").title(),
        "company_name": config.company_name,
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
    """Render the report HTML from a Jinja2 template"""
    # Assuming 'templates' is a directory in the same level as this script
    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    env = Environment(
        loader=FileSystemLoader(template_dir), autoescape=select_autoescape(["html"])
    )
    template = env.get_template("report_template.html")
    return template.render(report_data)
