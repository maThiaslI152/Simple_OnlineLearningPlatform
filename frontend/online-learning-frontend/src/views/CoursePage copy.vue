<template>
    <div class="course-page">
        <h1>Course: {{ course.title }}</h1>
        <p>{{ course.description }}</p>

        <hr />

        <h2>Notes</h2>
        <ul>
            <li v-for="note in course.notes" :key="note.id">
                <strong>{{ note.title }}</strong>
                <p>{{ note.content }}</p>
            </li>
        </ul>

        <div class="weeks-section">
            <h2>Weeks</h2>
            <div class="weeks-list">
                <button v-for="week in weeks" :key="week" class="week-button" @click="selectedWeek">
                    Week {{ week }}
                </button>
                <button @click="addWeek" class="add-week-button">+ Add Week</button>
            </div>
        </div>

        <div v-if="selectedWeek" class="week-section">
            <h3>Content for Week {{ selectedWeek }}</h3>

            <!-- Editable area for teacher -->
            <div v-if="isTeacher">
                <textarea v-model="weekContent[selectedWeek]"
                    placeholder="Write notes or instructions for this week"></textarea>
                <button @click="saveWeekContent">Save Content</button>
            </div>

            <!-- Display only if not teacher -->
            <div v-else>
                <p>{{ weekContent[selectedWeek] || 'No content yet for this week.' }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { courseApi } from '@/axios';

const weekContent = ref({}); // Store content per week

const saveWeekContent = () => {
    // You can connect this to the backend later!
    alert(`Content saved for Week ${selectedWeek}: ${weekContent.value[selectedWeek]}`);
};

const selectedWeek = ref(null)

const props = defineProps({
    id: Number,              // Accept course ID directly as Number
    isTeacher: Boolean,
});

// Use computed to safely handle the reactive prop
const courseId = computed(() => props.id);

const course = ref({});
const weeks = ref([]);
const nextWeekNumber = ref(1);  // Track next available week number

const loadCourse = async () => {
    if (!courseId.value) {
        console.error('Course ID is missing!');
        return;
    }
    try {
        const response = await courseApi.get(`${courseId.value}/`);
        course.value = response.data;
    } catch (error) {
        console.error('Failed to load course:', error);
    }
};

const loadWeeks = async () => {
    try {
        const response = await courseApi.get(`${courseId.value}/`);
        weeks.value = response.data.available_weeks || [];  // ← This line is important!
        nextWeekNumber.value = weeks.value.length > 0 ? Math.max(...weeks.value) + 1 : 1;
    } catch (error) {
        console.error('Error loading weeks:', error);
    }
};

const addWeek = async () => {
    try {
        await courseApi.post(`${courseId.value}/add_week/`);
        await loadWeeks();  // Refresh from backend
    } catch (error) {
        alert('Failed to add week.');
        console.error(error);
    }
};

onMounted(() => {
    loadCourse();
    loadWeeks();
});
</script>

<style scoped>
.course-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    color: #333;
}

ul {
    list-style: none;
    padding: 0;
}

li {
    background: #f5f5f5;
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 6px;
}

.weeks-section {
    margin-top: 30px;
}

.week-button,
.add-week-button {
    margin: 5px;
    padding: 10px 15px;
    border: 1px solid #aaa;
    border-radius: 6px;
    cursor: pointer;
    background-color: #f0f0f0;
}

.add-week-button {
    background-color: #e0ffe0;
}
</style>