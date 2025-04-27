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
        <button v-if="isTeacher" @click="addWeek" class="btn btn-primary">
          Add Week
        </button>
      </div>
      <ul class="list-group">
        <li
          v-for="week in weeks"
          :key="week"
          :class="['list-group-item', { active: week === selectedWeek }]"
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
          <button
            @click="openAdd('note')"
            class="btn btn-sm btn-outline-secondary me-2"
          >
            Add Note
          </button>
          <button
            @click="openAdd('video')"
            class="btn btn-sm btn-outline-secondary me-2"
          >
            Add Video
          </button>
          <button
            @click="openAdd('homework')"
            class="btn btn-sm btn-outline-secondary me-2"
          >
            Add Homework
          </button>
          <button
            @click="openAdd('test')"
            class="btn btn-sm btn-outline-secondary"
          >
            Add Test
          </button>
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
            <li
              v-for="n in notes"
              :key="n.id"
              class="list-group-item d-flex justify-content-between align-items-center"
              @click="selectNote(n)"
              style="cursor: pointer;"
            >
              <span>{{ n.title }}</span>
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
            <a
              v-if="activeNote.file_url"
              :href="activeNote.file_url"
              target="_blank"
              >Download File</a
            >
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
              <video
                :src="v.file_url"
                controls
                class="w-100 me-3"
              ></video>
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
                <small class="text-muted ms-2"
                  >Deadline: {{ formatDate(h.deadline) || 'None' }}</small
                >
                <small v-if="!isTeacher" class="ms-2"
                  >Status:
                  {{ submissions[h.id] ? 'Submitted' : 'Pending' }}</small
                >
              </div>
              <div>
                <button
                  v-if="isTeacher"
                  class="btn btn-sm btn-danger me-2"
                  @click.stop="deleteHomework(h.id)"
                >
                  Delete
                </button>
                <button
                  v-if="isTeacher"
                  class="btn btn-sm btn-outline-primary"
                  @click="setDeadline('homework', h)"
                >
                  Set Deadline
                </button>
              </div>
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
                <small class="text-muted ms-2"
                  >Deadline: {{ formatDate(t.deadline) || 'None' }}</small
                >
                <small v-if="!isTeacher" class="ms-2"
                  >Status:
                  {{ results[t.id]
                    ? `Completed (${results[t.id].score}%)`
                    : 'Pending' }}</small
                >
              </div>
              <div>
                <button
                  v-if="isTeacher"
                  class="btn btn-sm btn-danger me-2"
                  @click.stop="deleteTest(t.id)"
                >
                  Delete
                </button>
                <button
                  v-if="isTeacher"
                  class="btn btn-sm btn-outline-primary"
                  @click="setDeadline('test', t)"
                >
                  Set Deadline
                </button>
              </div>
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

// New state for detail view
const activeNote = ref(null)

// Helpers
const hasModules = computed(() =>
  notes.value.length ||
  videos.value.length ||
  homeworks.value.length ||
  tests.value.length
)
function formatDate(dt) {
  return dt ? new Date(dt).toLocaleString() : null
}

// Loaders
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
async function loadWeeks() {
  const { data } = await courseService.getDetail(courseId)
  weeks.value = data.available_weeks
  if (weeks.value.length) selectedWeek.value = weeks.value[0]
}
async function loadModules(week) {
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
}

// Watchers
watch(selectedWeek, (w) => {
  activeNote.value = null
  if (w !== null) loadModules(w)
})

// Handlers
function selectWeek(week) {
  selectedWeek.value = week
}
function selectNote(note) {
  activeNote.value = note
}
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
async function openAdd(type) {
  const week = selectedWeek.value
  if (!week) {
    alert('Please select a week before adding modules.')
    return
  }
  const title = prompt(`Enter ${type} title:`)
  if (!title) return
  try {
    await courseService[`create${capitalize(type)}`](courseId, week, { title })
    await loadModules(week)
  } catch (e) {
    console.error(e)
    alert(`Failed to add ${type}`)
  }
}
function capitalize(s) {
  return s[0].toUpperCase() + s.slice(1)
}

// Delete actions
async function deleteNote(id) {
  if (!confirm('Delete this note?')) return
  await courseService.deleteNote(courseId, selectedWeek.value, id)
  notes.value = notes.value.filter(n => n.id !== id)
  if (activeNote.value?.id === id) activeNote.value = null
}
async function deleteVideo(id) {
  if (!confirm('Delete this video?')) return
  await courseService.deleteVideo(courseId, selectedWeek.value, id)
  videos.value = videos.value.filter(v => v.id !== id)
}
async function deleteHomework(id) {
  if (!confirm('Delete this homework?')) return
  await courseService.deleteHomework(courseId, selectedWeek.value, id)
  homeworks.value = homeworks.value.filter(h => h.id !== id)
}
async function deleteTest(id) {
  if (!confirm('Delete this test?')) return
  await courseService.deleteTest(courseId, selectedWeek.value, id)
  tests.value = tests.value.filter(t => t.id !== id)
}

// Initial mount
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
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}
.teacher-photo {
  width: 40px;
  height: 40px;
}
</style>
