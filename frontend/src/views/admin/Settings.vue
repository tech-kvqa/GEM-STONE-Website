<template>
  <div class="admin-page">

    <div class="page-head">
      <div>
        <p class="label-caps">Configuration</p>
        <h2 class="page-title">Settings</h2>
      </div>
    </div>

    <!-- Admin profile -->
    <div class="settings-section">
      <div class="section-label">
        <p class="label-caps">Admin Profile</p>
        <div class="divider-line"></div>
      </div>
      <div class="settings-card">
        <div class="profile-row">
          <div class="profile-avatar">{{ adminAuth.user?.name?.[0]?.toUpperCase() || 'A' }}</div>
          <div>
            <p class="profile-name">{{ adminAuth.user?.name }}</p>
            <p class="profile-role label-caps">{{ adminAuth.user?.role || 'admin' }}</p>
            <p class="profile-email">{{ adminAuth.user?.email }}</p>
          </div>
        </div>
        <div class="divider-gold"><span>✦</span></div>
        <div class="form-grid">
          <div class="field">
            <label class="input-label">Display Name</label>
            <input v-model="profile.name" class="input-field" />
          </div>
          <div class="field">
            <label class="input-label">Phone</label>
            <input v-model="profile.phone" class="input-field" placeholder="+91 98765 43210" />
          </div>
          <div class="field">
            <label class="input-label">Email (read-only)</label>
            <input :value="adminAuth.user?.email" disabled class="input-field input-field--disabled" />
          </div>
          <div class="field">
            <label class="input-label">Role (read-only)</label>
            <input :value="adminAuth.user?.role" disabled class="input-field input-field--disabled" style="text-transform:capitalize" />
          </div>
        </div>
        <div class="action-row">
          <button class="btn btn-gold btn-sm" @click="saveProfile" :disabled="savingProfile">
            <span>{{ savingProfile ? 'Saving…' : 'Save Profile' }}</span>
          </button>
          <span v-if="profileMsg" :class="['feedback', profileMsg.ok ? 'fb--ok' : 'fb--err']">{{ profileMsg.text }}</span>
        </div>
      </div>
    </div>

    <!-- Change password -->
    <div class="settings-section">
      <div class="section-label">
        <p class="label-caps">Security</p>
        <div class="divider-line"></div>
      </div>
      <div class="settings-card">
        <div class="form-grid">
          <div class="field span-2">
            <label class="input-label">Current Password</label>
            <input v-model="pwd.current" type="password" class="input-field" placeholder="••••••••" />
          </div>
          <div class="field">
            <label class="input-label">New Password</label>
            <input v-model="pwd.new1" type="password" class="input-field" placeholder="Min. 6 characters" />
          </div>
          <div class="field">
            <label class="input-label">Confirm New Password</label>
            <input v-model="pwd.new2" type="password" class="input-field"
              :class="{ 'input-field--error': pwd.new2 && pwd.new1 !== pwd.new2 }" />
          </div>
        </div>
        <p v-if="pwd.new2 && pwd.new1 !== pwd.new2" class="field-error">Passwords do not match</p>
        <div class="action-row">
          <button class="btn btn-ghost btn-sm" @click="changePassword"
            :disabled="savingPwd || !canChangePwd">
            <span>{{ savingPwd ? 'Updating…' : 'Update Password' }}</span>
          </button>
          <span v-if="pwdMsg" :class="['feedback', pwdMsg.ok ? 'fb--ok' : 'fb--err']">{{ pwdMsg.text }}</span>
        </div>
      </div>
    </div>

    <!-- Store information -->
    <div class="settings-section">
      <div class="section-label">
        <p class="label-caps">Store Information</p>
        <div class="divider-line"></div>
      </div>
      <div class="settings-card">
        <div class="form-grid">
          <div class="field">
            <label class="input-label">Store Name</label>
            <input v-model="store.name" class="input-field" />
          </div>
          <div class="field">
            <label class="input-label">Support Email</label>
            <input v-model="store.email" type="email" class="input-field" />
          </div>
          <div class="field">
            <label class="input-label">Support Phone</label>
            <input v-model="store.phone" class="input-field" />
          </div>
          <div class="field">
            <label class="input-label">Free Shipping Above (₹)</label>
            <input v-model.number="store.freeShipping" type="number" class="input-field" />
          </div>
          <div class="field span-2">
            <label class="input-label">Business Address</label>
            <textarea v-model="store.address" rows="2" class="input-field" style="resize:none"></textarea>
          </div>
        </div>
        <p class="info-note">
          ✦ Store settings are saved locally. Wire to your backend settings endpoint to persist across sessions.
        </p>
        <div class="action-row">
          <button class="btn btn-gold btn-sm" @click="saveStore"><span>Save Store Info</span></button>
          <span v-if="storeMsg" class="feedback fb--ok">{{ storeMsg }}</span>
        </div>
      </div>
    </div>

    <!-- Admin accounts (superadmin only) -->
    <div v-if="adminAuth.isSuperAdmin" class="settings-section">
      <div class="section-label">
        <p class="label-caps">Admin Accounts</p>
        <div class="divider-line"></div>
      </div>
      <div class="settings-card">

        <!-- Existing admins -->
        <div class="admin-list">
          <div v-for="a in adminList" :key="a.id" class="admin-row">
            <div class="admin-avatar">{{ a.name?.[0]?.toUpperCase() }}</div>
            <div class="admin-info">
              <p class="admin-name">{{ a.name }}</p>
              <p class="admin-email">{{ a.email }}</p>
            </div>
            <span :class="['role-badge', a.role === 'superadmin' ? 'role--super' : 'role--admin']">
              {{ a.role || 'admin' }}
            </span>
          </div>
          <p v-if="!adminList.length" class="empty-mini label-caps">Loading…</p>
        </div>

        <div class="divider-gold" style="margin:1.5rem 0"><span>✦</span></div>

        <!-- Create admin -->
        <p class="subsection-title label-caps">Create New Admin</p>
        <div class="form-grid" style="margin-top:0.75rem">
          <div class="field">
            <label class="input-label">Full Name</label>
            <input v-model="newAdmin.full_name" class="input-field" />
          </div>
          <div class="field">
            <label class="input-label">Email</label>
            <input v-model="newAdmin.email" type="email" class="input-field" />
          </div>
          <div class="field">
            <label class="input-label">Password</label>
            <input v-model="newAdmin.password" type="password" class="input-field" />
          </div>
          <div class="field">
            <label class="input-label">Role</label>
            <select v-model="newAdmin.role" class="input-field">
              <option value="admin">Admin</option>
              <option value="superadmin">Superadmin</option>
            </select>
          </div>
        </div>
        <div class="action-row">
          <button class="btn btn-outline btn-sm" @click="createAdmin" :disabled="creatingAdmin">
            <span>{{ creatingAdmin ? 'Creating…' : '+ Create Admin' }}</span>
          </button>
          <span v-if="createMsg" :class="['feedback', createMsg.ok ? 'fb--ok' : 'fb--err']">{{ createMsg.text }}</span>
        </div>
      </div>
    </div>

    <!-- API endpoints reference -->
    <div class="settings-section">
      <div class="section-label">
        <p class="label-caps">API Reference</p>
        <div class="divider-line"></div>
      </div>
      <div class="settings-card">
        <div class="api-grid">
          <div v-for="ep in apiEndpoints" :key="ep.path" class="api-row">
            <span :class="['method-badge', `method--${ep.method.toLowerCase()}`]">{{ ep.method }}</span>
            <code class="api-path">{{ ep.path }}</code>
            <span class="api-desc">{{ ep.desc }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Danger zone -->
    <div class="settings-section">
      <div class="section-label">
        <p class="label-caps" style="color:#c07070">Danger Zone</p>
        <div class="divider-line" style="background:rgba(224,112,112,0.2)"></div>
      </div>
      <div class="settings-card settings-card--danger">
        <div class="danger-row">
          <div>
            <p class="danger-title">Sign Out of Admin Panel</p>
            <p class="danger-sub">You will be redirected to the admin login page.</p>
          </div>
          <button class="btn btn-danger btn-sm" @click="logout"><span>Sign Out</span></button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify'
import { useAdminAuthStore } from '@/store/adminAuth'
import { adminAuthApi } from '@/api'

const router    = useRouter()
const adminAuth = useAdminAuthStore()

/* ── Profile ─────────────────────────────────────────────────────────────── */
const profile      = ref({ name: adminAuth.user?.name || '', phone: adminAuth.user?.phone || '' })
const savingProfile = ref(false)
const profileMsg   = ref(null)

async function saveProfile() {
  savingProfile.value = true; profileMsg.value = null
  await new Promise(r => setTimeout(r, 600))   // wire to: adminApi.put('/admin/auth/me', profile.value)
  if (adminAuth.user) adminAuth.user.name = profile.value.name
  profileMsg.value = { ok: true, text: 'Profile saved' }
  savingProfile.value = false
  setTimeout(() => profileMsg.value = null, 3000)
}

/* ── Password ────────────────────────────────────────────────────────────── */
const pwd       = ref({ current: '', new1: '', new2: '' })
const savingPwd = ref(false)
const pwdMsg    = ref(null)
const canChangePwd = computed(() =>
  pwd.value.current && pwd.value.new1 && pwd.value.new1 === pwd.value.new2 && pwd.value.new1.length >= 6
)

async function changePassword() {
  if (!canChangePwd.value) return
  savingPwd.value = true; pwdMsg.value = null
  await new Promise(r => setTimeout(r, 700))   // wire to: adminApi.post('/admin/auth/change-password', {...})
  pwdMsg.value = { ok: true, text: 'Password updated successfully' }
  pwd.value = { current: '', new1: '', new2: '' }
  savingPwd.value = false
  setTimeout(() => pwdMsg.value = null, 3000)
}

/* ── Store settings ──────────────────────────────────────────────────────── */
const store    = ref({ name: 'Glow With Ritz', email: 'hello@glowwithritz.com', phone: '+91 98765 43210', freeShipping: 999, address: '' })
const storeMsg = ref('')

function saveStore() {
  localStorage.setItem('gwr_store_settings', JSON.stringify(store.value))
  storeMsg.value = 'Saved locally ✓'
  setTimeout(() => storeMsg.value = '', 3000)
}

/* ── Admin list & create (superadmin) ────────────────────────────────────── */
const adminList     = ref([])
const newAdmin      = ref({ full_name: '', email: '', password: '', role: 'admin' })
const creatingAdmin = ref(false)
const createMsg     = ref(null)

async function loadAdmins() {
  if (!adminAuth.isSuperAdmin) return
  try { const { data } = await adminAuthApi.list(); adminList.value = data } catch {}
}

async function createAdmin() {
  if (!newAdmin.value.full_name || !newAdmin.value.email || !newAdmin.value.password) {
    createMsg.value = { ok: false, text: 'All fields required' }; return
  }
  creatingAdmin.value = true; createMsg.value = null
  try {
    await adminAuthApi.create(newAdmin.value)
    toast.success(`Admin '${newAdmin.value.full_name}' created`)
    newAdmin.value = { full_name: '', email: '', password: '', role: 'admin' }
    loadAdmins()
  } catch (e) {
    createMsg.value = { ok: false, text: e?.response?.data?.detail || 'Create failed' }
  } finally { creatingAdmin.value = false; setTimeout(() => createMsg.value = null, 4000) }
}

/* ── Logout ──────────────────────────────────────────────────────────────── */
function logout() { adminAuth.logout(); router.push({ name: 'AdminLogin' }) }

/* ── API reference ───────────────────────────────────────────────────────── */
const apiEndpoints = [
  { method: 'POST',  path: '/api/admin/auth/login',          desc: 'Admin login' },
  { method: 'GET',   path: '/api/admin/dashboard',           desc: 'Dashboard KPIs + charts' },
  { method: 'GET',   path: '/api/admin/products',            desc: 'All products (incl. inactive)' },
  { method: 'PATCH', path: '/api/admin/products/:id',        desc: 'Update product fields' },
  { method: 'GET',   path: '/api/admin/orders',              desc: 'All orders with filters' },
  { method: 'PATCH', path: '/api/admin/orders/:id/status',   desc: 'Update order status' },
  { method: 'GET',   path: '/api/admin/users',               desc: 'All consumer accounts' },
  { method: 'GET',   path: '/api/admin/consultations',       desc: 'All consultation bookings' },
  { method: 'GET',   path: '/api/admin/reviews',             desc: 'All reviews' },
  { method: 'GET',   path: '/api/admin/inventory',           desc: 'Stock report' },
]

onMounted(() => {
  const saved = localStorage.getItem('gwr_store_settings')
  if (saved) try { store.value = { ...store.value, ...JSON.parse(saved) } } catch {}
  loadAdmins()
})
</script>

<style scoped>
.admin-page { display: flex; flex-direction: column; gap: 2rem; max-width: 820px; }

.page-head { margin-bottom: 0.25rem; }
.page-title { font-family: var(--font-serif); font-size: 2rem; font-weight: 300; color: var(--ink); margin-top: 0.2rem; }

/* Section layout */
.settings-section { display: flex; flex-direction: column; gap: 0.9rem; }
.section-label { display: flex; align-items: center; gap: 1rem; }
.divider-line { flex: 1; height: 1px; background: rgba(196,135,106,0.18); }

/* Card */
.settings-card {
  background: var(--bg-card);
  border: 1px solid rgba(196,135,106,0.12);
  padding: 2rem;
  display: flex; flex-direction: column; gap: 1.25rem;
}
.settings-card--danger { border-color: rgba(224,112,112,0.2); }

/* Profile row */
.profile-row { display: flex; align-items: center; gap: 1.2rem; }
.profile-avatar {
  width: 56px; height: 56px; flex-shrink: 0;
  background: linear-gradient(135deg, var(--rose-gold-deep), var(--mauve));
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-serif); font-size: 1.5rem; color: #fff;
}
.profile-name  { font-family: var(--font-serif); font-size: 1.1rem; color: var(--ink); }
.profile-role  { color: var(--rose-gold); font-size: 0.58rem; margin-top: 0.15rem; }
.profile-email { font-size: 0.75rem; color: var(--muted); margin-top: 0.1rem; }

/* Form grid */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.field { display: flex; flex-direction: column; gap: 0.4rem; }
.span-2 { grid-column: 1 / -1; }
.input-field { background: var(--bg-main); border: 1px solid rgba(196,135,106,0.2); color: var(--ink); }
.input-field:focus { border-color: var(--rose-gold); }
.input-field--disabled { opacity: 0.45; cursor: not-allowed; }
.input-field--error { border-color: rgba(224,112,112,0.5) !important; }
.field-error { font-size: 0.72rem; color: #c07070; margin-top: -0.5rem; }

/* Action row */
.action-row { display: flex; align-items: center; gap: 1rem; margin-top: 0.25rem; }
.btn-sm { padding: 0.6rem 1.5rem; font-size: 0.62rem; }
.feedback { font-size: 0.72rem; }
.fb--ok  { color: #5a9e5e; }
.fb--err { color: #c07070; }

/* Info note */
.info-note { font-size: 0.72rem; color: var(--muted); background: rgba(196,135,106,0.05); padding: 0.75rem 1rem; border-left: 2px solid rgba(196,135,106,0.3); }

/* Admin accounts */
.admin-list { display: flex; flex-direction: column; gap: 0; }
.admin-row { display: flex; align-items: center; gap: 0.9rem; padding: 0.8rem 0; border-bottom: 1px solid rgba(196,135,106,0.08); }
.admin-row:last-child { border-bottom: 0; }
.admin-avatar { width: 32px; height: 32px; background: linear-gradient(135deg, var(--blush-mid), var(--rose-gold-dim)); display: flex; align-items: center; justify-content: center; font-family: var(--font-serif); font-size: 0.9rem; color: #fff; flex-shrink: 0; }
.admin-info { flex: 1; min-width: 0; }
.admin-name  { font-size: 0.85rem; color: var(--ink); }
.admin-email { font-size: 0.68rem; color: var(--muted); }
.role-badge { font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.18rem 0.5rem; border: 1px solid; }
.role--super { border-color: rgba(196,135,106,0.4); color: var(--rose-gold); }
.role--admin { border-color: rgba(196,135,106,0.2); color: var(--muted); }
.subsection-title { letter-spacing: 0.15em; color: var(--rose-gold-dim); }
.empty-mini { color: var(--muted); }

/* API grid */
.api-grid { display: flex; flex-direction: column; gap: 0.4rem; }
.api-row { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0; border-bottom: 1px solid rgba(196,135,106,0.06); }
.api-row:last-child { border-bottom: 0; }
.method-badge { font-size: 0.58rem; font-weight: 600; letter-spacing: 0.08em; padding: 0.15rem 0.45rem; width: 52px; text-align: center; flex-shrink: 0; }
.method--get   { background: rgba(100,181,246,0.12); color: #4a80ba; }
.method--post  { background: rgba(102,187,106,0.12); color: #5a9e5e; }
.method--patch { background: rgba(196,135,106,0.12); color: var(--rose-gold); }
.method--delete { background: rgba(224,112,112,0.1); color: #c07070; }
.api-path { font-size: 0.72rem; color: var(--ink); font-family: monospace; flex: 1; }
.api-desc { font-size: 0.7rem; color: var(--muted); white-space: nowrap; }

/* Danger */
.danger-row { display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; }
.danger-title { font-family: var(--font-serif); font-size: 0.95rem; color: var(--ink); }
.danger-sub   { font-size: 0.72rem; color: var(--muted); margin-top: 0.2rem; }
.btn-danger { background: rgba(224,112,112,0.9); color: #fff; padding: 0.6rem 1.4rem; font-size: 0.62rem; letter-spacing: 0.15em; text-transform: uppercase; transition: background 0.2s; }
.btn-danger:hover { background: #c07070; }

@media (max-width: 640px) {
  .form-grid { grid-template-columns: 1fr; }
  .span-2 { grid-column: 1; }
  .api-desc { display: none; }
}
</style>
