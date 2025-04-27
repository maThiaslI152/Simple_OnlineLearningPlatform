<template>
  <div class="dashboard">
    <div v-if="loading">
      <h1>Loading courses…</h1>
    </div>
    <div v-else>
      <h1>Welcome, {{ user.username }} (Student)</h1>
      <button @click="logout">Logout</button>
      <hr />

      <h2>Available Courses</h2>
      <ul>
        <li v-for="c in courses" :key="c.id">
          <router-link :to="{ name: 'CoursePage', params: { id: c.id } }">
            {{ c.title }} — {{ c.description }}
          </router-link>
        </li>
      </ul>
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

onMounted(async () => {
  if (!isLoggedIn.value) {
    return router.replace({ name: 'login' })
  }
  try {
    await refresh()
    // students see all courses (or you could call a dedicated endpoint)
    const { data } = await courseService.listAll()
    courses.value = data
  } catch (e) {
    console.error('StudentDashboard error:', e)
    logout()
    router.replace({ name: 'login' })
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dashboard {
  max-width: 600px;
  margin: 40px auto;
  font-family: sans-serif;
}

button {
  padding: 8px 16px;
  margin-top: 10px;
  cursor: pointer
}

ul {
  list-style: none;
  padding: 0
}

li+li {
  margin-top: 6px
}

a {
  color: #4caf50;
  text-decoration: none
}

a:hover {
  text-decoration: underline
}
</style>
