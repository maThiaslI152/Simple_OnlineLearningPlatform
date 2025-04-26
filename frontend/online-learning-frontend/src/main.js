import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import api from './axios'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const token = localStorage.getItem('accessToken')
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  store.dispatch('auth/fetchUser').catch(() => {
    store.dispatch('auth/logout')
    router.push('/login')
  })
}

createApp(App).use(store).use(router).mount('#app')
