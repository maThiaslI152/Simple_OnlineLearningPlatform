// src/store/index.js
import { createStore } from 'vuex'
import api from '../axios'

export default createStore({
  modules: {
    auth: {
      namespaced: true,
      state: () => ({
        accessToken:  localStorage.getItem('accessToken'),
        refreshToken: localStorage.getItem('refreshToken'),
        user:         JSON.parse(localStorage.getItem('user') || '{}')
      }),
      mutations: {
        setTokens(state, { access, refresh }) {
          state.accessToken  = access
          state.refreshToken = refresh
          localStorage.setItem('accessToken', access)
          localStorage.setItem('refreshToken', refresh)
        },
        setUser(state, user) {
          state.user = user
          localStorage.setItem('user', JSON.stringify(user))
        },
        clearAuth(state) {
          state.accessToken  = null
          state.refreshToken = null
          state.user         = {}
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          localStorage.removeItem('user')
        }
      },
      actions: {
        async login({ commit, dispatch }, creds) {
          const { data } = await api.post('token/', creds)
          commit('setTokens', data)
          await dispatch('fetchUser')
        },
        async fetchUser({ commit }) {
          const { data } = await api.get('whoami/')
          commit('setUser', data)
        },
        logout({ commit }) {
          commit('clearAuth')
          delete api.defaults.headers.common['Authorization']
        },
        async register(_, regData) {
          const endpoint = regData.isTeacher
            ? 'register/teacher/'
            : 'register/student/'
          await api.post(endpoint, {
            username:   regData.username,
            email:      regData.email,
            password:   regData.password,
            ...(regData.isTeacher && {
              expertise:  regData.expertise,
              department: regData.department
            })
          })
        }
      },
      getters: {
        isLoggedIn: state => !!state.accessToken
      }
    }
  }
})
 