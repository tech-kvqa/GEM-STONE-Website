<template>
  <div class="admin-page">

    <div class="page-head">
      <div>
        <p class="label-caps">Moderation</p>
        <h2 class="page-title">Reviews</h2>
      </div>
      <span class="result-badge">{{ total }} reviews</span>
    </div>

    <!-- Approval tabs -->
    <div class="status-tabs">
      <button v-for="tab in tabs" :key="tab.value"
        :class="['status-tab', { 'status-tab--active': filterApproved === tab.value }]"
        @click="filterApproved = tab.value; page = 1; load()">
        {{ tab.label }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="review-list">
      <div v-for="i in 5" :key="i" class="skeleton" style="height:120px;margin-bottom:1px"></div>
    </div>

    <!-- Reviews -->
    <div v-else class="review-list">
      <div v-for="r in reviews" :key="r.id" class="review-card">
        <div class="review-card__head">
          <div class="review-card__left">
            <div class="reviewer-avatar">{{ r.user_name?.[0]?.toUpperCase() || '?' }}</div>
            <div>
              <p class="reviewer-name">{{ r.user_name || 'Anonymous' }}</p>
              <p class="review-product label-caps">{{ r.product_name }}</p>
            </div>
          </div>
          <div class="review-card__right">
            <div class="stars">
              <span v-for="i in 5" :key="i" :class="i <= r.rating ? 'star-filled' : 'star-empty'">★</span>
            </div>
            <span :class="['review-badge', r.is_approved ? 'badge--approved' : 'badge--pending']">
              {{ r.is_approved ? 'Approved' : 'Pending' }}
            </span>
          </div>
        </div>

        <div class="review-card__body">
          <p v-if="r.title" class="review-title">{{ r.title }}</p>
          <p class="review-body">{{ r.body || '—' }}</p>
          <p class="review-date label-caps">{{ fmtDate(r.created_at) }}</p>
        </div>

        <div class="review-card__foot" v-if="!r.is_approved">
          <button class="btn btn-gold btn-sm" @click="approve(r)">
            <span>Approve Review</span>
          </button>
          <p class="review-hint">Once approved, this review will appear on the product page.</p>
        </div>
        <div class="review-card__foot review-card__foot--approved" v-else>
          <span class="approved-mark">✦ Published on product page</span>
        </div>
      </div>

      <div v-if="!reviews.length" class="empty-state">
        <span class="empty-icon">★</span>
        <p>No reviews found</p>
      </div>
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
import { adminReviewApi } from '@/api'

const reviews  = ref([])
const total    = ref(0)
const loading  = ref(false)
const page     = ref(1)
const limit    = 20
const filterApproved = ref('')

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / limit)))

const tabs = [
  { label: 'All Reviews',    value: '' },
  { label: 'Pending',        value: '0' },
  { label: 'Approved',       value: '1' },
]

async function load() {
  loading.value = true
  try {
    const params = { page: page.value, limit }
    if (filterApproved.value !== '') params.approved = Number(filterApproved.value)
    const { data } = await adminReviewApi.list(params)
    reviews.value = data.reviews || []
    total.value   = data.total   || 0
  } catch { toast.error('Failed to load reviews') } finally { loading.value = false }
}

onMounted(load)

async function approve(r) {
  try {
    await adminReviewApi.approve(r.id)
    toast.success('Review approved and published')
    load()
  } catch { toast.error('Failed to approve review') }
}

function fmtDate(d) {
  return d ? new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'
}
</script>

<style scoped>
.admin-page { display: flex; flex-direction: column; gap: 1.5rem; }

.page-head { display: flex; align-items: flex-end; justify-content: space-between; }
.page-title { font-family: var(--font-serif); font-size: 2rem; font-weight: 300; color: var(--ink); margin-top: 0.2rem; }
.result-badge { font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }

/* Tabs */
.status-tabs { display: flex; border-bottom: 1px solid rgba(196,135,106,0.15); }
.status-tab { padding: 0.7rem 1.1rem; font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); border-bottom: 2px solid transparent; transition: all var(--dur-fast); }
.status-tab:hover { color: var(--rose-gold); }
.status-tab--active { color: var(--rose-gold); border-bottom-color: var(--rose-gold); }

/* Review list */
.review-list { display: flex; flex-direction: column; gap: 1px; }

.review-card {
  background: var(--bg-card);
  border: 1px solid rgba(196,135,106,0.12);
  transition: box-shadow var(--dur-fast);
}
.review-card:hover { box-shadow: 0 2px 16px rgba(196,135,106,0.08); }

.review-card__head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1rem 1.4rem;
  border-bottom: 1px solid rgba(196,135,106,0.08);
}
.review-card__left { display: flex; align-items: center; gap: 0.8rem; }

.reviewer-avatar {
  width: 36px; height: 36px; flex-shrink: 0;
  background: linear-gradient(135deg, var(--blush-mid), var(--rose-gold-dim));
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-serif); font-size: 1rem; color: #fff;
}
.reviewer-name { font-size: 0.88rem; color: var(--ink); }
.review-product { color: var(--rose-gold-dim); font-size: 0.58rem; margin-top: 0.15rem; }

.review-card__right { display: flex; flex-direction: column; align-items: flex-end; gap: 0.4rem; }
.stars { display: flex; gap: 1px; }
.star-filled { color: var(--rose-gold); font-size: 0.9rem; }
.star-empty  { color: var(--blush);     font-size: 0.9rem; }

.review-badge { font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.18rem 0.5rem; border: 1px solid; }
.badge--pending  { border-color: rgba(196,135,106,0.3); color: var(--rose-gold-dim); }
.badge--approved { border-color: rgba(102,187,106,0.35); color: #5a9e5e; }

.review-card__body { padding: 1rem 1.4rem; display: flex; flex-direction: column; gap: 0.4rem; }
.review-title { font-family: var(--font-serif); font-size: 1rem; font-weight: 300; color: var(--ink); }
.review-body { font-size: 0.82rem; color: var(--warm-brown); line-height: 1.6; }
.review-date { color: var(--muted); font-size: 0.6rem; }

.review-card__foot {
  display: flex; align-items: center; gap: 1rem;
  padding: 0.9rem 1.4rem;
  background: var(--bg-section);
  border-top: 1px solid rgba(196,135,106,0.08);
}
.review-card__foot--approved { background: rgba(102,187,106,0.04); }
.review-hint { font-size: 0.7rem; color: var(--muted); }
.approved-mark { font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase; color: #5a9e5e; }
.btn-sm { padding: 0.55rem 1.4rem; font-size: 0.62rem; }

/* Empty */
.empty-state { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; padding: 4rem; text-align: center; }
.empty-icon { font-size: 2.5rem; color: var(--rose-gold-dim); }
.empty-state p { font-size: 0.82rem; color: var(--muted); }

/* Pagination */
.pagination { display: flex; align-items: center; justify-content: center; gap: 1rem; }
.page-info { color: var(--muted); }
</style>
