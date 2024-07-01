<template>
    <button :id="props.id" :class="computedClass" @click="handleClick">
        <slot></slot>
    </button>
</template>

<script setup>
import { computed } from 'vue';
const props = defineProps({
    id: {
        type: [Number, String],
        required: true,
    },
    colorClasses: {
        type: [String, Array],
        default: ''
    }
})

// Clases estándar del enlace
const baseClasses = 'px-2 py-1 rounded-md text-center';

// Computa las clases finales combinando las bases con las proporcionadas
const computedClass = computed(() => {
    return [baseClasses, props.colorClasses].join(' ');
});

const emit = defineEmits(['abrirModal']);

function handleClick() {
    emit('abrirModal', props.id);
}

</script>