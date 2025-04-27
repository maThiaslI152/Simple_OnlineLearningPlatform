import axios from 'axios'
import store from './store'

// Axios
const api = axios.create({
  baseURL: 'http://localhost:8000/api/auth/',
  headers: { 'Content-Type': 'application/json' }
})

// Request: attach token
api.interceptors.request.use(cfg => {
  const token = store.state.auth.accessToken
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// Response: handle 401 → try refresh once, then logout
api.interceptors.response.use(null, async err => {
  const { response, config } = err
  if (response?.status === 401 && store.state.auth.refreshToken) {
    // ▶️ use `api.post`, not bare `axios.post`, so baseURL + path works
    const { data } = await api.post('token/refresh/', {
      refresh: store.state.auth.refreshToken
    })
    store.commit('auth/setAccessToken', data.access)
    // retry original request
    config.headers.Authorization = `Bearer ${data.access}`
    return api.request(config)
  }
  return Promise.reject(err)
})

export default api
