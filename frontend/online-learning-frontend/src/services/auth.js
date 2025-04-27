// src/services/auth.js
import api from '../axios'
export default {
  login: creds => api.post('token/', creds),
  refresh: refresh => api.post('token/refresh/', { refresh }),
  whoami: () => api.get('whoami/'),
  register: data  => api.post('register/', data),
  updateProfile: formData =>
    api.patch('profile/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
}
