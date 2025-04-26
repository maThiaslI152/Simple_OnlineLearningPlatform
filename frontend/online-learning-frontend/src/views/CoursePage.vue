<template>
    <div class="course-page">
      <!-- Course header -->
      <h1>Course: {{ course.title }}</h1>
      <p>{{ course.description }}</p>
      <hr />
  
      <!-- Week buttons + Add Week (teachers only) -->
      <div class="weeks-buttons">
        <button
          v-for="w in weeks"
          :key="w"
          :class="['week-button', { active: w === selectedWeek }]"
          @click="selectWeek(w)"
        >
          Week {{ w }}
        </button>
        <button v-if="isTeacher" class="add-week-button" @click="addWeek">
          + Add Week
        </button>
      </div>
  
      <!-- Modules for the selected week -->
      <div v-if="selectedWeek !== null" class="module-sections">
        <NoteSection
          :notes="notes"
          :week="selectedWeek"
          :course-id="courseId"
          @refreshModules="loadModules(selectedWeek)"
        />
        <VideoSection
          :videos="videos"
          :week="selectedWeek"
          :course-id="courseId"
          @refreshModules="loadModules(selectedWeek)"
        />
        <HomeworkSection
          :homeworks="homeworks"
          :week="selectedWeek"
          :course-id="courseId"
          @refreshModules="loadModules(selectedWeek)"
        />
        <TestSection
          :tests="tests"
          :week="selectedWeek"
          :course-id="courseId"
          @refreshModules="loadModules(selectedWeek)"
        />
      </div>
    </div>
  </template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

import NoteSection from '@/components/courseModule/NoteSection.vue'
import VideoSection from '@/components/courseModule/VideoSection.vue'
import HomeworkSection from '@/components/courseModule/HomeworkSection.vue'
import TestSection from '@/components/courseModule/TestSection.vue'

// Route param
const route = useRoute()
const router = useRouter()
const courseId = computed(() => Number(route.params.id))

// Auth & role
const { isLoggedIn, user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)

// Data
const course = ref({ title: '', description: '' })
const weeks = ref([])
const selectedWeek = ref(null)

// Module lists
const notes = ref([])
const videos = ref([])
const homeworks = ref([])
const tests = ref([])

// Load course detail and available weeks
async function loadCourseDetail() {
    if (!isLoggedIn.value) {
        return router.replace({ name: 'login' })
    }
    const { data } = await courseService.getDetail(courseId.value)
    course.value = data
    weeks.value = data.available_weeks || []
    // auto-select first week if none
    if (weeks.value.length && selectedWeek.value === null) {
        selectWeek(weeks.value[0])
    }
}

// Load all modules for a given week in parallel
async function loadModules(week) {
    const [n, v, h, t] = await Promise.all([
        courseService.listNotes(courseId.value, week),
        courseService.listVideos(courseId.value, week),
        courseService.listHomework(courseId.value, week),
        courseService.listTests(courseId.value, week),
    ])
    notes.value = n.data
    videos.value = v.data
    homeworks.value = h.data
    tests.value = t.data
}

// Handle week button click
function selectWeek(week) {
    selectedWeek.value = week
    loadModules(week)
}

// Teachers can add a new week
async function addWeek() {
    await courseService.addWeek(courseId.value)
    // reload weeks list
    await loadCourseDetail()
}

// On mount: fetch everything
onMounted(async () => {
    try {
        await loadCourseDetail()
    } catch (e) {
        console.error('Failed to load course:', e)
        router.replace({ name: 'dashboard' })
    }
})
</script>

<style scoped>
.course-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.weeks-buttons {
    margin-bottom: 20px;
}

.week-button,
.add-week-button {
    margin: 5px;
    padding: 10px 15px;
    border: 1px solid #aaa;
    border-radius: 6px;
    cursor: pointer;
    background-color: #f0f0f0;
}

.week-button.active {
    background-color: #ddd;
}

.add-week-button {
    background-color: #e0ffe0;
}

.module-sections>* {
    margin-top: 20px;
}
</style>