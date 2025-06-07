import { motion } from 'framer-motion';
import { Brain, BarChart3, Shield, FileText } from 'lucide-react';

const Features = () => (
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
);

export default Features; 