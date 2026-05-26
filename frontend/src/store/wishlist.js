import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { wishlistApi } from '@/api'
import { useAuthStore } from './auth'

export const useWishlistStore = defineStore('wishlist', () => {
  const items = ref([])

  const ids = computed(() => items.value.map(i => i.product.id))
  const count = computed(() => items.value.length)

  function isWishlisted(productId) { return ids.value.includes(productId) }

  async function fetch() {
    const auth = useAuthStore()
    if (!auth.isLoggedIn) { items.value = []; return }
    const { data } = await wishlistApi.get()
    items.value = data
  }

  async function toggle(productId) {
    const auth = useAuthStore()
    if (!auth.isLoggedIn) throw new Error('login_required')
    if (isWishlisted(productId)) {
      await wishlistApi.remove(productId)
      items.value = items.value.filter(i => i.product.id !== productId)
    } else {
      await wishlistApi.add(productId)
      await fetch()
    }
  }

  return { items, count, isWishlisted, fetch, toggle }
})
