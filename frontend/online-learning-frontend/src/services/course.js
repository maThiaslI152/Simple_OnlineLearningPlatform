// src/services/course.js
import axios from 'axios'
import store from '@/store'

const courseApi = axios.create({
  baseURL: 'http://localhost:8000/api/course/',
  headers: { 'Content-Type': 'application/json' }
})

// Attach JWT
courseApi.interceptors.request.use(cfg => {
  const t = store.state.auth.accessToken
  if (t) cfg.headers.Authorization = `Bearer ${t}`
  return cfg
})

// Auto-refresh on 401
courseApi.interceptors.response.use(null, async err => {
  const { response, config } = err
  if (response?.status === 401 && store.state.auth.refreshToken) {
    const { data } = await axios.post(
      'http://localhost:8000/api/auth/token/refresh/',
      { refresh: store.state.auth.refreshToken }
    )
    store.commit('auth/setAccessToken', data.access)
    config.headers.Authorization = `Bearer ${data.access}`
    return courseApi.request(config)
  }
  return Promise.reject(err)
})

export default {
  // Course CRUD
  listAll:     ()           => courseApi.get(''),               // GET /api/course/
  listMine:    ()           => courseApi.get('mine/'),          // GET /api/course/mine/
  getDetail:   id           => courseApi.get(`${id}/`),         // GET /api/course/:id/
  create:      payload      => courseApi.post('', payload),     // POST /api/course/

  // Week management
  addWeek:     id           => courseApi.post(`${id}/add_week/`),// POST /api/course/:id/add_week/

  // Module listings (nested under course/:id)
  listNotes:   (c, w)       => courseApi.get(`${c}/note/`,      { params: { week_number: w } }),
  listVideos:  (c, w)       => courseApi.get(`${c}/video/`,     { params: { week_number: w } }),
  listHomework:(c, w)       => courseApi.get(`${c}/homework/`,  { params: { week_number: w } }),
  listTests:   (c, w)       => courseApi.get(`${c}/test/`,      { params: { week_number: w } }),

  // Module creation (pass course and week_number in body)
  createNote:     (c, w, data) => courseApi.post(`${c}/note/`,     { ...data, course: c, week_number: w }),
  createVideo:    (c, w, data) => courseApi.post(`${c}/video/`,    { ...data, course: c, week_number: w }),
  createHomework: (c, w, data) => courseApi.post(`${c}/homework/`, { ...data, course: c, week_number: w }),
  createTest:     (c, w, data) => courseApi.post(`${c}/test/`,     { ...data, course: c, week_number: w }),
}

