// src/services/course.js
import axios from 'axios'
import store from '@/store'

const courseApi = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/api/courses/'
})

// Attach auth token
courseApi.interceptors.request.use(cfg => {
  const token = store.state.auth.accessToken
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// Handle token refresh
courseApi.interceptors.response.use(
  response => response,
  async err => {
    const { response, config } = err
    if (response?.status === 401 && store.state.auth.refreshToken) {
      const { data } = await axios.post(
        `${process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'}/api/auth/token/refresh/`,
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
  listAll:    ()               => courseApi.get(''),
  listMine:   ()               => courseApi.get('mine/'),
  getDetail:  id               => courseApi.get(`${id}/`),
  create:     data             => courseApi.post('', data),
  update:     (id, data)       => courseApi.put(`${id}/`, data),
  delete:     id               => courseApi.delete(`${id}/`),

  // — Weeks —
  listWeeks:  courseId         => courseApi.get(`${courseId}/weeks/`),
  addWeek:    (courseId, data) => courseApi.post(`${courseId}/add_week/`, data),

  // — Notes —
  listNotes:   (cId, wId)            => courseApi.get(`${cId}/weeks/${wId}/notes/`),
  createNote:  (cId, wId, fd)        => courseApi.post(
                                        `${cId}/weeks/${wId}/notes/`,
                                        fd,
                                        { headers: { 'Content-Type': 'multipart/form-data' } }
                                      ),
  deleteNote:  (cId, wId, noteId)    => courseApi.delete(`${cId}/weeks/${wId}/notes/${noteId}/`),

  // — Videos —
  listVideos:  (cId, wId)            => courseApi.get(`${cId}/weeks/${wId}/videos/`),
  createVideo: (cId, wId, fd)        => courseApi.post(
                                        `${cId}/weeks/${wId}/videos/`,
                                        fd,
                                        { headers: { 'Content-Type': 'multipart/form-data' } }
                                      ),
  deleteVideo: (cId, wId, videoId)   => courseApi.delete(`${cId}/weeks/${wId}/videos/${videoId}/`),

  // — Homework —
  listHomework:    (cId, wId)                 => courseApi.get(`${cId}/weeks/${wId}/homework/`),
  createHomework:  (cId, wId, fd)             => courseApi.post(
                                                `${cId}/weeks/${wId}/homework/`,
                                                fd,
                                                { headers: { 'Content-Type': 'multipart/form-data' } }
                                              ),
  submitHomework:  (cId, wId, hwId, fd)       => courseApi.post(
                                                `${cId}/weeks/${wId}/homework/${hwId}/submit/`,
                                                fd,
                                                { headers: { 'Content-Type': 'multipart/form-data' } }
                                              ),
  deleteHomework:  (cId, wId, hwId)           => courseApi.delete(`${cId}/weeks/${wId}/homework/${hwId}/`),
  listSubmissions: (cId, wId, hwId)           => courseApi.get(`${cId}/weeks/${wId}/homework/${hwId}/submissions/`),

  // — Tests —
  listTests:   (cId, wId)             => courseApi.get(`${cId}/weeks/${wId}/tests/`),
  createTest:  (cId, wId, payload)    => courseApi.post(
                                        `${cId}/weeks/${wId}/tests/`,
                                        payload,
                                        // tests use JSON
                                        { headers: { 'Content-Type': 'application/json' } }
                                      ),
  deleteTest:  (cId, wId, testId)     => courseApi.delete(`${cId}/weeks/${wId}/tests/${testId}/`),
}
