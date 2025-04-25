import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/user/',
});

export const courseApi = axios.create({
  baseURL: 'http://localhost:8000/course/',
});

// Attach token
const attachToken = (config) => {
  const token = localStorage.getItem('access');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
};

api.interceptors.request.use(attachToken);
courseApi.interceptors.request.use(attachToken);

// Refresh token handling shared by both api and courseApi
const handleRefresh = async (error, originalRequest) => {
  const refresh = localStorage.getItem('refresh');
  if (error.response?.status === 401 && refresh && !originalRequest._retry) {
    originalRequest._retry = true;
    try {
      const res = await axios.post(
        'http://localhost:8000/user/token/refresh/',
        { refresh }
      );
      const newAccess = res.data.access;
      localStorage.setItem('access', newAccess);
      originalRequest.headers['Authorization'] = `Bearer ${newAccess}`;
      return axios(originalRequest);
    } catch (refreshError) {
      console.error('Refresh token expired. Logging out.');
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      window.location.href = '/login';
      return Promise.reject(refreshError);
    }
  }
  return Promise.reject(error);
};

api.interceptors.response.use((res) => res, (error) => handleRefresh(error, error.config));
courseApi.interceptors.response.use((res) => res, (error) => handleRefresh(error, error.config));

export default api;
