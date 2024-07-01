<template>
    <Navbar />
    <main class="container mx-auto p-4 pt-20">
        <h1 class="text-2xl font-bold mb-4">Mis Pedidos</h1>
        <section v-if="pedidos.length">
            <article v-for="pedido in pedidos" :key="pedido.id" class="mb-4 p-4 border rounded-lg shadow">
                <h2 class="text-xl font-semibold mb-2">Pedido #{{ pedido.id }}</h2>
                <div class="my-4 flex items-center justify-between relative progress-container">
                    <div class="absolute w-full h-1 bg-gray-300 progress-line"></div>
                    <div class="absolute h-1 bg-green-500 progress-line-active"
                        :style="{ width: calculateProgressWidth(pedido.estado) }"></div>
                    <div class="text-center icon-container">
                        <font-awesome-icon :icon="['fas', 'circle-check']"
                            :class="{ 'text-green-500': isEstado('pendiente', pedido.estado) }" />
                        <p>Recibido</p>
                    </div>
                    <div class="text-center icon-container">
                        <font-awesome-icon :icon="['fas', 'fire-burner']"
                            :class="{ 'text-green-500': isEstado('en_preparacion', pedido.estado) }" />
                        <p>Preparación</p>
                    </div>
                    <div class="text-center icon-container">
                        <font-awesome-icon :icon="['fas', 'truck-fast']"
                            :class="{ 'text-green-500': isEstado('en_camino', pedido.estado) }" />
                        <p>En camino</p>
                    </div>
                    <div class="text-center icon-container">
                        <font-awesome-icon :icon="['fas', 'location-dot']"
                            :class="{ 'text-green-500': isEstado('entregado', pedido.estado) }" />
                        <p>Entregado</p>
                    </div>
                </div>
                <p class="text-gray-600 mb-2">Fecha: {{ formatDate(pedido.fecha) }}</p>
                <p class="text-gray-600 mb-2">Estado: {{ replaceUnderscore(pedido.estado) }}</p>
                <p class="text-gray-600 mb-2">Total: {{ formatter(pedido.total) }}</p>
                <p class="text-gray-600 mb-2">Tipo de entrega: {{ pedido.tipo_entrega }}</p>
                <p class="text-gray-600 mb-2">Dirección de entrega: {{ pedido.direccion_entrega }}</p>
                <p class="text-gray-600 mb-2">Fecha de actualización: {{ formatDate(pedido.fecha_actualizacion) }}</p>
                <div class="mt-4">
                    <h3 class="text-lg font-semibold mb-2">Productos:</h3>
                    <ul>
                        <li v-for="producto in pedido.productos" :key="producto.id" class="flex items-center mb-2">
                            <img :src="getFullImageUrl(producto.imagen)" :alt="producto.nombre"
                                class="w-16 h-16 object-cover mr-4">
                            <div>
                                <p class="font-semibold">{{ producto.nombre }}</p>
                                <p class="text-gray-600">{{ producto.descripcion }}</p>
                                <p class="mt-1">Precio: {{ producto.porcentaje_descuento ? formatter((producto.precio -
                                    (producto.porcentaje_descuento * producto.precio))) : formatter(producto.precio) }}
                                </p>
                            </div>
                        </li>
                    </ul>
                </div>
            </article>
        </section>
        <section v-else>
            <p class="text-gray-500 mb-4">No tienes pedidos</p>
            <RouterLink to="/" class="px-4 py-2 bg-yellow-500 text-white font-semibold rounded hover:bg-yellow-400">
                Volver al menú
            </RouterLink>
        </section>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useRouter } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
import { RouterLink } from 'vue-router';

const pedidos = ref([]);
const authStore = useAuthStore();
const router = useRouter();
const user_id = authStore.userId;

const fetchPedidos = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/pedido/pedidos_usuario/?user_id=${user_id}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authStore.token}`
            }
        });
        if (!response.ok) {
            throw new Error('Error al obtener los pedidos');
        }
        pedidos.value = await response.json();
    } catch (error) {
        console.error(error);
    }
};

onMounted(() => {
    if (!authStore.isAuthenticated) {
        router.push('/login');
    } else {
        fetchPedidos();
    }
});

function formatter(monto) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP'
    }).format(monto);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('es-CL', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getFullImageUrl(imagePath) {
    const baseUrl = 'http://127.0.0.1:8000';
    return `${baseUrl}${imagePath}`;
}

function isEstado(expected, current) {
    const estados = {
        pendiente: 1,
        en_preparacion: 2,
        en_camino: 3,
        entregado: 4
    };
    return estados[current] >= estados[expected];
}

function calculateProgressWidth(estado) {
    const estados = {
        pendiente: '0%',
        en_preparacion: '33%',
        en_camino: '66%',
        entregado: '100%'
    };
    return estados[estado] || '0%';
}

// funcion para eliminar los _ por espacios y colocar la primera letra en mayuscula
function replaceUnderscore(text) {
    return text.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
}

</script>

<style scoped>
.progress-container {
    position: relative;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.progress-line {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    height: 2px;
    background: #d1d5db;
    transform: translateY(-50%);
}

.progress-line-active {
    position: absolute;
    top: 100%;
    left: 0;
    height: 2px;
    background: #10b981;
    transform: translateY(-50%);
}

.icon-container {
    position: relative;
    z-index: 1;
}
</style>
