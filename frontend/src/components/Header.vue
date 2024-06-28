<template>
    <div class="w-full min-h-[500px] bg-gradient-to-b from-yellow-400 to-yellow-500 flex flex-col items-center">
        <nav class="bg-white shadow-md flex w-full fixed z-50">
            <div class="container mx-auto px-4 py-2 flex justify-between items-center">
                <div class="flex items-center">
                    <img src="../assets/burgerLogo.svg" alt="Logo" class="w-12 h-12">
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
                    <RouterLink to="/login"
                        class="px-4 py-2 text-yellow-600 font-semibold rounded shadow-lg hover:bg-gray-200 transition-all duration-100">
                        <font-awesome-icon :icon="['fas', 'user']" /> {{ cliente ? cliente : 'Login' }}</RouterLink>
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
        <header
            class="container flex min-h-min flex-col md:flex-row md:h-[500px] items-center justify-between gap-4 mt-20 md:mt-0">
            <div class="flex flex-col items-start justify-center h-full md:pl-20 text-white w-1/2">
                <h1 class="text-6xl font-bold mb-4">Tienes hambre?</h1>
                <p class="text-lg mb-10">El Comilón, tiene los mejores platos para ti</p>
                <a href="#carta" @click.prevent="smoothScroll('#carta')"
                    class="px-4 py-3 bg-orange-500 text-gray-50 rounded-3xl font-medium hover:bg-orange-600">CONSULTA
                    LA
                    CARTA</a>
            </div>
            <div class="flex w-1/2 h-full flex-col md:justify-end md:items-end md:mr-20">
                <img src="../assets/img/ImageBase.png" alt="Plato de Comida" class="max-w-sm">
            </div>
        </header>
    </div>
</template>

<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { RouterLink } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { computed, defineProps } from 'vue'
const props = defineProps({
    cliente: {
        type: String,
        required: false
    },
    direccion: {
        type: String,
        required: false
    }
});

const cartStore = useCartStore();
const cartCount = computed(() => cartStore.cartCount);
const smoothScroll = (target) => {
    document.querySelector(target).scrollIntoView({ behavior: 'smooth' });
}
</script>