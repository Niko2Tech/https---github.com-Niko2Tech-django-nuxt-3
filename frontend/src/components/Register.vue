<template>
    <div class="container mx-auto p-10 shadow-xl rounded-md">
        <div class="flex items-center mb-6 justify-center">
            <img src="@/assets/burgerLogo.svg" alt="Logo" class="w-12 h-12">
            <span class="ml-2 text-2xl font-bold text-yellow-500">
                <span class="text-orange-600">EL</span> COMILON
            </span>
        </div>
        <form @submit.prevent="handleRegister" class="space-y-4">
            <div v-if="errorGeneral" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
                role="alert">
                <strong class="font-bold">Error! </strong>
                <span class="block sm:inline">{{ errorGeneral }}</span>
            </div>
            <div>
                <input v-model="formValues.email" type="text" placeholder="Correo"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-600 focus:border-orange-600 sm:text-sm" />
            </div>
            <div>
                <p v-if="FormError.email" class="text-red-500 text-sm">{{ FormError.email }}</p>
            </div>
            <div>
                <input v-model="formValues.password" type="password" placeholder="Contraseña"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-600 focus:border-orange-600 sm:text-sm" />
            </div>
            <div>
                <p v-if="FormError.password" class="text-red-500 text-sm">{{ FormError.password }}</p>
            </div>
            <div>
                <input v-model="formValues.password_confirmation" type="password" placeholder="Confirmar Contraseña"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-600 focus:border-orange-600 sm:text-sm" />
            </div>
            <div>
                <p v-if="FormError.password_confirmation" class="text-red-500 text-sm">{{
                    FormError.password_confirmation
                    }}</p>
            </div>
            <div>
                <input v-model="formValues.nombre" type="text" placeholder="Nombre"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-600 focus:border-orange-600 sm:text-sm" />
            </div>
            <div>
                <p v-if="FormError.nombre" class="text-red-500 text-sm">{{ FormError.nombre }}</p>
            </div>
            <div>
                <input v-model="formValues.direccion" type="text" placeholder="Direccion"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-600 focus:border-orange-600 sm:text-sm" />
            </div>
            <div>
                <p v-if="FormError.direccion" class="text-red-500 text-sm">{{ FormError.direccion }}</p>
            </div>
            <div>
                <input v-model="formValues.telefono" type="text" placeholder="Telefono"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-orange-600 focus:border-orange-600 sm:text-sm" />
            </div>
            <div>
                <p v-if="FormError.telefono" class="text-red-500 text-sm">{{ FormError.telefono }}</p>
            </div>
            <div>
                <button type="submit"
                    class="w-full px-4 py-2 bg-orange-600 text-white font-medium rounded-md hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500">
                    Registrarse
                </button>
            </div>
            <p class="mt-4 text-center">Volver al <a @click="$emit('mostrar-login')"
                    class="text-orange-600 font-medium hover:border-b hover:border-orange-600 cursor-pointer">
                    login
                </a></p>
        </form>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const props = defineProps({
    redirect: {
        type: String,
        default: '/'
    }
})

const emit = defineEmits(['mostrar-login'])
const router = useRouter()

const authStore = useAuthStore()
const formValues = reactive({
    email: '',
    password: '',
    password_confirmation: '',
    nombre: '',
    direccion: '',
    telefono: '',
    saldo_cuenta: 0,
})

const FormError = reactive({
    email: '',
    password: '',
    password_confirmation: '',
    nombre: '',
    direccion: '',
    telefono: '',
    saldo_cuenta: '',
})
const errorGeneral = ref('')

const handleRegister = async () => {
    FormError.email = ''
    FormError.password = ''
    FormError.password_confirmation = ''
    FormError.nombre = ''
    FormError.direccion = ''
    FormError.telefono = ''
    FormError.saldo_cuenta = ''
    errorGeneral.value = ''

    if (formValues.password !== formValues.password_confirmation) {
        FormError.password_confirmation = 'Las contraseñas no coinciden'
        return
    }

    try {
        let data = await authStore.register(formValues)
        if (data.error) {
            console.log(data.error)

            if (data.error.error) {
                errorGeneral.value = data.error.error
                return
            }

            if (data.error.non_field_errors) {
                errorGeneral.value = data.error.non_field_errors[0]
                return
            }

            FormError.email = data.error.email ? data.error.email[0] : ''
            FormError.password = data.error.password ? data.error.password[0] : ''
            FormError.password_confirmation = data.error.password_confirmation ? data.error.password_confirmation[0] : ''
            FormError.nombre = data.error.nombre ? data.error.nombre[0] : ''
            FormError.direccion = data.error.direccion ? data.error.direccion[0] : ''
            FormError.telefono = data.error.telefono ? data.error.telefono[0] : ''
            FormError.saldo_cuenta = data.error.saldo_cuenta ? data.error.saldo_cuenta[0] : ''
        } else {
            FormError.email = ''
            FormError.password = ''
            FormError.password_confirmation = ''
            FormError.nombre = ''
            FormError.direccion = ''
            FormError.telefono = ''
            FormError.saldo_cuenta = ''
            router.push(props.redirect)
        }
    } catch (e) {
        console.error("Unexpected error:", e)
        errorGeneral.value = 'Ocurrió un error inesperado. Por favor, inténtelo de nuevo.'
    }
}
</script>