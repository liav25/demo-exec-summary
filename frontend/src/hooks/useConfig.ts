import { useState, useEffect } from 'react';
import { getConfig } from '../services/api';

interface Config {
  report_types: Record<string, { name: string; description: string }>;
  focus_areas: Array<{
    id: string;
    name: string;
    description: string;
    color: string;
    icon: string;
  }>;
  company_name: string;
}

export const useConfig = () => {
  const [config, setConfig] = useState<Config | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadConfig = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await getConfig();
        setConfig(data);
      } catch (err: any) {
        console.error('Configuration loading error:', err);
        setError('Failed to load configuration. Please ensure the backend server is running.');
      } finally {
        setIsLoading(false);
      }
    };

    loadConfig();
  }, []);

  return { config, error, isLoading };
}; 