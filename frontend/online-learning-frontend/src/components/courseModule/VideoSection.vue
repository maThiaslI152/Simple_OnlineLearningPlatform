<template>
    <div class="video-section">
        <h2>Videos</h2>

        <ul>
            <li v-for="video in videos" :key="video.id">
                <strong>{{ video.title }}</strong>
                <video v-if="video.video_file" :src="video.video_file" controls width="400"></video>
            </li>
        </ul>

        <div v-if="isTeacher">
            <h3>Add New Video</h3>
            <input v-model="newVideo.title" placeholder="Video Title" />
            <input type="file" @change="handleFileUpload" />
            <button @click="addVideo">Add Video</button>
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

const videos = ref([]);
const newVideo = ref({
    title: '',
    video_file: null,
});

const loadVideos = async () => {
    try {
        const response = await courseApi.get('video/');
        videos.value = response.data.filter(video => video.course === props.courseId);
    } catch (error) {
        console.error('Error loading videos:', error);
    }
};

const handleFileUpload = (e) => {
    newVideo.value.video_file = e.target.files[0];
};

const addVideo = async () => {
    if (!newVideo.value.title || !newVideo.value.video_file) {
        alert('Please provide both title and video file.');
        return;
    }

    const formData = new FormData();
    formData.append('title', newVideo.value.title);
    formData.append('video_file', newVideo.value.video_file);
    formData.append('course', props.courseId);

    try {
        await courseApi.post('video/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        alert('Video added successfully!');
        newVideo.value = { title: '', video_file: null };
        await loadVideos();
    } catch (error) {
        alert('Failed to add video.');
        console.error(error);
    }
};

onMounted(() => {
    loadVideos();
});
</script>

<style scoped>
.video-section {
    text-align: left;
    margin-top: 30px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
}

video {
    margin-top: 10px;
}

input,
button {
    margin-top: 10px;
}
</style>