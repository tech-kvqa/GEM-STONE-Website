<template>
  <div class="admin-page">

    <!-- Header -->
    <div class="page-head">
      <div>
        <p class="label-caps">Overview</p>
        <h2 class="page-title">Dashboard</h2>
      </div>
      <button @click="load" :disabled="loading" class="btn btn-ghost btn-sm">
        <span :class="loading && 'spin'">✦</span>
        <span>Refresh</span>
      </button>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="kpi-grid">
      <div v-for="i in 4" :key="i" class="kpi-card skeleton" style="height:108px"></div>
    </div>

    <template v-else-if="kpis">

      <!-- KPI Cards -->
      <div class="kpi-grid">
        <div class="kpi-card" v-for="c in kpiCards" :key="c.label">
          <div class="kpi-card__top">
            <span class="kpi-card__icon">{{ c.icon }}</span>
            <span class="kpi-card__tag" :class="c.alert ? 'kpi-tag--alert' : 'kpi-tag--ok'">
              {{ c.tag }}
            </span>
          </div>
          <p class="kpi-card__value">{{ c.value }}</p>
          <p class="kpi-card__label label-caps">{{ c.label }}</p>
        </div>
      </div>

      <!-- Charts row -->
      <div class="charts-row">

        <!-- Revenue bar chart -->
        <div class="panel panel--chart">
          <div class="panel__head">
            <h3 class="panel__title">Revenue — Last 7 Days</h3>
          </div>
          <div class="bar-chart">
            <div v-for="d in revenueChart" :key="d.date" class="bar-col">
              <span class="bar-tip">₹{{ fmtK(d.revenue) }}</span>
              <div class="bar" :style="{ height: barPct(d.revenue) + '%' }"></div>
              <span class="bar-label">{{ shortDate(d.date) }}</span>
            </div>
            <div v-if="!revenueChart.length" class="chart-empty">No data yet</div>
          </div>
        </div>

        <!-- Order status -->
        <div class="panel panel--status">
          <div class="panel__head">
            <h3 class="panel__title">Orders by Status</h3>
          </div>
          <div class="status-list">
            <div v-for="(count, status) in ordersByStatus" :key="status" class="status-row">
              <span class="status-dot" :class="`dot--${status}`"></span>
              <span class="status-name">{{ status }}</span>
              <span class="status-count">{{ count }}</span>
            </div>
            <div v-if="!Object.keys(ordersByStatus).length" class="chart-empty">No orders yet</div>
          </div>
        </div>
      </div>

      <!-- Bottom row -->
      <div class="bottom-row">

        <!-- Recent orders -->
        <div class="panel">
          <div class="panel__head">
            <h3 class="panel__title">Recent Orders</h3>
            <router-link :to="{ name: 'AdminOrders' }" class="panel__link">View all ↗</router-link>
          </div>
          <div class="order-list">
            <div v-for="o in recentOrders" :key="o.id" class="order-row">
              <div class="order-row__left">
                <p class="order-row__num">{{ o.order_number }}</p>
                <p class="order-row__name">{{ o.user_name || 'Guest' }}</p>
              </div>
              <span :class="['order-status', `status--${o.status}`]">{{ o.status }}</span>
              <p class="order-row__total">₹{{ fmt(o.total) }}</p>
            </div>
            <div v-if="!recentOrders.length" class="empty-state">
              <span class="empty-icon">◇</span><p>No orders yet</p>
            </div>
          </div>
        </div>

        <!-- Top products -->
        <div class="panel">
          <div class="panel__head">
            <h3 class="panel__title">Top Products</h3>
            <router-link :to="{ name: 'AdminProducts' }" class="panel__link">View all ↗</router-link>
          </div>
          <div class="top-products">
            <div v-for="(p, i) in topProducts" :key="p.name" class="top-row">
              <span class="top-rank">{{ i + 1 }}</span>
              <div class="top-row__info">
                <p class="top-row__name">{{ p.name }}</p>
                <p class="top-row__units label-caps">{{ p.units }} sold</p>
              </div>
              <p class="top-row__revenue">₹{{ fmt(p.revenue) }}</p>
            </div>
            <div v-if="!topProducts.length" class="empty-state">
              <span class="empty-icon">◇</span><p>No sales data yet</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Alerts -->
      <div v-if="kpis.low_stock_products > 0 || kpis.pending_consultations > 0" class="alerts-row">
        <div v-if="kpis.low_stock_products > 0" class="alert-card alert-card--warn">
          <span class="alert-card__icon">⚠</span>
          <div>
            <p class="alert-card__title">Low Stock Alert</p>
            <p class="alert-card__sub">{{ kpis.low_stock_products }} products with ≤10 units remaining</p>
          </div>
          <router-link :to="{ name: 'AdminInventory' }" class="btn btn-outline btn-sm">Review</router-link>
        </div>
        <div v-if="kpis.pending_consultations > 0" class="alert-card alert-card--info">
          <span class="alert-card__icon">✦</span>
          <div>
            <p class="alert-card__title">Pending Consultations</p>
            <p class="alert-card__sub">{{ kpis.pending_consultations }} bookings awaiting your response</p>
          </div>
          <router-link :to="{ name: 'AdminConsultations' }" class="btn btn-outline btn-sm">Review</router-link>
        </div>
      </div>

    </template>

    <div v-else class="error-state">
      <p class="empty-icon">◇</p>
      <p>Failed to load dashboard — check your backend connection.</p>
      <button @click="load" class="btn btn-outline" style="margin-top:1rem"><span>Retry</span></button>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminAuthStore } from '@/store/adminAuth'
import { adminDashboardApi } from '@/api'

const adminAuth     = useAdminAuthStore()
const loading       = ref(false)
const kpis          = ref(null)
const revenueChart  = ref([])
const topProducts   = ref([])
const recentOrders  = ref([])
const ordersByStatus = ref({})

async function load() {
  loading.value = true
  try {
    const { data } = await adminDashboardApi.summary()
    kpis.value           = data.kpis || {}
    revenueChart.value   = data.revenue_last_7_days || []
    topProducts.value    = data.top_products || []
    recentOrders.value   = data.recent_orders || []
    ordersByStatus.value = data.kpis?.orders_by_status || {}
  } catch (e) { kpis.value = null } finally { loading.value = false }
}

onMounted(load)

const kpiCards = computed(() => [
  { icon: '◈', label: 'Total Revenue', value: '₹' + fmt(kpis.value?.total_revenue || 0), tag: 'All time', alert: false },
  { icon: '◻', label: 'Total Orders',  value: kpis.value?.total_orders  || 0, tag: (kpis.value?.orders_by_status?.pending || 0) + ' pending', alert: false },
  { icon: '◉', label: 'Customers',     value: kpis.value?.total_users   || 0, tag: 'Registered', alert: false },
  { icon: '▣', label: 'Low Stock',     value: kpis.value?.low_stock_products || 0, tag: 'Alert', alert: (kpis.value?.low_stock_products || 0) > 0 },
])

const maxRev = computed(() => Math.max(...revenueChart.value.map(d => d.revenue), 1))
function barPct(r) { return Math.max((r / maxRev.value) * 100, 2) }
function fmt(n)   { return Number(n || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 }) }
function fmtK(n)  { return n >= 1000 ? (n / 1000).toFixed(1) + 'k' : Math.round(n) }
function shortDate(d) { return d ? new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' }) : '' }
</script>

<style scoped>
.admin-page { display: flex; flex-direction: column; gap: 1.75rem; }

/* Head */
.page-head { display: flex; align-items: flex-end; justify-content: space-between; }
.page-title { font-family: var(--font-serif); font-size: 2rem; font-weight: 300; color: var(--ink); margin-top: 0.2rem; }
.btn-sm { padding: 0.55rem 1.2rem; font-size: 0.62rem; }
.spin { display: inline-block; animation: sparkle 1.2s linear infinite; }

/* KPI Grid */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.kpi-card {
  background: var(--bg-card);
  border: 1px solid rgba(196,135,106,0.12);
  padding: 1.5rem;
  transition: box-shadow var(--dur-fast);
}
.kpi-card:hover { box-shadow: 0 4px 20px rgba(196,135,106,0.1); }
.kpi-card__top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.kpi-card__icon { font-size: 1.3rem; color: var(--rose-gold); }
.kpi-card__tag {
  font-size: 0.58rem; letter-spacing: 0.12em; text-transform: uppercase;
  padding: 0.2rem 0.5rem;
}
.kpi-tag--ok   { background: rgba(102,187,106,0.1); color: #5a9e5e; }
.kpi-tag--alert { background: rgba(224,112,112,0.1); color: #c07070; }
.kpi-card__value { font-family: var(--font-serif); font-size: 1.8rem; font-weight: 300; color: var(--ink); }
.kpi-card__label { margin-top: 0.2rem; }

/* Charts row */
.charts-row { display: grid; grid-template-columns: 1fr 320px; gap: 1rem; }
.panel {
  background: var(--bg-card);
  border: 1px solid rgba(196,135,106,0.12);
  overflow: hidden;
}
.panel__head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid rgba(196,135,106,0.1);
}
.panel__title { font-family: var(--font-serif); font-size: 1rem; font-weight: 300; color: var(--ink); }
.panel__link { font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--rose-gold); }
.panel__link:hover { text-decoration: underline; }

/* Bar chart */
.bar-chart { display: flex; align-items: flex-end; gap: 0.5rem; padding: 1.5rem; height: 180px; }
.bar-col { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 0.4rem; height: 100%; justify-content: flex-end; }
.bar-tip { font-size: 0.6rem; color: var(--muted); }
.bar { width: 100%; background: linear-gradient(to top, var(--rose-gold-deep), var(--rose-gold)); transition: height 0.6s var(--ease-silk); min-height: 3px; }
.bar-label { font-size: 0.6rem; color: var(--muted); white-space: nowrap; }
.chart-empty { width: 100%; text-align: center; color: var(--light-muted); font-size: 0.8rem; align-self: center; }

/* Status list */
.status-list { padding: 1.2rem 1.5rem; display: flex; flex-direction: column; gap: 0.75rem; }
.status-row { display: flex; align-items: center; gap: 0.75rem; }
.status-dot { width: 8px; height: 8px; flex-shrink: 0; }
.dot--pending    { background: var(--dusty-rose); }
.dot--confirmed  { background: #66bb6a; }
.dot--processing { background: var(--lavender); }
.dot--shipped    { background: #64b5f6; }
.dot--delivered  { background: #66bb6a; }
.dot--cancelled  { background: #e07070; }
.dot--refunded   { background: var(--muted); }
.status-name { flex: 1; font-size: 0.78rem; color: var(--warm-brown); text-transform: capitalize; }
.status-count { font-family: var(--font-serif); font-size: 1rem; color: var(--ink); }

/* Bottom row */
.bottom-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

/* Order list */
.order-list { padding: 0.5rem 0; }
.order-row {
  display: flex; align-items: center; gap: 1rem;
  padding: 0.85rem 1.5rem;
  border-bottom: 1px solid rgba(196,135,106,0.06);
  transition: background 0.15s;
}
.order-row:hover { background: rgba(196,135,106,0.03); }
.order-row__left { flex: 1; min-width: 0; }
.order-row__num { font-family: var(--font-serif); font-size: 0.85rem; color: var(--rose-gold); }
.order-row__name { font-size: 0.7rem; color: var(--muted); margin-top: 0.1rem; }
.order-row__total { font-family: var(--font-serif); font-size: 0.9rem; color: var(--ink); white-space: nowrap; }

/* Order status badge */
.order-status {
  font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase;
  padding: 0.2rem 0.55rem; border: 1px solid; white-space: nowrap;
}
.status--pending    { border-color: rgba(196,135,106,0.3); color: var(--rose-gold-dim); }
.status--confirmed,
.status--shipped    { border-color: rgba(102,187,106,0.35); color: #5a9e5e; }
.status--delivered  { background: rgba(102,187,106,0.08); border-color: #66bb6a; color: #5a9e5e; }
.status--cancelled  { border-color: rgba(224,112,112,0.3); color: #c07070; }
.status--processing { border-color: rgba(196,168,212,0.3); color: var(--mauve); }

/* Top products */
.top-products { padding: 0.5rem 0; }
.top-row {
  display: flex; align-items: center; gap: 1rem;
  padding: 0.85rem 1.5rem;
  border-bottom: 1px solid rgba(196,135,106,0.06);
}
.top-rank {
  font-family: var(--font-serif); font-size: 1.2rem;
  color: var(--blush-mid); width: 20px; text-align: center; flex-shrink: 0;
}
.top-row__info { flex: 1; min-width: 0; }
.top-row__name { font-size: 0.82rem; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.top-row__units { color: var(--muted); font-size: 0.58rem; margin-top: 0.1rem; }
.top-row__revenue { font-family: var(--font-serif); font-size: 0.9rem; color: var(--rose-gold); white-space: nowrap; }

/* Alerts */
.alerts-row { display: flex; flex-direction: column; gap: 0.75rem; }
.alert-card {
  display: flex; align-items: center; gap: 1.2rem;
  padding: 1.2rem 1.5rem;
  border: 1px solid;
}
.alert-card--warn { background: rgba(196,135,106,0.05); border-color: rgba(196,135,106,0.25); }
.alert-card--info { background: rgba(200,180,212,0.05); border-color: rgba(200,180,212,0.25); }
.alert-card__icon { font-size: 1.4rem; color: var(--rose-gold); flex-shrink: 0; }
.alert-card__title { font-family: var(--font-serif); font-size: 0.95rem; color: var(--ink); }
.alert-card__sub { font-size: 0.72rem; color: var(--muted); margin-top: 0.15rem; }
.alert-card .btn-outline { margin-left: auto; flex-shrink: 0; }

/* Empty / error */
.empty-state { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; padding: 2.5rem; text-align: center; }
.empty-icon { font-size: 2rem; color: var(--blush-mid); display: block; }
.empty-state p, .error-state p { font-size: 0.82rem; color: var(--muted); }
.error-state { text-align: center; padding: 4rem 2rem; }
.error-state .empty-icon { font-size: 3rem; color: var(--blush-mid); margin-bottom: 0.5rem; }

@media (max-width: 1024px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
  .charts-row { grid-template-columns: 1fr; }
  .bottom-row { grid-template-columns: 1fr; }
}
</style>
