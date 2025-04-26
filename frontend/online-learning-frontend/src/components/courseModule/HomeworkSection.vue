<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

const props = defineProps({
  homeworks: Array,
  week: Number,
  courseId: Number
})
const emit = defineEmits(['refreshModules', 'deleteHomework'])

const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)

const title = ref('')
const description = ref('')
const file = ref(null)
const expanded = ref(null) // For collapse toggle
const submissionFile = ref({}) // Store student's upload file per homework
const submissions = ref({})    // Store fetched submissions per homework

function onFileChange(event) {
  file.value = event.target.files[0] || null
}

function onSubmissionChange(hwId, event) {
  submissionFile.value[hwId] = event.target.files[0] || null
}

async function loadSubmissions(homeworkId) {
  try {
    const { data } = await courseService.listSubmissions(props.courseId, homeworkId)
    submissions.value[homeworkId] = data
  } catch (error) {
    console.error('Failed to load submissions:', error)
    submissions.value[homeworkId] = []
  }
}

function toggleExpanded(hwId) {
  expanded.value = expanded.value === hwId ? null : hwId
  if (expanded.value !== null && isTeacher.value) {
    loadSubmissions(hwId)
  }
}

async function saveHomework() {
  if (!title.value || !description.value || !file.value) {
    alert('Please fill in title, description, and select a PDF file.')
    return
  }

  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('description', description.value)
  formData.append('file', file.value)

  try {
    await courseService.createHomework(props.courseId, props.week, formData)
    alert('Homework uploaded successfully!')
    title.value = ''
    description.value = ''
    file.value = null
    emit('refreshModules')
  } catch (error) {
    console.error('Upload failed:', error.response?.data || error)
    alert('Failed to upload homework. Check the console for details.')
  }
}

async function submitHomework(hwId) {
  const subFile = submissionFile.value[hwId]
  if (!subFile) {
    alert('Please select a file to submit.')
    return
  }

  const formData = new FormData()
  formData.append('file', subFile)

  try {
    await courseService.submitHomework(props.courseId, hwId, formData)
    alert('Submission successful!')
    emit('refreshModules')
  } catch (error) {
    console.error('Submission failed:', error.response?.data || error)
    alert('Failed to submit homework.')
  }
}
</script>

<template>
  <div class="container mt-4">
    <h3>Homework (Week {{ week }})</h3>
    <div v-if="!homeworks.length" class="alert alert-info">No homework for this week.</div>
    <ul v-else class="list-group mb-4">
      <li v-for="h in homeworks" :key="h.id" class="list-group-item">
        <div class="d-flex justify-content-between align-items-center">
          <span @click="toggleExpanded(h.id)" style="cursor: pointer;">
            {{ h.title }}
          </span>
          <button v-if="isTeacher" @click="$emit('deleteHomework', h.id)" class="btn btn-danger btn-sm">Delete</button>
        </div>

        <!-- Collapse Area -->
        <div v-if="expanded === h.id" class="mt-2">
          <p><strong>Description:</strong> {{ h.description }}</p>
          <p v-if="h.file_url">
            <strong>Attached File:</strong>
            <a :href="h.file_url" target="_blank" rel="noopener noreferrer">Download PDF</a>
          </p>

          <!-- Student submission form -->
          <div v-if="!isTeacher" class="mt-3">
            <label class="form-label">Submit your work:</label>
            <input type="file" accept="application/pdf" class="form-control mb-2"
              @change="e => onSubmissionChange(h.id, e)" />
            <button @click="submitHomework(h.id)" class="btn btn-success btn-sm">Submit Homework</button>
          </div>

          <!-- Teacher: View student submissions -->
          <div v-if="isTeacher" class="mt-3">
            <strong>Student Submissions:</strong>
            <ul v-if="submissions[h.id]?.length">
              <li v-for="s in submissions[h.id]" :key="s.id">
                {{ s.student_name }}:
                <a :href="s.file_url" target="_blank" rel="noopener noreferrer">Download Submission</a>
              </li>
            </ul>
            <p v-else class="text-muted">No submissions yet.</p>
          </div>
        </div>
      </li>
    </ul>

    <!-- Teacher Upload Form -->
    <div v-if="isTeacher" class="card p-3">
      <h5 class="card-title">Add Homework (PDF Upload)</h5>
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
      <button @click="saveHomework" class="btn btn-primary">Save Homework</button>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 700px;
}
</style>
