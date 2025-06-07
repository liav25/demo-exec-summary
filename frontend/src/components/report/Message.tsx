import { motion } from 'framer-motion';

interface MessageProps {
  message: { type: string; text: string };
  onClose: () => void;
}

const Message = ({ message, onClose }: MessageProps) => (
  <motion.div
    className={`alert alert-${message.type}`}
    initial={{ opacity: 0, y: -20 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -20 }}
  >
    {message.text}
    <button
      className="alert-close"
      onClick={onClose}
    >
      ×
    </button>
  </motion.div>
);

export default Message; 