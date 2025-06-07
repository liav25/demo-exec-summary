import { Brain } from 'lucide-react';

const Footer = () => (
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
);

export default Footer; 