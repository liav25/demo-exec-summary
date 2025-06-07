import { useConfig } from './hooks/useConfig';
import { useReportGenerator } from './hooks/useReportGenerator';
import Layout from './components/layout/Layout';
import Hero from './components/report/Hero';
import Features from './components/report/Features';
import ReportForm from './components/report/ReportForm';
import Message from './components/report/Message';
import Loader from './components/report/Loader';
import './App.css';

function App() {
  const { config, error: configError, isLoading: isConfigLoading } = useConfig();
  const { isLoading: isGenerating, message, generate, setMessage } = useReportGenerator();

  if (isConfigLoading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <p>Loading configuration...</p>
      </div>
    );
  }

  if (configError) {
    return (
      <div className="loading-screen">
        <p>{configError}</p>
      </div>
    );
  }

  return (
    <Layout>
      {message && <Message message={message} onClose={() => setMessage(null)} />}
      <Hero />
      <div className="form-wrapper">
        <div className="glass-container">
          {!isGenerating ? (
            config && <ReportForm config={config} onSubmit={generate} isLoading={isGenerating} />
          ) : (
            <Loader text="Analyzing Your Security Data" />
          )}
        </div>
      </div>
      <Features />
    </Layout>
  );
}

export default App;
