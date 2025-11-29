import axios, { AxiosError, AxiosResponse } from 'axios';
import config from "../utils/config.json"
import { toast } from 'react-toastify';

const API_URL = config.BACKEND_API_URL;

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    if (error.response) {
      switch (error.response.status) {
        case 400:
          // Bad Request - Validation error
          toast('An occur has occurred while attempting to validate your data')
          console.error('Validation Error:', error.response.data);
          break;
        case 401:
          // Unauthorized - Authentication required
          toast('You need to log in first')
          console.error('Authentication Error:', error.response.data);
          break;
        case 403:
          // Forbidden - Insufficient permissions
          toast('You do not have sufficient permissions to do that')
          console.error('Permission Error:', error.response.data);
          break;
        case 404:
          // Not Found
          toast('The resource you are looking for does not exist')
          console.error('Resource Not Found:', error.response.data);
          break;
        case 429:
          // Too Many Requests
          toast('Rate limit exceeded, try again later')
          console.error('Rate Limit Exceeded:', error.response.data);
          break;
        case 500:
          // Internal Server Error
          toast('We are currently experiencing issues from our end')
          console.error('Server Error:', error.response.data);
          break;
        default:
          toast('Error, try again later')
          console.error('API Error:', error.response.data);
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No Response Received:', error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Request Setup Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;