import axios from 'axios';
import { useSelector } from 'react-redux';
import { BASE_URL } from './host';

const API_URL = 'http://192.168.1.9:8000/api/tasks/'; // Django API adresi


const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

export const setCsrfToken = (csrf) => {
  if (token) {
    api.defaults.headers.common['X-Csrftoken'] = csrf;
  } else {
    delete api.defaults.headers.common['X-Csrftoken'];

  }
};

export default api;
