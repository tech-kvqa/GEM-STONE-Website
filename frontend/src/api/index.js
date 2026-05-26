// import axios from 'axios'

// const api = axios.create({
//   baseURL: '/api',
//   timeout: 15000,
//   headers: { 'Content-Type': 'application/json' }
// })

// // Attach auth token
// api.interceptors.request.use(config => {
//   const token = localStorage.getItem('cl_token')
//   if (token) config.headers.Authorization = `Bearer ${token}`
//   return config
// })

// // Handle 401 globally
// api.interceptors.response.use(
//   res => res,
//   err => {
//     if (err.response?.status === 401) {
//       localStorage.removeItem('cl_token')
//       localStorage.removeItem('cl_user')
//     }
//     return Promise.reject(err)
//   }
// )

// // ── Products ──────────────────────────────────────────────────────────────────
// export const productApi = {
//   list: (params = {}) => api.get('/products/', { params }),
//   get: slug => api.get(`/products/${slug}`),
//   featured: () => api.get('/products/featured'),
//   bestsellers: () => api.get('/products/bestsellers'),
//   newArrivals: () => api.get('/products/new-arrivals'),
//   create: data => api.post('/products', data),
//   update: (id, data) => api.put(`/products/${id}`, data),
//   delete: id => api.delete(`/products/${id}`)
// }

// // ── Categories ────────────────────────────────────────────────────────────────
// export const categoryApi = {
//   list: () => api.get('/categories/'),
//   get: slug => api.get(`/categories/${slug}`)
// }

// // ── Auth ──────────────────────────────────────────────────────────────────────
// export const authApi = {
//   register: data => api.post('/auth/register', data),
//   login: data => api.post('/auth/login', data),
//   me: () => api.get('/auth/me'),
//   update: data => api.put('/auth/me', data)
// }

// // ── Cart ──────────────────────────────────────────────────────────────────────
// export const cartApi = {
//   get: () => api.get('/cart/'),
//   add: data => api.post('/cart/', data),
//   update: (id, data) => api.put(`/cart/${id}`, data),
//   remove: (id) => api.delete(`/cart/${id}`),
//   clear: () => api.delete('/cart/')
// }

// // ── Wishlist ──────────────────────────────────────────────────────────────────
// export const wishlistApi = {
//   get: () => api.get('/wishlist/'),
//   add: id => api.post(`/wishlist/${id}`),
//   remove: id => api.delete(`/wishlist/${id}`)
// }

// // ── Orders ────────────────────────────────────────────────────────────────────
// export const orderApi = {
//   list: () => api.get('/orders/'),
//   get: id => api.get(`/orders/${id}`),
//   place: data => api.post('/orders/', data),
//   cancel: id => api.post(`/orders/${id}/cancel`)
// }

// // ── Reviews ───────────────────────────────────────────────────────────────────
// export const reviewApi = {
//   list: productId => api.get(`/reviews/product/${productId}`),
//   add: (productId, data) => api.post(`/reviews/product/${productId}`, data),
//   delete: id => api.delete(`/reviews/${id}`)
// }

// export default api


/**
 * frontend/src/api/index.js  ←  REPLACE YOUR EXISTING api/index.js WITH THIS
 * =============================================================================
 * All original consumer API calls are UNCHANGED.
 * adminApi block added at the bottom using a SEPARATE axios instance
 * that reads the admin token from localStorage key 'admin_token'.
 */

import axios from 'axios'

// ── Consumer API instance (unchanged) ─────────────────────────────────────────
const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('cl_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('cl_token')
      localStorage.removeItem('cl_user')
    }
    return Promise.reject(err)
  }
)

// ── Admin API instance (NEW — separate token key) ─────────────────────────────
const adminApi = axios.create({
  baseURL: '/api',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' }
})

adminApi.interceptors.request.use(config => {
  const token = localStorage.getItem('admin_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

adminApi.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')
      // Redirect to admin login if not already there
      if (window.location.pathname.startsWith('/admin') &&
          window.location.pathname !== '/admin/login') {
        window.location.href = '/admin/login'
      }
    }
    return Promise.reject(err)
  }
)

// ══════════════════════════════════════════════════════════════════════════════
// CONSUMER APIs  (all original — nothing changed)
// ══════════════════════════════════════════════════════════════════════════════

export const productApi = {
  list:        (params = {}) => api.get('/products',            { params }),
  get:         slug           => api.get(`/products/${slug}`),
  featured:    ()             => api.get('/products/featured'),
  bestsellers: ()             => api.get('/products/bestsellers'),
  newArrivals: ()             => api.get('/products/new-arrivals'),
  create:      data           => api.post('/products', data),
  update:      (id, data)     => api.put(`/products/${id}`, data),
  delete:      id             => api.delete(`/products/${id}`)
}

export const categoryApi = {
  list: ()     => api.get('/categories/'),
  get:  slug   => api.get(`/categories/${slug}`)
}

export const authApi = {
  register: data => api.post('/auth/register', data),
  login:    data => api.post('/auth/login',    data),
  me:       ()   => api.get('/auth/me'),
  update:   data => api.put('/auth/me',        data)
}

export const cartApi = {
  get:    ()          => api.get('/cart/'),
  add:    data        => api.post('/cart/', data),
  update: (id, data)  => api.put(`/cart/${id}`, data),
  remove: id          => api.delete(`/cart/${id}`),
  clear:  ()          => api.delete('/cart/')
}

export const wishlistApi = {
  get:    ()   => api.get('/wishlist/'),
  add:    id   => api.post(`/wishlist/${id}`),
  remove: id   => api.delete(`/wishlist/${id}`)
}

export const orderApi = {
  list:   ()      => api.get('/orders/'),
  get:    id      => api.get(`/orders/${id}`),
  place:  data    => api.post('/orders/', data),
  cancel: id      => api.post(`/orders/${id}/cancel`)
}

export const reviewApi = {
  list:   productId       => api.get(`/reviews/product/${productId}`),
  add:    (productId, data) => api.post(`/reviews/product/${productId}`, data),
  delete: id              => api.delete(`/reviews/${id}`)
}

// ══════════════════════════════════════════════════════════════════════════════
// ADMIN APIs  (NEW — all prefixed /api/admin/*)
// ══════════════════════════════════════════════════════════════════════════════

export const adminAuthApi = {
  /** POST /api/admin/auth/login  →  { access_token, admin } */
  login:  data   => adminApi.post('/admin/auth/login', data),
  me:     ()     => adminApi.get('/admin/auth/me'),
  list:   ()     => adminApi.get('/admin/auth/list'),
  create: data   => adminApi.post('/admin/auth/create', data),
}

export const adminDashboardApi = {
  /** GET /api/admin/dashboard  →  KPIs + charts + recent orders */
  summary:  ()       => adminApi.get('/admin/dashboard'),
  revenue:  period   => adminApi.get('/admin/analytics/revenue', { params: { period } }),
  inventory: ()      => adminApi.get('/admin/inventory'),
}

export const adminProductApi = {
  /** GET /api/admin/products  — all products incl. inactive */
  list:   (params = {}) => adminApi.get('/admin/products',            { params }),
  update: (id, data)    => adminApi.patch(`/admin/products/${id}`,    data),
  upload: (id, formData)=> adminApi.post(`/admin/products/${id}/image`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  deactivate: id        => adminApi.delete(`/admin/products/${id}`),
}

export const adminOrderApi = {
  /** GET /api/admin/orders  — all orders, filterable */
  list:          (params = {})     => adminApi.get('/admin/orders',                 { params }),
  get:           id                => adminApi.get(`/admin/orders/${id}`),
  updateStatus:  (id, data)        => adminApi.patch(`/admin/orders/${id}/status`,  data),
  updatePayment: (id, data)        => adminApi.patch(`/admin/orders/${id}/payment`, data),
}

export const adminUserApi = {
  list:   (params = {}) => adminApi.get('/admin/users',                { params }),
  get:    id            => adminApi.get(`/admin/users/${id}`),
  toggle: id            => adminApi.patch(`/admin/users/${id}/toggle`),
}

export const adminConsultationApi = {
  list:   (params = {}) => adminApi.get('/admin/consultations',        { params }),
  update: (id, data)    => adminApi.patch(`/admin/consultations/${id}`, data),
}

export const adminReviewApi = {
  list:    (params = {}) => adminApi.get('/admin/reviews',             { params }),
  approve: id            => adminApi.patch(`/admin/reviews/${id}/approve`),
}

export { adminApi }
export default api
