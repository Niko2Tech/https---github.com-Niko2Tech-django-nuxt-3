import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        userId: null,
        cliente: null,
        direccion: null,
        saldo: null,
        accessToken: localStorage.getItem('access_token') || null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.accessToken,
    },
    actions: {
        async login(email, password) {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/user/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username: email, password }),
                })

                if (!response.ok) {
                    const data = await response.json()
                    return data
                }

                const data = await response.json()

                this.accessToken = data.access

                this.user = data.username
                this.userId = data.user_id
                this.cliente = data.cliente
                this.direccion = data.direccion
                this.saldo = data.saldo

                localStorage.setItem('access_token', this.accessToken)


                return data
            } catch (error) {
                console.error(error)
                throw error
            }
        },
        async register(data) {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/user/register/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                })

                if (!response.ok) {
                    const data = await response.json()
                    return { error: data }
                }

                const responseData = await response.json()
                this.accessToken = responseData.access
                this.user = responseData.username
                this.userId = responseData.user_id
                this.cliente = responseData.cliente
                this.direccion = responseData.direccion
                this.saldo = responseData.saldo

                localStorage.setItem('access_token', this.accessToken)
                return responseData
            } catch (error) {
                console.error(error)
                throw error
            }
        },
        async logout() {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/user/logout/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })

                this.accessToken = null
                this.user = null
                this.userId = null
                this.cliente = null
                this.direccion = null
                this.saldo = null
                localStorage.removeItem('access_token')
                const responseData = await response.json()
                return responseData
            } catch (error) {
                console.error(error)
                throw error
            }
        },
        async checkAuth() {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/user/check_auth/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ token: this.accessToken }),
                })

                if (!response.ok) {
                    throw new Error('Error durante la verificación del token')
                }

                const data = await response.json()

                this.user = data.username
                this.userId = data.user_id
                this.cliente = data.cliente
                this.direccion = data.direccion
                this.saldo = data.saldo

                return data
            } catch (error) {
                console.error(error)
                this.logout()
            }
        },
    },
})
