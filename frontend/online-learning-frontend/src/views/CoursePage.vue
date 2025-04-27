<template>
  <div class="course-page container mt-4">
      <!-- Section 1: Course Info -->
      <div class="course-info card mb-4 p-4">
          <h1>{{ course.title }}</h1>
          <p>{{ course.description }}</p>
          <div class="teacher-info d-flex align-items-center">
              <img v-if="course.teacher.picture" :src="course.teacher.picture" alt="Teacher Photo"
                  class="teacher-photo rounded-circle me-2" />
              <span>{{ course.teacher.name }}</span>
          </div>
      </div>

      <!-- Section 2: Weeks -->
      <div class="weeks-section card mb-4 p-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
              <h2>Weeks</h2>
              <button v-if="isTeacher" @click="addWeek" class="btn btn-primary">Add Week</button>
          </div>
          <div class="list-group">
              <button
                  v-for="week in weeks"
                  :key="week"
                  @click="selectWeek(week)"
                  :class="['list-group-item list-group-item-action', { active: selectedWeek === week }]"
              >
                  Week {{ week }}
              </button>
          </div>
      </div>

      <!-- Section 3: Modules -->
      <div class="modules-section card p-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
              <h2>Modules for Week {{ selectedWeek }}</h2>
              <div v-if="isTeacher">
                  <button @click="openAdd('note')" class="btn btn-sm btn-outline-secondary me-2">Add Note</button>
                  <button @click="openAdd('video')" class="btn btn-sm btn-outline-secondary me-2">Add Video</button>
                  <button @click="openAdd('homework')" class="btn btn-sm btn-outline-secondary me-2">Add Homework</button>
                  <button @click="openAdd('test')" class="btn btn-sm btn-outline-secondary">Add Test</button>
              </div>
          </div>

          <!-- Notes -->
          <div v-if="notes.length" class="mb-3">
              <h3>Notes</h3>
              <ul class="list-group">
                  <li
                      v-for="n in notes"
                      :key="n.id"
                      class="list-group-item d-flex justify-content-between align-items-center"
                  >
                      <div @click="selectNote(n)" style="cursor: pointer;">
                          {{ n.title }}
                          <small class="text-muted ms-2">{{ formatDate(n.created_at) }}</small>
                      </div>
                      <button
                          v-if="isTeacher"
                          class="btn btn-sm btn-danger"
                          @click.stop="deleteNote(n.id)"
                      >
                          Delete
                      </button>
                  </li>
              </ul>
              <div v-if="activeNote" class="card mt-2 p-3">
                  <h5>{{ activeNote.title }}</h5>
                  <p>{{ activeNote.content }}</p>
                  <a v-if="activeNote.file_url" :href="activeNote.file_url" target="_blank">Download File</a>
              </div>
          </div>

          <!-- Videos -->
          <div v-if="videos.length" class="mb-3">
              <h3>Videos</h3>
              <ul class="list-group">
                  <li
                      v-for="v in videos"
                      :key="v.id"
                      class="list-group-item d-flex justify-content-between align-items-center"
                  >
                      <div>
                          <a :href="v.file_url" target="_blank">{{ v.title }}</a>
                          <small class="text-muted ms-2">{{ formatDate(v.created_at) }}</small>
                      </div>
                      <button
                          v-if="isTeacher"
                          class="btn btn-sm btn-danger"
                          @click.stop="deleteVideo(v.id)"
                      >
                          Delete
                      </button>
                  </li>
              </ul>
          </div>

          <!-- Homeworks -->
          <div v-if="homeworks.length" class="mb-3">
              <h3>Homeworks</h3>
              <ul class="list-group">
                  <li
                      v-for="h in homeworks"
                      :key="h.id"
                      class="list-group-item d-flex justify-content-between align-items-center"
                  >
                      <div>
                          <a :href="h.file_url" target="_blank">{{ h.title }}</a>
                          <small class="text-muted ms-2">Deadline: {{ formatDate(h.deadline) || 'None' }}</small>
                          <small v-if="!isTeacher" class="ms-2">
                              Status: {{ submissions[h.id] ? 'Submitted' : 'Pending' }}
                          </small>
                      </div>
                      <button
                          v-if="isTeacher"
                          class="btn btn-sm btn-danger"
                          @click.stop="deleteHomework(h.id)"
                      >
                          Delete
                      </button>
                  </li>
              </ul>
          </div>

          <!-- Tests -->
          <div v-if="tests.length" class="mb-3">
              <h3>Tests</h3>
              <ul class="list-group">
                  <li
                      v-for="t in tests"
                      :key="t.id"
                      class="list-group-item d-flex justify-content-between align-items-center"
                  >
                      <div>
                          {{ t.title }}
                          <small class="text-muted ms-2">Created: {{ formatDate(t.created_at) }}</small>
                      </div>
                      <button
                          v-if="isTeacher"
                          class="btn btn-sm btn-danger"
                          @click.stop="deleteTest(t.id)"
                      >
                          Delete
                      </button>
                  </li>
              </ul>
          </div>

      </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import courseService from '@/services/course'
import { useAuth } from '@/composables/useAuth'

// Auth & Routing
const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)
const route = useRoute()
const courseId = Number(route.params.id)

// State
const course = ref({ title: '', description: '', teacher: {} })
const weeks = ref([])
const selectedWeek = ref(null)
const notes = ref([])
const videos = ref([])
const homeworks = ref([])
const tests = ref([])
const submissions = ref({})
const activeNote = ref(null)

// Load course details
async function loadCourse() {
try {
  const { data } = await courseService.getDetail(courseId)
  course.value = data
  submissions.value = data.submissions || {}
} catch (e) {
  console.error(e)
}
}

// Load weeks as numbers
async function loadWeeks() {
try {
  const { data } = await courseService.listWeeks(courseId)
  weeks.value = data.map(w => w.week_number)
  if (weeks.value.length) selectedWeek.value = weeks.value[0]
} catch (e) {
  console.error(e)
}
}

// Load modules
async function loadModules(week) {
try {
  const [n, v, h, t] = await Promise.all([
    courseService.listNotes(courseId, week),
    courseService.listVideos(courseId, week),
    courseService.listHomework(courseId, week),
    courseService.listTests(courseId, week)
  ])
  notes.value = n.data
  videos.value = v.data
  homeworks.value = h.data
  tests.value = t.data
} catch (e) {
  console.error(e)
}
}

// Selectors
function selectWeek(week) {
selectedWeek.value = week
}
function selectNote(note) {
activeNote.value = note
}

// Add a module
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
    const content = prompt('Enter note content:')
    if (!content) return
    const file = await pickFile()
    const fd = new FormData()
    fd.append('title', title)
    fd.append('content', content)
    if (file) fd.append('file', file)
    await courseService.createNote(courseId, week, fd)
  } else if (type === 'video') {
    const file = await pickFile()
    if (!file) { alert('No video selected'); return }
    const fd = new FormData()
    fd.append('title', title)
    fd.append('file', file)
    await courseService.createVideo(courseId, week, fd)
  } else if (type === 'homework') {
    const description = prompt('Enter homework description:')
    if (!description) return
    const file = await pickFile()
    const fd = new FormData()
    fd.append('title', title)
    fd.append('description', description)
    if (file) fd.append('file', file)
    await courseService.createHomework(courseId, week, fd)
  } else if (type === 'test') {
    const payload = { title }
    await courseService.createTest(courseId, week, payload)
  } else {
    console.warn('Unknown module type:', type)
    return
  }

  await loadModules(week)
} catch (e) {
  console.error(e)
  alert(`Failed to add ${type}`)
}
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

// File picker for uploads
async function pickFile() {
return new Promise(resolve => {
  const input = document.createElement('input')
  input.type = 'file'
  input.onchange = () => resolve(input.files[0])
  input.click()
})
}

// Deletions
async function deleteNote(id) { try { await courseService.deleteNote(courseId, selectedWeek.value, id); await loadModules(selectedWeek.value) } catch (e) { console.error(e) } }
async function deleteVideo(id) { try { await courseService.deleteVideo(courseId, selectedWeek.value, id); await loadModules(selectedWeek.value) } catch (e) { console.error(e) } }
async function deleteHomework(id) { try { await courseService.deleteHomework(courseId, selectedWeek.value, id); await loadModules(selectedWeek.value) } catch (e) { console.error(e) } }
async function deleteTest(id) { try { await courseService.deleteTest(courseId, selectedWeek.value, id); await loadModules(selectedWeek.value) } catch (e) { console.error(e) } }

// Format date utility
function formatDate(dt) {
return dt ? new Date(dt).toLocaleString() : 'N/A'
}

// Initial load
onMounted(async () => {
await loadCourse()
await loadWeeks()
// load modules for the first week (so students see content)
if (selectedWeek.value !== null) {
  await loadModules(selectedWeek.value)
}
})
</script>

<style scoped>
.course-info,
.weeks-section,
.modules-section {
  background: #fff;
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.teacher-photo {
  width: 40px;
  height: 40px;
  object-fit: cover;
}
</style>
