import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cartApi } from '@/api'
import { useAuthStore } from './auth'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const loading = ref(false)
  const open = ref(false)

  const count = computed(() => items.value.reduce((s, i) => s + i.quantity, 0))
  const subtotal = computed(() =>
    items.value.reduce((s, i) => s + i.product.price * i.quantity, 0)
  )
  const shipping = computed(() => subtotal.value >= 999 ? 0 : 99)
  const total = computed(() => subtotal.value + shipping.value)

  async function fetchCart() {
    const auth = useAuthStore()
    if (!auth.isLoggedIn) { items.value = []; return }
    loading.value = true
    try {
      const { data } = await cartApi.get()
      items.value = data
    } finally {
      loading.value = false
    }
  }

  async function addItem(productId, quantity = 1) {
    const auth = useAuthStore()
    if (!auth.isLoggedIn) throw new Error('login_required')
    const { data } = await cartApi.add({ product_id: productId, quantity })
    await fetchCart()
    open.value = true
    return data
  }

  async function updateItem(itemId, quantity) {
    if (quantity <= 0) return removeItem(itemId)
    await cartApi.update(itemId, { quantity })
    await fetchCart()
  }

  async function removeItem(itemId) {
    await cartApi.remove(itemId)
    items.value = items.value.filter(i => i.id !== itemId)
  }

  async function clearCart() {
    await cartApi.clear()
    items.value = []
  }

  function toggleCart() { open.value = !open.value }

  return { items, loading, open, count, subtotal, shipping, total,
           fetchCart, addItem, updateItem, removeItem, clearCart, toggleCart }
})
