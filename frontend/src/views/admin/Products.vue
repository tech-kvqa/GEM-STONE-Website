<template>
  <div class="admin-page">

    <!-- Header -->
    <div class="page-head">
      <div>
        <p class="label-caps">Catalogue</p>
        <h2 class="page-title">Products</h2>
      </div>
      <span class="result-badge">{{ total }} products</span>
    </div>

    <!-- Filter bar -->
    <div class="filter-bar">
      <input v-model="search" @input="debounceLoad" placeholder="Search by name or SKU…" class="input-field filter-search" />
      <select v-model="filterLowStock" @change="load" class="input-field filter-select">
        <option value="">All stock</option>
        <option value="true">Low stock only (≤10)</option>
      </select>
      <select v-model="filterActive" @change="load" class="input-field filter-select">
        <option value="">All status</option>
        <option value="1">Active only</option>
        <option value="0">Inactive only</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="table-wrap">
      <div v-for="i in 6" :key="i" class="skeleton" style="height:56px;margin-bottom:1px"></div>
    </div>

    <!-- Table -->
    <div v-else class="table-wrap">
      <table class="admin-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th class="col-num">Price</th>
            <th class="col-num">Stock</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id">
            <td>
              <div class="prod-cell">
                <!-- <img :src="p.images?.[0] || 'https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=60'" 
                 :alt="p.name" class="prod-thumb" />-->
                <img
                  :src="p.images?.[0]
                    ? getImageUrl(p.images[0])
                    : 'https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=60'"
                  :alt="p.name"
                  class="prod-thumb"
                />
                <div>
                  <p class="prod-name">{{ p.name }}</p>
                  <p class="prod-sku label-caps">{{ p.sku || '—' }}</p>
                </div>
              </div>
            </td>
            <td><span class="tag-pill">{{ p.category || '—' }}</span></td>
            <td class="col-num">
              <span class="price-main">₹{{ fmt(p.price) }}</span>
              <span v-if="p.compare_price" class="price-compare">₹{{ fmt(p.compare_price) }}</span>
            </td>
            <td class="col-num">
              <span :class="['stock-badge', stockClass(p.stock_qty)]">{{ p.stock_qty ?? '—' }}</span>
            </td>
            <td>
              <span :class="['status-pill', p.is_active ? 'pill--active' : 'pill--inactive']">
                {{ p.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td>
              <div class="action-row">
                <button class="action-btn" @click="openEdit(p)" title="Edit">✎</button>
                <button class="action-btn action-btn--danger" @click="confirmDeactivate(p)"
                  v-if="p.is_active" title="Deactivate">✕</button>
              </div>
            </td>
          </tr>
          <tr v-if="!products.length">
            <td colspan="6" class="empty-row">
              <span class="empty-icon">◇</span>
              <p>No products found</p>
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

    <!-- Edit drawer -->
    <div v-if="editProduct" class="drawer-overlay" @click.self="closeEdit">
      <aside class="drawer">
        <div class="drawer__head">
          <h3 class="drawer__title">Edit Product</h3>
          <button @click="closeEdit" class="drawer__close">✕</button>
        </div>
        <div class="drawer__body">
          <div class="field">
            <label class="input-label">Name</label>
            <input v-model="editForm.name" class="input-field" />
          </div>
          <div class="field-row">
            <div class="field">
              <label class="input-label">Price (₹)</label>
              <input v-model.number="editForm.price" type="number" class="input-field" />
            </div>
            <div class="field">
              <label class="input-label">Compare Price (₹)</label>
              <input v-model.number="editForm.compare_price" type="number" class="input-field" />
            </div>
          </div>
          <div class="field-row">
            <div class="field">
              <label class="input-label">Stock Qty</label>
              <input v-model.number="editForm.stock_qty" type="number" class="input-field" />
            </div>
            <div class="field">
              <label class="input-label">Status</label>
              <select v-model="editForm.is_active" class="input-field">
                <option :value="true">Active</option>
                <option :value="false">Inactive</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label class="input-label">Featured</label>
            <select v-model="editForm.is_featured" class="input-field">
              <option :value="true">Yes — show on homepage</option>
              <option :value="false">No</option>
            </select>
          </div>

          <!-- Image upload -->
          <div class="field" style="margin-top:0.5rem">
            <label class="input-label">Upload New Image</label>
            <input type="file" accept="image/*" @change="onFileChange" class="input-field" style="padding:0.5rem" />
          </div>
          <div v-if="editProduct.images?.length" class="img-preview-row">
            <!-- <img v-for="(img, i) in editProduct.images" :key="i" :src="img" class="img-thumb" /> -->
            <img
              v-for="(img, i) in editProduct.images"
              :key="i"
              :src="getImageUrl(img)"
              class="img-thumb"
            />
          </div>

          <div v-if="editMsg" :class="['edit-msg', editMsg.ok ? 'msg--ok' : 'msg--err']">{{ editMsg.text }}</div>
        </div>
        <div class="drawer__foot">
          <button class="btn btn-ghost btn-sm" @click="closeEdit">Cancel</button>
          <button class="btn btn-gold btn-sm" @click="saveEdit" :disabled="saving">
            <span>{{ saving ? 'Saving…' : 'Save Changes' }}</span>
          </button>
        </div>
      </aside>
    </div>

  </div>
</template>

<script setup>
import { getImageUrl } from '@/utils/image'
import { ref, computed, onMounted } from 'vue'
import { toast } from 'vue3-toastify'
import { adminProductApi } from '@/api'

const products     = ref([])
const total        = ref(0)
const loading      = ref(false)
const page         = ref(1)
const limit        = 20
const search       = ref('')
const filterLowStock = ref('')
const filterActive = ref('')
let   debounceTimer = null

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / limit)))

async function load() {
  loading.value = true
  try {
    const params = { page: page.value, limit, search: search.value || undefined }
    if (filterLowStock.value) params.low_stock = true
    if (filterActive.value !== '') params.is_active = Number(filterActive.value)
    const { data } = await adminProductApi.list(params)
    products.value = data.products || []
    total.value    = data.total    || 0
  } catch { toast.error('Failed to load products') } finally { loading.value = false }
}

function debounceLoad() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { page.value = 1; load() }, 400)
}

onMounted(load)

// Edit
const editProduct = ref(null)
const editForm    = ref({})
const editFile    = ref(null)
const saving      = ref(false)
const editMsg     = ref(null)

function openEdit(p) {
  editProduct.value = p
  editForm.value = { name: p.name, price: p.price, compare_price: p.compare_price,
                     stock_qty: p.stock_qty, is_active: p.is_active, is_featured: p.is_featured }
  editMsg.value = null; editFile.value = null
}
function closeEdit() { editProduct.value = null }

function onFileChange(e) { editFile.value = e.target.files[0] || null }

async function saveEdit() {
  saving.value = true; editMsg.value = null
  try {
    await adminProductApi.update(editProduct.value.id, editForm.value)
    if (editFile.value) {
      const fd = new FormData()
      fd.append('file', editFile.value)
      await adminProductApi.upload(editProduct.value.id, fd)
    }
    toast.success('Product updated')
    closeEdit(); load()
  } catch (e) {
    editMsg.value = { ok: false, text: e?.response?.data?.detail || 'Update failed' }
  } finally { saving.value = false }
}

async function confirmDeactivate(p) {
  if (!confirm(`Deactivate "${p.name}"? It will be hidden from the store.`)) return
  try {
    await adminProductApi.deactivate(p.id)
    toast.success('Product deactivated'); load()
  } catch { toast.error('Failed to deactivate') }
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
.result-badge { font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }

/* Filter bar */
.filter-bar { display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap; }
.filter-search { flex: 1; min-width: 200px; }
.filter-select { width: 180px; }
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

/* Product cell */
.prod-cell { display: flex; align-items: center; gap: 0.75rem; }
.prod-thumb { width: 44px; height: 44px; object-fit: cover; flex-shrink: 0; }
.prod-name { font-size: 0.85rem; color: var(--ink); font-weight: 300; }
.prod-sku { color: var(--muted); font-size: 0.58rem; margin-top: 0.1rem; }

/* Pills & badges */
.tag-pill { font-size: 0.65rem; padding: 0.2rem 0.6rem; background: rgba(196,135,106,0.08); color: var(--rose-gold-dim); }
.price-main { font-family: var(--font-serif); font-size: 0.9rem; color: var(--ink); }
.price-compare { font-size: 0.72rem; color: var(--light-muted); text-decoration: line-through; margin-left: 0.4rem; }
.stock-badge { font-size: 0.72rem; padding: 0.18rem 0.5rem; font-weight: 500; }
.stock--ok  { background: rgba(102,187,106,0.1); color: #5a9e5e; }
.stock--low { background: rgba(196,135,106,0.12); color: var(--rose-gold); }
.stock--out { background: rgba(224,112,112,0.1); color: #c07070; }
.status-pill { font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.2rem 0.55rem; border: 1px solid; }
.pill--active   { border-color: rgba(102,187,106,0.35); color: #5a9e5e; }
.pill--inactive { border-color: rgba(196,135,106,0.25); color: var(--muted); }

/* Actions */
.action-row { display: flex; gap: 0.5rem; }
.action-btn {
  width: 30px; height: 30px; border: 1px solid rgba(196,135,106,0.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; color: var(--muted); transition: all 0.2s;
}
.action-btn:hover { border-color: var(--rose-gold); color: var(--rose-gold); background: rgba(196,135,106,0.06); }
.action-btn--danger:hover { border-color: #c07070; color: #c07070; background: rgba(224,112,112,0.06); }

/* Empty row */
.empty-row { text-align: center; padding: 3rem !important; }
.empty-icon { font-size: 2rem; color: var(--blush-mid); display: block; margin-bottom: 0.5rem; }
.empty-row p { font-size: 0.82rem; color: var(--muted); }

/* Pagination */
.pagination { display: flex; align-items: center; justify-content: center; gap: 1rem; }
.page-info { color: var(--muted); }
.btn-sm { padding: 0.55rem 1.2rem; font-size: 0.62rem; }

/* Drawer */
.drawer-overlay {
  position: fixed; inset: 0; z-index: 100;
  background: rgba(42,31,26,0.5);
  backdrop-filter: blur(4px);
  display: flex; justify-content: flex-end;
}
.drawer {
  width: 420px; height: 100%;
  background: var(--bg-card);
  border-left: 1px solid rgba(196,135,106,0.2);
  display: flex; flex-direction: column;
  animation: fadeIn 0.25s var(--ease-silk);
}
.drawer__head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(196,135,106,0.12);
}
.drawer__title { font-family: var(--font-serif); font-size: 1.2rem; font-weight: 300; color: var(--ink); }
.drawer__close { font-size: 0.8rem; color: var(--muted); transition: color 0.2s; }
.drawer__close:hover { color: var(--rose-gold); }
.drawer__body { flex: 1; overflow-y: auto; padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.drawer__foot { padding: 1.2rem 1.5rem; border-top: 1px solid rgba(196,135,106,0.12); display: flex; gap: 0.75rem; justify-content: flex-end; }
.field { display: flex; flex-direction: column; gap: 0.4rem; }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.img-preview-row { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.img-thumb { width: 60px; height: 60px; object-fit: cover; border: 1px solid rgba(196,135,106,0.2); }
.edit-msg { font-size: 0.75rem; padding: 0.6rem 0.9rem; }
.msg--ok  { background: rgba(102,187,106,0.08); color: #5a9e5e; border: 1px solid rgba(102,187,106,0.2); }
.msg--err { background: rgba(224,112,112,0.08); color: #c07070; border: 1px solid rgba(224,112,112,0.2); }
</style>
