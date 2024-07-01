<!-- Componente Modal.vue -->
<template>
    <div v-if="visible"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 cursor-default overflow-x-auto">
        <div class="bg-white min-w-min rounded-lg">
            <header class="border-b-2">
                <div class="flex p-4 justify-between items-center">
                    <h2 class="text-xl font-semibold">{{ title }}</h2>
                    <button @click="closeModal" class="text-red-500 text-4xl"><font-awesome-icon
                            :icon="['fas', 'xmark']" /></button>
                </div>
            </header>
            <slot></slot>
        </div>
    </div>
</template>

<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
const props = defineProps({
    title: {
        type: String,
        required: true
    },
    visible: {
        type: Boolean,
        required: true
    }
});

const emit = defineEmits(['update:visible']);

const closeModal = () => {
    emit('update:visible', false);
};
</script>
