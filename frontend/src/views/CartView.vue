<template>
    <div>
        <h1>Cart View</h1>
        {{ cart }}
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getCart } from '@/utils/cart';

const cart = ref([]);

onMounted(async () => {
    cart.value = getCart();
});
</script>