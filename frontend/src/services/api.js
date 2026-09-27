import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 5000,
});

export const getHealth = async () => {
  try {
    const response = await api.get('/health');
    return { data: response.data, error: null };
  } catch (error) {
    return { data: null, error: error.message };
  }
};

export const getSystemInfo = async () => {
  try {
    const response = await api.get('/system/info');
    return { data: response.data, error: null };
  } catch (error) {
    return { data: null, error: error.message };
  }
};

export default api;
