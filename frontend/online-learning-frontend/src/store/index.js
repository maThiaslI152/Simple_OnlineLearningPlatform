import { createStore } from 'vuex'
import api from '../axios'

export default createStore({
  modules: {
    auth: {
      namespaced: true,
      state: () => ({
        accessToken:  null,
        refreshToken: null,
        user:         {}
      }),
      mutations: {
        setTokens(state, { access, refresh }) {
          state.accessToken  = access
          state.refreshToken = refresh
        },
        setAccessToken(state, access) {
          state.accessToken = access
        },
        setUser(state, user) {
          state.user = user
        },
        clearAuth(state) {
          state.accessToken  = null
          state.refreshToken = null
          state.user         = {}
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
        },
        async register(_, regData) {
          // pick endpoint based on isTeacher flag
          const endpoint = regData.isTeacher
            ? 'register/teacher/'
            : 'register/student/'
          // build payload
          const payload = {
            username:   regData.username,
            email:      regData.email,
            password:   regData.password,
            ...(regData.isTeacher && {
              expertise:  regData.expertise,
              department: regData.department
            })
          }
          // call API; errors bubble up
          await api.post(endpoint, payload)
        }
      }
    }
  }
})
