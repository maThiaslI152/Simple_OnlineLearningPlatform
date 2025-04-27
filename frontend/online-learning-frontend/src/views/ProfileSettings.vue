<template>
    <div class="container mt-5" style="max-width: 500px;">
        <h2 class="mb-4">Profile Settings</h2>

        <form @submit.prevent="onSubmit" novalidate>
            <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input id="username" v-model="form.username" type="text" class="form-control" :disabled="saving"
                    required />
            </div>

            <div class="mb-3">
                <label for="picture" class="form-label">Profile Picture</label>
                <input id="picture" type="file" class="form-control" @change="onFileChange" :disabled="saving"
                    accept="image/*" />
                <div v-if="preview" class="mt-2">
                    <p class="mb-1">Preview:</p>
                    <img :src="preview" class="img-thumbnail" style="max-width: 150px;" />
                </div>
            </div>

            <button type="submit" class="btn btn-primary" :disabled="saving">
                {{ saving ? 'Saving…' : 'Save Profile' }}
            </button>
            <div v-if="error" class="mt-3 alert alert-danger">{{ error }}</div>
            <div v-if="success" class="mt-3 alert alert-success">Profile updated!</div>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import authService from '@/services/auth'

const form = ref({
    username: '',
    picture: null   // file object
})
const preview = ref('')    // data URL for preview
const saving = ref(false)
const error = ref('')
const success = ref(false)

// fetch current profile
onMounted(async () => {
    try {
        const res = await authService.whoami()
        form.value.username = res.data.username
        // if backend returns a picture URL under `picture`
        preview.value = res.data.picture || ''
    } catch (e) {
        console.error(e)
        error.value = 'Failed to load profile.'
    }
})

function onFileChange(e) {
    const file = e.target.files[0]
    if (!file) return
    form.value.picture = file

    // generate a quick preview
    const reader = new FileReader()
    reader.onload = () => { preview.value = reader.result }
    reader.readAsDataURL(file)
}

async function onSubmit() {
    error.value = ''
    success.value = false

    if (!form.value.username) {
        error.value = 'Username is required.'
        return
    }

    const data = new FormData()
    data.append('username', form.value.username)
    if (form.value.picture) {
        data.append('picture', form.value.picture)
    }

    saving.value = true
    try {
        await authService.updateProfile(data)
        success.value = true
    } catch (e) {
        console.error(e)
        error.value = 'Failed to save profile.'
    } finally {
        saving.value = false
    }
}
</script>

<style scoped>
.container {
    background: #fff;
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
</style>