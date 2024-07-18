<template>
    <section id="carta" class="container mx-auto my-5">
        <article v-for="(categoria, index) in data" :key="index">
            <h3 class="text-3xl font-bold text-center my-8">{{ categoria.nombre }}</h3>
            <div class="flex flex-wrap gap-8 justify-center">
                <div v-for="producto in categoria.productos" :key="producto.id">
                    <CardOferta :data="producto" />
                </div>
            </div>
        </article>
    </section>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import CardOferta from './CardOferta.vue';
async function getProductos() {
    const response = await fetch('http://127.0.0.1:8000/api/producto/productos_categoria/');
    const data = await response.json();
    return data;
}

const data = ref([]);

onMounted(async () => {
    data.value = await getProductos();
});

</script>