<template>
    <section class="notes-section">
      <h3>Notes (Week {{ week }})</h3>
      <ul v-if="notes.length">
        <li v-for="n in notes" :key="n.id">
          <strong>{{ n.title }}</strong>
          <p>{{ n.content }}</p>
        </li>
      </ul>
      <p v-else>No notes for this week.</p>
  
      <div v-if="isTeacher" class="add-note-form">
        <h4>Add a Note</h4>
        <input v-model="newNote.title" placeholder="Title" />
        <textarea v-model="newNote.content" placeholder="Content"></textarea>
        <button @click="addNote">Save Note</button>
      </div>
    </section>
  </template>
  
  <script setup>
  import { computed, ref } from 'vue'
  import { useAuth } from '@/composables/useAuth'
  import courseService from '@/services/course'
  
  const props = defineProps({
    notes:    { type: Array, default: () => [] },
    week:     { type: Number, required: true },
    courseId: { type: Number, required: true }
  })
  const emit = defineEmits(['refreshModules'])
  
  const { user } = useAuth()
  const isTeacher = computed(() => user.value.roles?.is_teacher)
  
  const newNote = ref({ title: '', content: '' })
  
  async function addNote() {
    if (!newNote.value.title.trim() || !newNote.value.content.trim()) return
    await courseService.createNote(props.courseId, props.week, newNote.value)
    newNote.value = { title: '', content: '' }
    emit('refreshModules')
  }
  </script>
  
  <style scoped>
  .notes-section { margin-top: 20px; }
  .add-note-form { margin-top: 15px; }
  .add-note-form input,
  .add-note-form textarea {
    display: block;
    width: 100%;
    margin: 5px 0;
  }
  .add-note-form button {
    margin-top: 5px;
    padding: 6px 12px;
  }
  </style>