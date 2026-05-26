<template>
  <div class="admin-page">

    <!-- Back + header -->
    <div class="page-head">
      <div class="head-left">
        <router-link :to="{ name: 'AdminOrders' }" class="back-link">← All Orders</router-link>
        <h2 class="page-title">{{ order?.order_number || '…' }}</h2>
      </div>
      <div class="head-right" v-if="order">
        <span :class="['order-status', `status--${order.status}`]">{{ order.status }}</span>
        <span class="date-meta label-caps">{{ fmtDate(order.created_at) }}</span>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="skeleton-grid">
      <div class="skeleton" style="height:250px"></div>
      <div class="skeleton" style="height:250px"></div>
    </div>

    <template v-else-if="order">

      <div class="detail-grid">

        <!-- Left column -->
        <div class="detail-col">

          <!-- Items -->
          <div class="panel">
            <div class="panel__head">
              <h3 class="panel__title">Order Items</h3>
              <span class="panel__meta">{{ order.items?.length || 0 }} items</span>
            </div>
            <div class="items-list">
              <div v-for="item in order.items" :key="item.id" class="item-row">
                <img :src="item.product_image || 'https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=60'"
                  :alt="item.product_name" class="item-img" />
                <div class="item-info">
                  <p class="item-name">{{ item.product_name }}</p>
                  <p class="item-meta label-caps">Qty: {{ item.quantity }} · ₹{{ fmt(item.unit_price) }} each</p>
                </div>
                <p class="item-total">₹{{ fmt(item.total_price ?? item.total) }}</p>
              </div>
            </div>
            <div class="order-totals">
              <div class="total-row"><span>Subtotal</span><span>₹{{ fmt(order.subtotal) }}</span></div>
              <div class="total-row" v-if="order.discount > 0"><span>Discount</span><span class="discount-val">−₹{{ fmt(order.discount) }}</span></div>
              <div class="total-row" v-if="order.shipping_charge > 0"><span>Shipping</span><span>₹{{ fmt(order.shipping_charge) }}</span></div>
              <div class="total-row total-row--grand">
                <span>Total</span>
                <span class="grand-total">₹{{ fmt(order.total) }}</span>
              </div>
            </div>
          </div>

          <!-- Tracking timeline -->
          <div class="panel">
            <div class="panel__head">
              <h3 class="panel__title">Tracking Timeline</h3>
            </div>
            <div class="timeline">
              <div v-for="(t, i) in order.tracking" :key="t.id"
                :class="['timeline-event', { 'tl--last': i === order.tracking.length - 1 }]">
                <div class="tl-line"></div>
                <div :class="['tl-dot', `dot--${t.status}`]"></div>
                <div class="tl-content">
                  <p class="tl-status">{{ t.status }}</p>
                  <p class="tl-msg">{{ t.message }}</p>
                  <p class="tl-meta label-caps">{{ t.location }} · {{ fmtDate(t.created_at) }}</p>
                </div>
              </div>
              <div v-if="!order.tracking?.length" class="empty-state">
                <p>No tracking events yet</p>
              </div>
            </div>
          </div>

        </div>

        <!-- Right column -->
        <div class="detail-col">

          <!-- Update status -->
          <div class="panel">
            <div class="panel__head">
              <h3 class="panel__title">Update Order</h3>
            </div>
            <div class="update-form">
              <div class="field">
                <label class="input-label">New Status</label>
                <select v-model="statusForm.status" class="input-field">
                  <option v-for="s in validStatuses" :key="s" :value="s">{{ s }}</option>
                </select>
              </div>
              <div class="field">
                <label class="input-label">Tracking Number (optional)</label>
                <input v-model="statusForm.tracking_number" class="input-field" placeholder="e.g. DTDC123456" />
              </div>
              <div class="field">
                <label class="input-label">Note for customer (optional)</label>
                <input v-model="statusForm.message" class="input-field" placeholder="e.g. Your order has been dispatched" />
              </div>
              <button class="btn btn-gold w-full" :disabled="saving" @click="saveStatus">
                <span>{{ saving ? 'Updating…' : 'Update Status' }}</span>
              </button>
            </div>
          </div>

          <!-- Payment -->
          <div class="panel">
            <div class="panel__head">
              <h3 class="panel__title">Payment</h3>
            </div>
            <div class="info-grid">
              <div class="info-row">
                <span class="info-key label-caps">Method</span>
                <span class="info-val">{{ order.payment_method?.toUpperCase() }}</span>
              </div>
              <div class="info-row">
                <span class="info-key label-caps">Status</span>
                <span :class="['pay-badge', `pay--${order.payment_status}`]">{{ order.payment_status }}</span>
              </div>
            </div>
            <div class="update-form" style="margin-top:1rem">
              <div class="field">
                <label class="input-label">Update Payment Status</label>
                <select v-model="paymentStatus" class="input-field">
                  <option value="pending">Pending</option>
                  <option value="paid">Paid</option>
                  <option value="failed">Failed</option>
                  <option value="refunded">Refunded</option>
                </select>
              </div>
              <button class="btn btn-outline btn-sm w-full" @click="savePayment">
                <span>Update Payment</span>
              </button>
            </div>
          </div>

          <!-- Customer -->
          <div class="panel">
            <div class="panel__head">
              <h3 class="panel__title">Customer</h3>
            </div>
            <div class="info-grid">
              <div class="info-row">
                <span class="info-key label-caps">Name</span>
                <span class="info-val">{{ order.user_name }}</span>
              </div>
              <div class="info-row" v-if="order.user_email">
                <span class="info-key label-caps">Email</span>
                <span class="info-val">{{ order.user_email }}</span>
              </div>
            </div>
          </div>

          <!-- Shipping address -->
          <div class="panel">
            <div class="panel__head">
              <h3 class="panel__title">Shipping Address</h3>
            </div>
            <div class="address-block">
              <p class="address-name">{{ order.ship_name || order.shipping_name }}</p>
              <p>{{ order.ship_phone || order.shipping_phone }}</p>
              <p>{{ order.ship_address || order.shipping_line1 }}</p>
              <p>{{ order.ship_city || order.shipping_city }}, {{ order.ship_pincode || order.shipping_pincode }}</p>
              <p>{{ order.ship_state || order.shipping_state }}</p>
            </div>
          </div>

        </div>
      </div>

    </template>

    <div v-else class="error-state">
      <p class="empty-icon">◇</p>
      <p>Order not found</p>
      <router-link :to="{ name: 'AdminOrders' }" class="btn btn-outline" style="margin-top:1rem"><span>Back to Orders</span></router-link>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { toast } from 'vue3-toastify'
import { adminOrderApi } from '@/api'

const route   = useRoute()
const order   = ref(null)
const loading = ref(true)
const saving  = ref(false)

const validStatuses = ['pending','confirmed','processing','shipped','delivered','cancelled','refunded']
const statusForm   = ref({ status: 'pending', tracking_number: '', message: '' })
const paymentStatus = ref('pending')

async function load() {
  loading.value = true
  try {
    const { data } = await adminOrderApi.get(route.params.id)
    order.value      = data
    statusForm.value.status = data.status
    paymentStatus.value     = data.payment_status
  } catch { order.value = null } finally { loading.value = false }
}

async function saveStatus() {
  saving.value = true
  try {
    await adminOrderApi.updateStatus(order.value.id, {
      status:           statusForm.value.status,
      tracking_number:  statusForm.value.tracking_number || undefined,
      message:          statusForm.value.message         || undefined,
    })
    toast.success('Status updated')
    load()
  } catch (e) { toast.error(e?.response?.data?.detail || 'Update failed') } finally { saving.value = false }
}

async function savePayment() {
  try {
    await adminOrderApi.updatePayment(order.value.id, { payment_status: paymentStatus.value })
    toast.success('Payment status updated'); load()
  } catch { toast.error('Update failed') }
}

onMounted(load)

function fmt(n)    { return Number(n || 0).toLocaleString('en-IN') }
function fmtDate(d){ return d ? new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : '—' }
</script>

<style scoped>
.admin-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.head-left { display: flex; flex-direction: column; gap: 0.4rem; }
.back-link { font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--rose-gold); transition: opacity 0.2s; }
.back-link:hover { opacity: 0.7; }
.page-title { font-family: var(--font-serif); font-size: 2rem; font-weight: 300; color: var(--ink); }
.head-right { display: flex; align-items: center; gap: 1rem; padding-top: 0.5rem; }
.date-meta { color: var(--muted); }

.order-status { font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.25rem 0.65rem; border: 1px solid; }
.status--pending    { border-color: rgba(196,135,106,0.3); color: var(--rose-gold-dim); }
.status--confirmed  { border-color: rgba(100,181,246,0.35); color: #5a8fc0; }
.status--processing { border-color: rgba(196,168,212,0.3); color: var(--mauve); }
.status--shipped    { border-color: rgba(100,181,246,0.4); color: #4a80ba; }
.status--delivered  { background: rgba(102,187,106,0.08); border-color: rgba(102,187,106,0.4); color: #5a9e5e; }
.status--cancelled  { border-color: rgba(224,112,112,0.3); color: #c07070; }

/* Grid */
.skeleton-grid, .detail-grid { display: grid; grid-template-columns: 1fr 360px; gap: 1.25rem; align-items: start; }
.detail-col { display: flex; flex-direction: column; gap: 1.25rem; }

/* Panel */
.panel { background: var(--bg-card); border: 1px solid rgba(196,135,106,0.12); }
.panel__head { display: flex; align-items: center; justify-content: space-between; padding: 1.1rem 1.4rem; border-bottom: 1px solid rgba(196,135,106,0.1); }
.panel__title { font-family: var(--font-serif); font-size: 1rem; font-weight: 300; color: var(--ink); }
.panel__meta { font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); }

/* Items */
.items-list { padding: 0.5rem 0; }
.item-row { display: flex; align-items: center; gap: 0.9rem; padding: 0.9rem 1.4rem; border-bottom: 1px solid rgba(196,135,106,0.06); }
.item-img { width: 48px; height: 48px; object-fit: cover; flex-shrink: 0; }
.item-info { flex: 1; min-width: 0; }
.item-name { font-size: 0.85rem; color: var(--ink); }
.item-meta { color: var(--muted); font-size: 0.6rem; margin-top: 0.15rem; }
.item-total { font-family: var(--font-serif); font-size: 0.9rem; color: var(--ink); white-space: nowrap; }

/* Totals */
.order-totals { padding: 1rem 1.4rem; border-top: 1px solid rgba(196,135,106,0.08); display: flex; flex-direction: column; gap: 0.5rem; }
.total-row { display: flex; justify-content: space-between; font-size: 0.82rem; color: var(--warm-brown); }
.total-row--grand { border-top: 1px solid rgba(196,135,106,0.15); padding-top: 0.5rem; margin-top: 0.2rem; }
.grand-total { font-family: var(--font-serif); font-size: 1.1rem; color: var(--ink); }
.discount-val { color: #5a9e5e; }

/* Timeline */
.timeline { padding: 1.2rem 1.4rem; display: flex; flex-direction: column; gap: 0; }
.timeline-event { display: flex; gap: 1rem; position: relative; padding-bottom: 1.2rem; }
.tl-line { position: absolute; left: 7px; top: 16px; bottom: 0; width: 1px; background: rgba(196,135,106,0.2); }
.tl--last .tl-line { display: none; }
.tl-dot { width: 15px; height: 15px; border: 2px solid var(--rose-gold); flex-shrink: 0; margin-top: 3px; position: relative; z-index: 1; background: var(--bg-card); }
.dot--delivered { background: var(--rose-gold); }
.tl-content { flex: 1; padding-bottom: 0.5rem; }
.tl-status { font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--rose-gold); }
.tl-msg { font-size: 0.82rem; color: var(--ink); margin-top: 0.15rem; }
.tl-meta { color: var(--muted); font-size: 0.6rem; margin-top: 0.15rem; }

/* Update form */
.update-form { padding: 1.2rem 1.4rem; display: flex; flex-direction: column; gap: 0.9rem; }
.field { display: flex; flex-direction: column; gap: 0.35rem; }
.input-field { background: var(--bg-card); border: 1px solid rgba(196,135,106,0.2); color: var(--ink); }
.input-field:focus { border-color: var(--rose-gold); }
.w-full { width: 100%; }
.btn-sm { padding: 0.55rem 1rem; font-size: 0.62rem; }

/* Info grid */
.info-grid { padding: 1rem 1.4rem; display: flex; flex-direction: column; gap: 0.6rem; }
.info-row { display: flex; align-items: center; gap: 1rem; }
.info-key { color: var(--muted); width: 80px; flex-shrink: 0; }
.info-val { font-size: 0.82rem; color: var(--ink); }
.pay-badge { font-size: 0.6rem; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.18rem 0.5rem; border: 1px solid rgba(196,135,106,0.2); color: var(--muted); }
.pay--paid { border-color: rgba(102,187,106,0.3); color: #5a9e5e; }
.pay--failed { border-color: rgba(224,112,112,0.3); color: #c07070; }

/* Address */
.address-block { padding: 1rem 1.4rem; display: flex; flex-direction: column; gap: 0.3rem; }
.address-name { font-family: var(--font-serif); font-size: 1rem; color: var(--ink); }
.address-block p { font-size: 0.8rem; color: var(--warm-brown); }

.empty-state { padding: 2rem 1.4rem; text-align: center; }
.empty-state p { font-size: 0.8rem; color: var(--muted); }
.error-state { text-align: center; padding: 4rem; }
.empty-icon { font-size: 3rem; color: var(--blush-mid); display: block; margin-bottom: 0.5rem; }
.error-state p { font-size: 0.82rem; color: var(--muted); }

@media (max-width: 1024px) {
  .detail-grid, .skeleton-grid { grid-template-columns: 1fr; }
}
</style>
