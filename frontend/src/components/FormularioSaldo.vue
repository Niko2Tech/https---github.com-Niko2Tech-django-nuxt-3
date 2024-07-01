<template>
    <section class="container mx-auto p-4">
        <div class="max-w-lg mx-auto bg-white p-6">
            <h2 class="text-2xl font-bold mb-4">Saldo Actual</h2>
            <p class="text-xl mb-4">Saldo: {{ formatter(authStore.saldo) }}</p>
            <div class="mb-4">
                <label for="addSaldo" class="block text-gray-700 font-bold mb-2">Agregar Saldo</label>
                <input type="number" id="addSaldo" v-model.number="montoAgregar" class="mt-2 p-2 border rounded w-full"
                    placeholder="Ingrese monto a agregar">
            </div>
            <div class="mb-4">
                <p class="mb-2"><span class="font-semibold">Método de Pago:</span></p>
                <p v-if="error" class="text-red-500 mb-2">{{ error }}</p>
                <div class="flex flex-wrap gap-4">
                    <button @click="selectPaymentMethod('debito')"
                        :class="{ 'bg-orange-500 text-white': paymentMethod === 'debito', 'bg-gray-200': paymentMethod !== 'debito' }"
                        class="px-4 py-2 rounded-lg focus:outline-none">
                        Débito <font-awesome-icon :icon="['fas', 'credit-card']" />
                    </button>
                    <button @click="selectPaymentMethod('credito')"
                        :class="{ 'bg-orange-500 text-white': paymentMethod === 'credito', 'bg-gray-200': paymentMethod !== 'credito' }"
                        class="px-4 py-2 rounded-lg focus:outline-none">
                        Crédito <font-awesome-icon :icon="['fas', 'credit-card']" />
                    </button>
                    <button @click="selectPaymentMethod('webpay')"
                        :class="{ 'bg-orange-500 text-white': paymentMethod === 'webpay', 'bg-gray-200': paymentMethod !== 'webpay' }"
                        class="px-4 py-2 rounded-lg focus:outline-none">
                        WebPay <font-awesome-icon :icon="['fas', 'globe']" />
                    </button>
                </div>
            </div>
            <div v-if="paymentMethod === 'debito' || paymentMethod === 'credito'" class="mb-4">
                <label for="cardNumber" class="block text-gray-700 font-bold mb-2">Número de Tarjeta</label>
                <input type="text" id="cardNumber" v-model="cardNumber" class="mt-2 p-2 border rounded w-full"
                    placeholder="Ingrese número de tarjeta" @input="validateCardNumber" maxlength="16">
                <div class="flex gap-4">
                    <input type="text" id="expiryDate" v-model="expiryDate" class="mt-2 p-2 border rounded w-full"
                        placeholder="MM/AAAA" @input="validateExpiryDate">
                    <input type="text" id="cvv" v-model="cvv" class="mt-2 p-2 border rounded w-full"
                        placeholder="Ingrese CVV" maxlength="3">
                </div>
            </div>
            <button @click="agregarSaldo"
                class="w-full bg-green-500 text-white py-2 rounded-lg focus:outline-none hover:bg-green-600">
                Agregar Saldo
            </button>
        </div>
    </section>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

const emit = defineEmits(['update:visible']);

const authStore = useAuthStore();
const montoAgregar = ref(0);
const paymentMethod = ref('');
const cardNumber = ref('');
const expiryDate = ref('');
const cvv = ref('');
const error = ref(null);

const selectPaymentMethod = (method) => {
    paymentMethod.value = method;
    error.value = null;  // Clear any previous errors
};

const validateCardNumber = () => {
    const regex = /^[0-9]{16}$/;
    if (!regex.test(cardNumber.value)) {
        error.value = 'Número de tarjeta no válido. Debe contener 16 dígitos.';
    } else {
        error.value = null;
    }
};

watch(expiryDate, (newValue) => {
    let value = newValue.replace(/[^0-9]/g, '');
    if (value.length > 6) value = value.slice(0, 6);
    if (value.length >= 3) value = value.slice(0, 2) + '/' + value.slice(2);
    expiryDate.value = value;

    validateExpiryDate();
});

const validateExpiryDate = () => {
    const regex = /^(0[1-9]|1[0-2])\/\d{4}$/;
    if (!regex.test(expiryDate.value)) {
        error.value = 'La fecha de vencimiento no es válida.';
        return;
    }

    const [month, year] = expiryDate.value.split('/');
    const expiry = new Date(year, month - 1);
    const currentDate = new Date();

    if (expiry < currentDate) {
        error.value = 'La fecha de vencimiento no es válida.';
    } else {
        error.value = null;
    }
};

const agregarSaldo = async () => {
    if (!paymentMethod.value) {
        error.value = 'Debes seleccionar un método de pago';
        return;
    }

    if (montoAgregar.value <= 0) {
        error.value = 'Debes ingresar un monto válido';
        return;
    }

    if (paymentMethod.value === 'debito' || paymentMethod.value === 'credito') {
        if (!cardNumber.value || error.value) {
            error.value = 'Debes ingresar un número de tarjeta válido';
            return;
        }

        if (!expiryDate.value || error.value) {
            error.value = 'Debes ingresar una fecha de vencimiento válida';
            return;
        }

        if (!cvv.value || cvv.value.length !== 3) {
            error.value = 'Debes ingresar un código de seguridad válido';
            return;
        }
    }

    const formValues = {
        user_id: authStore.userId,
        saldo_cuenta: montoAgregar.value,
    };

    // enviamos los datos al backend
    const response = await fetch('http://127.0.0.1:8000/api/cliente/agregar_saldo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}`
        },
        body: JSON.stringify(formValues)
    });

    if (response.ok) {
        const data = await response.json();
        authStore.saldo = data.saldo;
        montoAgregar.value = 0;
        paymentMethod.value = '';
        cardNumber.value = '';
        expiryDate.value = '';
        cvv.value = '';
        error.value = null;
        emit('update:visible', false);
    } else {
        error.value = 'Ha ocurrido un error al agregar saldo. Por favor, intenta nuevamente.';
    }
};

onMounted(() => {
    if (!authStore.isAuthenticated) {
        router.push('/login');
    }
});

function formatter(monto) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP'
    }).format(monto);
}
</script>