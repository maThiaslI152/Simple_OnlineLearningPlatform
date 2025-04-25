<template>
    <div class="homework-section">
        <h2>Homework</h2>

        <ul>
            <li v-for="homework in homeworks" :key="homework.id">
                {{ homework.title }} - Due: {{ homework.due_date }}
                <a :href="homework.file" target="_blank">Download</a>
            </li>
        </ul>

        <div v-if="isTeacher">
            <h3>Add New Homework</h3>
            <input v-model="newHomework.title" placeholder="Homework Title" />
            <textarea v-model="newHomework.description" placeholder="Description"></textarea>
            <input v-model="newHomework.due_date" type="date" />
            <input type="file" @change="handleFileUpload" />
            <button @click="addHomework">Add Homework</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api, { courseApi } from '@/axios';

const props = defineProps({
    courseId: Number,
    isTeacher: Boolean,
});

const homeworks = ref([]);
const newHomework = ref({
    title: '',
    description: '',
    due_date: '',
    file: null,
});

const loadHomeworks = async () => {
    try {
        const response = await courseApi.get('homework/', {
            params: { course: props.courseId },  // Optional if your API supports filtering
        });
        homeworks.value = response.data.filter(hw => hw.course === props.courseId);
    } catch (error) {
        console.error('Error loading homework:', error);
    }
};

const handleFileUpload = (e) => {
    newHomework.value.file = e.target.files[0];
};

const addHomework = async () => {
    if (!newHomework.value.title || !newHomework.value.description || !newHomework.value.file || !newHomework.value.due_date) {
        alert('Please fill out all fields and select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('title', newHomework.value.title);
    formData.append('description', newHomework.value.description);
    formData.append('due_date', newHomework.value.due_date);
    formData.append('file', newHomework.value.file);
    formData.append('course', props.courseId);

    try {
        await courseApi.post('homework/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        alert('Homework added successfully!');
        newHomework.value = { title: '', description: '', due_date: '', file: null };
        await loadHomeworks();
    } catch (error) {
        alert('Failed to add homework.');
        console.error(error);
    }
};

onMounted(() => {
    loadHomeworks();
});
</script>

<style scoped>
.homework-section {
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
    height: 80px;
}

input,
button {
    margin-top: 10px;
}
</style>