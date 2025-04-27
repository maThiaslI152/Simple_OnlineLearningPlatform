<template>
  <div class="dashboard container py-5">
    <!-- Loading state -->
    <div
      v-if="loading"
      class="d-flex justify-content-center align-items-center"
      style="height: 60vh;"
    >
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading…</span>
      </div>
    </div>

    <div v-else>
      <!-- Header and Add Course button -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Welcome, {{ user.username }} (Teacher)</h1>
        <button class="btn btn-primary" @click="showModal = true">
          Add Course
        </button>
      </div>

      <!-- Course list with Edit/Delete -->
      <h2>Your Courses</h2>
      <ul class="list-group mb-4">
        <li
          v-for="c in courses"
          :key="c.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          <div>
            <router-link :to="{ name: 'CoursePage', params: { id: c.id } }">
              {{ c.title }} — {{ c.description }}
            </router-link>
          </div>
          <div>
            <button
              class="btn btn-sm btn-outline-secondary me-2"
              @click="openEdit(c)"
            >
              Edit
            </button>
            <button
              class="btn btn-sm btn-danger"
              @click="confirmDelete(c.id)"
            >
              Delete
            </button>
          </div>
        </li>
      </ul>

      <!-- Add Course Modal -->
      <div
        class="modal fade"
        tabindex="-1"
        :class="{ show: showModal }"
        :style="{ display: showModal ? 'block' : 'none' }"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add New Course</h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <input
                v-model="newCourse.title"
                class="form-control mb-3"
                placeholder="Title"
                :disabled="saving"
              />
              <textarea
                v-model="newCourse.description"
                class="form-control"
                placeholder="Description"
                :disabled="saving"
              ></textarea>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="closeModal">
                Cancel
              </button>
              <button
                class="btn btn-primary"
                @click="addCourse"
                :disabled="saving"
              >
                {{ saving ? 'Saving…' : 'Create Course' }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div
        class="modal-backdrop fade"
        :class="{ show: showModal }"
        v-if="showModal"
      ></div>

      <!-- Edit Course Modal -->
      <div
        class="modal fade"
        tabindex="-1"
        :class="{ show: showEditModal }"
        :style="{ display: showEditModal ? 'block' : 'none' }"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Course</h5>
              <button type="button" class="btn-close" @click="closeEdit"></button>
            </div>
            <div class="modal-body">
              <input
                v-model="editCourseData.title"
                class="form-control mb-3"
                placeholder="Title"
                :disabled="saving"
              />
              <textarea
                v-model="editCourseData.description"
                class="form-control"
                placeholder="Description"
                :disabled="saving"
              ></textarea>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="closeEdit">
                Cancel
              </button>
              <button
                class="btn btn-primary"
                @click="updateCourse"
                :disabled="saving"
              >
                {{ saving ? 'Updating…' : 'Save Changes' }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div
        class="modal-backdrop fade"
        :class="{ show: showEditModal }"
        v-if="showEditModal"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

const { user, isLoggedIn, refresh, logout } = useAuth()
const router = useRouter()

const loading = ref(true)
const courses = ref([])
const newCourse = ref({ title: '', description: '' })
const editCourseData = ref({ id: null, title: '', description: '' })
const saving = ref(false)
const showModal = ref(false)
const showEditModal = ref(false)

onMounted(async () => {
  if (!isLoggedIn.value) return router.replace({ name: 'login' })
  try {
    await refresh()
    const { data } = await courseService.listMine()
    courses.value = data
  } catch {
    logout()
    router.replace({ name: 'login' })
  } finally {
    loading.value = false
  }
})

function closeModal() {
  showModal.value = false
  newCourse.value = { title: '', description: '' }
}

async function addCourse() {
  if (!newCourse.value.title) return
  saving.value = true
  try {
    await courseService.create(newCourse.value)
    const { data } = await courseService.listMine()
    courses.value = data
    closeModal()
  } finally {
    saving.value = false
  }
}

// Edit handlers
function openEdit(course) {
  editCourseData.value = { ...course }
  showEditModal.value = true
}
function closeEdit() {
  showEditModal.value = false
  editCourseData.value = { id: null, title: '', description: '' }
}
async function updateCourse() {
  if (!editCourseData.value.title) return
  saving.value = true
  try {
    await courseService.update(editCourseData.value.id, {
      title: editCourseData.value.title,
      description: editCourseData.value.description
    })
    const { data } = await courseService.listMine()
    courses.value = data
    closeEdit()
  } finally {
    saving.value = false
  }
}

// Delete handler
function confirmDelete(id) {
  if (confirm('Delete this course?')) deleteCourse(id)
}
async function deleteCourse(id) {
  saving.value = true
  try {
    await courseService.delete(id)
    courses.value = courses.value.filter(c => c.id !== id)
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
}
</style>