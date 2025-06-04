import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Tuple, Optional
import json
import os
import base64


class ChartGenerator:
    """Generates interactive charts using Plotly for security reports"""

    def __init__(self):
        # Define color schemes for consistent branding using soft, beautiful palette
        self.color_scheme = {
            # Primary colors from the beautiful palette
            "primary": "#1C4E80",  # Deep Blue
            "secondary": "#4CB5F5",  # Sky Blue
            "success": "#6AB187",  # Sage Green
            "warning": "#DBAE58",  # Golden Yellow
            "info": "#A5D8DD",  # Soft Teal
            "critical": "#AC3E31",  # Warm Red
            "accent": "#488A99",  # Teal
            # Neutral tones
            "rich_black": "#23282D",  # Dark Charcoal
            "charcoal": "#484848",  # Medium Charcoal
            "slate": "#7E909A",  # Blue Gray
            "light_gray": "#CED2CC",  # Light Gray
            "off_white": "#F1F1F1",  # Off White
            "white": "#FFFFFF",  # Pure White
            "cream": "#DADADA",  # Light Cream
            # Severity color mapping with soft palette
            "severity_colors": {
                "Critical": "#AC3E31",  # Warm Red
                "High": "#1C4E80",  # Deep Blue
                "Medium": "#DBAE58",  # Golden Yellow
                "Low": "#6AB187",  # Sage Green
                "Info": "#A5D8DD",  # Soft Teal
            },
            # Status colors with soft palette
            "status_colors": {
                "Resolved": "#6AB187",  # Sage Green
                "Investigating": "#4CB5F5",  # Sky Blue
                "Monitoring": "#DBAE58",  # Golden Yellow
                "Blocked": "#AC3E31",  # Warm Red
                "Contained": "#488A99",  # Teal
                "Active": "#1C4E80",  # Deep Blue
                "Pending": "#7E909A",  # Blue Gray
            },
            # Beautiful gradient combinations
            "gradients": [
                ["#A5D8DD", "#4CB5F5"],  # Teal to Sky Blue
                ["#6AB187", "#DBAE58"],  # Green to Gold
                ["#1C4E80", "#488A99"],  # Deep Blue to Teal
                ["#F1F1F1", "#CED2CC"],  # Light Gray gradient
                ["#DBAE58", "#AC3E31"],  # Gold to Red
            ],
            # Chart-specific color palettes
            "chart_palette": [
                "#1C4E80",  # Deep Blue
                "#4CB5F5",  # Sky Blue
                "#6AB187",  # Sage Green
                "#DBAE58",  # Golden Yellow
                "#A5D8DD",  # Soft Teal
                "#488A99",  # Teal
                "#AC3E31",  # Warm Red
                "#7E909A",  # Blue Gray
                "#23282D",  # Dark Charcoal
                "#CED2CC",  # Light Gray
            ],
            # Soft background colors for different chart types
            "backgrounds": {
                "light": "#F1F1F1",
                "subtle": "rgba(241, 241, 241, 0.3)",
                "accent": "rgba(165, 216, 221, 0.1)",
                "warm": "rgba(219, 174, 88, 0.1)",
                "cool": "rgba(76, 181, 245, 0.1)",
            },
        }

        # Default to PDF mode for better compatibility
        self.pdf_mode = True

    def set_pdf_mode(self, pdf_mode: bool):
        """Set whether to generate charts optimized for PDF or interactive web view"""
        self.pdf_mode = pdf_mode

    def _generate_chart_html(
        self, fig, div_id: str, use_static_for_pdf: bool = None
    ) -> str:
        """Generate HTML for chart with PDF compatibility following Plotly documentation approach"""
        # Use instance setting if not explicitly overridden
        if use_static_for_pdf is None:
            use_static_for_pdf = self.pdf_mode

        # Apply beautiful styling to all charts
        fig.update_layout(
            paper_bgcolor=self.color_scheme["white"],
            plot_bgcolor=self.color_scheme["backgrounds"]["light"],
            font=dict(
                family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
                size=12,
                color=self.color_scheme["rich_black"],
            ),
            title=dict(
                font=dict(
                    family="Source Serif Pro, serif",
                    size=16,
                    color=self.color_scheme["rich_black"],
                ),
                x=0.5,
                y=0.95,
            ),
            margin=dict(l=60, r=60, t=80, b=60),
            showlegend=True,
            legend=dict(
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor=self.color_scheme["light_gray"],
                borderwidth=1,
                font=dict(size=11),
            ),
        )

        try:
            if use_static_for_pdf:
                # Following the Plotly PDF documentation approach
                # Generate static image for better PDF compatibility
                width = 800
                height = 500

                # Use Plotly's to_image with explicit engine specification
                img_bytes = fig.to_image(
                    format="png", width=width, height=height, engine="kaleido"
                )
                img_base64 = base64.b64encode(img_bytes).decode("utf-8")

                # Create HTML template following Plotly documentation pattern
                template = f"""
                <div id="{div_id}" style="text-align: center; margin: 20px 0;">
                    <img style="width: {width}px; height: {height}px; max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);" 
                         src="data:image/png;base64,{img_base64}" 
                         alt="Chart: {div_id}" />
                </div>
                """

                return template
            else:
                # Use interactive HTML for web view
                return fig.to_html(include_plotlyjs="inline", div_id=div_id)

        except ImportError as e:
            print(f"Kaleido not installed, falling back to inline HTML: {str(e)}")
            # Fallback to inline HTML if kaleido is not available
            return fig.to_html(include_plotlyjs="inline", div_id=div_id)
        except Exception as e:
            print(
                f"Error generating static chart image, falling back to HTML: {str(e)}"
            )
            # Fallback to inline HTML if image generation fails
            return fig.to_html(include_plotlyjs="inline", div_id=div_id)

    def create_security_events_overview(self, events_df: pd.DataFrame) -> str:
        """Create an overview chart of security events by type and severity"""
        if events_df.empty:
            return self._create_empty_chart("No security events data available")

        # Create subplot with beautiful styling
        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=("Events by Type", "Events by Severity"),
            specs=[[{"type": "bar"}, {"type": "pie"}]],
            horizontal_spacing=0.15,
        )

        # Events by type with gradient colors
        event_counts = events_df["event_type"].value_counts()

        # Create gradient bar colors
        bar_colors = []
        for i, event_type in enumerate(event_counts.index):
            color_index = i % len(self.color_scheme["chart_palette"])
            bar_colors.append(self.color_scheme["chart_palette"][color_index])

        fig.add_trace(
            go.Bar(
                x=event_counts.index,
                y=event_counts.values,
                name="Event Count",
                marker=dict(
                    color=bar_colors,
                    line=dict(color=self.color_scheme["light_gray"], width=1),
                    pattern=dict(shape=""),
                ),
                hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
            ),
            row=1,
            col=1,
        )

        # Events by severity (pie chart) with beautiful colors
        severity_counts = events_df["severity"].value_counts()
        colors = [
            self.color_scheme["severity_colors"].get(sev, self.color_scheme["primary"])
            for sev in severity_counts.index
        ]

        fig.add_trace(
            go.Pie(
                labels=severity_counts.index,
                values=severity_counts.values,
                name="Severity Distribution",
                marker=dict(
                    colors=colors, line=dict(color=self.color_scheme["white"], width=2)
                ),
                hole=0.3,  # Donut chart for modern look
                hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
            ),
            row=1,
            col=2,
        )

        fig.update_layout(
            title_text="Security Events Overview",
            height=450,
        )

        fig.update_xaxes(
            title_text="Event Type",
            row=1,
            col=1,
            tickangle=-45,
            gridcolor=self.color_scheme["light_gray"],
            gridwidth=1,
        )
        fig.update_yaxes(
            title_text="Number of Events",
            row=1,
            col=1,
            gridcolor=self.color_scheme["light_gray"],
            gridwidth=1,
        )

        return self._generate_chart_html(fig, "security_events_overview")

    def create_events_timeline(self, events_df: pd.DataFrame) -> str:
        """Create a timeline chart showing events over time"""
        if events_df.empty:
            return self._create_empty_chart("No timeline data available")

        # Group by month and severity
        events_df["month"] = events_df["date"].dt.to_period("M").astype(str)
        timeline_data = (
            events_df.groupby(["month", "severity"]).size().reset_index(name="count")
        )

        fig = px.line(
            timeline_data,
            x="month",
            y="count",
            color="severity",
            title="Security Events Timeline",
            color_discrete_map=self.color_scheme["severity_colors"],
            markers=True,
        )

        # Enhance the timeline with better styling
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8, line=dict(width=2, color=self.color_scheme["white"])),
        )

        fig.update_layout(
            height=400,
            xaxis=dict(
                title="Month",
                gridcolor=self.color_scheme["light_gray"],
                gridwidth=1,
                showgrid=True,
            ),
            yaxis=dict(
                title="Number of Events",
                gridcolor=self.color_scheme["light_gray"],
                gridwidth=1,
                showgrid=True,
            ),
            hovermode="x unified",
        )

        return self._generate_chart_html(fig, "events_timeline")

    def create_phishing_analysis(self, phishing_df: pd.DataFrame) -> str:
        """Create phishing analysis charts"""
        if phishing_df.empty:
            return self._create_empty_chart("No phishing data available")

        # Create subplots
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Success Rate by Campaign Type",
                "Blocked vs Clicked",
                "Threat Level Distribution",
                "Monthly Phishing Trends",
            ),
            specs=[
                [{"type": "bar"}, {"type": "scatter"}],
                [{"type": "pie"}, {"type": "scatter"}],
            ],
        )

        # Success rate by campaign type
        campaign_success = (
            phishing_df.groupby("campaign_type")["success_rate"]
            .mean()
            .sort_values(ascending=False)
        )
        fig.add_trace(
            go.Bar(
                x=campaign_success.index,
                y=campaign_success.values * 100,
                name="Success Rate %",
                marker_color=self.color_scheme["warning"],
            ),
            row=1,
            col=1,
        )

        # Blocked vs Clicked scatter
        fig.add_trace(
            go.Scatter(
                x=phishing_df["blocked_count"],
                y=phishing_df["clicked_count"],
                mode="markers",
                name="Campaigns",
                marker=dict(
                    size=phishing_df["success_rate"] * 500,
                    color=phishing_df["success_rate"],
                    colorscale="Reds",
                    showscale=True,
                ),
                text=phishing_df["campaign_type"],
                hovertemplate="<b>%{text}</b><br>Blocked: %{x}<br>Clicked: %{y}<extra></extra>",
            ),
            row=1,
            col=2,
        )

        # Threat level distribution
        threat_counts = phishing_df["threat_level"].value_counts()
        fig.add_trace(
            go.Pie(
                labels=threat_counts.index,
                values=threat_counts.values,
                name="Threat Levels",
            ),
            row=2,
            col=1,
        )

        # Monthly trends
        phishing_df["month"] = phishing_df["date"].dt.to_period("M").astype(str)
        monthly_trends = (
            phishing_df.groupby("month")
            .agg({"success_rate": "mean", "clicked_count": "sum"})
            .reset_index()
        )

        fig.add_trace(
            go.Scatter(
                x=monthly_trends["month"],
                y=monthly_trends["success_rate"] * 100,
                mode="lines+markers",
                name="Success Rate %",
                line=dict(color=self.color_scheme["warning"]),
                yaxis="y",
            ),
            row=2,
            col=2,
        )

        fig.add_trace(
            go.Scatter(
                x=monthly_trends["month"],
                y=monthly_trends["clicked_count"],
                mode="lines+markers",
                name="Total Clicks",
                line=dict(color=self.color_scheme["primary"]),
                yaxis="y2",
            ),
            row=2,
            col=2,
        )

        fig.update_layout(
            title_text="Phishing Campaign Analysis",
            showlegend=True,
            height=600,
            font=dict(size=10),
        )

        fig.update_xaxes(title_text="Campaign Type", row=1, col=1)
        fig.update_yaxes(title_text="Success Rate (%)", row=1, col=1)

        fig.update_xaxes(title_text="Blocked Count", row=1, col=2)
        fig.update_yaxes(title_text="Clicked Count", row=1, col=2)

        fig.update_xaxes(title_text="Month", row=2, col=2)
        fig.update_yaxes(title_text="Success Rate (%)", row=2, col=2)

        return self._generate_chart_html(fig, "phishing_analysis")

    def create_compliance_dashboard(self, compliance_df: pd.DataFrame) -> str:
        """Create compliance status dashboard"""
        if compliance_df.empty:
            return self._create_empty_chart("No compliance data available")

        # Create subplots
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Compliance by Framework",
                "Control Status Distribution",
                "Compliance Scores Over Time",
                "Risk Level Assessment",
            ),
            specs=[
                [{"type": "bar"}, {"type": "pie"}],
                [{"type": "scatter"}, {"type": "bar"}],
            ],
        )

        # Compliance by framework
        framework_compliance = (
            compliance_df.groupby("framework")["compliance_score"]
            .mean()
            .sort_values(ascending=False)
        )
        fig.add_trace(
            go.Bar(
                x=framework_compliance.index,
                y=framework_compliance.values,
                name="Avg Compliance Score",
                marker_color=self.color_scheme["primary"],
            ),
            row=1,
            col=1,
        )

        # Control status distribution
        status_counts = compliance_df["status"].value_counts()
        colors = [
            self.color_scheme["status_colors"].get(status, self.color_scheme["primary"])
            for status in status_counts.index
        ]
        fig.add_trace(
            go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                name="Control Status",
                marker_colors=colors,
            ),
            row=1,
            col=2,
        )

        # Compliance scores over time
        compliance_df["month"] = compliance_df["date"].dt.to_period("M").astype(str)
        monthly_compliance = (
            compliance_df.groupby("month")["compliance_score"].mean().reset_index()
        )
        fig.add_trace(
            go.Scatter(
                x=monthly_compliance["month"],
                y=monthly_compliance["compliance_score"],
                mode="lines+markers",
                name="Monthly Compliance",
                line=dict(color=self.color_scheme["success"]),
            ),
            row=2,
            col=1,
        )

        # Risk level assessment
        risk_counts = compliance_df["risk_level"].value_counts()
        fig.add_trace(
            go.Bar(
                x=risk_counts.index,
                y=risk_counts.values,
                name="Risk Distribution",
                marker_color=self.color_scheme["warning"],
            ),
            row=2,
            col=2,
        )

        fig.update_layout(
            title_text="Compliance Status Dashboard",
            showlegend=True,
            height=600,
            font=dict(size=10),
        )

        fig.update_xaxes(title_text="Framework", row=1, col=1)
        fig.update_yaxes(title_text="Compliance Score", row=1, col=1)

        fig.update_xaxes(title_text="Month", row=2, col=1)
        fig.update_yaxes(title_text="Compliance Score", row=2, col=1)

        fig.update_xaxes(title_text="Risk Level", row=2, col=2)
        fig.update_yaxes(title_text="Number of Controls", row=2, col=2)

        return self._generate_chart_html(fig, "compliance_dashboard")

    def create_kpi_cards(self, metrics: Dict) -> str:
        """Create beautiful KPI cards with improved styling"""

        kpis = []

        # Security metrics KPIs
        if "security_metrics" in metrics:
            sec_metrics = metrics["security_metrics"]
            kpis.extend(
                [
                    {
                        "title": "Total Security Events",
                        "value": sec_metrics.get("total_events", 0),
                        "color": self.color_scheme["primary"],
                        "icon": "🛡️",
                        "trend": "neutral",
                    },
                    {
                        "title": "Critical Events",
                        "value": sec_metrics.get("critical_events", 0),
                        "color": self.color_scheme["critical"],
                        "icon": "🚨",
                        "trend": (
                            "down"
                            if sec_metrics.get("critical_events", 0) < 10
                            else "up"
                        ),
                    },
                    {
                        "title": "Resolution Rate",
                        "value": f"{sec_metrics.get('resolution_rate', 0):.1f}%",
                        "color": self.color_scheme["success"],
                        "icon": "✅",
                        "trend": "up",
                    },
                    {
                        "title": "Avg Impact Score",
                        "value": f"{sec_metrics.get('avg_impact_score', 0):.1f}",
                        "color": self.color_scheme["warning"],
                        "icon": "📊",
                        "trend": "neutral",
                    },
                ]
            )

        # Phishing metrics KPIs
        if "phishing_metrics" in metrics:
            phish_metrics = metrics["phishing_metrics"]
            kpis.extend(
                [
                    {
                        "title": "Phishing Campaigns",
                        "value": phish_metrics.get("total_campaigns", 0),
                        "color": self.color_scheme["info"],
                        "icon": "🎣",
                        "trend": "neutral",
                    },
                    {
                        "title": "Avg Success Rate",
                        "value": f"{phish_metrics.get('avg_success_rate', 0):.1f}%",
                        "color": self.color_scheme["critical"],
                        "icon": "📈",
                        "trend": "down",
                    },
                    {
                        "title": "Emails Blocked",
                        "value": phish_metrics.get("total_blocked", 0),
                        "color": self.color_scheme["success"],
                        "icon": "🛡️",
                        "trend": "up",
                    },
                ]
            )

        # Compliance metrics KPIs
        if "compliance_metrics" in metrics:
            comp_metrics = metrics["compliance_metrics"]
            kpis.extend(
                [
                    {
                        "title": "Compliance Rate",
                        "value": f"{comp_metrics.get('compliance_rate', 0):.1f}%",
                        "color": self.color_scheme["success"],
                        "icon": "📋",
                        "trend": "up",
                    },
                    {
                        "title": "Total Controls",
                        "value": comp_metrics.get("total_controls", 0),
                        "color": self.color_scheme["primary"],
                        "icon": "🔧",
                        "trend": "neutral",
                    },
                    {
                        "title": "Avg Compliance Score",
                        "value": f"{comp_metrics.get('avg_compliance_score', 0):.1f}",
                        "color": self.color_scheme["accent"],
                        "icon": "⭐",
                        "trend": "up",
                    },
                ]
            )

        # Create beautiful HTML KPI cards
        html_content = """
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0;">
        """

        for kpi in kpis:
            trend_arrow = (
                "📈"
                if kpi["trend"] == "up"
                else "📉" if kpi["trend"] == "down" else "➡️"
            )

            html_content += f"""
            <div style="
                background: linear-gradient(135deg, {kpi['color']} 0%, rgba(255,255,255,0.9) 100%);
                border-radius: 12px;
                padding: 25px 20px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border: 1px solid {self.color_scheme['light_gray']};
                position: relative;
                overflow: hidden;
            ">
                <div style="position: absolute; top: 10px; right: 15px; font-size: 20px; opacity: 0.7;">
                    {kpi['icon']}
                </div>
                <div style="position: absolute; bottom: 10px; right: 15px; font-size: 16px; opacity: 0.6;">
                    {trend_arrow}
                </div>
                <div style="
                    font-family: 'Source Serif Pro', serif;
                    font-size: 32px;
                    font-weight: 600;
                    color: {self.color_scheme['rich_black']};
                    margin: 10px 0 15px 0;
                    line-height: 1;
                ">
                    {kpi['value']}
                </div>
                <div style="
                    font-size: 12px;
                    color: {self.color_scheme['slate']};
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                ">
                    {kpi['title']}
                </div>
            </div>
            """

        html_content += "</div>"

        return html_content

    def create_trend_analysis(
        self, events_df: pd.DataFrame, metric: str = "impact_score"
    ) -> str:
        """Create trend analysis chart"""
        if events_df.empty:
            return self._create_empty_chart("No data available for trend analysis")

        try:
            # Create monthly trends
            events_df["month"] = events_df["date"].dt.to_period("M").astype(str)

            # Calculate trends by severity
            monthly_trends = (
                events_df.groupby(["month", "severity"])
                .agg({metric: "mean", "event_id": "count"})
                .reset_index()
            )
            monthly_trends.rename(columns={"event_id": "event_count"}, inplace=True)

            fig = px.line(
                monthly_trends,
                x="month",
                y=metric,
                color="severity",
                title=f"Security Trends Analysis - {metric.replace('_', ' ').title()}",
                color_discrete_map=self.color_scheme["severity_colors"],
                markers=True,
            )

            fig.update_layout(
                xaxis_title="Month",
                yaxis_title=metric.replace("_", " ").title(),
                height=400,
                font=dict(size=12),
            )

            return self._generate_chart_html(fig, "trend_analysis")

        except Exception as e:
            return self._create_empty_chart(f"Error creating trend analysis: {str(e)}")

    def _create_empty_chart(self, message: str) -> str:
        """Create an empty chart with a message"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            xanchor="center",
            yanchor="middle",
            showarrow=False,
            font=dict(size=16, color="gray"),
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            height=300,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        return self._generate_chart_html(fig, "empty_chart")
