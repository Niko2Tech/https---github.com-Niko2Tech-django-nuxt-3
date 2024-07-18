<template>
    <div class="max-w-lg mx-auto bg-white p-6 rounded-lg shadow-md">
        <div class="mb-4">
            <p><span class="font-semibold">Saldo:</span> {{ formatter(saldo) }}</p>
            <p><span class="font-semibold">Dirección de envío:</span> {{ direccion }}</p>
            <p><span class="font-semibold">Total a Pagar:</span> {{ formatter(total) }}</p>
        </div>
        <div class="mb-4">
            <p class="mb-2"><span class="font-semibold">Método de Pago:</span></p>
            <p v-if="error" class="text-red-500 mb-2">{{ error }}</p>
            <div class="flex flex-wrap gap-4">
                <button @click="selectPaymentMethod('debito')"
                    :class="{ 'bg-orange-500 text-white': paymentMethod === 'debito', 'bg-gray-200': paymentMethod !== 'debito' }"
                    class="px-4 py-2 rounded-lg focus:outline-none">
                    Débito al entregar <font-awesome-icon :icon="['fas', 'credit-card']" />
                </button>
                <button @click="selectPaymentMethod('credito')"
                    :class="{ 'bg-orange-500 text-white': paymentMethod === 'credito', 'bg-gray-200': paymentMethod !== 'credito' }"
                    class="px-4 py-2 rounded-lg focus:outline-none">
                    Crédito al entregar <font-awesome-icon :icon="['fas', 'credit-card']" />
                </button>
                <button @click="selectPaymentMethod('efectivo')"
                    :class="{ 'bg-orange-500 text-white': paymentMethod === 'efectivo', 'bg-gray-200': paymentMethod !== 'efectivo' }"
                    class="px-4 py-2 rounded-lg focus:outline-none">
                    Efectivo al entregar <font-awesome-icon :icon="['fas', 'money-bill-wave']" />
                </button>
                <button @click="selectPaymentMethod('webpay')"
                    :class="{ 'bg-orange-500 text-white': paymentMethod === 'webpay', 'bg-gray-200': paymentMethod !== 'webpay' }"
                    class="px-4 py-2 rounded-lg focus:outline-none">
                    WebPay <font-awesome-icon :icon="['fas', 'globe']" />
                </button>
            </div>
        </div>

        <button @click="finalizePurchase"
            class="w-full px-4 py-2 bg-yellow-500 text-white font-semibold rounded hover:bg-yellow-400">
            Finalizar Compra
        </button>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { useCartStore } from '@/stores/cart';

const props = defineProps({
    saldo: {
        type: Number,
        required: true
    },
    direccion: {
        type: String,
        required: true
    },
    totalPagar: {
        type: Number,
        required: true
    }
});
const error = ref(null);
const paymentMethod = ref('');
const total = computed(() => {
    return Math.max(0, props.totalPagar - props.saldo);
});

const selectPaymentMethod = (method) => {
    paymentMethod.value = method;
};

const router = useRouter();
const authStore = useAuthStore();
const cartStore = useCartStore();

const finalizePurchase = async () => {
    if (!paymentMethod.value) {
        error.value = 'Debes seleccionar un método de pago';
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/api/pedido/generar_pedido/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authStore.token}`
            },
            body: JSON.stringify({
                estado: 'pendiente',
                total: props.totalPagar,
                cliente: authStore.userId,
                tipo_entrega: 'domicilio',
                direccion_entrega: props.direccion,
                productos: cartStore.cart.map(item => ({
                    id: item.id,
                    cantidad: item.quantity
                })),
                metodo_pago: paymentMethod.value,
                monto: props.totalPagar,
            })
        });

        if (!response.ok) {
            throw new Error('Error al finalizar la compra');
        }
        const data = await response.json();
        cartStore.clearCart();
        router.push('/pedidos');
    } catch (error) {
        error.value = error.message;
    }
};
function formatter(monto) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP'
    }).format(monto);
}
</script>
