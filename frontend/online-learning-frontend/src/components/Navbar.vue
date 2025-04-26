<script setup>
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import courseService from '@/services/course'

const { isLoggedIn, logout, user } = useAuth()
const router = useRouter()

const courses = ref([])

async function loadCourses() {
    try {
        const { data } = await courseService.listMine()
        courses.value = data
    } catch (error) {
        console.error('Failed to load courses:', error.response?.data || error)
    }
}

function handleLogout() {
    logout()
    router.push('/login')
}

onMounted(() => {
    if (isLoggedIn.value) {
        loadCourses()
    }
})
</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container-fluid">
            <!-- Brand links to dashboard -->
            <router-link class="navbar-brand" to="/dashboard">
                Online Learning Platform
            </router-link>

            <div class="collapse navbar-collapse">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="isLoggedIn">
                    <!-- Dropdown for courses -->
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
                </ul>

                <div class="d-flex">
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

<style scoped>
.navbar-text {
    color: #fff;
}
</style>
