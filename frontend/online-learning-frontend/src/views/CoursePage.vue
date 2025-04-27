<template>
  <div class="course-page container mt-4">
    <!-- Section 1: Course Info -->
    <div class="course-info card mb-4 p-4">
      <h1>{{ course.title }}</h1>
      <p>{{ course.description }}</p>
      <div class="teacher-info d-flex align-items-center">
        <img
          v-if="course.teacher.picture"
          :src="course.teacher.picture"
          alt="Teacher Photo"
          class="teacher-photo rounded-circle me-2"
        />
        <span>{{ course.teacher.name }}</span>
      </div>
    </div>

    <!-- Section 2: Weeks -->
    <div class="weeks-section card mb-4 p-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2>Weeks</h2>
        <button v-if="isTeacher" @click="addWeek" class="btn btn-primary">Add Week</button>
      </div>
      <ul class="list-group">
        <li
          v-for="week in weeks"
          :key="week"
          :class="['list-group-item', { active: week === selectedWeek } ]"
          @click="selectWeek(week)"
        >
          Week {{ week }}
        </li>
      </ul>
    </div>

    <!-- Section 3: Modules & Deadlines -->
    <div class="modules-section card p-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2>Week {{ selectedWeek }} Modules</h2>
        <div v-if="isTeacher">
          <button @click="openAdd('note')" class="btn btn-sm btn-outline-secondary me-2">Add Note</button>
          <button @click="openAdd('video')" class="btn btn-sm btn-outline-secondary me-2">Add Video</button>
          <button @click="openAdd('homework')" class="btn btn-sm btn-outline-secondary me-2">Add Homework</button>
          <button @click="openAdd('test')" class="btn btn-sm btn-outline-secondary">Add Test</button>
        </div>
      </div>

      <div v-if="!hasModules">
        <p>There is nothing this week.</p>
      </div>

      <div v-else>
        <!-- Notes -->
        <div v-if="notes.length" class="mb-3">
          <h3>Notes</h3>
          <ul class="list-group">
            <li v-for="n in notes" :key="n.id" class="list-group-item">
              <a :href="n.file_url" target="_blank">{{ n.title }}</a>
            </li>
          </ul>
        </div>

        <!-- Videos -->
        <div v-if="videos.length" class="mb-3">
          <h3>Videos</h3>
          <ul class="list-group">
            <li v-for="v in videos" :key="v.id" class="list-group-item">
              <video width="320" controls :src="v.file_url"></video>
            </li>
          </ul>
        </div>

        <!-- Homeworks -->
        <div v-if="homeworks.length" class="mb-3">
          <h3>Homeworks</h3>
          <ul class="list-group">
            <li v-for="h in homeworks" :key="h.id" class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <a :href="h.file_url" target="_blank">{{ h.title }}</a>
                <small class="text-muted ms-2">Deadline: {{ formatDate(h.deadline) || 'None' }}</small>
                <small v-if="!isTeacher" class="ms-2">Status: {{ submissions[h.id] ? 'Submitted' : 'Pending' }}</small>
              </div>
              <button v-if="isTeacher" @click="setDeadline('homework', h)" class="btn btn-sm btn-outline-primary">Set Deadline</button>
            </li>
          </ul>
        </div>

        <!-- Tests -->
        <div v-if="tests.length" class="mb-3">
          <h3>Tests</h3>
          <ul class="list-group">
            <li v-for="t in tests" :key="t.id" class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                {{ t.title }}
                <small class="text-muted ms-2">Deadline: {{ formatDate(t.deadline) || 'None' }}</small>
                <small v-if="!isTeacher" class="ms-2">Status: {{ results[t.id] ? `Completed (${results[t.id].score}%)` : 'Pending' }}</small>
              </div>
              <button v-if="isTeacher" @click="setDeadline('test', t)" class="btn btn-sm btn-outline-primary">Set Deadline</button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)
const route = useRoute()
const courseId = Number(route.params.id)

// Reactive state
const course = ref({ title: '', description: '', teacher: {} })
const weeks = ref([])
const selectedWeek = ref(null)
const notes = ref([])
const videos = ref([])
const homeworks = ref([])
const tests = ref([])
const submissions = ref({})
const results = ref({})

// Computed helper
const hasModules = computed(() =>
  notes.value.length || videos.value.length || homeworks.value.length || tests.value.length
)

function formatDate(dt) {
  return dt ? new Date(dt).toLocaleString() : null
}

// Load course metadata
async function loadCourse() {
  const { data } = await courseService.getDetail(courseId)
  course.value = {
    title: data.title,
    description: data.description,
    teacher: {
      name: data.teacher.username,
      picture: data.teacher.picture || null
    }
  }
}

// Load weeks and default selection
async function loadWeeks() {
  const { data } = await courseService.getDetail(courseId)
  weeks.value = data.available_weeks
  if (weeks.value.length) selectedWeek.value = weeks.value[0]
}

// Watch week selection and load modules
watch(selectedWeek, (newWeek) => {
  if (newWeek !== null) loadModules(newWeek)
})

// Fetch module lists for a given week
async function loadModules(week) {
  const [nRes, vRes, hRes, tRes] = await Promise.all([
    courseService.listNotes(courseId, week),
    courseService.listVideos(courseId, week),
    courseService.listHomework(courseId, week),
    courseService.listTests(courseId, week)
  ])
  notes.value = nRes.data
  videos.value = vRes.data
  homeworks.value = hRes.data
  tests.value = tRes.data
}

// Select a week from the list
function selectWeek(week) {
  selectedWeek.value = week
}

// Add a new week
async function addWeek() {
  if (!confirm('Add a new week?')) return
  try {
    await courseService.addWeek(courseId)
    await loadWeeks()
    alert('Week added')
  } catch (e) {
    console.error(e)
    alert('Failed to add week')
  }
}

// Generic module creation handler
async function openAdd(type) {
  const week = selectedWeek.value
  if (!week) {
    alert('Please select a week before adding modules.')
    return
  }

  const title = prompt(`Enter ${type} title:`)
  if (!title) return

  try {
    if (type === 'note') {
      const fd = new FormData()
      fd.append('title', title)
      const content = prompt('Enter note content:')
      if (content) fd.append('content', content)
      await courseService.createNote(courseId, week, fd)
    }
    if (type === 'video') {
      const fd = new FormData()
      fd.append('title', title)
      // TODO: implement file picker instead of prompt
      await courseService.createVideo(courseId, week, fd)
    }
    if (type === 'homework') {
      const fd = new FormData()
      fd.append('title', title)
      const desc = prompt('Enter homework description:')
      if (desc) fd.append('description', desc)
      await courseService.createHomework(courseId, week, fd)
    }
    if (type === 'test') {
      const payload = { title }
      const questionsJson = prompt('Enter questions JSON array:')
      payload.questions = JSON.parse(questionsJson)
      await courseService.createTest(courseId, week, payload)
    }
    await loadModules(week)
    alert(`${type.charAt(0).toUpperCase() + type.slice(1)} added.`)
  } catch (e) {
    console.error(e)
    alert(`Failed to add ${type}`)
  }
}

// Deadline setter (TODO: implement modal)
function setDeadline(type, item) {
  console.log('set deadline', type, item)
}

// Initial data fetch
onMounted(async () => {
  await loadCourse()
  await loadWeeks()
})
</script>

<style scoped>
.course-info,
.weeks-section,
.modules-section {
  background: #fff;
  border-radius: .5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}
.teacher-photo {
  width: 40px;
  height: 40px;
}
</style>
