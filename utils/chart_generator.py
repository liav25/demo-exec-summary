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
        # Define color schemes for consistent branding
        self.color_scheme = {
            "primary": "#0080ff",  # Electric Blue
            "secondary": "#39ff14",  # Cyber Green
            "success": "#39ff14",  # Cyber Green
            "warning": "#ff4444",
            "info": "#0080ff",  # Electric Blue
            "critical": "#ff4444",
            "rich_black": "#0a0a0a",
            "white": "#ffffff",
            "severity_colors": {
                "Critical": "#ff4444",
                "High": "#0080ff",  # Electric Blue
                "Medium": "#39ff14",  # Cyber Green
                "Low": "#0a0a0a",  # Rich Black
            },
            "status_colors": {
                "Resolved": "#39ff14",  # Cyber Green
                "Investigating": "#0080ff",  # Electric Blue
                "Monitoring": "#ff4444",
                "Blocked": "#0a0a0a",  # Rich Black
                "Contained": "#0080ff",  # Electric Blue
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
                    <img style="width: {width}px; height: {height}px; max-width: 100%; height: auto; border: 1px solid #ddd;" 
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

        # Create subplot with secondary y-axis
        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=("Events by Type", "Events by Severity"),
            specs=[[{"type": "bar"}, {"type": "pie"}]],
        )

        # Events by type
        event_counts = events_df["event_type"].value_counts()
        fig.add_trace(
            go.Bar(
                x=event_counts.index,
                y=event_counts.values,
                name="Event Count",
                marker_color=self.color_scheme["primary"],
            ),
            row=1,
            col=1,
        )

        # Events by severity (pie chart)
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
                marker_colors=colors,
            ),
            row=1,
            col=2,
        )

        fig.update_layout(
            title_text="Security Events Overview",
            showlegend=True,
            height=400,
            font=dict(size=12),
        )

        fig.update_xaxes(title_text="Event Type", row=1, col=1)
        fig.update_yaxes(title_text="Number of Events", row=1, col=1)

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
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Number of Events",
            height=400,
            font=dict(size=12),
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
        """Create KPI visualization cards"""
        try:
            # Extract key metrics
            kpi_data = []

            if "security_metrics" in metrics:
                sec = metrics["security_metrics"]
                kpi_data.extend(
                    [
                        {
                            "label": "Total Events",
                            "value": sec.get("total_events", 0),
                            "trend": "neutral",
                        },
                        {
                            "label": "Critical Events",
                            "value": sec.get("critical_events", 0),
                            "trend": "warning",
                        },
                        {
                            "label": "Resolution Rate",
                            "value": f"{sec.get('resolution_rate', 0):.1f}%",
                            "trend": "success",
                        },
                    ]
                )

            if "phishing_metrics" in metrics:
                phish = metrics["phishing_metrics"]
                kpi_data.extend(
                    [
                        {
                            "label": "Phishing Campaigns",
                            "value": phish.get("total_campaigns", 0),
                            "trend": "info",
                        },
                        {
                            "label": "Emails Blocked",
                            "value": phish.get("total_blocked", 0),
                            "trend": "success",
                        },
                    ]
                )

            if "compliance_metrics" in metrics:
                comp = metrics["compliance_metrics"]
                kpi_data.extend(
                    [
                        {
                            "label": "Compliance Rate",
                            "value": f"{comp.get('compliance_rate', 0):.1f}%",
                            "trend": "success",
                        },
                        {
                            "label": "Total Controls",
                            "value": comp.get("total_controls", 0),
                            "trend": "info",
                        },
                    ]
                )

            if not kpi_data:
                return self._create_empty_chart("No KPI data available")

            # Create a simple bar chart for KPIs
            labels = [kpi["label"] for kpi in kpi_data]
            values = []

            for kpi in kpi_data:
                val = kpi["value"]
                if isinstance(val, str) and "%" in val:
                    values.append(float(val.replace("%", "")))
                else:
                    values.append(
                        float(val) if str(val).replace(".", "").isdigit() else 0
                    )

            fig = go.Figure(
                data=[
                    go.Bar(
                        x=labels,
                        y=values,
                        marker_color=self.color_scheme["primary"],
                        text=[str(kpi["value"]) for kpi in kpi_data],
                        textposition="auto",
                    )
                ]
            )

            fig.update_layout(
                title="Key Performance Indicators",
                xaxis_title="Metrics",
                yaxis_title="Values",
                height=400,
                font=dict(size=12),
            )

            return self._generate_chart_html(fig, "kpi_cards")

        except Exception as e:
            return self._create_empty_chart(
                f"Error creating KPI visualization: {str(e)}"
            )

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
