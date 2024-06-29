<template>
    <div class="h-screen w-full flex justify-center items-center">
        <transition>
            <div class="w-96" v-if="login">
                <Login @mostrar-registro="mostrarRegistro" />

            </div>
        </transition>
        <transition>
            <div class="w-96" v-if="registro">
                <Register @mostrar-login="mostrarLogin" />
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'

const registro = ref(false)
const login = ref(true)

function mostrarRegistro() {
    login.value = false
    setTimeout(() => {
        registro.value = true
    }, 500)

}

function mostrarLogin() {
    registro.value = false
    setTimeout(() => {
        login.value = true
    }, 500)
}
</script>
<style scoped>
.v-enter-active,
.v-leave-active {
    transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
}
</style>