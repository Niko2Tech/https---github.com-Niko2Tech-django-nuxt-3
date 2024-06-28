// stores/cart.js
import { defineStore } from 'pinia'
import { getCart, addToCart as addProductToCart } from '@/utils/cart'

export const useCartStore = defineStore('cart', {
    state: () => ({
        cart: getCart()
    }),
    getters: {
        cartCount: (state) => state.cart.reduce((acc, item) => acc + item.quantity, 0)
    },
    actions: {
        addToCart(product) {
            addProductToCart(product)
            this.cart = getCart() // Actualizar el estado del carrito
        },
        clearCart() {
            this.cart = []
            clearCart()
        }
    }
})
