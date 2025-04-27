<template>
  <div class="dashboard container py-5">
    <!-- Loading state with Bootstrap spinner -->
    <div v-if="loading" class="d-flex justify-content-center align-items-center" style="height: 60vh;">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Once loaded: teacher or student dashboard -->
    <div v-else>
      <TeacherDashboard v-if="isTeacher" />
      <StudentDashboard v-else-if="isStudent" />

      <!-- Fallback unauthorized card -->
      <div v-else class="text-center mt-5">
        <div class="card mx-auto" style="max-width: 400px;">
          <div class="card-body">
            <h3 class="card-title mb-3">Unauthorized</h3>
            <p class="card-text">You don’t have access to this page.</p>
            <button @click="onLogout" class="btn btn-danger">
              Go to Login
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import TeacherDashboard from '@/components/TeacherDashboard.vue'
import StudentDashboard from '@/components/StudentDashboard.vue'

// Destructure auth composable
const { user, isLoggedIn, refresh, logout } = useAuth()
const router = useRouter()

// Flags
const loading = ref(true)
const isTeacher = computed(() => user.value.roles?.is_teacher)
const isStudent = computed(() => user.value.roles?.is_student)

// Logout + redirect helper
function onLogout() {
  logout()
  router.replace({ name: '/login' })
}

// Verify auth on mount
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
/* Override Bootstrap spacing if needed */
.dashboard {
  min-height: 100vh;
}
</style>
