import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/user/',
});

export const courseApi = axios.create({
  baseURL: 'http://localhost:8000/course/',
});

// Attach token to both api and courseApi
const attachToken = (config) => {
  const token = localStorage.getItem('access');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
};

api.interceptors.request.use(attachToken);
courseApi.interceptors.request.use(attachToken);

// Refresh token handling (keep as is for api only)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
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
        return api(originalRequest);
      } catch (refreshError) {
        console.error('Refresh token expired. Logging out.');
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
