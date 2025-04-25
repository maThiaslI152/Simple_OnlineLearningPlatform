<template>
  <div>
    <div class="dashboard">
      <h1>Loading your dashboard...</h1>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/axios';

const router = useRouter();
const username = ref('');
const role = ref('');

// Logout and cleanup tokens
const logout = () => {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
  router.push('/login');
};

// Check token, load user, and redirect by role
const checkAuthAndRedirect = async () => {
  const token = localStorage.getItem('access');
  const refresh = localStorage.getItem('refresh');

  if (!token || !refresh) {
    logout();
    return;
  }

  try {
    const response = await api.get('whoami/');
    username.value = response.data.username;
    role.value = response.data.role;

    if (role.value === 'teacher') {
      router.push('/teacher-dashboard');
    } else if (role.value === 'student') {
      router.push('/student-dashboard');
    } else {
      alert('Unknown role, contact admin.');
      logout();
    }
  } catch (error) {
    console.error('Token invalid or expired:', error);
    logout();
  }
};

onMounted(() => {
  checkAuthAndRedirect();
});
</script>

<style scoped>
.dashboard {
  text-align: center;
  margin-top: 100px;
}

button {
  padding: 8px 16px;
  cursor: pointer;
}
</style>
