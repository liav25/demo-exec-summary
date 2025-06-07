#!/usr/bin/env python3
"""
Test script to generate a PDF report via API with all areas of focus, YTD time frame, and quarterly report type
"""

import requests
import json
from datetime import datetime
import time
import os
import sys

# Get the directory where this script is located (backend directory)
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Change working directory to backend directory (in case we're running from elsewhere)
os.chdir(BACKEND_DIR)
print(f"📁 Working directory: {os.getcwd()}")

# API configuration
API_BASE_URL = "http://localhost:8000/api"
GENERATE_REPORT_ENDPOINT = f"{API_BASE_URL}/reports/generate-report"


def test_generate_pdf_via_api():
    """Generate a comprehensive PDF report using the API endpoint"""

    print("🚀 Testing PDF Generation via API")
    print("=" * 60)

    # Prepare request data
    request_data = {
        "recipient_email": "test@example.com",
        "report_type": "quarterly_review",
        "time_period": "ytd",
        "focus_areas": [
            "Phishing Statistics",
            "Malware Incidents",
            "Endpoint Compliance",
            "Network Security",
            "Data Protection",
            "Access Management",
            "Vulnerability Management",
            "Security Training",
        ],
        "specific_questions": """
        Please provide comprehensive analysis covering:
        1. Overall security posture assessment
        2. Critical vulnerabilities and remediation progress
        3. Compliance status across all frameworks
        4. Employee security awareness metrics
        5. Incident response effectiveness
        6. Strategic recommendations for improvement
        """,
    }

    print("📋 Request Configuration:")
    print(f"   - Endpoint: {GENERATE_REPORT_ENDPOINT}")
    print(f"   - Report Type: {request_data['report_type']}")
    print(f"   - Time Period: {request_data['time_period']}")
    print(f"   - Focus Areas: {len(request_data['focus_areas'])} areas")
    print(f"   - Email: {request_data['recipient_email']}")
    print()

    try:
        # Make API request
        print("📡 Sending request to API...")
        start_time = time.time()

        response = requests.post(
            GENERATE_REPORT_ENDPOINT,
            json=request_data,
            headers={"Content-Type": "application/json"},
        )

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"⏱️  Request completed in {elapsed_time:.2f} seconds")
        print(f"📊 Response Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("\n✅ Success!")
            print(f"   Status: {result.get('status')}")
            print(f"   Message: {result.get('message')}")
            print(f"   Report ID: {result.get('report_id')}")

            # Pretty print the full response
            print("\n📄 Full Response:")
            print(json.dumps(result, indent=2))

        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error!")
        print("   Make sure the FastAPI server is running:")
        print("   cd backend && uvicorn app.main:app --reload")

    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback

        traceback.print_exc()


def test_minimal_api_request():
    """Test with minimal parameters"""

    print("\n\n🚀 Testing Minimal API Request")
    print("=" * 60)

    request_data = {
        "recipient_email": "minimal@test.com",
        "report_type": "monthly_threat",
        "time_period": "last_week",
        "focus_areas": ["Network Security"],
        "specific_questions": "",
    }

    try:
        response = requests.post(
            GENERATE_REPORT_ENDPOINT,
            json=request_data,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            print("✅ Minimal request successful!")
            print(f"   Report ID: {response.json().get('report_id')}")
        else:
            print(f"❌ Error: {response.status_code}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def check_api_health():
    """Check if the API is running"""

    print("🏥 Checking API Health...")

    try:
        response = requests.get(f"{API_BASE_URL}/health/report-system")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ API is healthy!")
            print(f"   Status: {health_data.get('status')}")
            print(
                f"   Components: {json.dumps(health_data.get('components', {}), indent=2)}"
            )
            return True
        else:
            print(f"⚠️  Health check returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
        return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False


if __name__ == "__main__":
    print("🧪 API PDF Generation Test")
    print("========================\n")

    # First check if API is running
    if check_api_health():
        print()
        # Run comprehensive test
        test_generate_pdf_via_api()

        # Run minimal test
        test_minimal_api_request()

        print("\n\n✨ API tests completed!")
        print("\n💡 Check the 'generated_reports' directory for the PDFs")
    else:
        print("\n⚠️  Please start the API server first:")
        print("   cd backend")
        print("   uvicorn app.main:app --reload")
        print("\nThen run this test again.")
