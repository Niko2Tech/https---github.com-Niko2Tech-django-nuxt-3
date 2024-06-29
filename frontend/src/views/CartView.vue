<template>
    <Navbar />
    <main class="container mx-auto p-4 pt-20">
        <h1 class="text-2xl font-bold mb-4">Carrito de compras</h1>
        <section v-if="cart.length">
            <article v-for="item in cart" :key="item.id" class="flex items-center mb-4 p-4 border rounded-lg shadow">
                <img :src="getFullImageUrl(item.imagen)" :alt="item.nombre" class="w-24 h-24 object-cover mr-4">
                <div class="flex-1">
                    <h2 class="text-xl font-semibold">{{ item.nombre }}</h2>
                    <p class="text-gray-600">{{ item.descripcion }}</p>
                    <p class="mt-2">Precio: {{ formatter(item.precio) }}</p>
                    <p v-if="item.oferta" class="text-green-500">Descuento: {{ item.porcentaje_descuento * 100 }}%</p>
                    <p class="mt-2 font-bold">Total: {{ formatter(calculateItemTotal(item)) }}</p>
                    <input type="number" v-model.number="item.quantity" min="1" class="mt-2 p-2 border rounded w-20">
                </div>
                <button @click="handleRemoveFromCart(item)"
                    class="text-red-500 font-bold hover:text-red-400">Eliminar</button>
            </article>
            <div class="mt-6 p-4 border-t flex items-center justify-end gap-4">
                <p class="text-xl font-bold">Total Carrito: {{ formatter(calculateCartTotal()) }}</p>
                <button class="px-4 py-2 bg-yellow-500 text-white font-bold rounded hover:bg-yellow-400"
                    @click="comprarCarrito()">Comprar</button>
            </div>
        </section>
        <section v-else>
            <p class="text-gray-500">El carrito está vacío</p>
        </section>
    </main>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getCart, removeFromCart } from '@/utils/cart';
import Navbar from '@/components/Navbar.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const cart = ref([]);

onMounted(() => {
    cart.value = getCart();
});

function handleRemoveFromCart(item) {
    removeFromCart(item.id);
    cart.value = getCart();
}

function calculateItemTotal(item) {
    const price = parseFloat(item.precio);
    if (item.oferta) {
        const discount = price * parseFloat(item.porcentaje_descuento);
        return (price - discount) * item.quantity;
    }
    return price * item.quantity;
}

function calculateCartTotal() {
    return cart.value.reduce((total, item) => {
        return total + calculateItemTotal(item);
    }, 0).toFixed(2);
}

// Función para formatear moneda local Chile
function formatter(monto) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP'
    }).format(monto);
}

// Función para obtener la URL completa de la imagen
function getFullImageUrl(imagePath) {
    const baseUrl = 'http://127.0.0.1:8000';
    return `${baseUrl}${imagePath}`;
}

function comprarCarrito() {
    router.push('/checkout');
}
</script>