<template>
  <div class="admin-page">

    <div class="page-head">
      <div>
        <p class="label-caps">Order Management</p>
        <h2 class="page-title">Orders</h2>
      </div>
      <span class="result-badge">{{ total }} total</span>
    </div>

    <!-- Status tabs -->
    <div class="status-tabs">
      <button v-for="tab in statusTabs" :key="tab.value"
        :class="['status-tab', { 'status-tab--active': filterStatus === tab.value }]"
        @click="filterStatus = tab.value; page = 1; load()">
        {{ tab.label }}
      </button>
    </div>

    <!-- Search + date filters -->
    <div class="filter-bar">
      <input v-model="search" @input="debounceLoad" placeholder="Order number or customer name…"
        class="input-field filter-search" />
      <input v-model="dateFrom" type="date" @change="load" class="input-field filter-date" />
      <span class="filter-sep">to</span>
      <input v-model="dateTo" type="date" @change="load" class="input-field filter-date" />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="table-wrap">
      <div v-for="i in 8" :key="i" class="skeleton" style="height:58px;margin-bottom:1px"></div>
    </div>

    <!-- Table -->
    <div v-else class="table-wrap">
      <table class="admin-table">
        <thead>
          <tr>
            <th>Order #</th>
            <th>Customer</th>
            <th>Date</th>
            <th>Payment</th>
            <th class="col-num">Total</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="o in orders" :key="o.id">
            <td><span class="order-num">{{ o.order_number }}</span></td>
            <td>
              <p class="customer-name">{{ o.user_name || 'Guest' }}</p>
              <p class="customer-email">{{ o.user_email }}</p>
            </td>
            <td><span class="date-cell">{{ fmtDate(o.created_at) }}</span></td>
            <td>
              <span :class="['pay-badge', `pay--${o.payment_status}`]">
                {{ o.payment_method }} · {{ o.payment_status }}
              </span>
            </td>
            <td class="col-num">
              <span class="price-val">₹{{ fmt(o.total) }}</span>
            </td>
            <td>
              <span :class="['order-status', `status--${o.status}`]">{{ o.status }}</span>
            </td>
            <td>
              <router-link :to="{ name: 'AdminOrderDetail', params: { id: o.id } }"
                class="action-btn" title="View detail">→</router-link>
            </td>
          </tr>
          <tr v-if="!orders.length">
            <td colspan="7" class="empty-row">
              <span class="empty-icon">◇</span>
              <p>No orders found</p>
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

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { toast } from 'vue3-toastify'
import { adminOrderApi } from '@/api'

const orders      = ref([])
const total       = ref(0)
const loading     = ref(false)
const page        = ref(1)
const limit       = 20
const search      = ref('')
const filterStatus = ref('')
const dateFrom    = ref('')
const dateTo      = ref('')
let   timer       = null

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / limit)))

const statusTabs = [
  { label: 'All',         value: '' },
  { label: 'Pending',     value: 'pending' },
  { label: 'Confirmed',   value: 'confirmed' },
  { label: 'Processing',  value: 'processing' },
  { label: 'Shipped',     value: 'shipped' },
  { label: 'Delivered',   value: 'delivered' },
  { label: 'Cancelled',   value: 'cancelled' },
]

async function load() {
  loading.value = true
  try {
    const params = { page: page.value, limit }
    if (filterStatus.value) params.status   = filterStatus.value
    if (search.value)       params.search   = search.value
    if (dateFrom.value)     params.date_from = dateFrom.value
    if (dateTo.value)       params.date_to   = dateTo.value
    const { data } = await adminOrderApi.list(params)
    orders.value = data.orders || []
    total.value  = data.total  || 0
  } catch { toast.error('Failed to load orders') } finally { loading.value = false }
}

function debounceLoad() {
  clearTimeout(timer)
  timer = setTimeout(() => { page.value = 1; load() }, 400)
}

onMounted(load)

function fmt(n)    { return Number(n || 0).toLocaleString('en-IN') }
function fmtDate(d){ return d ? new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : '—' }
</script>

<style scoped>
.admin-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-head { display: flex; align-items: flex-end; justify-content: space-between; }
.page-title { font-family: var(--font-serif); font-size: 2rem; font-weight: 300; color: var(--ink); margin-top: 0.2rem; }
.result-badge { font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }

/* Status tabs */
.status-tabs { display: flex; gap: 0; border-bottom: 1px solid rgba(196,135,106,0.15); overflow-x: auto; }
.status-tab {
  padding: 0.7rem 1.1rem;
  font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--muted);
  border-bottom: 2px solid transparent;
  white-space: nowrap;
  transition: all var(--dur-fast);
}
.status-tab:hover { color: var(--rose-gold); }
.status-tab--active { color: var(--rose-gold); border-bottom-color: var(--rose-gold); }

/* Filter bar */
.filter-bar { display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap; }
.filter-search { flex: 1; min-width: 220px; }
.filter-date { width: 150px; }
.filter-sep { font-size: 0.75rem; color: var(--muted); }
.input-field { background: var(--bg-card); border: 1px solid rgba(196,135,106,0.2); color: var(--ink); }
.input-field:focus { border-color: var(--rose-gold); }

/* Table */
.table-wrap { background: var(--bg-card); border: 1px solid rgba(196,135,106,0.12); overflow-x: auto; }
.admin-table { width: 100%; border-collapse: collapse; }
.admin-table thead { background: var(--bg-section); border-bottom: 1px solid rgba(196,135,106,0.15); }
.admin-table th {
  padding: 0.85rem 1.2rem;
  text-align: left;
  font-size: 0.6rem; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--rose-gold-dim); font-weight: 500;
}
.col-num { text-align: right; }
.admin-table td { padding: 0.9rem 1.2rem; border-bottom: 1px solid rgba(196,135,106,0.06); vertical-align: middle; }
.admin-table tbody tr:hover { background: rgba(196,135,106,0.025); }

.order-num { font-family: var(--font-serif); font-size: 0.9rem; color: var(--rose-gold); }
.customer-name { font-size: 0.82rem; color: var(--ink); }
.customer-email { font-size: 0.68rem; color: var(--muted); margin-top: 0.1rem; }
.date-cell { font-size: 0.75rem; color: var(--warm-brown); }
.price-val { font-family: var(--font-serif); font-size: 0.9rem; color: var(--ink); }

.pay-badge { font-size: 0.6rem; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.18rem 0.5rem; border: 1px solid rgba(196,135,106,0.2); color: var(--muted); }
.pay--paid { border-color: rgba(102,187,106,0.3); color: #5a9e5e; }
.pay--failed { border-color: rgba(224,112,112,0.3); color: #c07070; }

.order-status { font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.2rem 0.55rem; border: 1px solid; white-space: nowrap; }
.status--pending    { border-color: rgba(196,135,106,0.3); color: var(--rose-gold-dim); }
.status--confirmed  { border-color: rgba(100,181,246,0.3); color: #5a8fc0; }
.status--processing { border-color: rgba(196,168,212,0.3); color: var(--mauve); }
.status--shipped    { border-color: rgba(100,181,246,0.35); color: #4a80ba; }
.status--delivered  { background: rgba(102,187,106,0.08); border-color: rgba(102,187,106,0.4); color: #5a9e5e; }
.status--cancelled  { border-color: rgba(224,112,112,0.3); color: #c07070; }
.status--refunded   { border-color: rgba(196,135,106,0.2); color: var(--muted); }

.action-btn {
  display: inline-flex; align-items: center; justify-content: center;
  width: 30px; height: 30px; border: 1px solid rgba(196,135,106,0.2);
  font-size: 0.9rem; color: var(--muted); transition: all 0.2s;
}
.action-btn:hover { border-color: var(--rose-gold); color: var(--rose-gold); background: rgba(196,135,106,0.06); }

.empty-row { text-align: center; padding: 3rem !important; }
.empty-icon { font-size: 2rem; color: var(--blush-mid); display: block; margin-bottom: 0.5rem; }
.empty-row p { font-size: 0.82rem; color: var(--muted); }

.pagination { display: flex; align-items: center; justify-content: center; gap: 1rem; }
.page-info { color: var(--muted); }
.btn-sm { padding: 0.55rem 1.2rem; font-size: 0.62rem; }
</style>
