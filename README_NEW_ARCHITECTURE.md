# AI Security Analyst - Refactored Architecture

This project has been refactored from a monolithic Flask application to a modern **React TypeScript frontend + FastAPI backend** architecture, while maintaining the exact same design and user experience.

## 🏗️ Architecture Overview

### Previous Architecture (Flask)
- **Monolithic**: Single Flask application serving both frontend (Jinja2 templates) and API endpoints
- **Frontend**: Server-side rendered HTML with Bootstrap + custom CSS
- **Backend**: Flask with utility modules

### New Architecture (React + FastAPI)

```
📁 Project Root
├── 📁 frontend/          # React TypeScript SPA
│   ├── 📁 src/
│   │   ├── App.tsx       # Main application component
│   │   ├── App.css       # Glassmorphism styling
│   │   └── main.tsx      # React entry point
│   ├── package.json      # Frontend dependencies
│   └── vite.config.ts    # Vite configuration
│
├── 📁 backend/           # FastAPI REST API
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── 📁 utils/         # Business logic modules
│   ├── 📁 templates/     # Jinja2 templates for PDF generation
│   ├── 📁 data/          # Sample data files
│   └── requirements.txt  # Python dependencies
│
└── package.json          # Root scripts for development
```

## ✨ Key Improvements

1. **Separation of Concerns**: Clear separation between frontend UI and backend API
2. **Modern Frontend**: React with TypeScript, form validation, and animations
3. **Better API**: FastAPI with automatic OpenAPI documentation and type validation
4. **Development Experience**: Hot reloading for both frontend and backend
5. **Maintainability**: Modular architecture that's easier to scale and modify
6. **Same UX**: Identical glassmorphism design and user experience

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **npm** or **yarn** (package manager)

### Option 1: Easy Setup (Recommended)

1. **Install concurrently** (to run both servers):
   ```bash
   npm install
   ```

2. **Install all dependencies**:
   ```bash
   npm run install-all
   ```

3. **Run both frontend and backend**:
   ```bash
   npm run dev
   ```

This will start:
- **Frontend**: http://localhost:5173 (Vite dev server)
- **Backend**: http://localhost:8000 (FastAPI server)
- **API Docs**: http://localhost:8000/docs (Swagger UI)

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup (in new terminal)
```bash
cd frontend
npm install
npm run dev
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the **backend** directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password
RESEND_API_KEY=your_resend_api_key

# Application Settings
COMPANY_NAME=SecureCorp Inc.
FLASK_DEBUG=false
SECRET_KEY=your_secret_key_here
```

### CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)

## 📱 Frontend Features

### React Components
- **Modern React Hooks**: `useState`, `useEffect`, `useForm`
- **Form Validation**: React Hook Form with Yup validation
- **Animations**: Framer Motion for smooth transitions
- **Icons**: Lucide React for beautiful icons
- **TypeScript**: Full type safety throughout

### UI/UX Features
- **Glassmorphism Design**: Identical to original Flask app
- **Grid Background**: Animated cyber-style background
- **Focus Area Pills**: Interactive selection components
- **Loading States**: Smooth loading animations
- **Responsive Design**: Mobile-friendly layout
- **Error Handling**: User-friendly error messages

## 🔗 API Endpoints

### FastAPI Backend

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/config` | GET | Get configuration (report types, focus areas) |
| `/generate-report` | POST | Generate and send security report |
| `/test-email` | GET | Test email configuration |
| `/docs` | GET | Swagger API documentation |

### API Documentation
Visit http://localhost:8000/docs when the backend is running to see the interactive API documentation.

## 🎨 Design System

The application maintains the exact same glassmorphism design system:

### Color Palette
- **Rich Black**: `#0D1117` (background)
- **Electric Blue**: `#0066CC` (primary)
- **Cyber Green**: `#00FF41` (accent)
- **White**: `#FFFFFF` (text)

### Components
- **Glass Containers**: Translucent backgrounds with blur effects
- **Focus Pills**: Interactive selection components
- **Form Elements**: Custom styled inputs and selects
- **Loading Animations**: Spinning cyber-style loaders

## 🔄 Development Workflow

### Frontend Development
```bash
cd frontend
npm run dev        # Start Vite dev server
npm run build      # Build for production
npm run preview    # Preview production build
```

### Backend Development
```bash
cd backend
uvicorn main:app --reload    # Start with auto-reload
python -m pytest            # Run tests (if available)
```

### Full Stack Development
```bash
npm run dev        # Run both frontend and backend
npm run frontend   # Run only frontend
npm run backend    # Run only backend
```

## 📦 Production Deployment

### Frontend (Static Build)
```bash
cd frontend
npm run build
# Deploy the 'dist' folder to your static hosting service
```

### Backend (Docker)
```bash
cd backend
# Create Dockerfile for FastAPI deployment
# Deploy to your cloud service (AWS, GCP, Azure, etc.)
```

## 🔍 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend CORS configuration includes your frontend URL
2. **API Connection**: Verify the API_BASE_URL in the frontend matches your backend
3. **Dependencies**: Run `npm run install-all` to ensure all dependencies are installed
4. **Environment Variables**: Check that `.env` file is in the backend directory

### Port Conflicts
- **Frontend**: Default port 5173 (Vite) or 3000 (Create React App)
- **Backend**: Default port 8000 (FastAPI)

Change ports if needed:
```bash
# Frontend
npm run dev -- --port 3001

# Backend
uvicorn main:app --port 8001
```

## 🚀 Next Steps

1. **Testing**: Add unit tests for both frontend and backend
2. **CI/CD**: Set up GitHub Actions for automated testing and deployment
3. **Docker**: Containerize both applications
4. **Monitoring**: Add logging and monitoring for production
5. **Authentication**: Add user authentication if needed

## 📚 Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Hook Form** - Form handling
- **Yup** - Schema validation
- **Framer Motion** - Animations
- **Axios** - HTTP client
- **Lucide React** - Icons

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Pandas** - Data processing
- **Plotly** - Chart generation
- **OpenAI** - AI content generation
- **WeasyPrint** - PDF generation

---

## 🎯 Summary

This refactoring successfully transforms the monolithic Flask application into a modern, scalable architecture while preserving the beautiful glassmorphism design and user experience. The new architecture provides better separation of concerns, improved development experience, and enhanced maintainability for future features. 