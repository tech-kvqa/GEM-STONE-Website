/**
 * frontend/src/router/admin.js  ←  NEW FILE — import this in your main router/index.js
 * ====================================================================================
 * All admin routes live under /admin/*
 * The beforeEach guard redirects unauthenticated users to /admin/login.
 *
 * HOW TO ADD TO YOUR EXISTING router/index.js:
 *   1. Import adminRoutes from './admin'
 *   2. Spread it into your routes array: routes = [...existingRoutes, ...adminRoutes]
 *   3. Add the guard (shown at bottom of this file) to your router.beforeEach
 */

import { useAdminAuthStore } from '@/store/adminAuth'

export const adminRoutes = [
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('@/views/admin/AdminLogin.vue'),
    meta: { adminPublic: true }   // accessible without admin auth
  },
  {
    path: '/admin',
    name: 'AdminLayout',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { requiresAdmin: true },
    redirect: '/admin',
    children: [
      { path: 'dashboard',     name: 'AdminDashboard',     component: () => import('@/views/admin/Dashboard.vue') },
      { path: 'products',      name: 'AdminProducts',      component: () => import('@/views/admin/Products.vue') },
      { path: 'orders',        name: 'AdminOrders',        component: () => import('@/views/admin/Orders.vue') },
      { path: 'orders/:id',    name: 'AdminOrderDetail',   component: () => import('@/views/admin/OrderDetail.vue') },
      { path: 'users',         name: 'AdminUsers',         component: () => import('@/views/admin/Users.vue') },
      { path: 'consultations', name: 'AdminConsultations', component: () => import('@/views/admin/Consultations.vue') },
      { path: 'reviews',       name: 'AdminReviews',       component: () => import('@/views/admin/Reviews.vue') },
      { path: 'inventory',     name: 'AdminInventory',     component: () => import('@/views/admin/Inventory.vue') },
      { path: 'settings',      name: 'AdminSettings',      component: () => import('@/views/admin/Settings.vue') },
    ]
  }
]

/**
 * Add this guard to your existing router.beforeEach in router/index.js:
 *
 *   router.beforeEach((to) => {
 *     // existing consumer auth guard ...
 *     if (to.meta.requiresAuth) { ... }
 *
 *     // NEW: admin guard
 *     if (to.meta.requiresAdmin) {
 *       const adminAuth = useAdminAuthStore()
 *       if (!adminAuth.isLoggedIn) return { name: 'AdminLogin' }
 *     }
 *   })
 */
export function adminRouteGuard(to) {
  if (to.meta.requiresAdmin) {
    const adminAuth = useAdminAuthStore()
    if (!adminAuth.isLoggedIn) return { name: 'AdminLogin' }
  }
}
