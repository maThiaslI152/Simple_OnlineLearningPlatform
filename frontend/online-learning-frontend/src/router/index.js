import { createRouter, createWebHistory } from 'vue-router';
import AuthView from '@/views/AuthView.vue';
import Dashboard from '@/views/Dashboard.vue';
import TeacherDashboard from '@/components/TeacherDashboard.vue';
import StudentDashboard from '@/components/StudentDashboard.vue';
import CoursePage from '@/views/CoursePage.vue';

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'login',
    component: AuthView,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
  },
  {
    path: '/teacher-dashboard',
    name: 'TeacherDashboard',
    component: TeacherDashboard,
  },
  {
    path: '/student-dashboard',
    name: 'StudentDashboard',
    component: StudentDashboard,
  },
  {
    path: '/course/:id',
    name: 'CoursePage',
    component: CoursePage,
    props: route => ({ id: Number(route.params.id) })
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Token Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access');
  const protectedPages = ['dashboard', 'TeacherDashboard', 'StudentDashboard', 'coursePage'];

  if (protectedPages.includes(to.name) && !token) {
    next('/login');
  } else if (to.name === 'login' && token) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;
