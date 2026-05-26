<template>
  <div class="admin-page">

    <div class="page-head">
      <div>
        <p class="label-caps">Stock Control</p>
        <h2 class="page-title">Inventory</h2>
      </div>
      <button @click="load" :disabled="loading" class="btn btn-ghost btn-sm">
        <span>Refresh</span>
      </button>
    </div>

    <!-- Stock summary cards -->
    <div v-if="summary" class="kpi-grid">
      <div class="kpi-card">
        <span class="kpi-card__icon">▣</span>
        <p class="kpi-card__value">{{ summary.total_products }}</p>
        <p class="kpi-card__label label-caps">Total Products</p>
      </div>
      <div class="kpi-card kpi-card--warn">
        <span class="kpi-card__icon">⚠</span>
        <p class="kpi-card__value">{{ summary.low_stock?.length || 0 }}</p>
        <p class="kpi-card__label label-caps">Low Stock (≤10)</p>
      </div>
      <div class="kpi-card kpi-card--danger">
        <span class="kpi-card__icon">◯</span>
        <p class="kpi-card__value">{{ summary.out_of_stock?.length || 0 }}</p>
        <p class="kpi-card__label label-caps">Out of Stock</p>
      </div>
    </div>

    <!-- View toggle -->
    <div class="view-toggle">
      <button :class="['toggle-btn', { 'toggle-btn--active': view === 'all' }]" @click="view = 'all'">All Products</button>
      <button :class="['toggle-btn', { 'toggle-btn--active': view === 'low' }]" @click="view = 'low'">
        Low Stock
        <span v-if="summary?.low_stock?.length" class="toggle-count">{{ summary.low_stock.length }}</span>
      </button>
      <button :class="['toggle-btn', { 'toggle-btn--active': view === 'out' }]" @click="view = 'out'">
        Out of Stock
        <span v-if="summary?.out_of_stock?.length" class="toggle-count toggle-count--danger">{{ summary.out_of_stock.length }}</span>
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="table-wrap">
      <div v-for="i in 8" :key="i" class="skeleton" style="height:56px;margin-bottom:1px"></div>
    </div>

    <!-- Table -->
    <div v-else class="table-wrap">
      <table class="admin-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th>SKU</th>
            <th class="col-num">Price</th>
            <th class="col-num">Stock</th>
            <th class="col-num">Sold</th>
            <th>Status</th>
            <th>Quick Edit</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in displayedProducts" :key="p.id"
            :class="{ 'row--out': p.stock_qty === 0, 'row--low': p.stock_qty > 0 && p.stock_qty <= 10 }">
            <td>
              <div class="prod-cell">
                <img :src="p.images?.[0] || 'https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=60'"
                  :alt="p.name" class="prod-thumb" />
                <p class="prod-name">{{ p.name }}</p>
              </div>
            </td>
            <td><span class="tag-pill">{{ p.category || '—' }}</span></td>
            <td><span class="sku-text">{{ p.sku || '—' }}</span></td>
            <td class="col-num"><span class="price-val">₹{{ fmt(p.price) }}</span></td>
            <td class="col-num">
              <span :class="['stock-badge', stockClass(p.stock_qty)]">{{ p.stock_qty ?? '—' }}</span>
            </td>
            <td class="col-num"><span class="sold-val">{{ p.total_sold ?? '—' }}</span></td>
            <td>
              <span :class="['status-pill', p.is_active ? 'pill--active' : 'pill--inactive']">
                {{ p.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td>
              <div class="quick-edit">
                <input v-model.number="p._newStock" type="number" min="0"
                  :placeholder="String(p.stock_qty ?? 0)"
                  class="input-field stock-input" />
                <button class="action-btn" @click="updateStock(p)" title="Save stock">✓</button>
              </div>
            </td>
          </tr>
          <tr v-if="!displayedProducts.length">
            <td colspan="8" class="empty-row">
              <span class="empty-icon">◇</span>
              <p>{{ view === 'low' ? 'No low-stock products — great!' : view === 'out' ? 'No out-of-stock products!' : 'No products found' }}</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { toast } from 'vue3-toastify'
import { adminDashboardApi, adminProductApi } from '@/api'

const summary  = ref(null)
const loading  = ref(false)
const view     = ref('all')

const displayedProducts = computed(() => {
  if (!summary.value) return []
  const list = view.value === 'low' ? summary.value.low_stock
             : view.value === 'out' ? summary.value.out_of_stock
             : summary.value.all_products
  return (list || []).map(p => ({ ...p, _newStock: null }))
})

async function load() {
  loading.value = true
  try {
    const { data } = await adminDashboardApi.inventory()
    summary.value = data
  } catch { toast.error('Failed to load inventory') } finally { loading.value = false }
}

onMounted(load)

async function updateStock(p) {
  if (p._newStock === null || p._newStock === undefined || p._newStock === '') return
  try {
    await adminProductApi.update(p.id, { stock_qty: Number(p._newStock) })
    toast.success(`Stock updated for "${p.name}"`)
    load()
  } catch { toast.error('Stock update failed') }
}

function fmt(n) { return Number(n || 0).toLocaleString('en-IN') }
function stockClass(s) {
  if (s === 0)   return 'stock--out'
  if (s <= 10)   return 'stock--low'
  return 'stock--ok'
}
</script>

<style scoped>
.admin-page { display: flex; flex-direction: column; gap: 1.5rem; }

.page-head { display: flex; align-items: flex-end; justify-content: space-between; }
.page-title { font-family: var(--font-serif); font-size: 2rem; font-weight: 300; color: var(--ink); margin-top: 0.2rem; }
.btn-sm { padding: 0.55rem 1.2rem; font-size: 0.62rem; }

/* KPI cards */
.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.kpi-card {
  background: var(--bg-card);
  border: 1px solid rgba(196,135,106,0.12);
  padding: 1.5rem;
  display: flex; flex-direction: column; gap: 0.4rem;
}
.kpi-card--warn   { border-color: rgba(196,135,106,0.3); background: rgba(196,135,106,0.04); }
.kpi-card--danger { border-color: rgba(224,112,112,0.25); background: rgba(224,112,112,0.04); }
.kpi-card__icon { font-size: 1.3rem; color: var(--rose-gold); }
.kpi-card--warn .kpi-card__icon   { color: var(--rose-gold); }
.kpi-card--danger .kpi-card__icon { color: #c07070; }
.kpi-card__value { font-family: var(--font-serif); font-size: 1.8rem; font-weight: 300; color: var(--ink); }
.kpi-card__label { }

/* View toggle */
.view-toggle { display: flex; gap: 0; border-bottom: 1px solid rgba(196,135,106,0.15); }
.toggle-btn {
  padding: 0.7rem 1.2rem;
  font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--muted);
  border-bottom: 2px solid transparent;
  display: flex; align-items: center; gap: 0.5rem;
  transition: all var(--dur-fast);
}
.toggle-btn:hover { color: var(--rose-gold); }
.toggle-btn--active { color: var(--rose-gold); border-bottom-color: var(--rose-gold); }
.toggle-count {
  font-size: 0.6rem; padding: 0.1rem 0.45rem;
  background: rgba(196,135,106,0.12); color: var(--rose-gold);
}
.toggle-count--danger { background: rgba(224,112,112,0.1); color: #c07070; }

/* Table */
.table-wrap { background: var(--bg-card); border: 1px solid rgba(196,135,106,0.12); overflow-x: auto; }
.admin-table { width: 100%; border-collapse: collapse; }
.admin-table thead { background: var(--bg-section); border-bottom: 1px solid rgba(196,135,106,0.15); }
.admin-table th {
  padding: 0.85rem 1.2rem; text-align: left;
  font-size: 0.6rem; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--rose-gold-dim); font-weight: 500;
}
.col-num { text-align: right; }
.admin-table td { padding: 0.9rem 1.2rem; border-bottom: 1px solid rgba(196,135,106,0.06); vertical-align: middle; }
.admin-table tbody tr:hover { background: rgba(196,135,106,0.025); }
.row--out { background: rgba(224,112,112,0.03) !important; }
.row--low { background: rgba(196,135,106,0.04) !important; }

.prod-cell { display: flex; align-items: center; gap: 0.75rem; }
.prod-thumb { width: 42px; height: 42px; object-fit: cover; flex-shrink: 0; }
.prod-name { font-size: 0.82rem; color: var(--ink); }
.tag-pill { font-size: 0.62rem; padding: 0.2rem 0.6rem; background: rgba(196,135,106,0.08); color: var(--rose-gold-dim); }
.sku-text { font-size: 0.72rem; color: var(--muted); font-family: monospace; }
.price-val { font-family: var(--font-serif); font-size: 0.9rem; color: var(--ink); }
.sold-val  { font-family: var(--font-serif); font-size: 0.9rem; color: var(--muted); }

.stock-badge { font-size: 0.75rem; padding: 0.2rem 0.55rem; font-weight: 500; }
.stock--ok  { background: rgba(102,187,106,0.1); color: #5a9e5e; }
.stock--low { background: rgba(196,135,106,0.12); color: var(--rose-gold); }
.stock--out { background: rgba(224,112,112,0.1); color: #c07070; }

.status-pill { font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.2rem 0.55rem; border: 1px solid; }
.pill--active   { border-color: rgba(102,187,106,0.35); color: #5a9e5e; }
.pill--inactive { border-color: rgba(196,135,106,0.25); color: var(--muted); }

/* Quick edit */
.quick-edit { display: flex; align-items: center; gap: 0.4rem; }
.stock-input { width: 72px; padding: 0.4rem 0.55rem; font-size: 0.8rem; text-align: center; background: var(--bg-card); border: 1px solid rgba(196,135,106,0.2); color: var(--ink); }
.stock-input:focus { border-color: var(--rose-gold); outline: none; }
.action-btn { width: 28px; height: 28px; border: 1px solid rgba(102,187,106,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: #5a9e5e; transition: all 0.2s; }
.action-btn:hover { background: rgba(102,187,106,0.1); }

.empty-row { text-align: center; padding: 3rem !important; }
.empty-icon { font-size: 2rem; color: var(--blush-mid); display: block; margin-bottom: 0.5rem; }
.empty-row p { font-size: 0.82rem; color: var(--muted); }

@media (max-width: 768px) { .kpi-grid { grid-template-columns: 1fr; } }
</style>
