<template>
  <main class="product-page" v-if="product">
    <div style="height: var(--nav-h)"></div>

    <!-- Breadcrumb -->
    <div class="breadcrumb container">
      <router-link to="/">Home</router-link>
      <span>›</span>
      <router-link to="/shop">Crystals</router-link>
      <span>›</span>
      <router-link :to="`/shop/${product.category.slug}`">{{ product.category.name }}</router-link>
      <span>›</span>
      <span>{{ product.name }}</span>
    </div>

    <!-- Main Product Section -->
    <section class="product-main container">
      <!-- Gallery -->
      <div class="product-gallery">
        <div class="gallery-main">
          <!-- <img :src="selectedImage" :alt="product.name" class="gallery-main__img" /> -->
           <img :src="getImageUrl(selectedImage)" :alt="product.name" class="gallery-main__img" />
        </div>
        <div v-if="product.images.length > 1" class="gallery-thumbs">
          <button
            v-for="img in product.images"
            :key="img.id"
            :class="['thumb', { active: selectedImage === img.url }]"
            @click="selectedImage = img.url"
          >
            <!-- <img :src="img.url" :alt="img.alt_text || product.name" /> -->
             <img :src="getImageUrl(img.url)" :alt="img.alt_text || product.name" />
          </button>
        </div>
      </div>

      <!-- Info Panel -->
      <div class="product-info">
        <p class="product-info__cat label-caps">{{ product.category.name }}</p>

        <h1 class="product-info__name">{{ product.name }}</h1>

        <div v-if="product.avg_rating" class="product-info__rating">
          <div class="stars">
            <span v-for="i in 5" :key="i" :class="i <= Math.round(product.avg_rating) ? '' : 'star-empty'">★</span>
          </div>
          <span class="rating-text">{{ product.avg_rating }} ({{ product.review_count }} reviews)</span>
        </div>

        <div class="product-info__price">
          <span class="price-main">₹{{ product.price.toLocaleString('en-IN') }}</span>
          <span v-if="product.compare_price && product.compare_price > product.price" class="price-old">
            ₹{{ product.compare_price.toLocaleString('en-IN') }}
          </span>
          <span v-if="discountPct" class="price-save">Save {{ discountPct }}%</span>
        </div>

        <div class="divider-gold"><span>✦</span></div>

        <!-- Meta tags -->
        <div class="product-meta">
          <div v-if="product.chakra" class="meta-item">
            <span class="meta-label">Chakra</span>
            <span class="meta-value">{{ product.chakra }}</span>
          </div>
          <div v-if="product.zodiac" class="meta-item">
            <span class="meta-label">Zodiac</span>
            <span class="meta-value">{{ product.zodiac }}</span>
          </div>
          <div v-if="product.origin" class="meta-item">
            <span class="meta-label">Origin</span>
            <span class="meta-value">{{ product.origin }}</span>
          </div>
          <div v-if="product.weight_grams" class="meta-item">
            <span class="meta-label">Weight</span>
            <span class="meta-value">~ {{ product.weight_grams }}g</span>
          </div>
          <div v-if="product.dimensions" class="meta-item">
            <span class="meta-label">Size</span>
            <span class="meta-value">{{ product.dimensions }}</span>
          </div>
        </div>

        <!-- Quantity + CTA -->
        <div class="product-actions">
          <div class="qty-wrapper">
            <label class="input-label">Qty</label>
            <div class="qty-ctrl">
              <button @click="qty = Math.max(1, qty - 1)">−</button>
              <span>{{ qty }}</span>
              <button @click="qty = Math.min(product.stock_qty, qty + 1)">+</button>
            </div>
          </div>
          <button
            class="btn btn-gold add-btn"
            @click="addToCart"
            :disabled="adding || product.stock_qty === 0"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
            <span>{{ product.stock_qty === 0 ? 'Out of Stock' : adding ? 'Adding…' : 'Add to Bag' }}</span>
          </button>
          <button class="btn btn-icon btn-ghost" @click="toggleWishlist" :title="isWishlisted ? 'Remove from Wishlist' : 'Add to Wishlist'">
            <svg width="18" height="18" viewBox="0 0 24 24" :fill="isWishlisted ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.5"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          </button>
        </div>

        <p v-if="product.stock_qty > 0 && product.stock_qty <= 5" class="low-stock">
          ⚠ Only {{ product.stock_qty }} remaining
        </p>

        <!-- Delivery Info -->
        <div class="delivery-info">
          <div class="delivery-item">🚚 <span>Free shipping on orders above ₹999</span></div>
          <div class="delivery-item">📦 <span>Dispatched in 1-3 business days</span></div>
          <div class="delivery-item">↩️ <span>7-day easy returns</span></div>
          <div class="delivery-item">✅ <span>Certified 100% natural crystal</span></div>
        </div>
      </div>
    </section>

    <!-- Crystal Story & Details -->
    <section class="product-deep container">
      <div class="deep-tabs">
        <button
          v-for="tab in tabs"
          :key="tab"
          :class="['deep-tab', { active: activeTab === tab }]"
          @click="activeTab = tab"
        >{{ tab }}</button>
      </div>

      <div class="deep-content">
        <div v-if="activeTab === 'The Story'" class="story-panel">
          <div class="story-panel__icon">✦</div>
          <p class="body-serif">{{ product.story || product.description }}</p>
        </div>
        <div v-if="activeTab === 'Healing Properties'" class="healing-panel">
          <p class="body-serif">{{ product.healing_props }}</p>
          <div v-if="product.chakra" class="healing-chakra">
            <p class="label-caps" style="margin-bottom:0.5rem">Associated Chakra</p>
            <p>{{ product.chakra }}</p>
          </div>
          <div v-if="product.zodiac" class="healing-chakra">
            <p class="label-caps" style="margin-bottom:0.5rem">Zodiac Signs</p>
            <p>{{ product.zodiac }}</p>
          </div>
        </div>
        <div v-if="activeTab === 'Reviews'" class="reviews-panel">
          <div v-if="reviews.length" class="reviews-list">
            <div v-for="r in reviews" :key="r.id" class="review-card">
              <div class="review-card__head">
                <div class="stars">
                  <span v-for="i in 5" :key="i" :class="i <= r.rating ? '' : 'star-empty'">★</span>
                </div>
                <span class="review-date">{{ formatDate(r.created_at) }}</span>
              </div>
              <p v-if="r.title" class="review-title">{{ r.title }}</p>
              <p class="review-body">{{ r.body }}</p>
              <p class="review-author">— {{ r.user.full_name }}
                <span v-if="r.is_verified" class="verified-badge">✓ Verified Purchase</span>
              </p>
            </div>
          </div>
          <p v-else class="body-serif" style="opacity:0.5">Be the first to review this crystal.</p>

          <!-- Write review -->
          <div v-if="auth.isLoggedIn" class="write-review">
            <h4>Share Your Experience</h4>
            <div class="star-input">
              <button v-for="i in 5" :key="i" @click="newReview.rating = i" :class="{ lit: i <= newReview.rating }">★</button>
            </div>
            <input v-model="newReview.title" class="input-field" placeholder="Review title" style="margin-bottom:0.75rem" />
            <textarea v-model="newReview.body" class="input-field" rows="4" placeholder="Tell others about this crystal…" style="resize:vertical"></textarea>
            <button class="btn btn-outline" style="margin-top:1rem" @click="submitReview"><span>Submit Review</span></button>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- Loading -->
  <div v-else-if="loading" class="container" style="padding-top:calc(var(--nav-h) + 4rem)">
    <div class="skeleton" style="height:600px"></div>
  </div>
</template>

<script setup>
import { getImageUrl } from '@/utils/image'
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { toast } from 'vue3-toastify'
import { productApi, reviewApi } from '@/api'
import { useCartStore } from '@/store/cart'
import { useWishlistStore } from '@/store/wishlist'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const cart = useCartStore()
const wishlist = useWishlistStore()
const auth = useAuthStore()

const product = ref(null)
const reviews = ref([])
const loading = ref(true)
const selectedImage = ref('')
const qty = ref(1)
const adding = ref(false)
const activeTab = ref('The Story')

const tabs = computed(() => {
  const t = ['The Story']
  if (product.value?.healing_props) t.push('Healing Properties')
  t.push('Reviews')
  return t
})

const newReview = ref({ rating: 5, title: '', body: '' })
const discountPct = computed(() => {
  if (!product.value?.compare_price) return 0
  return Math.round((1 - product.value.price / product.value.compare_price) * 100)
})
const isWishlisted = computed(() => product.value ? wishlist.isWishlisted(product.value.id) : false)

async function load() {
  loading.value = true
  try {
    const { data } = await productApi.get(route.params.slug)
    product.value = data
    selectedImage.value = data.images?.find(i => i.is_primary)?.url || data.images?.[0]?.url || ''
    const rev = await reviewApi.list(data.id)
    reviews.value = rev.data
  } finally { loading.value = false }
}

async function addToCart() {
  if (!auth.isLoggedIn) { toast.info('Please sign in first'); return }
  adding.value = true
  try {
    await cart.addItem(product.value.id, qty.value)
    toast.success(`${product.value.name} added to bag`)
  } catch { toast.error('Failed to add') }
  finally { setTimeout(() => adding.value = false, 1500) }
}

async function toggleWishlist() {
  if (!auth.isLoggedIn) { toast.info('Please sign in first'); return }
  await wishlist.toggle(product.value.id)
  toast.success(isWishlisted.value ? 'Saved to wishlist' : 'Removed from wishlist')
}

async function submitReview() {
  if (!newReview.value.rating) { toast.error('Please select a rating'); return }
  try {
    await reviewApi.add(product.value.id, newReview.value)
    toast.success('Review submitted!')
    newReview.value = { rating: 5, title: '', body: '' }
    const rev = await reviewApi.list(product.value.id)
    reviews.value = rev.data
  } catch (e) {
    toast.error(e.response?.data?.detail || 'Could not submit review')
  }
}

function formatDate(d) {
  return new Date(d).toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' })
}

watch(() => route.params.slug, load)
onMounted(load)
</script>

<style scoped>
.breadcrumb {
  display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;
  padding-top: 1.5rem; padding-bottom: 0;
  font-size: 0.7rem; color: var(--ivory-dim); opacity: 0.4;
}
.breadcrumb a:hover { color: var(--gold); opacity: 1; }
.breadcrumb span:not(a span) { color: var(--gold-dim); }

.product-main {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  padding-top: 2rem;
  padding-bottom: 4rem;
}

/* Gallery */
.gallery-main {
  aspect-ratio: 4/5;
  overflow: hidden;
  background: var(--charcoal);
}
.gallery-main__img { width: 100%; height: 100%; object-fit: cover; }
.gallery-thumbs { display: flex; gap: 0.5rem; margin-top: 0.75rem; flex-wrap: wrap; }
.thumb {
  width: 70px; height: 70px;
  overflow: hidden; border: 2px solid transparent;
  transition: border-color 0.2s;
}
.thumb.active { border-color: var(--gold); }
.thumb img { width: 100%; height: 100%; object-fit: cover; }

/* Info */
.product-info__cat { margin-bottom: 0.5rem; }
.product-info__name {
  font-family: var(--font-serif);
  font-size: clamp(1.8rem, 3vw, 2.8rem);
  font-weight: 300; color: var(--ivory);
  margin-bottom: 0.75rem; line-height: 1.2;
}
.product-info__rating { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; }
.rating-text { font-size: 0.75rem; color: var(--ivory-dim); opacity: 0.5; }

.product-info__price {
  display: flex; align-items: baseline; gap: 0.75rem;
  margin-bottom: 1.25rem;
}
.price-main { font-family: var(--font-serif); font-size: 1.8rem; color: var(--gold); }
.price-old { font-size: 1rem; color: var(--ivory-dim); opacity: 0.4; text-decoration: line-through; }
.price-save { font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; background: var(--gold); color: var(--black); padding: 0.2rem 0.5rem; }

.product-meta { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem 2rem; margin: 1.25rem 0; }
.meta-item { display: flex; flex-direction: column; }
.meta-label { font-size: 0.6rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--gold-dim); margin-bottom: 0.15rem; }
.meta-value { font-size: 0.85rem; color: var(--ivory-dim); }

.product-actions {
  display: flex; align-items: flex-end; gap: 0.75rem; margin: 1.5rem 0 0.75rem;
}
.qty-wrapper { display: flex; flex-direction: column; gap: 0.3rem; }
.qty-ctrl {
  display: flex; align-items: center;
  border: 1px solid rgba(201,168,76,0.25);
}
.qty-ctrl button {
  width: 36px; height: 40px;
  color: var(--gold-dim); font-size: 1.1rem;
  transition: all 0.2s;
}
.qty-ctrl button:hover { color: var(--gold); background: rgba(201,168,76,0.08); }
.qty-ctrl span { width: 40px; text-align: center; font-size: 0.9rem; color: var(--ivory); }
.add-btn { flex: 1; gap: 0.5rem; }

.low-stock { font-size: 0.75rem; color: #e07070; margin-bottom: 0.5rem; }

.delivery-info { margin-top: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.delivery-item { font-size: 0.78rem; color: var(--ivory-dim); opacity: 0.55; display: flex; gap: 0.5rem; }

/* Deep Tabs */
.product-deep { padding-bottom: 5rem; }
.deep-tabs {
  display: flex; gap: 0;
  border-bottom: 1px solid rgba(201,168,76,0.15);
  margin-bottom: 2.5rem;
}
.deep-tab {
  padding: 0.75rem 1.75rem;
  font-size: 0.68rem; font-weight: 500; letter-spacing: 0.15em; text-transform: uppercase;
  color: var(--ivory-dim); opacity: 0.5;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}
.deep-tab.active { color: var(--gold); opacity: 1; border-bottom-color: var(--gold); }
.deep-tab:hover { opacity: 1; color: var(--ivory); }

.story-panel { max-width: 700px; margin: 0 auto; text-align: center; }
.story-panel__icon { font-size: 2rem; color: var(--gold-dim); margin-bottom: 1.5rem; }
.healing-panel { max-width: 700px; }
.healing-chakra { margin-top: 2rem; padding: 1.25rem; border: 1px solid rgba(201,168,76,0.12); }

.reviews-list { display: flex; flex-direction: column; gap: 1.5rem; margin-bottom: 3rem; }
.review-card { padding: 1.5rem; border: 1px solid rgba(255,255,255,0.06); }
.review-card__head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
.review-date { font-size: 0.68rem; color: var(--ivory-dim); opacity: 0.4; }
.review-title { font-family: var(--font-serif); font-size: 1.05rem; color: var(--ivory); margin-bottom: 0.5rem; }
.review-body { font-size: 0.85rem; color: var(--ivory-dim); line-height: 1.7; margin-bottom: 0.75rem; opacity: 0.7; }
.review-author { font-size: 0.72rem; color: var(--gold-dim); }
.verified-badge { margin-left: 0.5rem; color: #66bb6a; font-size: 0.65rem; }

.write-review { border-top: 1px solid rgba(255,255,255,0.06); padding-top: 2rem; }
.write-review h4 { font-family: var(--font-serif); font-size: 1.3rem; font-weight: 300; color: var(--ivory); margin-bottom: 1rem; }
.star-input { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
.star-input button { font-size: 1.5rem; color: rgba(201,168,76,0.25); transition: color 0.2s; }
.star-input button.lit { color: var(--gold); }
.star-input button:hover { color: var(--gold-light); }

@media (max-width: 900px) {
  .product-main { grid-template-columns: 1fr; gap: 2rem; }
}
</style>
