import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getConfig = async () => {
  const response = await apiClient.get('/config');
  return response.data;
};

export const generateReport = async (data: any) => {
  const response = await apiClient.post('/generate-report', data);
  return response.data;
};

export const testEmailConnection = async () => {
  const response = await apiClient.get('/test-email');
  return response.data;
}; 