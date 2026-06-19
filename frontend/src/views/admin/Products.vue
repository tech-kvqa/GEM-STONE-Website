<template>
  <div class="admin-page">

    <!-- Header -->
    <div class="page-head">
      <div>
        <p class="label-caps">Catalogue</p>
        <h2 class="page-title">Products</h2>
      </div>
      <!-- <span class="result-badge">{{ total }} products</span> -->
      <div class="header-actions">
        <span class="result-badge">{{ total }} products</span>
        <button class="btn-create-new" @click="openCreate" title="Create new product">
          <span class="create-icon">+</span>
          <span class="create-text">New Product</span>
        </button>
      </div>
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
                  {{ JSON.stringify(p.images[0]) }}
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
                <button class="action-btn action-btn--warning" @click="confirmReactivate(p)"
                  v-else title="Reactivate">✓</button>
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
    <!-- <div class="pagination"> -->
    <div v-if="totalPages > 1" class="pagination">
      <button :disabled="page <= 1" class="btn btn-ghost btn-sm" @click="page--; load()">← Prev</button>
      <span class="page-info label-caps">Page {{ page }} of {{ totalPages }}</span>
      <button :disabled="page >= totalPages" class="btn btn-ghost btn-sm" @click="page++; load()">Next →</button>
    </div>

    <!-- CREATE PRODUCT MODAL - IMPROVED READABILITY -->
    <div v-if="showCreateDrawer" class="modal-overlay" @click.self="closeCreate">
      <div class="modal-container">
        <!-- Header -->
        <div class="modal-header">
          <div class="modal-header-content">
            <h2 class="modal-title">Create New Product</h2>
            <p class="modal-subtitle">Add a new product to your catalogue</p>
          </div>
          <button @click="closeCreate" class="modal-close-btn">✕</button>
        </div>

        <!-- Body -->
        <div class="modal-body">

          <!-- SECTION 1: BASIC INFORMATION -->
          <div class="form-section">
            <div class="section-header">
              <h3 class="section-title">📋 Basic Information</h3>
              <p class="section-subtitle">Required fields marked with <span class="required">*</span></p>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Product Name <span class="required">*</span></label>
                <input 
                  v-model="createForm.name" 
                  class="form-input" 
                  placeholder="e.g., Rose Quartz Cluster"
                  @input="generateSlug"
                />
                <p class="form-help">Give your product a clear, descriptive name</p>
              </div>

              <div class="form-group">
                <label class="form-label">Slug <span class="required">*</span></label>
                <input 
                  v-model="createForm.slug" 
                  class="form-input" 
                  placeholder="rose-quartz-cluster"
                />
                <p class="form-help">URL-friendly identifier (lowercase, hyphens)</p>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">SKU</label>
                <input 
                  v-model="createForm.sku" 
                  class="form-input" 
                  placeholder="e.g., RQ-001"
                />
                <p class="form-help">Stock Keeping Unit (optional)</p>
              </div>

              <div class="form-group">
                <label class="form-label">Category <span class="required">*</span></label>
                <select v-model.number="createForm.category_id" class="form-input form-select">
                  <option :value="null" disabled>— Select category —</option>
                  <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                </select>
              </div>
            </div>
          </div>

          <!-- SECTION 2: PRICING & INVENTORY -->
          <div class="form-section">
            <div class="section-header">
              <h3 class="section-title">💰 Pricing & Inventory</h3>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Selling Price (₹) <span class="required">*</span></label>
                <input 
                  v-model.number="createForm.price" 
                  type="number" 
                  class="form-input" 
                  placeholder="0.00"
                  min="0" 
                  step="0.01" 
                />
                <p class="form-help">Customer selling price</p>
              </div>

              <div class="form-group">
                <label class="form-label">Compare Price (₹)</label>
                <input 
                  v-model.number="createForm.compare_price" 
                  type="number" 
                  class="form-input" 
                  placeholder="0.00"
                  min="0" 
                  step="0.01" 
                />
                <p class="form-help">Original/MRP price (for discount)</p>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Stock Quantity</label>
                <input 
                  v-model.number="createForm.stock_qty" 
                  type="number" 
                  class="form-input" 
                  placeholder="0"
                  min="0" 
                />
                <p class="form-help">Available units in inventory</p>
              </div>
            </div>
          </div>

          <!-- SECTION 3: DESCRIPTION -->
          <div class="form-section">
            <div class="section-header">
              <h3 class="section-title">📝 Description</h3>
            </div>

            <div class="form-group">
              <label class="form-label">Product Description</label>
              <textarea 
                v-model="createForm.description" 
                class="form-textarea" 
                placeholder="Enter product description..."
                rows="3"
              ></textarea>
              <p class="form-help">Describe what makes this product special</p>
            </div>

            <div class="form-group">
              <label class="form-label">Healing Properties</label>
              <textarea 
                v-model="createForm.healing_props" 
                class="form-textarea" 
                placeholder="List healing properties..."
                rows="3"
              ></textarea>
              <p class="form-help">Metaphysical properties and benefits</p>
            </div>
          </div>

          <!-- SECTION 4: CRYSTAL DETAILS -->
          <div class="form-section">
            <div class="section-header">
              <h3 class="section-title">✨ Crystal Information</h3>
              <p class="section-subtitle">Optional</p>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Chakra</label>
                <input 
                  v-model="createForm.chakra" 
                  class="form-input" 
                  placeholder="e.g., Heart Chakra"
                />
              </div>

              <div class="form-group">
                <label class="form-label">Zodiac Sign</label>
                <input 
                  v-model="createForm.zodiac" 
                  class="form-input" 
                  placeholder="e.g., Pisces"
                />
              </div>
            </div>
          </div>

          <!-- SECTION 5: STATUS -->
          <div class="form-section">
            <div class="section-header">
              <h3 class="section-title">👁️ Status & Visibility</h3>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Product Status</label>
                <select v-model="createForm.is_active" class="form-input form-select">
                  <option :value="true">✓ Active (Visible)</option>
                  <option :value="false">✕ Inactive (Hidden)</option>
                </select>
                <p class="form-help">Control product visibility</p>
              </div>

              <div class="form-group">
                <label class="form-label">Featured on Homepage</label>
                <select v-model="createForm.is_featured" class="form-input form-select">
                  <option :value="false">No</option>
                  <option :value="true">Yes — Show on homepage</option>
                </select>
                <p class="form-help">Highlight this product</p>
              </div>
            </div>
          </div>

          <!-- Error/Success Message -->
          <div v-if="createMsg" :class="['alert-box', createMsg.ok ? 'alert-success' : 'alert-error']">
            <span class="alert-icon">{{ createMsg.ok ? '✓' : '⚠' }}</span>
            <span class="alert-text">{{ createMsg.text }}</span>
          </div>

        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeCreate">Cancel</button>
          <button class="btn-create-product" @click="saveCreate" :disabled="savingCreate">
            <span v-if="!savingCreate">Create Product</span>
            <span v-else>Creating...</span>
          </button>
        </div>
      </div>
    </div>

    <!-- EDIT PRODUCT DRAWER (Keep existing) -->
    <!-- <div v-if="editProduct" class="drawer-overlay" @click.self="closeEdit">
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
          </div> -->

          <!-- Image upload -->
          <!-- <div class="field" style="margin-top:0.5rem">
            <label class="input-label">Upload New Image</label>
            <input type="file" accept="image/*" @change="onFileChange" class="input-field" style="padding:0.5rem" />
          </div>
          <div v-if="editProduct.images?.length" class="img-preview-row"> -->
            <!-- <img v-for="(img, i) in editProduct.images" :key="i" :src="img" class="img-thumb" /> -->
            <!-- <img
              v-for="(img, i) in editProduct.images"
              :key="i"
              :src="getImageUrl(img)"
              class="img-thumb"
            />
          </div> -->

          <div v-if="editProduct" class="drawer-overlay" @click.self="closeEdit">
      <aside class="drawer drawer--wide">
        <div class="drawer__head">
          <h3 class="drawer__title">Edit Product</h3>
          <button @click="closeEdit" class="drawer__close">✕</button>
        </div>
        <div class="drawer__body">
          <div class="edit-main">
            <div class="section-label">
              <p class="label-caps">Product Details</p>
              <div class="divider-line"></div>
            </div>

            <div class="field">
              <label class="input-label">Name</label>
              <input v-model="editForm.name" class="input-field" />
            </div>
            <div class="field">
              <label class="input-label">Slug</label>
              <input v-model="editForm.slug" class="input-field" />
            </div>
            <div class="field">
              <label class="input-label">SKU</label>
              <input v-model="editForm.sku" class="input-field" />
            </div>
            <div class="field">
              <label class="input-label">Category</label>
              <select v-model.number="editForm.category_id" class="input-field">
                <option :value="null">— Select Category —</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
              </select>
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
                <option :value="false">No</option>
                <option :value="true">Yes</option>
              </select>
            </div>

            <div class="field">
              <label class="input-label">Description</label>
              <textarea v-model="editForm.description" class="input-field" rows="3" style="resize:none"></textarea>
            </div>
            <div class="field">
              <label class="input-label">Healing Properties</label>
              <textarea v-model="editForm.healing_props" class="input-field" rows="2" style="resize:none"></textarea>
            </div>
            <div class="field-row">
              <div class="field">
                <label class="input-label">Chakra</label>
                <input v-model="editForm.chakra" class="input-field" />
              </div>
              <div class="field">
                <label class="input-label">Zodiac</label>
                <input v-model="editForm.zodiac" class="input-field" />
              </div>
            </div>
          </div>

          <div class="edit-images">
            <div class="section-label">
              <p class="input-label">Product Images <span class="img-count-badge">{{ editProduct.images?.length || 0 }}</span></p>
              <div class="divider-line"></div>
            </div>

            <div v-if="editProduct.images?.length" class="img-gallery-grid">
              <div v-for="(img, i) in editProduct.images" :key="i" :class="['img-tile', img.is_primary && 'img-tile--primary']">
                <div class="img-tile__photo">
                  <!-- <img :src="img.url" :alt="`Product image ${i+1}`" /> -->
                  <img
                    :src="getImageUrl(img.url)"
                    :alt="`Product image ${i+1}`"
                  />
                  <div v-if="img.is_primary" class="img-tile__badge">Primary</div>
                </div>
                <div class="img-tile__actions">
                  <button v-if="!img.is_primary" class="img-btn img-btn--star" @click="setPrimaryImage(img.id)" title="Set as primary">★</button>
                  <button v-else class="img-btn img-btn--star" style="opacity:0.5" disabled>★</button>
                  <button class="img-btn img-btn--del" @click="deleteImage(img.id)" title="Delete image">✕</button>
                </div>
              </div>
            </div>
            <div v-else class="no-images-hint">No images yet. Upload one to get started.</div>

            <div class="upload-zone" :class="{ 'upload-zone--active': dragOver }" @dragover.prevent="dragOver = true"
              @dragleave="dragOver = false" @drop.prevent="onDrop">
              <input type="file" accept="image/*" @change="onFileChange" class="upload-file-input" />
              <div class="upload-zone__inner">
                <span class="upload-icon">📸</span>
                <span>Drop image here or click to upload</span>
                <span class="upload-ready" v-if="dragOver">Ready to upload!</span>
              </div>
            </div>
            <p v-if="uploadMsg" :class="['upload-feedback', uploadMsg.ok ? 'msg--ok' : 'msg--err']">{{ uploadMsg.text }}</p>
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
import { adminProductApi, categoryApi} from '@/api'

const products     = ref([])
const categories   = ref([])
const total        = ref(0)
const loading      = ref(false)
const page         = ref(1)
const limit        = 20
const search       = ref('')
const filterLowStock = ref('')
const filterActive = ref('')
let   debounceTimer = null

const showCreateDrawer = ref(false)
const editProduct = ref(null)
const dragOver = ref(false)

const createForm = ref({
  name: '',
  slug: '',
  sku: '',
  category_id: null,
  price: null,
  compare_price: null,
  stock_qty: 0,
  description: '',
  healing_props: '',
  chakra: '',
  zodiac: '',
  is_active: true,
  is_featured: false
})

const editForm = ref({})
const saving = ref(false)
const savingCreate = ref(false)
const editMsg = ref(null)
const createMsg = ref(null)
const uploadMsg = ref(null)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / limit)))

onMounted(async () => {
  await loadCategories()
  await load()
})

async function loadCategories() {
  try {
    const { data } = await categoryApi.list()
    categories.value = data || []
  } catch {
    // Categories optional, continue
  }
}

async function load() {
  loading.value = true
  try {
    const params = { page: page.value, limit, search: search.value || undefined }
    if (filterLowStock.value) params.low_stock = true
    if (filterActive.value !== '') params.is_active = Number(filterActive.value)
    const { data } = await adminProductApi.list(params)
    products.value = data.products || []
    total.value    = data.total    || 0
  // } catch { toast.error('Failed to load products') } finally { loading.value = false }
  } catch (e) {
    toast.error('Failed to load products')
  } finally {
    loading.value = false
  }
}

// function debounceLoad() {
//   clearTimeout(debounceTimer)
//   // debounceTimer = setTimeout(() => { page.value = 1; load() }, 400)
//   page.value = 1
//   debounceTimer = setTimeout(() => load(), 300)
// }

// onMounted(load)

// // Edit
// const editProduct = ref(null)
// const editForm    = ref({})
// const editFile    = ref(null)
// const saving      = ref(false)
// const editMsg     = ref(null)

// function openEdit(p) {
//   editProduct.value = p
//   editForm.value = { name: p.name, price: p.price, compare_price: p.compare_price,
//                      stock_qty: p.stock_qty, is_active: p.is_active, is_featured: p.is_featured }
//   editMsg.value = null; editFile.value = null
// }
// function closeEdit() { editProduct.value = null }

// function onFileChange(e) { editFile.value = e.target.files[0] || null }

// async function saveEdit() {
//   saving.value = true; editMsg.value = null
//   try {
//     await adminProductApi.update(editProduct.value.id, editForm.value)
//     if (editFile.value) {
//       const fd = new FormData()
//       fd.append('file', editFile.value)
//       await adminProductApi.upload(editProduct.value.id, fd)
//     }
//     toast.success('Product updated')
//     closeEdit(); load()
//   } catch (e) {
//     editMsg.value = { ok: false, text: e?.response?.data?.detail || 'Update failed' }
//   } finally { saving.value = false }
// }

// async function confirmDeactivate(p) {
//   if (!confirm(`Deactivate "${p.name}"? It will be hidden from the store.`)) return
//   try {
//     await adminProductApi.deactivate(p.id)
//     toast.success('Product deactivated'); load()
//   } catch { toast.error('Failed to deactivate') }
// }

// function fmt(n) { return Number(n || 0).toLocaleString('en-IN') }
// function stockClass(s) {
//   if (s === 0)   return 'stock--out'
//   if (s <= 10)   return 'stock--low'
//   return 'stock--ok'
// }

function debounceLoad() {
  clearTimeout(debounceTimer)
  page.value = 1
  debounceTimer = setTimeout(() => load(), 300)
}

function openCreate() {
  createForm.value = {
    name: '', slug: '', sku: '', category_id: null,
    price: null, compare_price: null, stock_qty: 0,
    description: '', healing_props: '', chakra: '', zodiac: '',
    is_active: true, is_featured: false
  }
  createMsg.value = null
  showCreateDrawer.value = true
}

function closeCreate() {
  showCreateDrawer.value = false
  createMsg.value = null
}

function generateSlug() {
  if (createForm.value.name && !createForm.value.slug) {
    createForm.value.slug = createForm.value.name
      .toLowerCase()
      .trim()
      .replace(/[^\w\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
  }
}

async function saveCreate() {
  if (!createForm.value.name || !createForm.value.slug || !createForm.value.category_id || createForm.value.price === null) {
    createMsg.value = { ok: false, text: 'Please fill all required fields' }
    return
  }

  savingCreate.value = true
  createMsg.value = null
  try {
    await adminProductApi.create(createForm.value)
    toast.success('Product created ✓')
    closeCreate()
    load()
  } catch (e) {
    createMsg.value = { ok: false, text: e?.response?.data?.detail || 'Creation failed' }
  } finally {
    savingCreate.value = false
  }
}

async function openEdit(p) {
  editProduct.value = p
  editForm.value = {
    name: p.name,
    slug: p.slug,
    sku: p.sku,
    category_id: p.category_id,
    price: p.price,
    compare_price: p.compare_price,
    stock_qty: p.stock_qty,
    is_active: p.is_active,
    is_featured: p.is_featured,
    description: p.description,
    healing_props: p.healing_props,
    chakra: p.chakra,
    zodiac: p.zodiac
  }
  editMsg.value = null
  uploadMsg.value = null
  
  try {
    const { data } = await adminProductApi.listImages(p.id)
    console.log('IMAGE DATA', data)
    editProduct.value.images = data || []
  } catch {
    editProduct.value.images = []
  }
}

function closeEdit() {
  editProduct.value = null
  editForm.value = {}
  editMsg.value = null
  uploadMsg.value = null
}

async function saveEdit() {
  saving.value = true
  editMsg.value = null
  try {
    await adminProductApi.update(editProduct.value.id, editForm.value)
    toast.success('Product updated ✓')
    closeEdit()
    load()
  } catch (e) {
    editMsg.value = { ok: false, text: e?.response?.data?.detail || 'Update failed' }
  } finally {
    saving.value = false
  }
}

function onFileChange(e) {
  const file = e.target.files?.[0]
  if (!file) return
  uploadImage(file)
  e.target.value = ''
}

function onDrop(e) {
  dragOver.value = false
  const file = e.dataTransfer.files?.[0]
  if (!file || !file.type.startsWith('image/')) {
    uploadMsg.value = { ok: false, text: 'Please drop an image file' }
    return
  }
  uploadImage(file)
}

async function uploadImage(file) {
  uploadMsg.value = null
  const formData = new FormData()
  formData.append('file', file)

  try {
    const { data } = await adminProductApi.upload(editProduct.value.id, formData)
    if (editProduct.value.images) {
      editProduct.value.images.push(data)
    } else {
      editProduct.value.images = [data]
    }
    uploadMsg.value = { ok: true, text: 'Image uploaded ✓' }
  } catch (e) {
    uploadMsg.value = { ok: false, text: e?.response?.data?.detail || 'Upload failed' }
  }
}

async function deleteImage(imgId) {
  if (!confirm('Delete this image?')) return
  try {
    await adminProductApi.deleteImage(editProduct.value.id, imgId)
    editProduct.value.images = editProduct.value.images.filter(i => i.id !== imgId)
    uploadMsg.value = { ok: true, text: 'Image deleted ✓' }
  } catch {
    uploadMsg.value = { ok: false, text: 'Failed to delete image' }
  }
}

async function setPrimaryImage(imgId) {
  try {
    await adminProductApi.setPrimary(editProduct.value.id, imgId)
    editProduct.value.images.forEach(i => i.is_primary = i.id === imgId)
    uploadMsg.value = { ok: true, text: 'Primary image updated ✓' }
  } catch {
    uploadMsg.value = { ok: false, text: 'Failed to update primary' }
  }
}

async function confirmDeactivate(p) {
  if (!confirm(`Deactivate "${p.name}"? It will be hidden from the store.`)) return
  try {
    await adminProductApi.deactivate(p.id)
    toast.success('Product deactivated')
    load()
  } catch {
    toast.error('Failed to deactivate')
  }
}

async function confirmReactivate(p) {
  if (!confirm(`Reactivate "${p.name}"? It will be visible in the store.`)) return
  try {
    await adminProductApi.update(p.id, { is_active: true })
    toast.success('Product reactivated')
    load()
  } catch {
    toast.error('Failed to reactivate')
  }
}

function fmt(n) { return Number(n || 0).toLocaleString('en-IN') }
function stockClass(s) {
  if (s === 0)  return 'stock--out'
  if (s <= 10)  return 'stock--low'
  return 'stock--ok'
}
</script>

<style scoped>
.admin-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-head { display: flex; align-items: flex-end; justify-content: space-between; }
.page-title { font-family: var(--font-serif); font-size: 2rem; font-weight: 300; color: var(--ink); margin-top: 0.2rem; }
.result-badge { font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }

.header-actions { display: flex; align-items: center; gap: 1rem; }

/* IMPROVED BUTTON - HIGHLY VISIBLE */
.btn-create-new {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #C4876A 0%, #A8694A 100%);
  color: #FFFFFF;
  border: 2px solid transparent;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(196, 135, 106, 0.3);
  text-transform: uppercase;
}

.btn-create-new:hover {
  background: linear-gradient(135deg, #B8754F 0%, #A8694A 100%);
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(196, 135, 106, 0.4);
}

.btn-create-new:active {
  transform: translateY(-1px);
}

.create-icon {
  font-size: 1.3rem;
  font-weight: 900;
  line-height: 1;
}

.create-text {
  font-weight: 700;
  letter-spacing: 0.08em;
}

/* Filter bar */
.filter-bar { display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap; }
.filter-search { flex: 1; min-width: 200px; }
.filter-select { width: 180px; }
/* .input-field { background: var(--bg-card); border: 1px solid rgba(196,135,106,0.2); color: var(--ink); }
.input-field:focus { border-color: var(--rose-gold); } */
.input-field { 
  background: #fff; 
  border: 1px solid rgba(196,135,106,0.2); 
  color: var(--ink); 
  padding: 0.65rem 0.9rem;
  border-radius: 4px;
  font-size: 0.9rem;
}
.input-field:focus { 
  outline: none; 
  border-color: var(--rose-gold);
  box-shadow: 0 0 0 3px rgba(196,135,106,0.1);
}

/* Table */
/* .table-wrap { background: var(--bg-card); border: 1px solid rgba(196,135,106,0.12); overflow-x: auto; }
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
.admin-table tbody tr:hover { background: rgba(196,135,106,0.025); } */

.table-wrap { background: #fff; border: 1px solid rgba(196,135,106,0.12); border-radius: 6px; overflow-x: auto; }
.admin-table { width: 100%; border-collapse: collapse; }
.admin-table thead { background: #FAF7F3; border-bottom: 1px solid rgba(196,135,106,0.15); }
.admin-table th {
  padding: 0.85rem 1.2rem;
  text-align: left;
  font-size: 0.6rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #A88870;
  font-weight: 600;
}
.col-num { text-align: right; }
.admin-table td { padding: 0.9rem 1.2rem; border-bottom: 1px solid rgba(196,135,106,0.06); vertical-align: middle; }
.admin-table tbody tr:hover { background: rgba(196,135,106,0.02); }

/* Product cell */
.prod-cell { display: flex; align-items: center; gap: 0.75rem; }
/* .prod-thumb { width: 44px; height: 44px; object-fit: cover; flex-shrink: 0; }
.prod-name { font-size: 0.85rem; color: var(--ink); font-weight: 300; }
.prod-sku { color: var(--muted); font-size: 0.58rem; margin-top: 0.1rem; } */
.prod-thumb { width: 44px; height: 44px; object-fit: cover; flex-shrink: 0; border-radius: 2px; }
.prod-name { font-size: 0.85rem; color: var(--ink); font-weight: 300; margin: 0; }
.prod-sku { color: var(--muted); font-size: 0.58rem; margin-top: 0.1rem; margin: 0; }

/* Pills & badges */
/* .tag-pill { font-size: 0.65rem; padding: 0.2rem 0.6rem; background: rgba(196,135,106,0.08); color: var(--rose-gold-dim); } */
.tag-pill { font-size: 0.65rem; padding: 0.2rem 0.6rem; background: rgba(196,135,106,0.08); color: var(--rose-gold-dim); border-radius: 2px; }
.price-main { font-family: var(--font-serif); font-size: 0.9rem; color: var(--ink); }
/* .price-compare { font-size: 0.72rem; color: var(--light-muted); text-decoration: line-through; margin-left: 0.4rem; }
.stock-badge { font-size: 0.72rem; padding: 0.18rem 0.5rem; font-weight: 500; } */
.price-compare { font-size: 0.72rem; color: #999; text-decoration: line-through; margin-left: 0.4rem; }
.stock-badge { font-size: 0.72rem; padding: 0.18rem 0.5rem; font-weight: 500; border-radius: 2px; }
.stock--ok  { background: rgba(102,187,106,0.1); color: #5a9e5e; }
/* .stock--low { background: rgba(196,135,106,0.12); color: var(--rose-gold); } */
.stock--low { background: rgba(196,135,106,0.12); color: #C4876A; }
.stock--out { background: rgba(224,112,112,0.1); color: #c07070; }
/* .status-pill { font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.2rem 0.55rem; border: 1px solid; } */
.status-pill { font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.2rem 0.55rem; border: 1px solid; border-radius: 2px; }
.pill--active   { border-color: rgba(102,187,106,0.35); color: #5a9e5e; }
.pill--inactive { border-color: rgba(196,135,106,0.25); color: var(--muted); }

/* Actions */
.action-row { display: flex; gap: 0.5rem; }
/* .action-btn {
  width: 30px; height: 30px; border: 1px solid rgba(196,135,106,0.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; color: var(--muted); transition: all 0.2s;
} */
.action-btn {
  width: 30px; height: 30px; border: 1px solid rgba(196,135,106,0.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; color: #999; transition: all 0.2s;
  background: #fff;
  border-radius: 3px;
  cursor: pointer;
}
.action-btn:hover { border-color: var(--rose-gold); color: var(--rose-gold); background: rgba(196,135,106,0.06); }
.action-btn--danger:hover { border-color: #c07070; color: #c07070; background: rgba(224,112,112,0.06); }
.action-btn--warning:hover { border-color: #5a9e5e; color: #5a9e5e; background: rgba(102,187,106,0.06); }

/* Empty row */
.empty-row { text-align: center; padding: 3rem !important; }
/* .empty-icon { font-size: 2rem; color: var(--blush-mid); display: block; margin-bottom: 0.5rem; } */
.empty-icon { font-size: 2rem; color: #E8D3C0; display: block; margin-bottom: 0.5rem; }
.empty-row p { font-size: 0.82rem; color: var(--muted); }

/* Pagination */
.pagination { display: flex; align-items: center; justify-content: center; gap: 1rem; }
.page-info { color: var(--muted); }
.btn-sm { padding: 0.55rem 1.2rem; font-size: 0.62rem; }

/* Drawer */
/* .drawer-overlay {
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
.msg--err { background: rgba(224,112,112,0.08); color: #c07070; border: 1px solid rgba(224,112,112,0.2); } */

/* ============= CREATE PRODUCT MODAL - IMPROVED READABILITY ============= */

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(42, 31, 26, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  overflow-y: auto;
}

.modal-container {
  background: #FFFFFF;
  border-radius: 12px;
  width: 100%;
  max-width: 680px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 15px 50px rgba(42, 31, 26, 0.2);
  animation: slideInCenter 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideInCenter {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Modal Header */
.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 2rem;
  border-bottom: 2px solid #F5EAE2;
  background: linear-gradient(135deg, rgba(196, 135, 106, 0.06) 0%, transparent 100%);
}

.modal-header-content {
  flex: 1;
}

.modal-title {
  font-family: var(--font-serif);
  font-size: 1.75rem;
  font-weight: 400;
  color: #2A1F1A;
  margin: 0 0 0.4rem 0;
  letter-spacing: 0.02em;
}

.modal-subtitle {
  font-size: 0.9rem;
  color: #6B5B54;
  margin: 0;
  font-weight: 300;
}

.modal-close-btn {
  font-size: 1.8rem;
  color: #9D8B84;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  border-radius: 6px;
  flex-shrink: 0;
}

.modal-close-btn:hover {
  color: #EF5350;
  background: rgba(239, 83, 80, 0.08);
}

/* Modal Body */
.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: #F5EAE2;
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: #C4876A;
  border-radius: 4px;
}

/* Form Sections */
.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #F5EAE2;
}

.form-section:last-of-type {
  border-bottom: none;
  padding-bottom: 0;
}

.section-header {
  padding-bottom: 1rem;
}

.section-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: #2A1F1A;
  margin: 0 0 0.3rem 0;
  letter-spacing: 0.02em;
}

.section-subtitle {
  font-size: 0.85rem;
  color: #6B5B54;
  margin: 0;
}

.required {
  color: #EF5350;
  font-weight: 700;
}

/* Form Grid */
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.2rem;
}

.form-row:has(.form-group:only-child) {
  grid-template-columns: 1fr;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Form Labels & Inputs */
.form-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #2A1F1A;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.form-input,
.form-select,
.form-textarea {
  padding: 0.9rem 1rem;
  background: #FFFFFF;
  border: 2px solid #E8D3C0;
  border-radius: 6px;
  color: #2A1F1A;
  font-family: var(--font-sans);
  font-size: 0.95rem;
  line-height: 1.5;
  transition: all 0.2s ease;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #C4876A;
  background: #FFFFFF;
  box-shadow: 0 0 0 4px rgba(196, 135, 106, 0.1);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #9D8B84;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
  font-family: var(--font-sans);
}

.form-help {
  font-size: 0.8rem;
  color: #6B5B54;
  margin: 0;
  font-style: italic;
}

/* Alerts */
.alert-box {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.1rem 1.3rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  margin-top: 0.5rem;
}

.alert-icon {
  font-size: 1.4rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
}

.alert-text {
  flex: 1;
}

.alert-success {
  background: rgba(102, 187, 106, 0.12);
  color: #5a9e5e;
  border: 1px solid rgba(102, 187, 106, 0.25);
}

.alert-error {
  background: rgba(239, 83, 80, 0.12);
  color: #c07070;
  border: 1px solid rgba(239, 83, 80, 0.25);
}

/* Modal Footer */
.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 2px solid #F5EAE2;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  background: #FAF7F3;
  border-radius: 0 0 12px 12px;
}

.btn-cancel {
  padding: 0.8rem 1.6rem;
  background: #FFFFFF;
  color: #6B5B54;
  border: 2px solid #E8D3C0;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  border-color: #C4876A;
  color: #2A1F1A;
  background: #F5EAE2;
}

.btn-create-product {
  padding: 0.8rem 1.8rem;
  background: linear-gradient(135deg, #C4876A 0%, #A8694A 100%);
  color: #FFFFFF;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(196, 135, 106, 0.25);
  min-width: 150px;
}

.btn-create-product:hover:not(:disabled) {
  background: linear-gradient(135deg, #B8754F 0%, #A8694A 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(196, 135, 106, 0.35);
}

.btn-create-product:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

/* Existing Drawer Styles (for Edit) */
.drawer-overlay { position: fixed; inset: 0; z-index: 100; background: rgba(42, 31, 26, 0.5); backdrop-filter: blur(4px); display: flex; justify-content: flex-end; }
.drawer { width: 420px; height: 100%; background: #fff; border-left: 1px solid rgba(196,135,106,0.2); display: flex; flex-direction: column; animation: fadeIn 0.25s ease; }
.drawer--wide { width: 900px; display: grid; grid-template-rows: auto 1fr auto; }
.drawer__head { display: flex; align-items: center; justify-content: space-between; padding: 1.5rem; border-bottom: 1px solid rgba(196,135,106,0.12); }
.drawer__title { font-family: var(--font-serif); font-size: 1.2rem; font-weight: 300; color: var(--ink); }
.drawer__close { font-size: 0.8rem; color: var(--muted); transition: color 0.2s; cursor: pointer; border: none; background: none; padding: 0; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; }
.drawer__close:hover { color: var(--rose-gold); }
.drawer__body { flex: 1; overflow-y: auto; padding: 1.5rem; display: flex; gap: 2rem; }
.drawer--wide .drawer__body { grid-column: 1 / -1; }
.drawer__foot { padding: 1.2rem 1.5rem; border-top: 1px solid rgba(196,135,106,0.12); display: flex; gap: 0.75rem; justify-content: flex-end; }

.field { display: flex; flex-direction: column; gap: 0.4rem; }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.input-label { font-size: 0.85rem; font-weight: 600; color: var(--ink); }
.edit-main { flex: 1; min-width: 0; }
.edit-images { flex: 1; min-width: 0; }
.section-label { margin-bottom: 1rem; }
.divider-line { height: 1px; background: rgba(196,135,106,0.1); margin-top: 0.5rem; }

.img-count-badge { display: inline-block; margin-left: 0.5rem; background: #F5EAE2; color: var(--rose-gold); font-size: 0.6rem; font-weight: 700; padding: 0.15rem 0.45rem; border-radius: 10px; }
.img-gallery-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.6rem; margin-bottom: 1rem; }
.img-tile { border: 2px solid rgba(196,135,106,0.2); border-radius: 4px; overflow: hidden; transition: border-color 0.2s; }
.img-tile--primary { border-color: var(--rose-gold); }
.img-tile__photo { position: relative; aspect-ratio: 1; overflow: hidden; }
.img-tile__photo img { width: 100%; height: 100%; object-fit: cover; }
.img-tile__badge { position: absolute; bottom: 0; left: 0; right: 0; background: var(--rose-gold); color: #fff; font-size: 0.55rem; font-weight: 700; text-align: center; padding: 0.2rem; text-transform: uppercase; }
.img-tile__actions { display: flex; gap: 0; border-top: 1px solid rgba(196,135,106,0.2); }
.img-btn { flex: 1; padding: 0.35rem; font-size: 0.6rem; font-weight: 600; border: none; cursor: pointer; transition: background 0.2s; background: none; text-align: center; }
.img-btn--star { background: #F5EAE2; color: var(--rose-gold); }
.img-btn--star:hover { background: var(--rose-gold); color: #fff; }
.img-btn--del { background: rgba(217,90,74,0.08); color: #c07070; border-left: 1px solid rgba(196,135,106,0.2); }
.img-btn--del:hover { background: #c07070; color: #fff; }

.no-images-hint { font-size: 0.78rem; color: var(--muted); text-align: center; padding: 1.5rem; border: 1px dashed rgba(196,135,106,0.2); border-radius: 4px; margin-bottom: 1rem; }
.upload-zone { border: 2px dashed rgba(196,135,106,0.2); border-radius: 4px; transition: all 0.2s; position: relative; }
.upload-zone--active { border-color: var(--rose-gold); background: rgba(196,135,106,0.06); }
.upload-file-input { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; z-index: 2; }
.upload-zone__inner { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; padding: 1.5rem 1rem; text-align: center; cursor: pointer; }
.upload-icon { font-size: 1.8rem; }
.upload-zone__inner span { font-size: 0.8rem; color: var(--muted); }
.upload-ready { color: var(--rose-gold) !important; font-weight: 700; }
.upload-feedback { font-size: 0.75rem; padding: 0.6rem 0.9rem; margin-top: 0.5rem; }
.edit-msg { font-size: 0.75rem; padding: 0.6rem 0.9rem; }
.msg--ok { background: rgba(102,187,106,0.08); color: #5a9e5e; border: 1px solid rgba(102,187,106,0.2); }
.msg--err { background: rgba(224,112,112,0.08); color: #c07070; border: 1px solid rgba(224,112,112,0.2); }

@media (max-width: 768px) {
  .modal-container { max-width: 95vw; max-height: 90vh; }
  .form-row { grid-template-columns: 1fr; }
  .modal-header { padding: 1.5rem; }
  .modal-body { padding: 1.5rem; }
  .modal-footer { padding: 1rem 1.5rem; }
  .btn-cancel, .btn-create-product { padding: 0.7rem 1.2rem; font-size: 0.9rem; }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
