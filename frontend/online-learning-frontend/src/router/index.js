import { createRouter, createWebHistory } from 'vue-router';
import AuthView from '@/views/AuthView.vue';
import Dashboard from '@/views/Dashboard.vue';

const routes = [
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
    path: '/',
    redirect: '/login',
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Route Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access');

  if (to.path === '/dashboard' && !token) {
    // Not logged in → kick to login
    next('/login');
  } else if (to.path === '/login' && token) {
    // Already logged in → block going back to login
    next('/dashboard');
  } else {
    // All other routes allowed
    next();
  }
});

export default router;
