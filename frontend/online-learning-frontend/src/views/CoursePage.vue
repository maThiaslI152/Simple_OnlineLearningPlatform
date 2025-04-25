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
                <button v-for="week in weeks" :key="week" @click="selectWeek(week)"
                    :class="{ active: selectedWeek === week }">
                    Week {{ week }}
                </button>
                <button @click="addWeek" class="add-week-button" v-if="isTeacher">
                    + Add Week
                </button>
            </div>

            <div v-if="selectedWeek" class="week-section">
                <h3>Content for Week {{ selectedWeek }}</h3>

                <!-- Editable area for teacher -->
                <div v-if="isTeacher">
                    <textarea v-model="weekContent[selectedWeek]"
                        placeholder="Write notes or instructions for this week"></textarea>
                    <button @click="saveWeekContent">Save Content</button>
                </div>

                <!-- View-only for students -->
                <div v-else>
                    <p>{{ weekContent[selectedWeek] || 'No content yet for this week.' }}</p>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { ref, onMounted, computed } from 'vue';
import { courseApi } from '@/axios';

const props = defineProps({
    id: Number,              // Course ID
    isTeacher: Boolean,      // Role check
});

// Reactive states
const course = ref({});
const weeks = ref([]);
const selectedWeek = ref(null);
const weekContent = ref({});  // For storing content per week

const courseId = computed(() => props.id);

// Load course info
const loadCourse = async () => {
    if (!courseId.value) {
        console.error('Course ID is missing!');
        return;
    }
    try {
        const response = await courseApi.get(`${courseId.value}/`);
        course.value = response.data;
        weeks.value = response.data.available_weeks || [];
    } catch (error) {
        console.error('Failed to load course:', error);
    }
};

// Add week (POST to backend)
const addWeek = async () => {
    try {
        await courseApi.post(`${courseId.value}/add_week/`);
        await loadCourse();  // Refresh weeks list
    } catch (error) {
        alert('Failed to add week.');
        console.error(error);
    }
};

// Select a week
const selectWeek = (weekNumber) => {
    selectedWeek.value = weekNumber;
};

// Save content logic (optional backend hookup later)
const saveWeekContent = () => {
    alert(`Content saved for Week ${selectedWeek.value}: ${weekContent.value[selectedWeek.value]}`);
};

// Initial load
onMounted(() => {
    loadCourse();
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