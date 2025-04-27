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
api.interceptors.response.use(
  res => res,
  async err => {
    const orig = err.config
    const status = err.response?.status

    // 1) If it’s the refresh call itself or we already retried, bail
    if (
      orig.url.includes('token/refresh') ||
      orig._retry
    ) {
      // clear everything and stop trying
      await store.dispatch('auth/logout')
      return Promise.reject(err)
    }

    // 2) On first 401, try refresh
    if (status === 401 && store.state.auth.refreshToken) {
      orig._retry = true
      try {
        const { data } = await api.post('token/refresh/', {
          refresh: store.state.auth.refreshToken
        })
        store.commit('auth/setTokens', {
          access: data.access,
          refresh: data.refresh || store.state.auth.refreshToken
        })
        orig.headers.Authorization = `Bearer ${data.access}`
        return api.request(orig)
      } catch (refreshErr) {
        // refresh failed → logout
        await store.dispatch('auth/logout')
        return Promise.reject(refreshErr)
      }
    }

    return Promise.reject(err)
  }
)

export default api
