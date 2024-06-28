<!-- views/Login.vue -->
<template>
    <div>
        <form @submit.prevent="handleLogin">
            <input v-model="email" type="text" placeholder="Email" required />
            <input v-model="password" type="password" placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const router = useRouter()

const authStore = useAuthStore()
const email = ref('')
const password = ref('')

const handleLogin = async () => {
    try {
        await authStore.login(email.value, password.value)
        // redirigir al index
        router.push('/')
    } catch (error) {
        alert('Error durante el inicio de sesión')
    }
}
</script>