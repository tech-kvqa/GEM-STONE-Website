import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { adminRoutes, adminRouteGuard } from './admin'

const routes = [
  ...adminRoutes,
  { path: '/',                    name: 'Home',         component: () => import('@/views/HomeView.vue') },
  { path: '/shop',                name: 'Shop',         component: () => import('@/views/ShopView.vue') },
  { path: '/shop/:category',      name: 'Category',     component: () => import('@/views/ShopView.vue') },
  { path: '/crystal/:slug',       name: 'Product',      component: () => import('@/views/ProductView.vue') },
  { path: '/cart',                name: 'Cart',         component: () => import('@/views/CartView.vue') },
  { path: '/checkout',            name: 'Checkout',     component: () => import('@/views/CheckoutView.vue'), meta: { requiresAuth: true } },
  { path: '/account',             name: 'Account',      component: () => import('@/views/AccountView.vue'), meta: { requiresAuth: true } },
  { path: '/account/orders',      name: 'Orders',       component: () => import('@/views/AccountView.vue'), meta: { requiresAuth: true } },
  { path: '/wishlist',            name: 'Wishlist',     component: () => import('@/views/WishlistView.vue'), meta: { requiresAuth: true } },
  { path: '/our-story',           name: 'Story',        component: () => import('@/views/StoryView.vue') },
  { path: '/crystal-guide',       name: 'Guide',        component: () => import('@/views/GuideView.vue') },
  { path: '/consultation',        name: 'Consultation', component: () => import('@/views/ConsultationView.vue') },
  { path: '/:pathMatch(.*)*',     name: 'NotFound',     component: () => import('@/views/NotFoundView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, saved) {
    if (saved) return saved
    return { top: 0, behavior: 'smooth' }
  }
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isLoggedIn) return { name: 'Home', query: { login: '1' } }
  }
})

// router.beforeEach((to) => {
//   // your existing consumer auth guard:
//   if (to.meta.requiresAuth) {
//     const auth = useAuthStore()
//     if (!auth.isLoggedIn) return { name: 'Home', query: { login: '1' } }
//   }
//   // NEW: admin guard
//   return adminRouteGuard(to)
// })

export default router
