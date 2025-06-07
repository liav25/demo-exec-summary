import { motion } from 'framer-motion';
import { Cpu } from 'lucide-react';

const Hero = () => (
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
);

export default Hero; 