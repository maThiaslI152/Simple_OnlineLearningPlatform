<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

const props = defineProps({
    videos: Array,
    week: Number,
    courseId: Number
})
const emit = defineEmits(['refreshModules', 'deleteVideo'])

const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)

const title = ref('')
const description = ref('')
const file = ref(null)

function onFileChange(event) {
    file.value = event.target.files[0] || null
}

async function saveVideo() {
    if (!title.value || !description.value || !file.value) {
        alert('Please fill in title, description, and select a video file.')
        return
    }

    const formData = new FormData()
    formData.append('title', title.value)
    formData.append('description', description.value)
    formData.append('file', file.value)

    try {
        await courseService.createVideo(props.courseId, props.week, formData)
        alert('Video uploaded successfully!')
        title.value = ''
        description.value = ''
        file.value = null
        emit('refreshModules')
    } catch (error) {
        console.error('Upload failed:', error.response?.data || error)
        alert('Failed to upload video.')
    }
}

function handleDelete(videoId) {
    if (confirm('Are you sure you want to delete this video?')) {
        emit('deleteVideo', videoId)
    }
}
</script>

<template>
    <div class="container mt-4">
        <h3>Videos (Week {{ week }})</h3>
        <div v-if="!videos.length" class="alert alert-info">No videos for this week.</div>
        <ul v-else class="list-group mb-4">
            <li v-for="v in videos" :key="v.id" class="list-group-item">
                <div class="d-flex justify-content-between align-items-center">
                    <span>{{ v.title }}</span>
                    <button v-if="isTeacher" @click="handleDelete(v.id)" class="btn btn-danger btn-sm">Delete</button>
                </div>

                <!-- Streaming Video Player -->
                <div class="mt-2" v-if="v.file_url">
                    <video width="640" height="360" controls>
                        <source :src="v.file_url" type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                    <p class="mt-1 text-muted">{{ v.description }}</p>
                </div>
            </li>
        </ul>

        <!-- Teacher Upload Form -->
        <div v-if="isTeacher" class="card p-3">
            <h5 class="card-title">Add Video (Upload & Stream)</h5>
            <div class="mb-3">
                <label class="form-label">Title</label>
                <input v-model="title" class="form-control" placeholder="Enter title" />
            </div>
            <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="description" class="form-control" placeholder="Enter description"></textarea>
            </div>
            <div class="mb-3">
                <label class="form-label">Choose Video File (MP4 recommended)</label>
                <input type="file" class="form-control" accept="video/*" @change="onFileChange" />
            </div>
            <button @click="saveVideo" class="btn btn-primary">Save Video</button>
        </div>
    </div>
</template>

<style scoped>
.container {
    max-width: 700px;
}
</style>
