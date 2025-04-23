<template>
  <div class="dashboard">
    <h1>Welcome to Teacher Dashboard!</h1>
    <p>You are logged in as: {{ username }}</p>
    <button @click="logout">Logout</button>

    <hr />

    <h2>Your Courses</h2>
    <ul>
      <li v-for="course in teacherCourses" :key="course.id">
        {{ course.title }} - {{ course.description }}
      </li>
    </ul>

    <h3>Add New Course</h3>
    <input v-model="newCourse.title" placeholder="Course Title" />
    <input v-model="newCourse.description" placeholder="Course Description" />
    <button @click="addCourse">Add Course</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api, { courseApi } from '@/axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const whoami = ref({});
const teacherCourses = ref([]);
const newCourse = ref({ title: '', description: '' });

onMounted(async () => {
  const token = localStorage.getItem('access');
  if (!token) {
    router.push('/login');
  }
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
    teacherCourses.value = courseResponse.data.filter(
      (course) => course.teacher === whoami.value.id
    );
  } catch (error) {
    console.error('Failed to load courses:', error);
  }
};

const addCourse = async () => {
  if (!newCourse.value.title || !newCourse.value.description) {
    alert('Please fill out both title and description.');
    return;
  }
  try {
    await courseApi.post('', newCourse.value);
    alert('Course added successfully!');
    newCourse.value = { title: '', description: '' };
    await loadCourses();
  } catch (error) {
    alert('Failed to add course.');
    console.error(error);
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

input {
  margin: 5px;
  padding: 8px;
}

button {
  padding: 8px 16px;
  margin-top: 10px;
  cursor: pointer;
}
</style>
