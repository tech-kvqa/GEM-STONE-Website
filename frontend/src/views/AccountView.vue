<!-- AccountView.vue -->
<template>
  <main class="account-page">
    <div style="height: var(--nav-h)"></div>
    <div class="container account-layout">
      <!-- Sidebar -->
      <aside class="account-sidebar">
        <div class="account-avatar">{{ auth.user?.full_name?.[0] }}</div>
        <div class="account-name">{{ auth.user?.full_name }}</div>
        <div class="account-email">{{ auth.user?.email }}</div>
        <nav class="account-nav">
          <button :class="{ active: tab === 'orders' }" @click="tab = 'orders'">My Orders</button>
          <button :class="{ active: tab === 'profile' }" @click="tab = 'profile'">Profile</button>
          <button @click="doLogout">Sign Out</button>
        </nav>
      </aside>

      <!-- Content -->
      <div class="account-content">
        <!-- Orders -->
        <div v-if="tab === 'orders'">
          <h2 class="account-title">My Orders</h2>
          <div v-if="orders.length" class="orders-list">
            <div v-for="order in orders" :key="order.id" class="order-card">
              <div class="order-card__head">
                <div>
                  <p class="order-num">{{ order.order_number }}</p>
                  <p class="order-date">{{ formatDate(order.created_at) }}</p>
                </div>
                <div class="order-card__right">
                  <span :class="['order-status', order.status]">{{ order.status }}</span>
                  <span class="order-total">₹{{ order.total.toLocaleString('en-IN') }}</span>
                </div>
              </div>
              <div class="order-items">
                <div v-for="item in order.items" :key="item.id" class="order-item">
                  <img :src="primaryImage(item.product)" :alt="item.product.name" />
                  <div>
                    <p>{{ item.product.name }}</p>
                    <p class="order-item__meta">Qty: {{ item.quantity }} · ₹{{ item.unit_price.toLocaleString('en-IN') }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <div class="empty-icon">✦</div>
            <p>No orders yet</p>
            <router-link to="/shop" class="btn btn-outline"><span>Start Shopping</span></router-link>
          </div>
        </div>

        <!-- Profile -->
        <div v-if="tab === 'profile'">
          <h2 class="account-title">My Profile</h2>
          <div class="form-grid">
            <div class="field">
              <label class="input-label">Full Name</label>
              <input v-model="profileForm.full_name" class="input-field" />
            </div>
            <div class="field">
              <label class="input-label">Phone</label>
              <input v-model="profileForm.phone" class="input-field" />
            </div>
            <div class="field span-2">
              <label class="input-label">Email</label>
              <input :value="auth.user?.email" class="input-field" disabled style="opacity:0.4" />
            </div>
          </div>
          <button class="btn btn-gold" @click="saveProfile"><span>Save Changes</span></button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify'
import { useAuthStore } from '@/store/auth'
import { orderApi, authApi } from '@/api'

const auth = useAuthStore()
const router = useRouter()
const tab = ref('orders')
const orders = ref([])

const profileForm = reactive({
  full_name: auth.user?.full_name || '',
  phone: auth.user?.phone || ''
})

const primaryImage = p =>
  p.images?.find(i => i.is_primary)?.url || p.images?.[0]?.url ||
  'https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=100'

function formatDate(d) {
  return new Date(d).toLocaleDateString('en-IN', { year: 'numeric', month: 'short', day: 'numeric' })
}

async function saveProfile() {
  try {
    await authApi.update(profileForm)
    await auth.fetchMe()
    toast.success('Profile updated')
  } catch { toast.error('Update failed') }
}

function doLogout() {
  auth.logout()
  router.push('/')
  toast.success('Signed out')
}

onMounted(async () => {
  const { data } = await orderApi.list()
  orders.value = data
})
</script>

<style scoped>
.account-layout {
  display: grid; grid-template-columns: 240px 1fr; gap: 3rem;
  padding-top: 3rem; padding-bottom: 5rem; align-items: start;
}
.account-sidebar {
  position: sticky; top: calc(var(--nav-h) + 2rem);
  text-align: center;
  border: 1px solid rgba(201,168,76,0.1); padding: 2rem;
}
.account-avatar {
  width: 64px; height: 64px; border-radius: 50%;
  background: var(--warm-dark); border: 2px solid var(--gold-dim);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-serif); font-size: 1.6rem; color: var(--gold);
  margin: 0 auto 0.75rem;
}
.account-name { font-family: var(--font-serif); font-size: 1.1rem; color: var(--ivory); margin-bottom: 0.2rem; }
.account-email { font-size: 0.72rem; color: var(--gold-dim); margin-bottom: 1.5rem; }
.account-nav { display: flex; flex-direction: column; gap: 0.25rem; }
.account-nav button {
  width: 100%; text-align: left; padding: 0.65rem 0.75rem;
  font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--ivory-dim); opacity: 0.55; transition: all 0.2s;
}
.account-nav button:hover { opacity: 1; color: var(--gold); padding-left: 1rem; }
.account-nav button.active { opacity: 1; color: var(--gold); border-left: 2px solid var(--gold); padding-left: calc(0.75rem - 2px); }

.account-title {
  font-family: var(--font-serif); font-size: 2rem; font-weight: 300;
  color: var(--ivory); margin-bottom: 2rem;
}
.orders-list { display: flex; flex-direction: column; gap: 1.5rem; }
.order-card { border: 1px solid rgba(201,168,76,0.1); padding: 1.5rem; }
.order-card__head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); }
.order-card__right { text-align: right; }
.order-num { font-family: var(--font-serif); font-size: 1rem; color: var(--gold); }
.order-date { font-size: 0.7rem; color: var(--ivory-dim); opacity: 0.4; margin-top: 0.2rem; }
.order-status { font-size: 0.62rem; letter-spacing: 0.12em; text-transform: uppercase; padding: 0.2rem 0.5rem; display: inline-block; margin-bottom: 0.3rem; }
.order-status.pending   { border: 1px solid rgba(201,168,76,0.3); color: var(--gold-dim); }
.order-status.confirmed, .order-status.shipped { border: 1px solid rgba(102,187,106,0.3); color: #66bb6a; }
.order-status.delivered { background: rgba(102,187,106,0.1); border: 1px solid #66bb6a; color: #66bb6a; }
.order-status.cancelled { border: 1px solid rgba(224,112,112,0.3); color: #e07070; }
.order-total { display: block; font-family: var(--font-serif); color: var(--ivory); }
.order-items { display: flex; flex-direction: column; gap: 0.75rem; }
.order-item { display: flex; align-items: center; gap: 0.75rem; }
.order-item img { width: 50px; height: 50px; object-fit: cover; background: var(--charcoal); }
.order-item p { font-size: 0.82rem; color: var(--ivory); }
.order-item__meta { font-size: 0.7rem; color: var(--gold-dim); margin-top: 0.15rem; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem; }
.field { display: flex; flex-direction: column; }
.span-2 { grid-column: 1 / -1; }

.empty-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem 0; text-align: center; }
.empty-icon { font-size: 3rem; color: var(--gold-dim); animation: float 3s ease-in-out infinite; }
.empty-state p { color: var(--ivory-dim); opacity: 0.5; }

@media (max-width: 768px) { .account-layout { grid-template-columns: 1fr; } }
</style>
