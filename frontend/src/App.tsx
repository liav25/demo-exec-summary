import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useForm } from 'react-hook-form'
import type { SubmitHandler } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import axios from 'axios'
import { Cpu, Mail, ChartLine, Calendar, Target, MessageCircle, Sparkles, Shield, BarChart3, FileText, Brain } from 'lucide-react'
import './App.css'

// Types
interface Config {
  report_types: Record<string, { name: string; description: string }>
  focus_areas: string[]
  company_name: string
}

interface ReportFormData {
  recipient_email: string
  report_type: string
  time_period: string
  focus_areas: string[]
  specific_questions: string
}

const schema = yup.object().shape({
  recipient_email: yup.string().email('Invalid email').required('Email is required'),
  report_type: yup.string().required('Report type is required'),
  time_period: yup.string().required('Time period is required'),
  focus_areas: yup.array().of(yup.string().required()).default([]),
  specific_questions: yup.string().default('')
})

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [config, setConfig] = useState<Config | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState<{ type: string; text: string } | null>(null)
  const [selectedFocusAreas, setSelectedFocusAreas] = useState<string[]>([])

  const { register, handleSubmit, formState: { errors } } = useForm<ReportFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      focus_areas: [],
      specific_questions: ''
    }
  })

  // Load configuration on mount
  useEffect(() => {
    const loadConfig = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/config`)
        setConfig(response.data)
      } catch (error) {
        console.error('Failed to load config:', error)
        setMessage({ type: 'error', text: 'Failed to load configuration' })
      }
    }
    loadConfig()
  }, [])

  const onSubmit: SubmitHandler<ReportFormData> = async (data) => {
    setIsLoading(true)
    setMessage(null)

    try {
      const response = await axios.post(`${API_BASE_URL}/generate-report`, {
        ...data,
        focus_areas: selectedFocusAreas
      })

      setMessage({ 
        type: response.data.status, 
        text: response.data.message 
      })
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to generate report'
      setMessage({ type: 'error', text: errorMessage })
    } finally {
      setIsLoading(false)
    }
  }

  const toggleFocusArea = (area: string) => {
    setSelectedFocusAreas(prev => 
      prev.includes(area) 
        ? prev.filter(a => a !== area)
        : [...prev, area]
    )
  }

  if (!config) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <p>Loading configuration...</p>
      </div>
    )
  }

  return (
    <div className="app">
      <div className="grid-background"></div>
      
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-brand">
            <Brain className="nav-icon" />
            <span className="brand-text">AI Security Analyst</span>
          </div>
        </div>
      </nav>

      <main className="main-content">
        {/* Message Display */}
        {message && (
          <motion.div 
            className={`alert alert-${message.type}`}
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            {message.text}
            <button 
              className="alert-close"
              onClick={() => setMessage(null)}
            >
              ×
            </button>
          </motion.div>
        )}

        {/* Hero Section */}
        <motion.div 
          className="hero-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="delivery-tag">
            <Cpu size={16} />
            <span>Powered by Advanced AI</span>
          </div>
          <h1 className="hero-title">Your AI Security Analyst</h1>
          <p className="hero-subtitle">
            Transform complex security data into executive insights with AI-driven analysis. 
            Generate comprehensive reports tailored to your organization's needs.
          </p>
        </motion.div>

        {/* Main Form */}
        <div className="form-wrapper">
          <div className="glass-container">
            {!isLoading ? (
              <form onSubmit={handleSubmit(onSubmit)} className="report-form">
                {/* Basic Information Section */}
                <div className="form-section">
                  <h2 className="section-title">
                    <Mail size={20} />
                    Basic Information
                  </h2>
                  
                  <div className="form-row">
                    <div className="form-group">
                      <label className="form-label">
                        <Mail size={16} />
                        Executive Email Address
                      </label>
                      <input
                        type="email"
                        className={`glass-input ${errors.recipient_email ? 'error' : ''}`}
                        placeholder="ceo@company.com"
                        {...register('recipient_email')}
                      />
                      {errors.recipient_email && (
                        <span className="error-text">{errors.recipient_email.message}</span>
                      )}
                      <div className="form-text">Report will be delivered to this address</div>
                    </div>
                    
                    <div className="form-group">
                      <label className="form-label">
                        <ChartLine size={16} />
                        Report Type
                      </label>
                      <select
                        className={`glass-input ${errors.report_type ? 'error' : ''}`}
                        {...register('report_type')}
                      >
                        <option value="">Select report type...</option>
                        {Object.entries(config.report_types).map(([key, value]) => (
                          <option key={key} value={key}>
                            {value.name}
                          </option>
                        ))}
                      </select>
                      {errors.report_type && (
                        <span className="error-text">{errors.report_type.message}</span>
                      )}
                    </div>
                  </div>
                  
                  <div className="form-row">
                    <div className="form-group">
                      <label className="form-label">
                        <Calendar size={16} />
                        Analysis Time Period
                      </label>
                      <select
                        className={`glass-input ${errors.time_period ? 'error' : ''}`}
                        {...register('time_period')}
                      >
                        <option value="">Select timeframe...</option>
                        <option value="last_quarter">Last Quarter (90 days)</option>
                        <option value="last_month">Last Month (30 days)</option>
                        <option value="last_6_months">Last 6 Months</option>
                        <option value="ytd">Year to Date</option>
                      </select>
                      {errors.time_period && (
                        <span className="error-text">{errors.time_period.message}</span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Focus Areas Section */}
                <div className="form-section">
                  <h2 className="section-title">
                    <Target size={20} />
                    Areas of Focus
                  </h2>
                  <p className="section-description">
                    Select the security domains you want emphasized in your report
                  </p>
                  
                  <div className="focus-pills">
                    {config.focus_areas.map((area) => (
                      <motion.div
                        key={area}
                        className={`focus-pill ${selectedFocusAreas.includes(area) ? 'selected' : ''}`}
                        onClick={() => toggleFocusArea(area)}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <div className="pill-content">
                          <Shield size={20} />
                          {area}
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Additional Details Section */}
                <div className="form-section">
                  <h2 className="section-title">
                    <MessageCircle size={20} />
                    Additional Details
                  </h2>
                  
                  <div className="form-group">
                    <label className="form-label">
                      Specific Questions or Requirements (Optional)
                    </label>
                    <textarea
                      className="glass-input"
                      rows={4}
                      placeholder="e.g., What are our top 3 security risks this quarter? How has our phishing success rate changed?"
                      {...register('specific_questions')}
                    />
                    <div className="form-text">
                      Include any specific questions or areas you'd like the AI to address
                    </div>
                  </div>
                </div>

                {/* Submit Section */}
                <div className="submit-section">
                  <motion.button
                    type="submit"
                    className="primary-btn"
                    disabled={isLoading}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <Sparkles size={20} />
                    Generate Security Report
                  </motion.button>
                </div>
              </form>
            ) : (
              <div className="loading-animation">
                <div className="loading-spinner"></div>
                <div className="loading-content">
                  <h3 className="loading-title">Analyzing Your Security Data</h3>
                  <p className="loading-text">Processing security metrics and generating insights...</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Features Section */}
        <motion.div 
          className="features-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <h2 className="features-title">What You'll Receive</h2>
          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-icon">
                <Brain size={24} />
              </div>
              <h4 className="feature-title">AI-Powered Analysis</h4>
              <p className="feature-description">
                Advanced algorithms analyze your security data to identify patterns, trends, and actionable insights for executives.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                <BarChart3 size={24} />
              </div>
              <h4 className="feature-title">Professional Visualizations</h4>
              <p className="feature-description">
                Clear, interactive charts and graphs that present complex security metrics in an executive-friendly format.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                <Shield size={24} />
              </div>
              <h4 className="feature-title">Risk Assessment</h4>
              <p className="feature-description">
                Comprehensive risk analysis with prioritized recommendations to strengthen your organization's security posture.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                <FileText size={24} />
              </div>
              <h4 className="feature-title">Executive Reports</h4>
              <p className="feature-description">
                Professional PDF reports delivered directly to your inbox, formatted for executive presentation and decision-making.
              </p>
            </div>
          </div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-left">
            <div className="footer-brand">
              <Brain size={20} />
              <h5 className="footer-title">AI Security Analyst</h5>
            </div>
            <p className="footer-subtitle">Intelligent security reporting powered by AI</p>
          </div>
          <div className="footer-right">
            <p className="footer-text">
              Built for Gen AI Security Hackathon<br />
              <span>Powered by OpenAI & Advanced Analytics</span>
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
