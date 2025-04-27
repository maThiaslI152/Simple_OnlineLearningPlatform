// src/services/userService.js
import api from '@/services/auth'    // your axios instance with baseURL + auth interceptor

export default {
  getProfile() {
    return api.get('/api/auth/whoami/')
  },
  updateProfile(formData) {
    // formData should be a FormData instance
    return api.patch('/api/auth/profile/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}
