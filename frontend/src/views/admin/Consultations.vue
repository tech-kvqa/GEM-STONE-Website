<template>
  <div class="admin-page">
    <div class="page-head">
      <div><p class="label-caps">Booking Management</p><h2 class="page-title">Consultations</h2></div>
      <span class="result-badge">{{ total }} bookings</span>
    </div>

    <!-- Status tabs -->
    <div class="status-tabs">
      <button v-for="tab in tabs" :key="tab.value"
        :class="['status-tab', { 'status-tab--active': filterStatus === tab.value }]"
        @click="filterStatus = tab.value; page = 1; load()">{{ tab.label }}</button>
    </div>

    <div class="filter-bar">
      <input v-model="search" @input="debounceLoad" placeholder="Search by name, email, subject…" class="input-field filter-search" />
    </div>

    <div v-if="loading" class="table-wrap">
      <div v-for="i in 6" :key="i" class="skeleton" style="height:68px;margin-bottom:1px"></div>
    </div>

    <div v-else class="consult-list">
      <div v-for="c in consultations" :key="c.id" class="consult-card">
        <div class="consult-card__head">
          <div class="consult-card__left">
            <div class="user-avatar">{{ c.name?.[0]?.toUpperCase() }}</div>
            <div>
              <p class="consult-name">{{ c.name }}</p>
              <p class="consult-meta">{{ c.email }} · {{ c.phone }}</p>
            </div>
          </div>
          <span :class="['consult-status', `cs--${c.status}`]">{{ c.status }}</span>
        </div>
        <div class="consult-card__body">
          <p class="consult-subject">{{ c.subject }}</p>
          <p v-if="c.message" class="consult-msg">{{ c.message }}</p>
          <div class="consult-meta-row">
            <span class="label-caps">{{ c.preferred_date || 'No date' }}</span>
            <span class="label-caps">{{ c.preferred_time || 'No time' }}</span>
            <span class="label-caps">{{ fmtDate(c.created_at) }}</span>
          </div>
          <div v-if="c.admin_notes" class="admin-note">
            <span class="label-caps">Admin note:</span> {{ c.admin_notes }}
          </div>
        </div>
        <div class="consult-card__foot">
          <div class="update-row">
            <select v-model="c._newStatus" class="input-field select-sm">
              <option v-for="s in statusOptions" :key="s" :value="s">{{ s }}</option>
            </select>
            <textarea v-model="c._notes" placeholder="Add admin notes…" class="input-field notes-input" rows="1"></textarea>
            <button class="btn btn-gold btn-sm" @click="updateConsult(c)"><span>Update</span></button>
          </div>
        </div>
      </div>
      <div v-if="!consultations.length" class="empty-state">
        <span class="empty-icon">✦</span>
        <p>No consultations found</p>
      </div>
    </div>

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
import { adminConsultationApi } from '@/api'

const consultations = ref([])
const total   = ref(0)
const loading = ref(false)
const page    = ref(1)
const limit   = 15
const search  = ref('')
const filterStatus = ref('')
let   timer   = null

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / limit)))
const statusOptions = ['pending','confirmed','completed','cancelled']
const tabs = [
  { label: 'All', value: '' }, { label: 'Pending', value: 'pending' },
  { label: 'Confirmed', value: 'confirmed' }, { label: 'Completed', value: 'completed' },
  { label: 'Cancelled', value: 'cancelled' },
]

async function load() {
  loading.value = true
  try {
    const params = { page: page.value, limit }
    if (filterStatus.value) params.status = filterStatus.value
    if (search.value)       params.search = search.value
    const { data } = await adminConsultationApi.list(params)
    consultations.value = (data.consultations || []).map(c => ({
      ...c, _newStatus: c.status, _notes: c.admin_notes || ''
    }))
    total.value = data.total || 0
  } catch { toast.error('Failed to load consultations') } finally { loading.value = false }
}

function debounceLoad() { clearTimeout(timer); timer = setTimeout(() => { page.value = 1; load() }, 400) }
onMounted(load)

async function updateConsult(c) {
  try {
    await adminConsultationApi.update(c.id, { status: c._newStatus, admin_notes: c._notes || undefined })
    toast.success('Consultation updated'); load()
  } catch { toast.error('Update failed') }
}

function fmtDate(d) { return d ? new Date(d).toLocaleDateString('en-IN', { day:'2-digit', month:'short', year:'numeric' }) : '—' }
</script>

<style scoped>
.admin-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-head { display: flex; align-items: flex-end; justify-content: space-between; }
.page-title { font-family: var(--font-serif); font-size: 2rem; font-weight: 300; color: var(--ink); margin-top: 0.2rem; }
.result-badge { font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }
.status-tabs { display: flex; gap: 0; border-bottom: 1px solid rgba(196,135,106,0.15); overflow-x: auto; }
.status-tab { padding: 0.7rem 1.1rem; font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); border-bottom: 2px solid transparent; white-space: nowrap; transition: all var(--dur-fast); }
.status-tab:hover { color: var(--rose-gold); }
.status-tab--active { color: var(--rose-gold); border-bottom-color: var(--rose-gold); }
.filter-bar { display: flex; }
.filter-search { flex: 1; max-width: 440px; }
.input-field { background: var(--bg-card); border: 1px solid rgba(196,135,106,0.2); color: var(--ink); }
.input-field:focus { border-color: var(--rose-gold); }

.consult-list { display: flex; flex-direction: column; gap: 1px; }
.consult-card { background: var(--bg-card); border: 1px solid rgba(196,135,106,0.12); }
.consult-card__head { display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.4rem; border-bottom: 1px solid rgba(196,135,106,0.08); }
.consult-card__left { display: flex; align-items: center; gap: 0.8rem; }
.user-avatar { width: 36px; height: 36px; background: linear-gradient(135deg, var(--blush-mid), var(--rose-gold-dim)); display: flex; align-items: center; justify-content: center; font-family: var(--font-serif); font-size: 1rem; color: #fff; flex-shrink: 0; }
.consult-name { font-size: 0.88rem; color: var(--ink); }
.consult-meta { font-size: 0.68rem; color: var(--muted); margin-top: 0.1rem; }
.consult-status { font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.2rem 0.55rem; border: 1px solid; }
.cs--pending    { border-color: rgba(196,135,106,0.3); color: var(--rose-gold-dim); }
.cs--confirmed  { border-color: rgba(100,181,246,0.35); color: #5a8fc0; }
.cs--completed  { border-color: rgba(102,187,106,0.35); color: #5a9e5e; }
.cs--cancelled  { border-color: rgba(224,112,112,0.3); color: #c07070; }
.consult-card__body { padding: 1rem 1.4rem; display: flex; flex-direction: column; gap: 0.5rem; }
.consult-subject { font-family: var(--font-serif); font-size: 0.95rem; color: var(--ink); }
.consult-msg { font-size: 0.78rem; color: var(--warm-brown); line-height: 1.5; }
.consult-meta-row { display: flex; gap: 1.5rem; }
.consult-meta-row .label-caps { color: var(--muted); font-size: 0.6rem; }
.admin-note { font-size: 0.75rem; color: var(--rose-gold-dim); background: rgba(196,135,106,0.06); padding: 0.5rem 0.75rem; border-left: 2px solid var(--rose-gold-dim); }
.admin-note .label-caps { font-size: 0.6rem; }
.consult-card__foot { padding: 0.9rem 1.4rem; background: var(--bg-section); border-top: 1px solid rgba(196,135,106,0.08); }
.update-row { display: flex; gap: 0.6rem; align-items: flex-start; }
.select-sm { width: 130px; padding: 0.5rem 0.75rem; font-size: 0.78rem; }
.notes-input { flex: 1; padding: 0.5rem 0.75rem; font-size: 0.78rem; resize: none; }
.btn-sm { padding: 0.55rem 1.2rem; font-size: 0.62rem; }
.empty-state { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; padding: 4rem; text-align: center; }
.empty-icon { font-size: 2.5rem; color: var(--rose-gold-dim); }
.empty-state p { font-size: 0.82rem; color: var(--muted); }
.pagination { display: flex; align-items: center; justify-content: center; gap: 1rem; }
.page-info { color: var(--muted); }
</style>
