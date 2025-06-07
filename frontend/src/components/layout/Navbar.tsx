import { Brain } from 'lucide-react';

const Navbar = () => (
  <nav className="navbar">
    <div className="nav-container">
      <div className="nav-brand">
        <Brain className="nav-icon" />
        <span className="brand-text">AI Security Analyst</span>
      </div>
    </div>
  </nav>
);

export default Navbar; 