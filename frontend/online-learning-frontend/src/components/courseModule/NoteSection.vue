<template>
    <div class="note-section">
        <h2>Notes (Week {{ weekNumber }})</h2>

        <ul>
            <li v-for="note in notes" :key="note.id">
                <strong>{{ note.title }}</strong>
                <p>{{ note.content }}</p>
            </li>
        </ul>

        <div v-if="isTeacher">
            <h3>Add New Note</h3>
            <input v-model="newNote.title" placeholder="Note Title" />
            <textarea v-model="newNote.content" placeholder="Note Content (Markdown supported)"></textarea>
            <button @click="addNote">Add Note</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { courseApi } from '@/axios';

const props = defineProps({
    courseId: Number,
    weekNumber: Number,
    isTeacher: Boolean,
});

const notes = ref([]);
const newNote = ref({
    title: '',
    content: '',
});

const loadNotes = async () => {
    try {
        const response = await courseApi.get('note/', {
            params: {
                course: props.courseId,
                week_number: props.weekNumber,  // Filter by week!
            },
        });
        notes.value = response.data;
    } catch (error) {
        console.error('Error loading notes:', error);
    }
};

const addNote = async () => {
    if (!newNote.value.title || !newNote.value.content) {
        alert('Please fill out both title and content.');
        return;
    }

    const payload = {
        title: newNote.value.title,
        content: newNote.value.content,
        course: props.courseId,
        week_number: props.weekNumber,  // Include week number here
    };

    try {
        await courseApi.post('note/', payload);
        alert('Note added successfully!');
        newNote.value = { title: '', content: '' };
        await loadNotes();
    } catch (error) {
        alert('Failed to add note.');
        console.error(error);
    }
};

onMounted(() => {
    loadNotes();
});
</script>

<style scoped>
.note-section {
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