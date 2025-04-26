<template>
  <div>
    <h3>Notes (Week {{ week }})</h3>

    <div v-if="!notes.length" class="alert alert-info">
      No notes for this week.
    </div>

    <!-- Accordion for notes -->
    <div v-else class="accordion" id="notesAccordion">
      <div
        class="accordion-item"
        v-for="n in notes"
        :key="n.id"
      >
        <h2
          class="accordion-header"
          :id="`heading${n.id}`"
        >
          <button
            class="accordion-button collapsed"
            type="button"
            @click="toggle(n.id)"
            :aria-expanded="visibleNotes.has(n.id)"
            :aria-controls="`collapse${n.id}`"
          >
            {{ n.title }}
          </button>
        </h2>
        <div
          :id="`collapse${n.id}`"
          class="accordion-collapse collapse"
          :class="{ show: visibleNotes.has(n.id) }"
          :aria-labelledby="`heading${n.id}`"
          data-bs-parent="#notesAccordion"
        >
          <div class="accordion-body">
            <p>{{ n.content }}</p>
            <a
              v-if="n.file_url"
              :href="n.file_url"
              target="_blank"
              class="btn btn-sm btn-outline-primary"
            >
              View PDF
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Only teachers can add notes -->
    <div v-if="isTeacher" class="mt-4 add-note-form">
      <h4>Add a Note</h4>
      <div class="mb-2">
        <input
          v-model="title"
          placeholder="Title"
          class="form-control"
        />
      </div>
      <div class="mb-2">
        <textarea
          v-model="content"
          placeholder="Content"
          class="form-control"
          rows="4"
        ></textarea>
      </div>
      <div class="mb-3">
        <input
          type="file"
          accept="application/pdf"
          @change="onFileChange"
          class="form-control"
        />
      </div>
      <button
        @click="saveNote"
        class="btn btn-primary"
      >
        Save Note
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
import store from '@/store'

const props = defineProps({ notes: Array, week: Number, courseId: Number })
const emit = defineEmits(['refreshModules'])

const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)

// Track which note accordions are open
const visibleNotes = ref(new Set())
function toggle(id) {
  if (visibleNotes.value.has(id)) {
    visibleNotes.value.delete(id)
  } else {
    visibleNotes.value.add(id)
  }
}

// Form fields
const title = ref('')
const content = ref('')
const file = ref(null)
function onFileChange(e) {
  const f = e.target.files[0]
  if (f && f.type === 'application/pdf') {
    file.value = f
  } else {
    file.value = null
  }
}

async function saveNote() {
  if (!title.value || !content.value) return

  const form = new FormData()
  form.append('title', title.value)
  form.append('content', content.value)
  form.append('course', props.courseId)
  form.append('week_number', props.week)
  if (file.value) {
    form.append('file', file.value)
  }

  const token = store.state.auth.accessToken
  await fetch(
    `/api/course/${props.courseId}/note/`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: form
    }
  )

  title.value = ''
  content.value = ''
  file.value = null
  emit('refreshModules')
}
</script>

<style scoped>
.add-note-form {
  margin-top: 20px;
}
.accordion-item {
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  margin-bottom: 0.5rem;
}
.accordion-button {
  background-color: #f8f9fa;
}
</style>
