<template>
    <div>
        <h3>Tests (Week {{ week }})</h3>

        <!-- No tests message -->
        <div v-if="tests.length === 0" class="alert alert-info">
            No tests for this week.
        </div>

        <!-- Accordion for tests -->
        <div v-else id="testsAccordion" class="accordion">
            <div v-for="test in tests" :key="test.id" class="accordion-item">
                <h2 :id="`headingTest${test.id}`" class="accordion-header">
                    <button class="accordion-button collapsed" type="button" @click="toggle(test.id)"
                        :aria-expanded="visibleTests.has(test.id)" :aria-controls="`collapseTest${test.id}`">
                        {{ test.title }}
                    </button>
                </h2>
                <div :id="`collapseTest${test.id}`" class="accordion-collapse collapse"
                    :class="{ show: visibleTests.has(test.id) }" :aria-labelledby="`headingTest${test.id}`"
                    data-bs-parent="#testsAccordion">
                    <div class="accordion-body">
                        <p>Questions: {{ test.questions.length }}</p>
                        <p>Time limit: {{ test.time_limit || 'No limit' }} minutes</p>
                        <a v-if="test.file_url" :href="test.file_url" target="_blank"
                            class="btn btn-sm btn-outline-primary">
                            View PDF
                        </a>
                        <div v-if="isTeacher" class="mt-2">
                            <button @click="deleteTest(test.id)" class="btn btn-sm btn-outline-danger">
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '@/composables/useAuth'
// Removed unused store import
import courseService from '@/services/course'

// Props with default to avoid undefined
const props = defineProps({
    tests: { type: Array, default: () => [] },
    week: Number,
    courseId: Number
})
const emit = defineEmits(['refreshModules'])

// Role check
const { user } = useAuth()
const isTeacher = computed(() => user.value.roles?.is_teacher)

// Accordion state
const visibleTests = ref(new Set())
function toggle(id) {
    visibleTests.value.has(id)
        ? visibleTests.value.delete(id)
        : visibleTests.value.add(id)
}

// Delete test
async function deleteTest(id) {
    if (!confirm('Delete this test?')) return
    try {
        await courseService.deleteTest(props.courseId, id)
        emit('refreshModules')
    } catch (err) {
        console.error('Failed to delete test', err)
    }
}
</script>

<style scoped>
.accordion-item {
    margin-bottom: 0.5rem;
}
</style>