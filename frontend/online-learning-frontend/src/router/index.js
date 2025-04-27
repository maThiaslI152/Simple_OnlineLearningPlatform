import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/AuthView.vue'
import Dashboard from '../views/Dashboard.vue'
import TeacherDashboard from '../components/TeacherDashboard'
import StudentDashboard from '../components/StudentDashboard'
import CoursePage from '../views/CoursePage.vue'
import store from '@/store'
import ProfileSettings from '@/views/ProfileSettings.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/teacher-dashboard', component: TeacherDashboard, meta: { requiresAuth: true } },
  { path: '/student-dashboard', component: StudentDashboard, meta: { requiresAuth: true } },
  {
    path: '/course/:id',
    name: 'CoursePage',
    component: CoursePage,
    meta: { requiresAuth: true },
    props: route => ({ id: Number(route.params.id) })
  },
  {
    path: '/profile',
    name: 'ProfileSettings',
    component: ProfileSettings,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // read from Vuex directly, or from the correctly named LS key
  const token = store.state.auth.accessToken 
    || localStorage.getItem('accessToken')

  if (to.meta.requiresAuth && !token) {
    return next({ name: 'login' })
  }
  if (to.name === 'login' && token) {
    return next({ name: 'dashboard' })
  }
  next()
})

export default router
