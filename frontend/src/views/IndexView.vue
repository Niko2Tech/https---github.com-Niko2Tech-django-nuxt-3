<script setup>
import Header from '@/components/Header.vue'
import SeccionOferta from '@/components/SeccionOferta.vue'
import SeccionInfo from '@/components/SeccionInfo.vue'
import SeccionCarta from '@/components/SeccionCarta.vue'
import { useAuthStore } from '@/stores/authStore'
import { onMounted, ref } from 'vue'

const cliente = ref('')
const direccion = ref('')
const authStore = useAuthStore()
// ejecutamos la funcion para verificar si el token es valido
onMounted(async () => {
  await authStore.checkAuth()
  cliente.value = authStore.cliente
  direccion.value = authStore.direccion
})
</script>

<template>
  <Header :cliente="cliente" :direccion="direccion" />
  <main>
    <SeccionOferta />
    <SeccionInfo />
    <SeccionCarta />
  </main>
</template>
