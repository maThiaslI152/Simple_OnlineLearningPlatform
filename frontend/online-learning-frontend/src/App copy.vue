<template>
  <div id="app">
    <nav v-if="showNavbar" class="navbar navbar-expand-lg navbar-light bg-light shadow-sm mb-4">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand fw-bold">Online Learning</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Home</router-link>
            </li>
          </ul>
          <span class="navbar-text me-3">
            You are logged in as: <strong>{{ username }}</strong>
          </span>
          <button class="btn btn-outline-danger" @click="logout">Logout</button>
        </div>
      </div>
    </nav>

    <!-- Page Content -->
    <router-view />
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
import { computed, ref, onMounted, watchEffect } from 'vue';

const route = useRoute();
const router = useRouter();

const showNavbar = computed(() => route.path !== '/' && route.path !== '/login');
const username = ref('');

const loadUsername = () => {
  username.value = localStorage.getItem('username') || 'Unknown';
};

onMounted(() => {
  loadUsername();
});

// Refresh username every time the route changes (handles logout/login switches)
watchEffect(() => {
  loadUsername();
});

const logout = () => {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
  localStorage.removeItem('username');
  router.push('/login');
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.navbar-brand {
  font-weight: bold;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}
</style>
