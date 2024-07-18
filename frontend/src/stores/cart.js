// stores/cart.js
import { defineStore } from 'pinia'
import { getCart, addToCart as addProductToCart, removeFromCart as removeProductFromCart, clearCart as deleteCard, removeSingleProductFromCart } from '@/utils/cart'

export const useCartStore = defineStore('cart', {
    state: () => ({
        cart: getCart()
    }),
    getters: {
        cartCount: (state) => state.cart.reduce((acc, item) => acc + item.quantity, 0)
    },
    actions: {
        async addToCart(product) {
            let resultado = await addProductToCart(product)
            this.cart = getCart()
            return resultado
        },
        async removeFromCart(productId) {
            let resultado = await removeProductFromCart(productId)
            this.cart = getCart()
            return resultado
        },
        async removeSingleProductFromCart(productId) {
            let resultado = await removeSingleProductFromCart(productId)
            this.cart = getCart()
            return resultado
        },
        clearCart() {
            this.cart = []
            deleteCard()
        }
    }
})
