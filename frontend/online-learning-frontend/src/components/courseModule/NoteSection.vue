<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

const props = defineProps({
  notes: Array,
  week: Number,
  courseId: Number
})
const emit = defineEmits(['refreshModules'])

const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)

const title = ref('')
const description = ref('')
const file = ref(null)

function onFileChange(event) {
  file.value = event.target.files[0] || null
}

async function saveNote() {
  if (!title.value || !description.value || !file.value) {
    alert('Please fill in title, description, and select a PDF file.')
    return
  }

  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('description', description.value)
  formData.append('content', description.value)

  try {
    await courseService.createNote(props.courseId, props.week, formData)
    alert('Note uploaded successfully!')
    title.value = ''
    description.value = ''
    file.value = null
    emit('refreshModules')
  } catch (error) {
    console.error('Upload failed:', error.response?.data || error)
    alert('Failed to upload note.')
  }
}
</script>

<template>
  <div class="container mt-4">
    <h3>Notes (Week {{ week }})</h3>
    <div v-if="!notes.length" class="alert alert-info">No notes for this week.</div>
    <ul v-else class="list-group mb-4">
      <li v-for="n in notes" :key="n.id" class="list-group-item">
        <div class="d-flex justify-content-between align-items-center">
          <span>{{ n.title }}</span>
          <a :href="n.file_url" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary">
            View PDF
          </a>
        </div>
        <p class="mt-2 text-muted">{{ n.description }}</p>
      </li>
    </ul>

    <div v-if="isTeacher" class="card p-3">
      <h5 class="card-title">Add Note (PDF Upload)</h5>
      <div class="mb-3">
        <label class="form-label">Title</label>
        <input v-model="title" class="form-control" placeholder="Enter title" />
      </div>
      <div class="mb-3">
        <label class="form-label">Description</label>
        <textarea v-model="description" class="form-control" placeholder="Enter description"></textarea>
      </div>
      <div class="mb-3">
        <label class="form-label">Choose PDF File</label>
        <input type="file" class="form-control" accept="application/pdf" @change="onFileChange" />
      </div>
      <button @click="saveNote" class="btn btn-primary">Save Note</button>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 700px;
}
</style>
