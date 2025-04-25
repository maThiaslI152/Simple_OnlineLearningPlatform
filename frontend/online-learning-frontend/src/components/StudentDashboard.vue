<template>
  <div class="dashboard">
    <h1>Welcome to Student Dashboard!</h1>
    <p>You are logged in as: {{ username }}</p>
    <button @click="logout">Logout</button>

    <hr />

    <h2>Your Enrolled Courses</h2>
    <ul>
      <li v-for="course in studentCourses" :key="course.id">
        {{ course.title }} - {{ course.description }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api, { courseApi } from '@/axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const whoami = ref({});
const studentCourses = ref([]);

onMounted(async () => {
  try {
    const userResponse = await api.get('whoami/');
    whoami.value = userResponse.data;
    username.value = whoami.value.username;
    await loadCourses();
  } catch (error) {
    console.error('Failed to fetch user info:', error);
    router.push('/login');
  }
});

const loadCourses = async () => {
  try {
    const courseResponse = await courseApi.get('');
    studentCourses.value = courseResponse.data;
  } catch (error) {
    console.error('Failed to load courses:', error);
  }
};

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

button {
  padding: 8px 16px;
  margin-top: 10px;
  cursor: pointer;
}
</style>
