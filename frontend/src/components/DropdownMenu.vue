<template>
    <div class="relative">
        <button @click="toggleDropdown"
            class="px-4 py-2 text-yellow-600 font-semibold rounded shadow-lg hover:bg-gray-200 transition-all duration-100">
            <font-awesome-icon :icon="['fas', 'user']" /> {{ cliente }}
        </button>
        <div v-if="isOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-50">
            <ul>
                <li><a href="#" class="block px-4 py-2 text-gray-800 hover:bg-gray-200">Historial de pedidos</a></li>
                <li><a href="#" class="block px-4 py-2 text-gray-800 hover:bg-gray-200">Ajustes</a></li>
                <li><a href="#" @click="logout" class="block px-4 py-2 text-gray-800 hover:bg-gray-200">Salir</a></li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'


const props = defineProps({
    cliente: {
        type: String,
        required: true
    }
})

const isOpen = ref(false)
const authStore = useAuthStore()

const toggleDropdown = () => {
    isOpen.value = !isOpen.value
}

const logout = () => {
    authStore.logout()
    window.location.href = '/'
}
</script>
