<template>
  <div class="auth-container">
    <h1>Online Learning Platform</h1>

    <div class="form-box">
      <!-- Login Section -->
      <h2>Login</h2>
      <input v-model="loginData.username" placeholder="Username" />
      <input v-model="loginData.password" type="password" placeholder="Password" />
      <button @click="onLogin">Login</button>

      <hr />

      <!-- Register Section (unchanged) -->
      <h2>Register</h2>
      <input v-model="registerData.username" placeholder="Username" />
      <input v-model="registerData.email" placeholder="Email" />
      <input v-model="registerData.password" type="password" placeholder="Password" />
      <input v-model="registerData.confirmPassword" type="password" placeholder="Confirm Password" />
      <label>
        <input type="checkbox" v-model="registerData.isTeacher" />
        I am a teacher
      </label>
      <div v-if="registerData.isTeacher">
        <input v-model="registerData.expertise" placeholder="Expertise" />
        <input v-model="registerData.department" placeholder="Department" />
      </div>
      <button @click="onRegister" :disabled="isRegistering">
        {{ isRegistering ? 'Registering...' : 'Register' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { login, register, isLoggedIn } = useAuth()

const loginData = ref({ username: '', password: '' })
const registerData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  isTeacher: false,
  expertise: '',
  department: ''
})
const isRegistering = ref(false)

watchEffect(() => {
  console.log('AuthView — isLoggedIn:', isLoggedIn.value)
  if (isLoggedIn.value) {
    console.log('Redirecting to /dashboard')
    router.push('/dashboard')
  }
})
async function onLogin() {
  try { await login(loginData.value) }
  catch { alert('Login failed. Check credentials.') }
}

async function onRegister() {
  if (registerData.value.password !== registerData.value.confirmPassword)
    return alert('Passwords must match.')
  if (isRegistering.value) return
  isRegistering.value = true

  try {
    await register(registerData.value)
    alert('Registered! Please log in.')
  }
  catch (e) {
    const msg = e.response?.data?.username
      ? 'Username already exists.'
      : e.message
    alert('Register failed: ' + msg)
  }
  finally { isRegistering.value = false }
}
</script>


<style scoped>
.auth-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-family: sans-serif;
}

.form-box {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

input {
  display: block;
  margin: 10px auto;
  padding: 8px;
  width: 200px;
}

button {
  margin: 5px 0;
  padding: 8px;
  width: 100%;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

hr {
  margin: 20px 0;
}
</style>
