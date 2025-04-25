<template>
    <div class="test-section">
        <h2>Tests</h2>

        <ul>
            <li v-for="test in tests" :key="test.id">
                <strong>{{ test.title }}</strong>
                <pre>{{ formatQuestions(test.questions) }}</pre>
            </li>
        </ul>

        <div v-if="isTeacher">
            <h3>Add New Test</h3>
            <input v-model="newTest.title" placeholder="Test Title (e.g., Pre-Test, Post-Test)" />
            <textarea v-model="newTest.questions" placeholder='Enter questions as JSON. Example:
  [{"question": "2+2=?", "options": ["3", "4"], "answer": "4"}]'></textarea>
            <button @click="addTest">Add Test</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { courseApi } from '@/axios';

const props = defineProps({
    courseId: Number,
    isTeacher: Boolean,
});

const tests = ref([]);
const newTest = ref({
    title: '',
    questions: '',
});

const loadTests = async () => {
    try {
        const response = await courseApi.get('test/');
        tests.value = response.data.filter(test => test.course === props.courseId);
    } catch (error) {
        console.error('Error loading tests:', error);
    }
};

const addTest = async () => {
    if (!newTest.value.title || !newTest.value.questions) {
        alert('Please fill out the title and questions.');
        return;
    }

    let questionsParsed;
    try {
        questionsParsed = JSON.parse(newTest.value.questions);
    } catch (err) {
        alert('Questions format is invalid JSON.');
        return;
    }

    const payload = {
        title: newTest.value.title,
        questions: questionsParsed,
        course: props.courseId,
    };

    try {
        await courseApi.post('test/', payload);
        alert('Test added successfully!');
        newTest.value = { title: '', questions: '' };
        await loadTests();
    } catch (error) {
        alert('Failed to add test.');
        console.error(error);
    }
};

const formatQuestions = (questions) => {
    return JSON.stringify(questions, null, 2);
};

onMounted(() => {
    loadTests();
});
</script>

<style scoped>
.test-section {
    text-align: left;
    margin-top: 30px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
}

textarea {
    display: block;
    margin-top: 10px;
    width: 100%;
    height: 100px;
}

input,
button {
    margin-top: 10px;
}
</style>