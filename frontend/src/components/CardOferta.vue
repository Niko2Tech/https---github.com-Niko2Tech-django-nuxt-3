<template>
    <div class="max-w-sm rounded-2xl overflow-hidden shadow-md my-4">
        <article class="relative h-48 w-full">
            <img :src="`http://127.0.0.1:8000${data.imagen}`" alt="data Imagen" class="w-full h-full object-cover" />
            <div v-if="data.oferta" class="absolute bottom-0 left-0 bg-yellow-500 text-black px-2 py-1 rounded-tr-lg">
                <div class="flex gap-1 items-center justify-center text-white ">
                    <p class="text-3xl font-semibold">{{ Math.round(data.porcentaje_descuento * 100) }}</p>
                    <div class="flex flex-col text-sm p-0 justify-center items-center">
                        <p class="font-semibold">%</p>
                        <p>Off</p>
                    </div>
                </div>
            </div>
        </article>
        <div class="px-6 py-4">
            <h3 class="font-bold text-xl mb-2">{{ data.nombre }}</h3>
            <p v-if="data.oferta" class="text-gray-700 flex gap-2">
                <span class="line-through text-gray-500">{{ formatter(data.precio) }}</span>
                <span class="font-bold text-red-500">{{ formatter((data.precio * (1 -
                    data.porcentaje_descuento)).toFixed(2)) }}</span>
            </p>
            <p v-else>
                <span class="font-semibold">{{ formatter(data.precio) }}</span>
            </p>
            <p class="text-gray-700 text-base min-w-36">
                Disponiblidad: <span :class="data.stock > 0 ? 'text-green-700' : 'text-red-500'">{{ data.stock }}</span>
            </p>
            <button @click="handleAddToCart" class="mt-4 text-white font-semibold py-2 px-4 rounded"
                :class="data.stock == 0 ? 'bg-gray-400' : 'bg-orange-500 hover:bg-orange-700'"
                :disabled="data.stock == 0">
                {{ data.disponibilidad ? 'Agregar' : 'No disponible' }}
            </button>
        </div>
    </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
import { onMounted } from 'vue';

const props = defineProps({
    data: {
        type: Object,
        required: true
    }
})

const cartStore = useCartStore()

async function handleAddToCart() {
    await cartStore.addToCart(props.data)
    // descontar stock del producto
    props.data.stock -= 1
    if (props.data.stock == 0) {
        props.data.disponibilidad = false
    }
    window.showNotification(`Producto ${props.data.nombre} agregado al carrito`)
}

onMounted(() => {
    if (props.data.stock == 0) {
        props.data.disponibilidad = false
    }
})

// función para formatear moneda local Chile
function formatter(monto) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP'
    }).format(monto)
}
</script>