import { createRouter, createWebHistory } from 'vue-router'
import IndexView from '../views/IndexView.vue'
import CartView from '../views/CartView.vue'
import LoginView from '../views/LoginView.vue'
import CheckOutView from '../views/CheckOutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: IndexView
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: CheckOutView
    }
  ]
})

export default router
