import openai
from typing import Dict, List, Optional
import json
from app.core.config import config


class AIGenerator:
    """Handles AI-powered content generation using OpenAI API"""

    def __init__(self):
        if not config.openai_api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY in your .env file."
            )

        self.client = openai.OpenAI(api_key=config.openai_api_key)

    def generate_executive_summary(
        self,
        report_type: str,
        period: str,
        metrics: Dict,
        focus_areas: List[str] = None,
    ) -> str:
        """Generate an executive summary based on security metrics"""

        # Create context from metrics
        context = self._build_metrics_context(metrics)
        focus_context = (
            f" with particular focus on {', '.join(focus_areas)}" if focus_areas else ""
        )

        prompt = f"""
        You are a cybersecurity expert writing an executive summary for a {report_type} covering the {period} period{focus_context}.
        
        Based on the following security metrics and data:
        {context}
        
        Write a professional, executive-level summary (2-3 paragraphs) that:
        1. Highlights the overall security posture and key findings
        2. Identifies the most critical risks and concerns
        3. Notes any positive trends or improvements
        4. Uses business-friendly language appropriate for C-level executives
        5. Focuses on actionable insights rather than technical details
        
        Keep the tone professional, confident, and solution-oriented. Avoid technical jargon.
        """

        try:
            response = self.client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior cybersecurity consultant writing executive reports.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=config.openai_max_tokens
                // 8,  # Use smaller token limit for summary
                temperature=config.openai_temperature,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error generating executive summary: {str(e)}"

    def generate_section_analysis(
        self, section_title: str, data_summary: str, chart_description: str
    ) -> str:
        """Generate analysis text for a specific report section"""

        prompt = f"""
        You are writing a section analysis for a cybersecurity report. The section is titled "{section_title}".
        
        Data Summary: {data_summary}
        Chart/Visualization: {chart_description}
        
        Write a concise analysis (1-2 paragraphs) that:
        1. Explains what the data shows in business terms
        2. Identifies key trends, patterns, or anomalies
        3. Provides context for why this matters to the organization
        4. Suggests implications or next steps if relevant
        
        Use clear, professional language suitable for executives. Focus on insights, not just data description.
        """

        try:
            response = self.client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity analyst writing report sections.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
                temperature=0.6,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error generating section analysis: {str(e)}"

    def generate_key_findings(self, metrics: Dict, report_type: str) -> List[str]:
        """Generate a list of key findings based on metrics"""

        context = self._build_metrics_context(metrics)

        prompt = f"""
        Based on the following security metrics for a {report_type}:
        {context}
        
        Generate 3-5 key findings that would be most important for executives to know. 
        Each finding should be:
        - One clear, concise sentence
        - Focused on business impact or risk
        - Actionable or decision-relevant
        
        Format as a JSON array of strings.
        """

        try:
            response = self.client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity expert identifying key findings for executives.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=400,
                temperature=0.5,
            )

            content = response.choices[0].message.content.strip()
            # Try to parse as JSON, fallback to simple list if needed
            try:
                findings = json.loads(content)
                return findings if isinstance(findings, list) else [content]
            except json.JSONDecodeError:
                # Fallback: split by lines and clean up
                lines = content.split("\n")
                findings = [
                    line.strip("- ").strip()
                    for line in lines
                    if line.strip() and not line.strip().startswith("[")
                ]
                return findings[:5]  # Limit to 5 findings

        except Exception as e:
            return [f"Error generating key findings: {str(e)}"]

    def generate_recommendations(
        self, metrics: Dict, focus_areas: List[str] = None
    ) -> List[str]:
        """Generate security recommendations based on metrics and focus areas"""

        context = self._build_metrics_context(metrics)
        focus_context = (
            f" Pay special attention to {', '.join(focus_areas)}."
            if focus_areas
            else ""
        )

        prompt = f"""
        Based on the following security metrics:
        {context}
        {focus_context}
        
        Generate 3-4 specific, actionable recommendations for improving the organization's security posture.
        Each recommendation should be:
        - Specific and actionable
        - Prioritized based on risk and impact
        - Feasible for implementation
        - Focused on addressing identified gaps or risks
        
        Format as a JSON array of strings.
        """

        try:
            response = self.client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity consultant providing strategic recommendations.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=400,
                temperature=0.6,
            )

            content = response.choices[0].message.content.strip()
            try:
                recommendations = json.loads(content)
                return (
                    recommendations if isinstance(recommendations, list) else [content]
                )
            except json.JSONDecodeError:
                lines = content.split("\n")
                recommendations = [
                    line.strip("- ").strip()
                    for line in lines
                    if line.strip() and not line.strip().startswith("[")
                ]
                return recommendations[:4]

        except Exception as e:
            return [f"Error generating recommendations: {str(e)}"]

    def generate_chart_explanation(
        self, chart_type: str, data_description: str, key_insights: str
    ) -> str:
        """Generate explanation text for a chart or visualization"""

        prompt = f"""
        You are explaining a {chart_type} chart in a cybersecurity report.
        
        Data Description: {data_description}
        Key Insights: {key_insights}
        
        Write a brief explanation (1 paragraph) that:
        1. Describes what the chart shows
        2. Highlights the most important patterns or trends
        3. Explains the business significance
        
        Use clear, non-technical language suitable for executives.
        """

        try:
            response = self.client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are explaining data visualizations to business executives.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=200,
                temperature=0.5,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error generating chart explanation: {str(e)}"

    def _build_metrics_context(self, metrics: Dict) -> str:
        """Build a formatted context string from metrics dictionary"""
        context_parts = []

        for category, data in metrics.items():
            if isinstance(data, dict):
                context_parts.append(f"\n{category.replace('_', ' ').title()}:")
                for key, value in data.items():
                    if isinstance(value, (int, float)):
                        if "rate" in key or "score" in key:
                            context_parts.append(
                                f"  - {key.replace('_', ' ').title()}: {value:.1f}%"
                            )
                        else:
                            context_parts.append(
                                f"  - {key.replace('_', ' ').title()}: {value}"
                            )
                    elif isinstance(value, dict) and len(value) <= 5:  # Top items
                        context_parts.append(
                            f"  - {key.replace('_', ' ').title()}: {', '.join([f'{k}({v})' for k, v in value.items()])}"
                        )
                    elif isinstance(value, list) and len(value) <= 5:
                        context_parts.append(
                            f"  - {key.replace('_', ' ').title()}: {', '.join(map(str, value))}"
                        )

        return "\n".join(context_parts)
