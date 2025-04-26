<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '@/components/Navbar.vue'

const route = useRoute()

const showNavbar = computed(() => {
  return route.path !== '/login' && route.path !== '/register'
})
</script>

<template>
  <div>
    <div>
      <Navbar v-if="showNavbar" />
    </div>
    <router-view />
  </div>
</template>

<style scoped>
/* Optional: You can keep global styles here if needed */
</style>
