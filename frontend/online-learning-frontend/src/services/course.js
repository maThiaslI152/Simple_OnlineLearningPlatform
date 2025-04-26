// src/services/course.js
import axios from 'axios'
import store from '@/store'

const courseApi = axios.create({
  baseURL: 'http://localhost:8000/api/course/'
})

// — Attach JWT to every request —
courseApi.interceptors.request.use(cfg => {
  const token = store.state.auth.accessToken
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// — Auto-refresh token on 401 —
courseApi.interceptors.response.use(
  response => response,
  async err => {
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
  }
)

export default {
  // — Course CRUD —
  listAll:    ()      => courseApi.get(''),
  listMine:   ()      => courseApi.get('mine/'),
  getDetail:  id      => courseApi.get(`${id}/`),
  create:     payload => courseApi.post('', payload),

  // — Weeks —
  addWeek:    id      => courseApi.post(`${id}/add_week/`),

  // — Module listings —
  listNotes:     (c, w) =>
    courseApi.get(`${c}/note/`, { params: { week_number: w } }),
  listVideos:    (c, w) =>
    courseApi.get(`${c}/video/`, { params: { week_number: w } }),
  listHomework:  (c, w) =>
    courseApi.get(`${c}/homework/`, { params: { week_number: w } }),
  listTests:     (c, w) =>
    courseApi.get(`${c}/test/`, { params: { week_number: w } }),
  listSubmissions: (c, h) =>
    courseApi.get(`${c}/homework/${h}/submissions/`),

  // — Module creation (with FormData) —
  createNote:       (c, w, fd) =>
    courseApi.post(
      `${c}/note/`,
      fd,
      {
        params: { week_number: w },
        headers: { 'Content-Type': 'multipart/form-data' }
      }
    ),

  createVideo:      (c, w, fd) =>
    courseApi.post(
      `${c}/video/`,
      fd,
      {
        params: { week_number: w },
        headers: { 'Content-Type': 'multipart/form-data' }
      }
    ),

  createHomework:   (c, w, fd) =>
    courseApi.post(
      `${c}/homework/`,
      fd,
      {
        params: { week_number: w },
        headers: { 'Content-Type': 'multipart/form-data' }
      }
    ),

  createTest:       (c, w, payload) =>
    courseApi.post(
      `${c}/test/`,
      { ...payload, course: c, week_number: w }
    ),

  // — Deletions —
  deleteNote:       (c, n) => courseApi.delete(`${c}/note/${n}/`),
  deleteHomework:   (c, h) => courseApi.delete(`${c}/homework/${h}/`),

  // — Student submits homework —
  submitHomework:   (c, h, fd) =>
    courseApi.post(`${c}/homework/${h}/submit/`, fd),
}
