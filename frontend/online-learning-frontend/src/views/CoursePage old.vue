<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'
import HomeworkSection from '@/components/courseModule/HomeworkSection.vue'
import NoteSection from '@/components/courseModule/NoteSection.vue'
import VideoSection from '@/components/courseModule/VideoSection.vue'
import TestSection from '@/components/courseModule/TestSection.vue'

const props = defineProps({ id: Number })
const { user } = useAuth()

const courseId = ref(props.id)
const course = ref({})
const weeks = ref([])
const selectedWeek = ref(1)

const notes = ref([])
const videos = ref([])
const homeworks = ref([])
const tests = ref([])

async function loadCourse() {
  const { data } = await courseService.getDetail(courseId.value)
  course.value = data
}

async function loadWeeks() {
  const { data } = await courseService.getDetail(courseId.value)
  weeks.value = data.available_weeks
}

async function loadModules() {
  const week = selectedWeek.value
  const [noteRes, videoRes, homeworkRes, testRes] = await Promise.all([
    courseService.listNotes(courseId.value, week),
    courseService.listVideos(courseId.value, week),
    courseService.listHomework(courseId.value, week),
    courseService.listTests(courseId.value, week)
  ])
  notes.value = noteRes.data
  videos.value = videoRes.data
  homeworks.value = homeworkRes.data
  tests.value = testRes.data
}

function selectWeek(week) {
  selectedWeek.value = week
  loadModules()
}

async function handleDeleteHomework(homeworkId) {
  if (confirm('Are you sure you want to delete this homework?')) {
    try {
      await courseService.deleteHomework(courseId.value, homeworkId)
      alert('Homework deleted.')
      loadModules()
    } catch (error) {
      console.error('Failed to delete homework:', error.response?.data || error)
      alert('Failed to delete homework.')
    }
  }
}

async function addWeek() {
  if (!confirm('Add a new week ?')) return
  try {
    await courseService.addWeek(courseId.value)
    await loadWeeks()    // reload available_weeks
    alert('Week added')
  } catch (err) {
    console.error('Failed to add week:', err.response?.data || err)
    alert('Failed to add week.')
  }
}

watch(
  () => props.id,
  (newId) => {
    courseId.value = newId
    loadCourse()
    loadWeeks()
    loadModules()
  }
)

onMounted(() => {
  loadCourse()
  loadWeeks()
  loadModules()
})
</script>

<template>
  <div class="container mt-4">
    <h2>Course: {{ course.title }}</h2>

    <div class="mb-3 d-flex align-items-center">
      <div>
        <button v-for="week in weeks" :key="week" @click="selectWeek(week)"
          :class="['btn', selectedWeek === week ? 'btn-primary' : 'btn-outline-primary', 'me-2']">
          Week {{ week }}
        </button>
      </div>
      <button v-if="user.roles?.is_teacher" @click="addWeek" class="btn btn-success btn-sm ms-3">
        Add Week
      </button>
    </div>

    <VideoSection :videos="videos" :week="selectedWeek" :courseId="courseId.value" @refreshModules="loadModules" />

    <NoteSection :notes="notes" :week="selectedWeek" :course-id="courseId" @refresh-modules="loadModules" />

    <HomeworkSection :homeworks="homeworks" :week="selectedWeek" :course-id="courseId" @refresh-modules="loadModules"
      @delete-homework="handleDeleteHomework" />


    <TestSection :tests="tests" :week="selectedWeek" :courseId="courseId.value" @refreshModules="loadModules" />
  </div>
</template>

<style scoped>
.container {
  max-width: 900px;
}
</style>
