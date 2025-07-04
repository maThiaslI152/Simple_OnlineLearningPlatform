<template>
  <div class="dashboard container mt-5">
    <!-- loading… -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading…</span>
      </div>
    </div>

    <div v-else>
      <h1 class="mb-4">Welcome, {{ user.username }}</h1>
      <hr />

      <h2>Available Courses</h2>
      <ul class="list-group">
        <li
          v-for="c in courses"
          :key="c.id"
          class="list-group-item"
        >
          <router-link
            :to="{ name: 'CoursePage', params: { id: c.id } }"
            class="text-decoration-none"
          >
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
    // students see all courses
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
  margin: auto;
}
.list-group-item + .list-group-item {
  margin-top: 6px;
}
a {
  color: #4caf50;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
</style>
