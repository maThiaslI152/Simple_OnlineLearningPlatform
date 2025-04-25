<template>
    <section class="videos-section">
        <h3>Videos (Week {{ week }})</h3>
        <ul v-if="videos.length">
            <li v-for="v in videos" :key="v.id">
                <a :href="v.url" target="_blank">{{ v.title }}</a>
            </li>
        </ul>
        <p v-else>No videos for this week.</p>

        <div v-if="isTeacher" class="add-video-form">
            <h4>Upload Video URL</h4>
            <input v-model="newVideo.title" placeholder="Title" />
            <input v-model="newVideo.url" placeholder="Video URL" />
            <button @click="addVideo">Save Video</button>
        </div>
    </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAuth } from '@/composables/useAuth'
import courseService from '@/services/course'

const props = defineProps({
    videos: { type: Array, default: () => [] },
    week: { type: Number, required: true },
    courseId: { type: Number, required: true }
})
const emit = defineEmits(['refreshModules'])

const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)

const newVideo = ref({ title: '', url: '' })

async function addVideo() {
    if (!newVideo.value.title.trim() || !newVideo.value.url.trim()) return
    await courseService.createVideo(props.courseId, props.week, newVideo.value)
    newVideo.value = { title: '', url: '' }
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