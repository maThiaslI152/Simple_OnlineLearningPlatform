<template>
  <div>
    <div class="container d-flex justify-content-center align-items-center" style="min-height: 100vh;">
      <div class="col-md-5">
        <div class="card shadow-sm p-4">
          <h1 class="text-center mb-4">Online Learning Platform</h1>

          <!-- Login Form -->
          <form @submit.prevent="onLogin">
            <div class="mb-3">
              <label for="loginUsername" class="form-label">Username</label>
              <input
                id="loginUsername"
                v-model="loginData.username"
                type="text"
                class="form-control"
                :disabled="loggingIn"
                required
              />
            </div>
            <div class="mb-3">
              <label for="loginPassword" class="form-label">Password</label>
              <input
                id="loginPassword"
                v-model="loginData.password"
                type="password"
                class="form-control"
                :disabled="loggingIn"
                required
              />
            </div>
            <button type="submit" class="btn btn-primary w-100" :disabled="loggingIn">
              {{ loggingIn ? 'Logging in…' : 'Login' }}
            </button>
            <div v-if="loginError" class="mt-2 text-danger">{{ loginError }}</div>
          </form>

          <hr class="my-4" />

          <!-- Register Button -->
          <button
            class="btn btn-secondary w-100"
            @click="showRegisterModal = true"
          >
            Register
          </button>
        </div>
      </div>
    </div>

    <!-- Register Modal -->
    <div
      v-if="showRegisterModal"
      class="modal fade show d-block"
      tabindex="-1"
      style="background: rgba(0,0,0,0.5);"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Register</h5>
            <button type="button" class="btn-close" @click="closeRegisterModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="onRegister">
              <div class="mb-3">
                <label for="regUsername" class="form-label">Username</label>
                <input
                  id="regUsername"
                  v-model="registerData.username"
                  type="text"
                  class="form-control"
                  :disabled="registering"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="regEmail" class="form-label">Email</label>
                <input
                  id="regEmail"
                  v-model="registerData.email"
                  type="email"
                  class="form-control"
                  :disabled="registering"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="regPassword" class="form-label">Password</label>
                <input
                  id="regPassword"
                  v-model="registerData.password"
                  type="password"
                  class="form-control"
                  :disabled="registering"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="regConfirm" class="form-label">Confirm Password</label>
                <input
                  id="regConfirm"
                  v-model="registerData.confirmPassword"
                  type="password"
                  class="form-control"
                  :disabled="registering"
                  required
                />
              </div>
              <div class="form-check mb-3">
                <input
                  id="isTeacher"
                  v-model="registerData.isTeacher"
                  class="form-check-input"
                  type="checkbox"
                  :disabled="registering"
                />
                <label for="isTeacher" class="form-check-label">I am a teacher</label>
              </div>
              <div v-if="registerData.isTeacher">
                <div class="mb-3">
                  <label for="expertise" class="form-label">Expertise</label>
                  <input
                    id="expertise"
                    v-model="registerData.expertise"
                    type="text"
                    class="form-control"
                    :disabled="registering"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="department" class="form-label">Department</label>
                  <input
                    id="department"
                    v-model="registerData.department"
                    type="text"
                    class="form-control"
                    :disabled="registering"
                    required
                  />
                </div>
              </div>

              <div v-if="registerError" class="alert alert-danger">{{ registerError }}</div>
              <div class="d-flex justify-content-end">
                <button
                  type="button"
                  class="btn btn-secondary me-2"
                  @click="closeRegisterModal"
                  :disabled="registering"
                >
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary" :disabled="registering">
                  {{ registering ? 'Registering…' : 'Register' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()

// Login state
const loginData = ref({ username: '', password: '' })
const loggingIn = ref(false)
const loginError = ref('')

// Register state
const showRegisterModal = ref(false)
const registerData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  isTeacher: false,
  expertise: '',
  department: ''
})
const registering = ref(false)
const registerError = ref('')

async function onLogin() {
  loginError.value = ''
  loggingIn.value = true
  try {
    await store.dispatch('auth/login', {
      username: loginData.value.username,
      password: loginData.value.password
    })
    router.replace('/dashboard')
  } catch (e) {
    loginError.value = 'Invalid credentials'
  } finally {
    loggingIn.value = false
  }
}

function closeRegisterModal() {
  showRegisterModal.value = false
  registerError.value = ''
}

async function onRegister() {
  registerError.value = ''
  if (registerData.value.password !== registerData.value.confirmPassword) {
    registerError.value = "Passwords don't match"
    return
  }
  registering.value = true
  try {
    await store.dispatch('auth/register', registerData.value)
    alert('Registration successful! You can now log in.')
    closeRegisterModal()
  } catch (e) {
    registerError.value = 'Registration failed'
  } finally {
    registering.value = false
  }
}
</script>

<style scoped>
/* No extra CSS needed */
</style>
