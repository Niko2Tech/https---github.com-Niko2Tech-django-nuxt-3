<template>
    <section v-if="ofertas && ofertas.length" class="container mx-auto my-5">
        <h2 class="text-3xl font-bold text-center my-8">Productos en oferta</h2>
        <div class="relative overflow-hidden w-full">
            <div x-data="{}" x-init="$nextTick(() => {
                        let ul = $refs.logos;
                        ul.insertAdjacentHTML('afterend', ul.outerHTML);
                        ul.nextSibling.setAttribute('aria-hidden', 'true');
                    })"
                class="w-full inline-flex flex-nowrap overflow-hidden [mask-image:_linear-gradient(to_right,transparent_0,_black_128px,_black_calc(100%-128px),transparent_100%)]">
                <ul x-ref="carousel"
                    class="flex items-center justify-center md:justify-start [&_li]:mx-8 [&_img]:max-w-none animate-infinite-scroll">
                    <li v-for="(oferta, index) in ofertas" :key="index">
                        <CardOferta :data="oferta" />
                    </li>
                </ul>
                <ul x-ref="carousel"
                    class="flex items-center justify-center md:justify-start [&_li]:mx-8 [&_img]:max-w-none animate-infinite-scroll">
                    <li v-for="(oferta, index) in ofertas" :key="index">
                        <CardOferta :data="oferta" />
                    </li>
                </ul>
            </div>
        </div>
    </section>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import CardOferta from './CardOferta.vue';

async function getOfertas() {
    const response = await fetch('http://127.0.0.1:8000/api/producto/productos_oferta/');
    const data = await response.json();
    return data;
}

const ofertas = ref([]);

onMounted(async () => {
    ofertas.value = await getOfertas();
});
</script>