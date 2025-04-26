<template>
  <div>
    <h3>Homework (Week {{ week }})</h3>
    <div v-if="!homeworks.length">No homework for this week.</div>
    <ul v-else>
      <li v-for="h in homeworks" :key="h.id">{{ h.title }}</li>
    </ul>

    <!-- Only teachers can create homework -->
    <div v-if="isTeacher">
      <h4>Create Homework</h4>
      <input v-model="title" placeholder="Title" />
      <textarea v-model="description" placeholder="Description"></textarea>
      <button @click="saveHomework">Save Homework</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

const props = defineProps({ homeworks: Array, week: Number, courseId: Number })
const emit = defineEmits(['refreshModules'])

const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)

const title = ref('')
const description = ref('')

async function saveHomework() {
  if (!title.value || !description.value) return
  await courseService.createHomework(props.courseId, props.week, {
    title: title.value,
    description: description.value,
  })
  title.value = ''
  description.value = ''
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