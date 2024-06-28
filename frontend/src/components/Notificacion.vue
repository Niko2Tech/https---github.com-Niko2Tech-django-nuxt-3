<!-- components/Notification.vue -->
<template>
    <transition name="slide-fade">
        <div v-if="visible"
            class="fixed top-16 left-1/2 transform -translate-x-1/2 bg-green-500 text-white p-4 rounded shadow-lg z-50">
            {{ message }}
        </div>
    </transition>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
    message: {
        type: String,
        required: true
    },
    duration: {
        type: Number,
        default: 2000
    },
    llave: {
        type: [String, Number],
        required: true
    }
})

const visible = ref(true)
let timer = null

const hideNotification = () => {
    visible.value = false
}

const resetTimer = () => {
    visible.value = true
    clearTimeout(timer)
    timer = setTimeout(hideNotification, props.duration)
}

watch(() => props.llave, resetTimer)

onMounted(resetTimer)

onUnmounted(() => {
    clearTimeout(timer)
})
</script>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
    transition: opacity 0.5s;
}

.slide-fade-enter,
.slide-fade-leave-to

/* .slide-fade-leave-active in <2.1.8 */
    {
    opacity: 0;
}
</style>