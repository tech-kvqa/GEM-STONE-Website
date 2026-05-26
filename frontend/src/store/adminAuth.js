/**
 * frontend/src/store/adminAuth.js  ←  NEW FILE — add to your store/ folder
 * =========================================================================
 * Mirrors the consumer auth store but uses 'admin_token' / 'admin_user'
 * localStorage keys and calls /api/admin/auth/* endpoints.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { adminAuthApi } from '@/api'

export const useAdminAuthStore = defineStore('adminAuth', () => {
  const user  = ref(JSON.parse(localStorage.getItem('admin_user') || 'null'))
  const token = ref(localStorage.getItem('admin_token') || null)

  const isLoggedIn    = computed(() => !!token.value && !!user.value)
  const isSuperAdmin  = computed(() => user.value?.role === 'superadmin')

  async function login(email, password) {
    const { data } = await adminAuthApi.login({ email, password })
    token.value = data.access_token
    user.value  = data.admin
    localStorage.setItem('admin_token', data.access_token)
    localStorage.setItem('admin_user',  JSON.stringify(data.admin))
    return data
  }

  function logout() {
    token.value = null
    user.value  = null
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
  }

  async function fetchMe() {
    if (!token.value) return
    try {
      const { data } = await adminAuthApi.me()
      user.value = data
      localStorage.setItem('admin_user', JSON.stringify(data))
    } catch {
      logout()
    }
  }

  return { user, token, isLoggedIn, isSuperAdmin, login, logout, fetchMe }
})
