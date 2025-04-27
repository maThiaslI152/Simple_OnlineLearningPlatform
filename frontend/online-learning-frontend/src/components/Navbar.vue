<!-- src/components/Navbar.vue -->
<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container-fluid">
            <!-- Brand -->
            <router-link class="navbar-brand" to="/dashboard">
                Online Learning Platform
            </router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="isLoggedIn">
                    <!-- Courses dropdown -->
                    <li class="nav-item dropdown" v-if="courses.length">
                        <a class="nav-link dropdown-toggle" href="#" id="courseDropdown" role="button"
                            data-bs-toggle="dropdown" aria-expanded="false">
                            Courses
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="courseDropdown">
                            <li v-for="c in courses" :key="c.id">
                                <router-link class="dropdown-item" :to="`/course/${c.id}`">
                                    {{ c.title }}
                                </router-link>
                            </li>
                        </ul>
                    </li>

                    <!-- Profile Settings link -->
                    <li class="nav-item">
                        <router-link class="nav-link" to="/profile">
                            Profile Settings
                        </router-link>
                    </li>
                </ul>

                <div class="d-flex align-items-center">
                    <span v-if="isLoggedIn" class="navbar-text me-3">
                        Logged in as: <strong>{{ user.username }}</strong>
                    </span>
                    <button v-if="isLoggedIn" class="btn btn-outline-light btn-sm" @click="handleLogout">
                        Logout
                    </button>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'
import courseService from '@/services/course'

const { isLoggedIn, logout, user } = useAuth()
const router = useRouter()
const courses = ref([])

async function loadCourses() {
    try {
        const { data } = await courseService.listMine()
        courses.value = data
    } catch (e) {
        console.error('Failed to load courses', e)
    }
}

// Logout + redirect by path
function handleLogout() {
    logout()
    router.replace('/login')
}

onMounted(() => {
    if (isLoggedIn.value) {
        loadCourses()
    }
})
</script>

<style scoped>
.navbar-text {
    color: #fff;
}
</style>