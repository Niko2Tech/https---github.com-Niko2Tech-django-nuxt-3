import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAuthStore } from './stores/authStore'

import App from './App.vue'
import router from './router'
// Importa Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';

// Añade los íconos que vas a utilizar
library.add(fas);

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon);
app.use(createPinia())
app.use(router)

app.mount('#app')

// Guard de navegación
router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()
    await authStore.checkAuth()
    // Check if the route requires authentication
    if (to.meta.requiresAuth) {
        // Check the auth status before navigating
        try {
            await authStore.checkAuth()
            next()
        } catch (error) {
            // If checkAuth fails, redirect to login page
            next('/login')
        }
    } else {
        next()
    }
})
