import { createRouter, createWebHistory } from 'vue-router';
import AuthView from '@/views/AuthView.vue';
import Dashboard from '@/views/Dashboard.vue';
import TeacherDashboard from '@/components/TeacherDashboard.vue';
import StudentDashboard from '@/components/StudentDashboard.vue';
import CoursePage from '@/views/CoursePage.vue';
import store from '@/store/index'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: AuthView },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/teacher-dashboard',
    name: 'TeacherDashboard',
    component: TeacherDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/student-dashboard',
    name: 'StudentDashboard',
    component: StudentDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/course/:id',
    name: 'CoursePage',
    component: CoursePage,
    props: route => ({ id: Number(route.params.id) }),
    meta: { requiresAuth: true }
  },
]


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = store.state.auth.accessToken
  if (to.meta.requiresAuth && !token) {
    return next({ name: 'login' })
  }
  if (to.name === 'login' && token) {
    return next({ name: 'dashboard' })
  }
  next()
})

export default router
