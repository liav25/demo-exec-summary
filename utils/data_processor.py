import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from config import Config


class DataProcessor:
    """Handles loading and processing of security data for report generation"""

    def __init__(self):
        self.config = Config()
        self.data_cache = {}

    def load_data(self, filename: str) -> pd.DataFrame:
        """Load data from CSV file with caching"""
        if filename in self.data_cache:
            return self.data_cache[filename].copy()

        filepath = os.path.join(self.config.DATA_DIR, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file not found: {filepath}")

        df = pd.read_csv(filepath)

        # Convert date columns to datetime
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])

        self.data_cache[filename] = df
        return df.copy()

    def filter_by_date_range(
        self, df: pd.DataFrame, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """Filter dataframe by date range"""
        if "date" not in df.columns:
            return df

        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)

        return df[(df["date"] >= start) & (df["date"] <= end)]

    def get_date_range_from_period(self, period: str) -> Tuple[str, str]:
        """Convert period string to start and end dates"""
        today = datetime.now()

        if period.lower() == "last_quarter":
            # Get last complete quarter
            current_quarter = (today.month - 1) // 3 + 1
            if current_quarter == 1:
                start_date = datetime(today.year - 1, 10, 1)
                end_date = datetime(today.year - 1, 12, 31)
            else:
                quarter_start_month = (current_quarter - 2) * 3 + 1
                start_date = datetime(today.year, quarter_start_month, 1)
                if current_quarter == 2:
                    end_date = datetime(today.year, 3, 31)
                elif current_quarter == 3:
                    end_date = datetime(today.year, 6, 30)
                else:  # current_quarter == 4
                    end_date = datetime(today.year, 9, 30)

        elif period.lower() == "last_month":
            if today.month == 1:
                start_date = datetime(today.year - 1, 12, 1)
                end_date = datetime(today.year - 1, 12, 31)
            else:
                start_date = datetime(today.year, today.month - 1, 1)
                # Get last day of previous month
                end_date = datetime(today.year, today.month, 1) - timedelta(days=1)

        elif period.lower() == "last_6_months":
            end_date = today
            start_date = today - timedelta(days=180)

        elif period.lower() == "ytd" or period.lower() == "year_to_date":
            start_date = datetime(today.year, 1, 1)
            end_date = today

        else:
            # Default to last 3 months
            end_date = today
            start_date = today - timedelta(days=90)

        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    def get_security_events_data(
        self, report_type: str, period: str, focus_areas: List[str] = None
    ) -> pd.DataFrame:
        """Get filtered security events data based on report parameters"""
        df = self.load_data("security_events.csv")

        # Filter by date range
        start_date, end_date = self.get_date_range_from_period(period)
        df = self.filter_by_date_range(df, start_date, end_date)

        # Apply focus area filters if specified
        if focus_areas:
            focus_filters = []
            for area in focus_areas:
                if "phishing" in area.lower():
                    focus_filters.append(
                        df["event_type"].str.contains("Phishing", case=False, na=False)
                    )
                elif "malware" in area.lower():
                    focus_filters.append(
                        df["event_type"].str.contains("Malware", case=False, na=False)
                    )
                elif "endpoint" in area.lower():
                    focus_filters.append(
                        df["target"].str.contains("Endpoint", case=False, na=False)
                    )
                elif "network" in area.lower():
                    focus_filters.append(
                        df["source"].str.contains("Network", case=False, na=False)
                    )

            if focus_filters:
                combined_filter = focus_filters[0]
                for f in focus_filters[1:]:
                    combined_filter = combined_filter | f
                df = df[combined_filter]

        return df

    def get_phishing_data(self, period: str) -> pd.DataFrame:
        """Get filtered phishing data"""
        df = self.load_data("phishing_data.csv")
        start_date, end_date = self.get_date_range_from_period(period)
        return self.filter_by_date_range(df, start_date, end_date)

    def get_compliance_data(self, period: str) -> pd.DataFrame:
        """Get filtered compliance data"""
        df = self.load_data("compliance_data.csv")
        start_date, end_date = self.get_date_range_from_period(period)
        return self.filter_by_date_range(df, start_date, end_date)

    def calculate_security_metrics(self, events_df: pd.DataFrame) -> Dict:
        """Calculate key security metrics from events data"""
        if events_df.empty:
            return {
                "total_events": 0,
                "critical_events": 0,
                "high_events": 0,
                "resolved_events": 0,
                "avg_impact_score": 0,
                "top_event_types": [],
                "resolution_rate": 0,
            }

        metrics = {
            "total_events": len(events_df),
            "critical_events": len(events_df[events_df["severity"] == "Critical"]),
            "high_events": len(events_df[events_df["severity"] == "High"]),
            "resolved_events": len(events_df[events_df["status"] == "Resolved"]),
            "avg_impact_score": events_df["impact_score"].mean(),
            "top_event_types": events_df["event_type"].value_counts().head(5).to_dict(),
            "resolution_rate": len(events_df[events_df["status"] == "Resolved"])
            / len(events_df)
            * 100,
        }

        return metrics

    def calculate_phishing_metrics(self, phishing_df: pd.DataFrame) -> Dict:
        """Calculate phishing-specific metrics"""
        if phishing_df.empty:
            return {
                "total_campaigns": 0,
                "avg_success_rate": 0,
                "total_blocked": 0,
                "total_clicked": 0,
                "total_reported": 0,
                "high_risk_campaigns": 0,
            }

        metrics = {
            "total_campaigns": len(phishing_df),
            "avg_success_rate": phishing_df["success_rate"].mean() * 100,
            "total_blocked": phishing_df["blocked_count"].sum(),
            "total_clicked": phishing_df["clicked_count"].sum(),
            "total_reported": phishing_df["reported_count"].sum(),
            "high_risk_campaigns": len(
                phishing_df[phishing_df["threat_level"].isin(["High", "Critical"])]
            ),
        }

        return metrics

    def calculate_compliance_metrics(self, compliance_df: pd.DataFrame) -> Dict:
        """Calculate compliance metrics"""
        if compliance_df.empty:
            return {
                "total_controls": 0,
                "compliant_controls": 0,
                "compliance_rate": 0,
                "avg_compliance_score": 0,
                "frameworks": [],
                "non_compliant_controls": 0,
            }

        # Get latest assessment for each control
        latest_assessments = (
            compliance_df.sort_values("date")
            .groupby(["framework", "control_id"])
            .tail(1)
        )

        metrics = {
            "total_controls": len(latest_assessments),
            "compliant_controls": len(
                latest_assessments[latest_assessments["status"] == "Compliant"]
            ),
            "compliance_rate": len(
                latest_assessments[latest_assessments["status"] == "Compliant"]
            )
            / len(latest_assessments)
            * 100,
            "avg_compliance_score": latest_assessments["compliance_score"].mean(),
            "frameworks": latest_assessments["framework"].unique().tolist(),
            "non_compliant_controls": len(
                latest_assessments[latest_assessments["status"] == "Non-Compliant"]
            ),
        }

        return metrics

    def get_trend_data(
        self, df: pd.DataFrame, metric_column: str, date_column: str = "date"
    ) -> pd.DataFrame:
        """Get trend data for visualization"""
        if df.empty or date_column not in df.columns:
            return pd.DataFrame()

        # Group by month and calculate metrics
        df["month"] = df[date_column].dt.to_period("M")
        trend_data = (
            df.groupby("month")
            .agg(
                {
                    metric_column: (
                        ["count", "mean"] if metric_column in df.columns else "count"
                    )
                }
            )
            .reset_index()
        )

        trend_data["month"] = trend_data["month"].astype(str)
        return trend_data
