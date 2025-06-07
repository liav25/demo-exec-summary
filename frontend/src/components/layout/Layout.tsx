import React from 'react';
import Navbar from './Navbar';
import Footer from './Footer';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="app">
    <div className="grid-background"></div>
    <Navbar />
    <main className="main-content">{children}</main>
    <Footer />
  </div>
);

export default Layout; 