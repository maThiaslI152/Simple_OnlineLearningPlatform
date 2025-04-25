// src/services/course.js
import axios from 'axios'
import store from '@/store'

const courseApi = axios.create({
  baseURL: 'http://localhost:8000/api/course/',
  headers: { 'Content-Type': 'application/json' }
})

courseApi.interceptors.request.use(cfg => {
  const t = store.state.auth.accessToken
  if (t) cfg.headers.Authorization = `Bearer ${t}`
  return cfg
})
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
  listAll:     ()           => courseApi.get(''), 
  listMine:    ()           => courseApi.get('mine/'),
  getDetail:   id           => courseApi.get(`${id}/`),
  create:      payload      => courseApi.post('', payload),
  // Week management
  addWeek:     id           => courseApi.post(`${id}/add_week/`),

  // Module listings
  listNotes:   (c, w)       => courseApi.get('note/',     { params: { course: c, week_number: w } }),
  listVideos:  (c, w)       => courseApi.get('video/',    { params: { course: c, week_number: w } }),
  listHomework:(c, w)       => courseApi.get('homework/', { params: { course: c, week_number: w } }),
  listTests:   (c, w)       => courseApi.get('test/',     { params: { course: c, week_number: w } }),

  // Module creation
  createNote:     (c, w, data) => courseApi.post('note/',     { ...data, course: c, week_number: w }),
  createVideo:    (c, w, data) => courseApi.post('video/',    { ...data, course: c, week_number: w }),
  createHomework: (c, w, data) => courseApi.post('homework/', { ...data, course: c, week_number: w }),
  createTest:     (c, w, data) => courseApi.post('test/',     { ...data, course: c, week_number: w }),
}
