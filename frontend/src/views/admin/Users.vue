<template>
  <div class="admin-page">

    <div class="page-head">
      <div>
        <p class="label-caps">Customer Management</p>
        <h2 class="page-title">Users</h2>
      </div>
      <span class="result-badge">{{ total }} customers</span>
    </div>

    <div class="filter-bar">
      <input v-model="search" @input="debounceLoad" placeholder="Search by name, email or phone…" class="input-field filter-search" />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="table-wrap">
      <div v-for="i in 8" :key="i" class="skeleton" style="height:60px;margin-bottom:1px"></div>
    </div>

    <!-- Table -->
    <div v-else class="table-wrap">
      <table class="admin-table">
        <thead>
          <tr>
            <th>Customer</th>
            <th>Phone</th>
            <th class="col-num">Orders</th>
            <th class="col-num">Lifetime Value</th>
            <th>Joined</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>
              <div class="user-cell">
                <div class="user-avatar">{{ u.name?.[0]?.toUpperCase() || '?' }}</div>
                <div>
                  <p class="user-name">{{ u.name }}</p>
                  <p class="user-email">{{ u.email }}</p>
                </div>
              </div>
            </td>
            <td><span class="meta-text">{{ u.phone || '—' }}</span></td>
            <td class="col-num"><span class="meta-num">{{ u.total_orders ?? '—' }}</span></td>
            <td class="col-num"><span class="price-val">{{ u.lifetime_value != null ? '₹' + fmt(u.lifetime_value) : '—' }}</span></td>
            <td><span class="meta-text">{{ fmtDate(u.created_at) }}</span></td>
            <td>
              <span :class="['status-pill', u.is_active !== false ? 'pill--active' : 'pill--inactive']">
                {{ u.is_active !== false ? 'Active' : 'Blocked' }}
              </span>
            </td>
            <td>
              <div class="action-row">
                <button class="action-btn" @click="viewUser(u)" title="View detail">→</button>
                <button class="action-btn action-btn--danger" @click="toggleUser(u)"
                  :title="u.is_active !== false ? 'Block' : 'Unblock'">
                  {{ u.is_active !== false ? '⊘' : '✓' }}
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="!users.length">
            <td colspan="7" class="empty-row">
              <span class="empty-icon">◇</span><p>No users found</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="pagination">
      <button :disabled="page <= 1" class="btn btn-ghost btn-sm" @click="page--; load()">← Prev</button>
      <span class="page-info label-caps">Page {{ page }} of {{ totalPages }}</span>
      <button :disabled="page >= totalPages" class="btn btn-ghost btn-sm" @click="page++; load()">Next →</button>
    </div>

    <!-- User detail drawer -->
    <div v-if="selectedUser" class="drawer-overlay" @click.self="selectedUser = null">
      <aside class="drawer">
        <div class="drawer__head">
          <div class="user-cell">
            <div class="user-avatar user-avatar--lg">{{ selectedUser.name?.[0]?.toUpperCase() }}</div>
            <div>
              <p class="drawer__title">{{ selectedUser.name }}</p>
              <p class="user-email">{{ selectedUser.email }}</p>
            </div>
          </div>
          <button @click="selectedUser = null" class="drawer__close">✕</button>
        </div>
        <div class="drawer__body">
          <div class="info-grid">
            <div class="info-row"><span class="info-key label-caps">Phone</span><span class="info-val">{{ selectedUser.phone || '—' }}</span></div>
            <div class="info-row"><span class="info-key label-caps">City</span><span class="info-val">{{ selectedUser.city || '—' }}</span></div>
            <div class="info-row"><span class="info-key label-caps">Pincode</span><span class="info-val">{{ selectedUser.pincode || '—' }}</span></div>
            <div class="info-row"><span class="info-key label-caps">Total Orders</span><span class="info-val">{{ selectedUser.total_orders || 0 }}</span></div>
            <div class="info-row"><span class="info-key label-caps">Lifetime Value</span><span class="info-val price-val">₹{{ fmt(selectedUser.lifetime_value || 0) }}</span></div>
          </div>
          <div class="divider-gold"><span>✦</span></div>
          <h4 class="drawer-sub">Recent Orders</h4>
          <div class="mini-orders">
            <div v-for="o in selectedUser.recent_orders" :key="o.id" class="mini-order">
              <span class="order-num">{{ o.order_number }}</span>
              <span :class="['order-status', `status--${o.status}`]">{{ o.status }}</span>
              <span class="price-val">₹{{ fmt(o.total) }}</span>
            </div>
            <p v-if="!selectedUser.recent_orders?.length" class="empty-mini">No orders yet</p>
          </div>
        </div>
      </aside>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { toast } from 'vue3-toastify'
import { adminUserApi } from '@/api'

const users    = ref([])
const total    = ref(0)
const loading  = ref(false)
const page     = ref(1)
const limit    = 20
const search   = ref('')
const selectedUser = ref(null)
let timer = null

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / limit)))

async function load() {
  loading.value = true
  try {
    const { data } = await adminUserApi.list({ page: page.value, limit, search: search.value || undefined })
    users.value = data.users || []
    total.value = data.total || 0
  } catch { toast.error('Failed to load users') } finally { loading.value = false }
}

function debounceLoad() { clearTimeout(timer); timer = setTimeout(() => { page.value = 1; load() }, 400) }
onMounted(load)

async function viewUser(u) {
  try {
    const { data } = await adminUserApi.get(u.id)
    selectedUser.value = data
  } catch { selectedUser.value = u }
}

async function toggleUser(u) {
  const action = u.is_active !== false ? 'block' : 'unblock'
  if (!confirm(`Are you sure you want to ${action} ${u.name}?`)) return
  try {
    await adminUserApi.toggle(u.id)
    toast.success(`User ${action}ed`); load()
  } catch { toast.error('Action failed') }
}

function fmt(n)    { return Number(n || 0).toLocaleString('en-IN') }
function fmtDate(d){ return d ? new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : '—' }
</script>

<style scoped>
.admin-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-head { display: flex; align-items: flex-end; justify-content: space-between; }
.page-title { font-family: var(--font-serif); font-size: 2rem; font-weight: 300; color: var(--ink); margin-top: 0.2rem; }
.result-badge { font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }
.filter-bar { display: flex; gap: 0.75rem; }
.filter-search { flex: 1; max-width: 440px; }
.input-field { background: var(--bg-card); border: 1px solid rgba(196,135,106,0.2); color: var(--ink); }
.input-field:focus { border-color: var(--rose-gold); }

.table-wrap { background: var(--bg-card); border: 1px solid rgba(196,135,106,0.12); overflow-x: auto; }
.admin-table { width: 100%; border-collapse: collapse; }
.admin-table thead { background: var(--bg-section); border-bottom: 1px solid rgba(196,135,106,0.15); }
.admin-table th { padding: 0.85rem 1.2rem; text-align: left; font-size: 0.6rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--rose-gold-dim); font-weight: 500; }
.col-num { text-align: right; }
.admin-table td { padding: 0.9rem 1.2rem; border-bottom: 1px solid rgba(196,135,106,0.06); vertical-align: middle; }
.admin-table tbody tr:hover { background: rgba(196,135,106,0.025); }

.user-cell { display: flex; align-items: center; gap: 0.8rem; }
.user-avatar { width: 36px; height: 36px; background: linear-gradient(135deg, var(--blush-mid), var(--rose-gold-dim)); display: flex; align-items: center; justify-content: center; font-family: var(--font-serif); font-size: 1rem; color: #fff; flex-shrink: 0; }
.user-avatar--lg { width: 44px; height: 44px; font-size: 1.2rem; }
.user-name { font-size: 0.85rem; color: var(--ink); }
.user-email { font-size: 0.68rem; color: var(--muted); margin-top: 0.1rem; }
.meta-text { font-size: 0.78rem; color: var(--warm-brown); }
.meta-num { font-family: var(--font-serif); font-size: 0.9rem; color: var(--ink); }
.price-val { font-family: var(--font-serif); font-size: 0.9rem; color: var(--rose-gold); }

.status-pill { font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.2rem 0.55rem; border: 1px solid; }
.pill--active   { border-color: rgba(102,187,106,0.35); color: #5a9e5e; }
.pill--inactive { border-color: rgba(224,112,112,0.3); color: #c07070; }

.action-row { display: flex; gap: 0.5rem; }
.action-btn { width: 30px; height: 30px; border: 1px solid rgba(196,135,106,0.2); display: flex; align-items: center; justify-content: center; font-size: 0.85rem; color: var(--muted); transition: all 0.2s; }
.action-btn:hover { border-color: var(--rose-gold); color: var(--rose-gold); }
.action-btn--danger:hover { border-color: #c07070; color: #c07070; }
.empty-row { text-align: center; padding: 3rem !important; }
.empty-icon { font-size: 2rem; color: var(--blush-mid); display: block; margin-bottom: 0.5rem; }
.empty-row p { font-size: 0.82rem; color: var(--muted); }
.pagination { display: flex; align-items: center; justify-content: center; gap: 1rem; }
.page-info { color: var(--muted); }
.btn-sm { padding: 0.55rem 1.2rem; font-size: 0.62rem; }

/* Drawer */
.drawer-overlay { position: fixed; inset: 0; z-index: 100; background: rgba(42,31,26,0.5); backdrop-filter: blur(4px); display: flex; justify-content: flex-end; }
.drawer { width: 400px; height: 100%; background: var(--bg-card); border-left: 1px solid rgba(196,135,106,0.2); display: flex; flex-direction: column; animation: fadeIn 0.25s var(--ease-silk); }
.drawer__head { display: flex; align-items: center; justify-content: space-between; padding: 1.5rem; border-bottom: 1px solid rgba(196,135,106,0.12); }
.drawer__title { font-family: var(--font-serif); font-size: 1rem; font-weight: 300; color: var(--ink); }
.drawer__close { font-size: 0.8rem; color: var(--muted); transition: color 0.2s; }
.drawer__close:hover { color: var(--rose-gold); }
.drawer__body { flex: 1; overflow-y: auto; padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.info-grid { display: flex; flex-direction: column; gap: 0.65rem; }
.info-row { display: flex; align-items: center; gap: 1rem; }
.info-key { color: var(--muted); width: 100px; flex-shrink: 0; font-size: 0.6rem; }
.info-val { font-size: 0.82rem; color: var(--ink); }
.drawer-sub { font-family: var(--font-serif); font-size: 0.9rem; font-weight: 300; color: var(--ink); }
.mini-orders { display: flex; flex-direction: column; gap: 0.5rem; }
.mini-order { display: flex; align-items: center; gap: 0.75rem; padding: 0.6rem 0; border-bottom: 1px solid rgba(196,135,106,0.06); }
.order-num { font-family: var(--font-serif); font-size: 0.82rem; color: var(--rose-gold); flex: 1; }
.order-status { font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.15rem 0.45rem; border: 1px solid rgba(196,135,106,0.2); color: var(--muted); }
.status--delivered { color: #5a9e5e; border-color: rgba(102,187,106,0.3); }
.status--cancelled { color: #c07070; border-color: rgba(224,112,112,0.3); }
.empty-mini { font-size: 0.78rem; color: var(--muted); }
</style>
