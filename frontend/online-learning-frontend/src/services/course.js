// src/services/course.js
import axios from 'axios'
import store from '@/store'

const courseApi = axios.create({
  baseURL: 'http://localhost:8000/api/course/',
  // No default Content-Type — allows multipart/form-data
})

// Attach JWT Token
courseApi.interceptors.request.use(cfg => {
  const t = store.state.auth.accessToken
  if (t) cfg.headers.Authorization = `Bearer ${t}`
  return cfg
})

// Auto-refresh token on 401
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
  listAll:        ()                => courseApi.get(''),
  listMine:       ()                => courseApi.get('mine/'),
  getDetail:      id                => courseApi.get(`${id}/`),
  create:         payload           => courseApi.post('', payload),

  // Week management
  addWeek:        id                => courseApi.post(`${id}/add_week/`),

  // Module listings
  listNotes:      (c, w)            => courseApi.get(`${c}/note/`,     { params: { week_number: w } }),
  listVideos:     (c, w)            => courseApi.get(`${c}/video/`,    { params: { week_number: w } }),
  listHomework:   (c, w)            => courseApi.get(`${c}/homework/`, { params: { week_number: w } }),
  listTests:      (c, w)            => courseApi.get(`${c}/test/`,     { params: { week_number: w } }),
  listSubmissions: (courseId, homeworkId) => courseApi.get(`${courseId}/homework/${homeworkId}/submissions/`),
  


  // Module creation
  createNote:     (c, w, data)      => courseApi.post(`${c}/note/`, data, { headers: { 'Content-Type': 'multipart/form-data' } }),
  createVideo: (courseId, weekNumber, formData) =>
    courseApi.post(`${courseId}/video/?week_number=${weekNumber}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
  
  createHomework: (c, w, formData)  => courseApi.post(`${c}/homework/`, formData, {params: { week_number: w },headers: { 'Content-Type': 'multipart/form-data' }}),
  createTest:     (c, w, payload)   => courseApi.post(`${c}/test/`, { ...payload, course: c, week_number: w }),

  // Module deletion
  deleteNote:     (courseId, noteId) => courseApi.delete(`${courseId}/note/${noteId}/`),
  deleteHomework: (courseId, homeworkId) => courseApi.delete(`${courseId}/homework/${homeworkId}/`),
  
  // Homework submission (student)
  submitHomework: (courseId, homeworkId, formData) => courseApi.post(`${courseId}/homework/${homeworkId}/submit/`, formData),
}
