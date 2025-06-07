# PDF Generation Test Script

## Overview
The `test_generate_pdf.py` script generates comprehensive PDF reports to test the new professional design with all available options.

## Features
The test script generates two types of reports:

### 1. Comprehensive Report
- **Report Type**: Quarterly Security Review
- **Time Period**: Year to Date (YTD)
- **Focus Areas**: All 8 available areas
  - Phishing Statistics
  - Malware Incidents
  - Endpoint Compliance
  - Network Security
  - Data Protection
  - Access Management
  - Vulnerability Management
  - Security Training
- **Includes**: Detailed AI-generated analysis and comprehensive questions

### 2. Minimal Report
- **Report Type**: Quarterly Security Review
- **Time Period**: Last Week
- **Focus Areas**: Only 2 areas (Network Security, Phishing Statistics)
- **Purpose**: For comparison with the comprehensive report

## Usage

### Prerequisites
1. Ensure you're in the backend directory
2. Activate your virtual environment
3. Make sure all dependencies are installed

### Running the Test

```bash
cd backend
python test_generate_pdf.py
```

Or if you made it executable:

```bash
cd backend
./test_generate_pdf.py
```

### Output
The script will:
1. Display detailed progress information
2. Generate two PDF reports in the `generated_reports` directory
3. Show a summary with file sizes
4. Display key metrics from the reports

### Generated Files
- `TEST_comprehensive_quarterly_review_ytd_[timestamp].pdf` - Full report with all options
- `TEST_minimal_quarterly_review_last_week_[timestamp].pdf` - Minimal report for comparison

### What to Check
After running the test, review the PDFs for:
- **Professional Design**: Modern color palette, typography, and layout
- **Chart Quality**: Beautiful visualizations with proper styling
- **Content Organization**: Clear hierarchy and sections
- **KPI Cards**: Gradient text values with accent bars
- **Tables**: Professional styling with alternating rows
- **Status Indicators**: Pill-shaped badges with proper colors

## Troubleshooting

### Common Issues

1. **Chart Generation Error**: Already fixed - removed unsupported `weight` property
2. **Missing AI Content**: Ensure `OPENAI_API_KEY` is set in `.env`
3. **File Not Found**: Make sure you're running from the `backend` directory

### Dependencies
Ensure these are installed:
- plotly
- kaleido (for static chart images)
- weasyprint (for PDF generation)
- pandas
- numpy

## Customization

To test different configurations, modify the parameters in the script:

```python
# Change report type
report_type = "monthly_threat"  # or any from REPORT_TYPES

# Change time period
time_period = "last_month"  # or: last_week, last_quarter, ytd

# Select specific focus areas
focus_areas = ["Network Security", "Data Protection"]
``` 