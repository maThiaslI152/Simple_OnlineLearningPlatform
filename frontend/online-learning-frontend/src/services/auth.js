// src/services/auth.js
import api from '../axios'
export default {
  login: creds => api.post('token/', creds),
  refresh: refresh => api.post('token/refresh/', { refresh }),
  whoami: () => api.get('whoami/')
}
