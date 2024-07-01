<template>
    <div class="container mx-auto p-10 shadow-xl rounded-md">
        <div class="flex items-center mb-6 justify-center">
            <img src="@/assets/burgerLogo.svg" alt="Logo" class="w-12 h-12">
            <span class="ml-2 text-2xl font-bold text-yellow-500">
                <span class="text-orange-600">EL</span> COMILON
            </span>
        </div>
        <form @submit.prevent="handleLogin" class="space-y-4">
            <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
                role="alert">
                <strong class="font-bold">Error! </strong>
                <span class="block sm:inline">{{ error }}</span>
            </div>
            <div>
                <input v-model="email" type="text" placeholder="Email" required
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
            </div>
            <div>
                <input v-model="password" type="password" placeholder="Password" required
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
            </div>
            <div>
                <button type="submit"
                    class="w-full px-4 py-2 bg-orange-600 text-white font-medium rounded-md hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500">
                    Entrar
                </button>
            </div>
            <p class="mt-4 text-center">No tienes cuenta? Ve a <a @click="$emit('mostrar-registro')"
                    class="text-yellow-600 font-medium hover:border-b hover:border-yellow-600 cursor-pointer">
                    registrarte
                </a></p>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const props = defineProps({
    redirect: {
        type: String,
        default: '/'
    }
})
const emit = defineEmits(['mostrar-registro'])

const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
    try {
        let data = await authStore.login(email.value, password.value)
        if (data.error) {
            error.value = data.error
            return
        }
        router.push(props.redirect)
    } catch (error) {
        alert('Error durante el inicio de sesión')
    }
}
</script>