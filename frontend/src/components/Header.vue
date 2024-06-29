<template>
    <div class="w-full min-h-[500px] bg-gradient-to-b from-yellow-400 to-yellow-500 flex flex-col items-center">
        <Navbar />
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
import Navbar from '@/components/Navbar.vue';
const smoothScroll = (target) => {
    document.querySelector(target).scrollIntoView({ behavior: 'smooth' });
}
</script>