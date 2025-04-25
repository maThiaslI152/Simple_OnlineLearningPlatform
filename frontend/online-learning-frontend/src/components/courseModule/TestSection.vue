<template>
    <section class="test-section">
        <h3>Tests (Week {{ week }})</h3>
        <ul v-if="tests.length">
            <li v-for="t in tests" :key="t.id">
                <strong>{{ t.title }}</strong>
                <p>{{ t.instructions }}</p>
            </li>
        </ul>
        <p v-else>No tests for this week.</p>

        <div v-if="isTeacher" class="add-test-form">
            <h4>Create Test</h4>
            <input v-model="newTest.title" placeholder="Title" />
            <textarea v-model="newTest.instructions" placeholder="Instructions"></textarea>
            <button @click="addTest">Save Test</button>
        </div>
    </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

const props = defineProps({
    tests: { type: Array, default: () => [] },
    week: { type: Number, required: true },
    courseId: { type: Number, required: true }
})
const emit = defineEmits(['refreshModules'])

const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)

const newTest = ref({ title: '', instructions: '' })

async function addTest() {
    if (!newTest.value.title.trim() || !newTest.value.instructions.trim()) return
    await courseService.createTest(props.courseId, props.week, newTest.value)
    newTest.value = { title: '', instructions: '' }
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