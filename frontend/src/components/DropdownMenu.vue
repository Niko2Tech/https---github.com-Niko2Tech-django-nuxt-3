<template>
    <div class="relative">
        <button @click="toggleDropdown"
            class="px-4 py-2 text-yellow-600 font-semibold rounded shadow-lg hover:bg-gray-200 transition-all duration-100">
            <font-awesome-icon :icon="['fas', 'user']" /> {{ cliente }}
        </button>
        <div v-if="isOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-50">
            <ul>
                <li>
                    <RouterLink to="/pedidos" class="block px-4 py-2 text-gray-800 hover:bg-gray-200 w-full">Historial
                        de
                        pedidos</RouterLink>
                </li>
                <li>
                    <BotonModal @abrirModal="abrirModal($event)" id="saldo"
                        class="block px-4 py-2 text-gray-800 hover:bg-gray-200 w-full text-start">
                        Agregar
                        saldo</BotonModal>
                </li>
                <li><a href="#" @click="logout" class="block px-4 py-2 text-gray-800 hover:bg-gray-200 w-full">Salir</a>
                </li>
            </ul>
        </div>
    </div>
    <Modal @update:visible="cerrarModal()" title="Agregar saldo" :visible="modalAbierto === 'saldo'">
        <FormularioSaldo @update:visible="cerrarModal($event)" />
    </Modal>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { RouterLink } from 'vue-router'
import FormularioSaldo from '@/components/FormularioSaldo.vue';
import Modal from '@/components/Modal.vue';
import BotonModal from '@/components/BotonModal.vue';


const props = defineProps({
    cliente: {
        type: String,
        required: true
    }
})

const modalAbierto = ref(null);
function abrirModal(id) {
    modalAbierto.value = id;
}
function cerrarModal() {
    modalAbierto.value = null;
}

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
