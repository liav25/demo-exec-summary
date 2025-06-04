# Gen AI Security Report Generator

An AI-powered security report generator that creates executive-level security reports with interactive visualizations and AI-generated insights. Perfect for CISOs, CTOs, and security executives who need automated, professional security reporting.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Clone and navigate to the project
cd demo-exec-summary

# Run the quick start script (handles everything automatically)
python start.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment (interactive)
python setup_env.py

# Run the application
python app.py
```

### Option 3: Demo Mode (No Setup Required)
```bash
# Generate sample reports instantly
python demo.py

# Interactive demo mode
python demo.py --interactive
```

## 🎯 Demo & Testing

### Generate Sample Reports
```bash
# Generate all demo reports (no email/API keys needed)
python demo.py

# Interactive demo with custom options
python demo.py --interactive

# View example environment configuration
python setup_env.py --example
```

### Test Application Components
```bash
# Health check endpoint
curl http://localhost:5000/health

# Test email configuration (when running)
curl http://localhost:5000/test_email
```

## 📁 Project Structure

```
demo-exec-summary/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── setup_env.py          # Interactive environment setup
├── start.py              # Quick start script with checks
├── demo.py               # Demo script for sample reports
├── .env                  # Environment variables (create this)
├── data/                 # Mock security data
│   ├── security_events.csv    # 50+ realistic security incidents
│   ├── phishing_data.csv      # 47 phishing campaigns
│   └── compliance_data.csv    # 44 compliance assessments
├── templates/            # HTML templates
│   ├── base.html              # Bootstrap layout
│   ├── index.html             # Main form interface
│   └── report_template.html   # PDF report template
├── static/              # Static files
│   ├── css/
│   │   └── style.css          # Modern responsive styling
│   └── images/
│       └── logo.png
├── utils/               # Utility modules
│   ├── __init__.py
│   ├── data_processor.py      # Data loading and metrics
│   ├── ai_generator.py        # OpenAI integration
│   ├── chart_generator.py     # Plotly visualizations
│   ├── pdf_generator.py       # WeasyPrint PDF generation
│   └── email_sender.py        # SMTP email delivery
└── generated_reports/   # Output directory for reports
```

## 🔧 Features

### Core Functionality
- **AI-Powered Content Generation**: Uses OpenAI GPT for executive summaries, key findings, and recommendations
- **Interactive Visualizations**: Creates professional charts using Plotly (bar, pie, line, scatter, histograms)
- **Professional PDF Reports**: Converts HTML reports to PDF with custom styling using WeasyPrint
- **Email Delivery System**: Automatically sends reports via SMTP with HTML email templates
- **Mock Data Integration**: Uses realistic security data for demonstration and testing

### Report Types
- **Quarterly Security Review**: Comprehensive security posture assessment
- **Monthly Threat Overview**: Threat landscape and incident summary
- **Phishing Deep Dive**: Detailed phishing attack analysis and trends
- **Compliance Status Report**: Current compliance posture across frameworks
- **Incident Response Summary**: Security incidents and response activities

### Time Periods & Filtering
- Last Month, Last Quarter, Last 6 Months, Year to Date
- Focus area filtering (Phishing, Malware, Endpoints, Network, etc.)
- Custom date range support
- Severity and impact-based filtering

## 🛠 Configuration

### Environment Variables
```bash
# Required for AI features
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Required for email delivery
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Optional customization
COMPANY_NAME=Your Company Name
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=true
```

### Email Setup (Gmail)
1. Enable 2-Factor Authentication
2. Generate an App Password: Google Account > Security > 2-Step Verification > App passwords
3. Use the App Password (not your regular password) in EMAIL_PASSWORD

### OpenAI Setup
1. Get API key from: https://platform.openai.com/api-keys
2. Add to .env file: `OPENAI_API_KEY=sk-your-key-here`
3. Recommended model: `gpt-4o-mini` (cost-effective and fast)

## 📊 Data Sources

### Security Events (security_events.csv)
- 50+ realistic security incidents
- Event types: Malware, Phishing, Unauthorized Access, Data Breach, etc.
- Severity levels: Low, Medium, High, Critical
- Status tracking: Open, In Progress, Resolved, Closed
- Impact scores and resolution times

### Phishing Data (phishing_data.csv)
- 47 phishing campaigns with success rates
- Email counts: sent, delivered, clicked, blocked
- Threat levels and campaign types
- Geographic and temporal distribution

### Compliance Data (compliance_data.csv)
- 44 compliance assessments
- Frameworks: SOC2, ISO27001, NIST, PCI-DSS, HIPAA
- Control categories and compliance scores
- Assessment dates and findings

## 🎨 User Interface

### Main Features
- **Modern Bootstrap Design**: Responsive, mobile-friendly interface
- **Hero Section**: Clear value proposition and call-to-action
- **Interactive Form**: Report type, time period, focus areas, custom questions
- **Loading Modal**: Progress indication during report generation
- **Flash Messages**: Success, error, and warning notifications
- **Features Showcase**: Highlights key capabilities

### Report Output
- **Executive Summary**: AI-generated high-level overview
- **Key Performance Indicators**: Visual KPI cards with metrics
- **Interactive Charts**: Embedded Plotly visualizations
- **Key Findings**: AI-identified important insights
- **Recommendations**: Actionable AI-generated suggestions
- **Professional Styling**: Corporate-ready PDF formatting

## 🚀 Deployment

### Local Development
```bash
python start.py  # Automated setup and launch
```

### Production Considerations
- Set `FLASK_DEBUG=false`
- Use a production WSGI server (gunicorn, uWSGI)
- Configure proper secret keys
- Set up SSL/TLS certificates
- Implement proper authentication
- Use environment-specific configurations

## 🔒 Security Notes

- **Demo Data**: This project uses mock data for demonstration
- **API Keys**: Store securely and rotate regularly
- **Email Credentials**: Use app passwords, not account passwords
- **Production**: Integrate with real security tools and APIs
- **Authentication**: Implement proper user authentication for production
- **Data Privacy**: Ensure compliance with data protection regulations

## 🛠 Development

### Built For
- Gen AI Security Hackathon
- Rapid prototyping and MVP development
- Executive-level security reporting automation
- Integration of AI and visualization technologies

### Technology Stack
- **Backend**: Python Flask
- **AI**: OpenAI GPT API
- **Visualizations**: Plotly
- **PDF Generation**: WeasyPrint
- **Frontend**: Bootstrap, HTML5, CSS3
- **Data Processing**: Pandas
- **Email**: SMTP with HTML templates

### Key Design Principles
- **Executive Focus**: Reports designed for C-level consumption
- **Automation**: End-to-end workflow from request to delivery
- **Professional Quality**: Corporate-ready output and styling
- **Flexibility**: Multiple report types and customization options
- **Scalability**: Modular architecture for easy extension

## 📝 Usage Workflow

1. **Access Interface**: Navigate to `http://localhost:5000`
2. **Fill Form**: Select report type, time period, focus areas, and add specific questions
3. **Submit Request**: Click "Generate Report" to start processing
4. **AI Processing**: System generates insights using OpenAI
5. **Visualization**: Creates interactive charts and KPIs
6. **PDF Generation**: Compiles everything into professional PDF
7. **Email Delivery**: Sends report to specified email address
8. **Confirmation**: Receive success notification and email

## 🤝 Contributing

This is a hackathon project designed for rapid development and demonstration. For production use, consider:
- Adding user authentication and authorization
- Implementing real-time data integration
- Adding more visualization types
- Enhancing AI prompt engineering
- Adding report scheduling and automation
- Implementing audit logging and compliance features

## 📄 License

This project is created for educational and demonstration purposes. Please ensure compliance with all applicable licenses for dependencies and APIs used. 