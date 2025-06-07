import { useState } from 'react';
import { generateReport } from '../services/api';

interface ReportFormData {
  recipient_email: string;
  report_type: string;
  time_period: string;
  focus_areas: string[];
  specific_questions: string;
}

export const useReportGenerator = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<{ type: string; text: string } | null>(null);

  const generate = async (data: ReportFormData) => {
    setIsLoading(true);
    setMessage(null);
    try {
      const response = await generateReport(data);
      setMessage({ type: response.status, text: response.message });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to generate report';
      setMessage({ type: 'error', text: errorMessage });
    } finally {
      setIsLoading(false);
    }
  };

  return { isLoading, message, generate, setMessage };
}; 