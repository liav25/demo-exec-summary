interface LoaderProps {
  text: string;
}

const Loader = ({ text }: LoaderProps) => (
  <div className="loading-animation">
    <div className="loading-spinner"></div>
    <div className="loading-content">
      <h3 className="loading-title">{text}</h3>
      <p className="loading-text">Processing security metrics and generating insights...</p>
    </div>
  </div>
);

export default Loader; 