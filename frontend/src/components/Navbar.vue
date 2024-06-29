<template>
    <nav class="bg-white shadow-md flex w-full fixed z-50 h-16">
        <div class="container mx-auto px-4 py-2 flex justify-between items-center">
            <div class="flex items-center">
                <img src="@/assets/burgerLogo.svg" alt="Logo" class="w-12 h-12">
                <span class="ml-2 text-2xl font-bold text-yellow-500"><span
                        class="text-orange-600">EL</span>COMILON</span>
            </div>
            <div class="gap-1 hidden md:flex">
                <p class="text-sm text-gray-600">Envios: </p>
                <p class="text-sm text-gray-600 font-semibold"><span class="text-yellow-600"><font-awesome-icon
                            icon="fa-solid fa-location-dot" />
                    </span> {{ direccion ? direccion : 'No disponible' }}</p>
            </div>
            <div class="flex space-x-4 items-center">
                <RouterLink to="/login" v-if="!cliente"
                    class="px-4 py-2 text-yellow-600 font-semibold rounded shadow-lg hover:bg-gray-200 transition-all duration-100">
                    <font-awesome-icon :icon="['fas', 'user']" /> Login
                </RouterLink>
                <DropdownMenu v-else :cliente="cliente" />
                <div class="relative">
                    <RouterLink to="/cart"
                        class="text-yellow-600 hover:text-yellow-500 transition-all duration-100 text-xl px-4">
                        <font-awesome-icon :icon="['fas', 'cart-shopping']" />
                        <span v-if="cartCount > 0"
                            class="absolute bottom-0 right-1 bg-red-600 text-white rounded-full text-xs w-5 h-5 flex items-center justify-center hover:bg-red-500 transition-all duration-100">
                            {{ cartCount }}
                        </span>
                    </RouterLink>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { RouterLink } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import DropdownMenu from '@/components/DropdownMenu.vue'
import { useAuthStore } from '@/stores/authStore'
import { onMounted, ref, computed } from 'vue'

const authStore = useAuthStore()
const cliente = ref('')
const direccion = ref('')
onMounted(async () => {
    cliente.value = authStore.cliente
    direccion.value = authStore.direccion
})

const cartStore = useCartStore();
const cartCount = computed(() => cartStore.cartCount);
</script>