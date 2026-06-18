<template>
  <div id="crystal-luxe">
    <!-- <AppNavbar />
    <CartDrawer />
    <AuthModal v-if="showAuth" @close="showAuth = false" /> -->

    <AppNavbar v-if="!isAdminRoute"/>
    <CartDrawer v-if="!isAdminRoute"/>
    <AuthModal v-if="showAuth && !isAdminRoute" @close="showAuth = false" />

    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>

    <AppFooter />
  </div>
</template>

<script setup>
// import { ref, watch, onMounted } from 'vue'
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import CartDrawer from '@/components/cart/CartDrawer.vue'
import AuthModal from '@/components/common/AuthModal.vue'
import { useAuthStore } from '@/store/auth'
import { useCartStore } from '@/store/cart'
import { useWishlistStore } from '@/store/wishlist'

const route = useRoute()
const auth = useAuthStore()
const cart = useCartStore()
const wishlist = useWishlistStore()
const showAuth = ref(false)
const isAdminRoute = computed(() => route.path.startsWith('/admin'))

onMounted(async () => {
  await auth.fetchMe()
  if (auth.isLoggedIn) {
    cart.fetchCart()
    wishlist.fetch()
  }
  if (route.query.login) showAuth.value = true
})

watch(() => route.query.login, (v) => { if (v) showAuth.value = true })
</script>
