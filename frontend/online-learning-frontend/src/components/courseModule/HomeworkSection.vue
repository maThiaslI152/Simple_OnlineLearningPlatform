<template>
    <section class="homework-section">
      <h3>Homework (Week {{ week }})</h3>
      <ul v-if="homeworks.length">
        <li v-for="h in homeworks" :key="h.id">
          <strong>{{ h.title }}</strong>
          <p>{{ h.description }}</p>
        </li>
      </ul>
      <p v-else>No homework for this week.</p>
  
      <div v-if="isTeacher" class="add-homework-form">
        <h4>Create Homework</h4>
        <input v-model="newHw.title" placeholder="Title" />
        <textarea v-model="newHw.description" placeholder="Description"></textarea>
        <button @click="addHomework">Save Homework</button>
      </div>
    </section>
  </template>
  
  <script setup>
  import { computed, ref } from 'vue'
  import { useAuth } from '@/composables/useAuth'
  import courseService from '@/services/course'
  
  const props = defineProps({
    homeworks:{ type: Array, default: () => [] },
    week:     { type: Number, required: true },
    courseId: { type: Number, required: true }
  })
  const emit = defineEmits(['refreshModules'])
  
  const { user } = useAuth()
  const isTeacher = computed(() => user.value.roles?.is_teacher)
  
  const newHw = ref({ title: '', description: '' })
  
  async function addHomework() {
    if (!newHw.value.title.trim() || !newHw.value.description.trim()) return
    await courseService.createHomework(props.courseId, props.week, newHw.value)
    newHw.value = { title: '', description: '' }
    emit('refreshModules')
  }
  </script>
  
  <style scoped>
  .homework-section { margin-top: 20px; }
  .add-homework-form input,
  .add-homework-form textarea {
    display: block;
    width: 100%;
    margin: 5px 0;
  }
  .add-homework-form button {
    margin-top: 5px;
    padding: 6px 12px;
  }
  </style>