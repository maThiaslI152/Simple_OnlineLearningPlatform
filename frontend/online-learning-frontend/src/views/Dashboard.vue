<template>
  <div class="dashboard">
    <h1>Welcome to Dashboard!</h1>
    <p>You are logged in as: {{ username }} ({{ role }})</p>

    <StudentDashboard v-if="role === 'student'" />
    <TeacherDashboard v-if="role === 'teacher'" />

    <button @click="logout">Logout</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/axios';
import { useRouter } from 'vue-router';

import StudentDashboard from '@/components/StudentDashboard.vue';
import TeacherDashboard from '@/components/TeacherDashboard.vue';

const router = useRouter();
const username = ref('');
const role = ref('');

onMounted(async () => {
  const token = localStorage.getItem('access');
  if (!token) {
    router.push('/');
    return;
  }
  try {
    const whoami = await api.get('whoami/');
    username.value = whoami.data.username;
    role.value = whoami.data.role.toLowerCase(); // Safe lowercase
  } catch (error) {
    console.error('Failed to fetch user info:', error);
    router.push('/');
  }
});

const logout = () => {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
  router.push('/login');
};
</script>

<style scoped>
.dashboard {
  text-align: center;
  margin-top: 100px;
}
</style>
