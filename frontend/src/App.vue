<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'
import Notification from '@/components/Notificacion.vue'

const notificationMessage = ref('')
const notificationKey = ref(0)


window.showNotification = (message) => {
  notificationMessage.value = message
  notificationKey.value += 1
}
</script>

<template>
  <RouterView />
  <Notification v-if="notificationMessage" :message="notificationMessage" :llave="notificationKey"
    @close="notificationMessage = ''" />
</template>

<style scoped></style>
