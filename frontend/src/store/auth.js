import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('cl_user') || 'null'))
  // const token = ref(localStorage.getItem('cl_token') || null)

  const token = ref(null)

  // hydrate immediately
  const storedToken = localStorage.getItem('cl_token')
  if (storedToken) token.value = storedToken

  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_admin || false)

  async function login(email, password) {
    const { data } = await authApi.login({ email, password })
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('cl_token', data.access_token)
    localStorage.setItem('cl_user', JSON.stringify(data.user))
    return data
  }

  async function register(payload) {
    const { data } = await authApi.register(payload)
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('cl_token', data.access_token)
    localStorage.setItem('cl_user', JSON.stringify(data.user))
    return data
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('cl_token')
    localStorage.removeItem('cl_user')
  }

  async function fetchMe() {
    if (!token.value) return
    try {
      const { data } = await authApi.me()
      user.value = data
      localStorage.setItem('cl_user', JSON.stringify(data))
    } catch {
      logout()
    }
  }

  return { user, token, isLoggedIn, isAdmin, login, register, logout, fetchMe }
})
