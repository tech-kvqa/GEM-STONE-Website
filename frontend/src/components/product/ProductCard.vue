<template>
  <article class="product-card" @mouseenter="hovered = true" @mouseleave="hovered = false">
    <router-link :to="`/crystal/${product.slug}`" class="product-card__media">
      <div class="product-card__img-wrap">
        <img :src="primaryImage" :alt="product.name" class="product-card__img product-card__img--primary" loading="lazy" />
        <img v-if="secondImage" :src="secondImage" :alt="product.name" class="product-card__img product-card__img--hover" loading="lazy" />
      </div>
      <div class="product-card__badges">
        <span v-if="product.is_new_arrival" class="badge badge-gold">New</span>
        <span v-else-if="product.is_bestseller" class="badge badge-outline">Bestseller</span>
        <span v-if="product.compare_price && product.compare_price > product.price" class="badge badge-gold">{{ discountPct }}% Off</span>
      </div>
      <div :class="['product-card__actions', { visible: hovered }]">
        <button class="action-pill" @click.prevent="addToCart" :disabled="adding">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
          {{ adding ? 'Added ✓' : 'Add to Bag' }}
        </button>
        <button class="action-icon" @click.prevent="toggleWishlist" :class="{ wishlisted: wishlist.isWishlisted(product.id) }">
          <svg width="13" height="13" viewBox="0 0 24 24" :fill="wishlist.isWishlisted(product.id) ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.5"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
        </button>
      </div>
      <div v-if="product.stock_qty === 0" class="product-card__oos"><span>Out of Stock</span></div>
    </router-link>

    <div class="product-card__info">
      <p v-if="product.category" class="product-card__cat">{{ product.category.name }}</p>
      <router-link :to="`/crystal/${product.slug}`" class="product-card__name">{{ product.name }}</router-link>
      <div v-if="product.avg_rating" class="product-card__rating">
        <div class="stars">
          <span v-for="i in 5" :key="i" :class="i <= Math.round(product.avg_rating) ? '' : 'star-empty'">★</span>
        </div>
        <span class="rating-count">({{ product.review_count }})</span>
      </div>
      <div v-if="product.chakra" class="product-card__chakra">{{ product.chakra }}</div>
      <div class="product-card__price">
        <span class="price-main">₹{{ product.price.toLocaleString('en-IN') }}</span>
        <span v-if="product.compare_price && product.compare_price > product.price" class="price-old">
          ₹{{ product.compare_price.toLocaleString('en-IN') }}
        </span>
      </div>
    </div>
  </article>
</template>

<script setup>
import { getImageUrl } from '@/utils/image'
import { ref, computed } from 'vue'
import { toast } from 'vue3-toastify'
import { useCartStore } from '@/store/cart'
import { useWishlistStore } from '@/store/wishlist'
import { useAuthStore } from '@/store/auth'

const props   = defineProps({ product: { type: Object, required: true } })
const cart    = useCartStore()
const wishlist= useWishlistStore()
const auth    = useAuthStore()
const hovered = ref(false)
const adding  = ref(false)

// const primaryImage = computed(() =>
//   props.product.images?.find(i => i.is_primary)?.url ||
//   props.product.images?.[0]?.url ||
//   'https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=600'
// )
const primaryImage = computed(() => {
  const img =
    props.product.images?.find(i => i.is_primary)?.url ||
    props.product.images?.[0]?.url

  return img
    ? getImageUrl(img)
    : 'https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=600'
})
// const secondImage = computed(() => props.product.images?.find(i => !i.is_primary)?.url || null)
const secondImage = computed(() => {
  const img = props.product.images?.find(i => !i.is_primary)?.url
  return img ? getImageUrl(img) : null
})
const discountPct = computed(() => {
  if (!props.product.compare_price) return 0
  return Math.round((1 - props.product.price / props.product.compare_price) * 100)
})

async function addToCart() {
  if (props.product.stock_qty === 0) return
  if (!auth.isLoggedIn) { toast.info('Please sign in to add items'); return }
  adding.value = true
  try {
    await cart.addItem(props.product.id)
    toast.success(`${props.product.name} added to bag ✦`)
  } catch { toast.error('Could not add to bag') }
  finally { setTimeout(() => adding.value = false, 1400) }
}

async function toggleWishlist() {
  if (!auth.isLoggedIn) { toast.info('Please sign in to save items'); return }
  try {
    await wishlist.toggle(props.product.id)
    toast.success(wishlist.isWishlisted(props.product.id) ? 'Saved to wishlist ♡' : 'Removed from wishlist')
  } catch {}
}
</script>

<style scoped>
.product-card { display: flex; flex-direction: column; }
.product-card__media {
  position: relative; aspect-ratio: 4/5; overflow: hidden;
  background: var(--blush-light); display: block;
}
.product-card__img-wrap { width: 100%; height: 100%; position: relative; }
.product-card__img {
  position: absolute; inset: 0; width: 100%; height: 100%;
  object-fit: cover; transition: transform 0.6s var(--ease-silk), opacity 0.5s;
}
.product-card__img--primary { z-index: 1; }
.product-card__img--hover   { z-index: 2; opacity: 0; }
.product-card:hover .product-card__img--primary { transform: scale(1.04); }
.product-card:hover .product-card__img--hover   { opacity: 1; }

.product-card__badges {
  position: absolute; top: 0.75rem; left: 0.75rem;
  display: flex; flex-direction: column; gap: 0.3rem; z-index: 5;
}

.product-card__actions {
  position: absolute; bottom: 0; left: 0; right: 0;
  display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem;
  background: linear-gradient(to top, rgba(42,31,26,0.55), transparent);
  transform: translateY(100%); transition: transform 0.35s var(--ease-silk); z-index: 5;
}
.product-card__actions.visible { transform: translateY(0); }

.action-pill {
  flex: 1; background: var(--rose-gold); color: #fff;
  font-size: 0.6rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase;
  padding: 0.6rem 1rem; display: flex; align-items: center; justify-content: center; gap: 0.4rem;
  transition: background 0.2s;
}
.action-pill:hover { background: var(--rose-gold-bright); }
.action-pill:disabled { opacity: 0.8; }

.action-icon {
  width: 36px; height: 36px;
  background: rgba(255,255,255,0.85); border: none;
  display: flex; align-items: center; justify-content: center;
  color: var(--rose-gold-dim); transition: all 0.2s;
}
.action-icon:hover, .action-icon.wishlisted { background: var(--rose-gold); color: #fff; }

.product-card__oos {
  position: absolute; inset: 0; z-index: 6;
  background: rgba(253,240,236,0.6);
  display: flex; align-items: center; justify-content: center;
}
.product-card__oos span {
  font-size: 0.62rem; letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--warm-brown); border: 1px solid var(--blush-mid); padding: 0.4rem 0.9rem;
  background: rgba(255,255,255,0.8);
}

.product-card__info { padding: 0.85rem 0 0.5rem; }
.product-card__cat { font-size: 0.58rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--rose-gold); margin-bottom: 0.3rem; }
.product-card__name {
  font-family: var(--font-serif); font-size: 1rem; font-weight: 400;
  color: var(--ink); line-height: 1.3; display: block; margin-bottom: 0.35rem;
  transition: color 0.2s;
}
.product-card__name:hover { color: var(--rose-gold); }
.product-card__rating { display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.3rem; }
.rating-count { font-size: 0.68rem; color: var(--muted); }
.product-card__chakra { font-size: 0.6rem; letter-spacing: 0.1em; color: var(--mauve); margin-bottom: 0.35rem; }
.product-card__price { display: flex; align-items: baseline; gap: 0.5rem; }
.price-main { font-family: var(--font-serif); font-size: 1.05rem; color: var(--rose-gold); }
.price-old  { font-size: 0.78rem; color: var(--muted); text-decoration: line-through; }
</style>
