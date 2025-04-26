<template>
    <div>
        <h3>Tests (Week {{ week }})</h3>
        <div v-if="!tests.length">No tests for this week.</div>
        <ul v-else>
            <li v-for="t in tests" :key="t.id">{{ t.title }}</li>
        </ul>

        <!-- Only teachers can create tests -->
        <div v-if="isTeacher">
            <h4>Create Test</h4>
            <input v-model="title" placeholder="Title" />
            <textarea v-model="questions" placeholder="Questions (JSON)"></textarea>
            <button @click="saveTest">Save Test</button>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

const props = defineProps({ tests: Array, week: Number, courseId: Number })
const emit = defineEmits(['refreshModules'])

const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)

const title = ref('')
const questions = ref('')

async function saveTest() {
    if (!title.value || !questions.value) return
    await courseService.createTest(props.courseId, props.week, {
        title: title.value,
        questions: JSON.parse(questions.value),
    })
    title.value = ''
    questions.value = ''
    emit('refreshModules')
}
</script>

<style scoped>
.test-section {
    margin-top: 20px;
}

.add-test-form input,
.add-test-form textarea {
    display: block;
    width: 100%;
    margin: 5px 0;
}

.add-test-form button {
    margin-top: 5px;
    padding: 6px 12px;
}
</style>