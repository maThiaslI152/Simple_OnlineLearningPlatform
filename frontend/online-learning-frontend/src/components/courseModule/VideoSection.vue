<template>
    <div>
        <h3>Videos (Week {{ week }})</h3>
        <div v-if="!videos.length">No videos for this week.</div>
        <ul v-else>
            <li v-for="v in videos" :key="v.id">{{ v.title }}</li>
        </ul>

        <!-- Only teachers can upload videos -->
        <div v-if="isTeacher">
            <h4>Upload Video URL</h4>
            <input v-model="title" placeholder="Title" />
            <input v-model="url" placeholder="Video URL" />
            <button @click="saveVideo">Save Video</button>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

const props = defineProps({ videos: Array, week: Number, courseId: Number })
const emit = defineEmits(['refreshModules'])

const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)

const title = ref('')
const url = ref('')

async function saveVideo() {
    if (!title.value || !url.value) return
    await courseService.createVideo(props.courseId, props.week, {
        title: title.value,
        url: url.value,
    })
    title.value = ''
    url.value = ''
    emit('refreshModules')
}
</script>

<style scoped>
.videos-section {
    margin-top: 20px;
}

.add-video-form input {
    display: block;
    width: 100%;
    margin: 5px 0;
}

.add-video-form button {
    margin-top: 5px;
    padding: 6px 12px;
}
</style>