<!-- src/views/Dashboard.vue -->
<template>
  <div>
    <!-- show spinner while checking auth -->
    <div v-if="loading" class="dashboard">
      <h1>Loading your dashboard…</h1>
    </div>

    <!-- once loaded, display the correct dashboard -->
    <TeacherDashboard v-else-if="isTeacher" />
    <StudentDashboard v-else-if="isStudent" />

    <!-- fallback if neither -->
    <div v-else class="dashboard">
      <h1>Unauthorized</h1>
      <button @click="onLogout">Go to Login</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import TeacherDashboard from '@/components/TeacherDashboard.vue'
import StudentDashboard from '@/components/StudentDashboard.vue'

// Destructure your auth composable once
const { user, isLoggedIn, refresh, logout } = useAuth()
const router = useRouter()

// Reactive flags
const loading = ref(true)
const isTeacher = computed(() => user.value.roles?.is_teacher)
const isStudent = computed(() => user.value.roles?.is_student)

// Unified logout + redirect
function onLogout() {
  logout()
  router.replace({ name: 'login' })
}

// On mount: verify auth, fetch whoami, then hide spinner
onMounted(async () => {
  if (!isLoggedIn.value) {
    return router.replace({ name: 'login' })
  }
  try {
    await refresh()
  } catch {
    return onLogout()
  } finally {
    loading.value = false
  }
})
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
