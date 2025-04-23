<template>
  <div class="auth-container">
    <h1>Online Learning Platform</h1>

    <div class="form-box">
      <!-- Login Section -->
      <h2>Login</h2>
      <input v-model="loginData.username" placeholder="Username" />
      <input
        v-model="loginData.password"
        type="password"
        placeholder="Password"
      />
      <button @click="login">Login</button>

      <hr />

      <!-- Register Section -->
      <h2>Register</h2>
      <input v-model="registerData.username" placeholder="Username" />
      <input v-model="registerData.email" placeholder="Email" />
      <input
        v-model="registerData.password"
        type="password"
        placeholder="Password"
      />
      <input
        v-model="registerData.confirmPassword"
        type="password"
        placeholder="Confirm Password"
      />
      <label>
        <input type="checkbox" v-model="registerData.isTeacher" /> I am a
        teacher
      </label>
      <div v-if="registerData.isTeacher">
        <input
          v-model="registerData.expertise"
          placeholder="Expertise (required for teachers)"
        />
        <input
          v-model="registerData.department"
          placeholder="Department (required for teachers)"
        />
      </div>
      <button @click="register" :disabled="isRegistering">
        {{ isRegistering ? 'Registering...' : 'Register' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const isRegistering = ref(false);

const loginData = ref({ username: '', password: '' });
const registerData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  isTeacher: false,
  expertise: '',
  department: '',
});

const login = async () => {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
  try {
    const response = await api.post('token/', loginData.value);
    if (response && response.data) {
      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);

      const whoami = await api.get('whoami/');

      const role = whoami.data.role.toLowerCase();
      router.push('/dashboard');
    }
  } catch (error) {
    console.error(
      'Login Failed:',
      error.response ? error.response.data : error.message
    );
    alert('Login failed! Please check your username and password.');
  }
};

const register = async () => {
  if (registerData.value.password !== registerData.value.confirmPassword) {
    alert('Passwords do not match!');
    return;
  }

  if (isRegistering.value) return;
  isRegistering.value = true;

  try {
    const endpoint = registerData.value.isTeacher
      ? 'register/teacher/'
      : 'register/student/';

    const payload = {
      username: registerData.value.username,
      password: registerData.value.password,
      email: registerData.value.email,
    };

    if (registerData.value.isTeacher) {
      payload.expertise = registerData.value.expertise;
      payload.department = registerData.value.department;
    }

    await api.post(endpoint, payload);
    alert('Register Success! You can now log in.');
  } catch (error) {
    console.error(
      'Register Failed:',
      error.response ? error.response.data : error.message
    );
    if (error.response && error.response.data.username) {
      alert('Username already exists. Please try a different one.');
    } else {
      alert(
        'Register Failed: ' +
          (error.response ? JSON.stringify(error.response.data) : error.message)
      );
    }
  } finally {
    isRegistering.value = false;
  }
};
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
