<template>
  <div class="dashboard">
    <!-- loading… -->
    <div v-if="loading">
      <h1>Loading your dashboard…</h1>
    </div>

    <div v-else>
      <!-- header + logout -->
      <h1>Welcome, {{ user.username }} (Teacher)</h1>
      <button @click="logout">Logout</button>
      <hr />

      <!-- your courses list -->
      <h2>Your Courses</h2>
      <ul>
        <li v-for="c in courses" :key="c.id">
          <router-link :to="{ name: 'CoursePage', params: { id: c.id } }">
            {{ c.title }} — {{ c.description }}
          </router-link>
        </li>
      </ul>

      <!-- add new course -->
      <hr />
      <h3>Add New Course</h3>
      <input v-model="newCourse.title" placeholder="Title" :disabled="saving" />
      <input v-model="newCourse.description" placeholder="Description" :disabled="saving" />
      <button @click="addCourse" :disabled="saving">
        {{ saving ? 'Saving…' : 'Create Course' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

const { user, isLoggedIn, refresh, logout } = useAuth()
const router = useRouter()
const loading = ref(true)
const courses = ref([])
const newCourse = ref({ title: '', description: '' })
const saving = ref(false)

onMounted(async () => {
  if (!isLoggedIn.value) {
    return router.replace({ name: 'login' })
  }
  try {
    await refresh()
    const { data } = await courseService.listMine()
    courses.value = data
  } catch (e) {
    console.error('TeacherDashboard onMounted error:', e)
    logout()
    return router.replace({ name: 'login' })
  } finally {
    loading.value = false
  }
})

async function addCourse() {
  if (!newCourse.value.title) return
  saving.value = true
  try {
    await courseService.create(newCourse.value)
    newCourse.value = { title: '', description: '' }
    const { data } = await courseService.listMine()
    courses.value = data
  } catch (e) {
    console.error(e)
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 600px;
  margin: 40px auto;
  font-family: sans-serif;
}

input {
  display: block;
  width: 100%;
  margin: 8px 0;
  padding: 6px
}

button {
  padding: 8px 16px;
  margin-top: 10px;
  cursor: pointer
}

a {
  color: #4caf50;
  text-decoration: none
}

a:hover {
  text-decoration: underline
}
</style>
