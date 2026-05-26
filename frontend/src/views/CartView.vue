<template>
  <main class="cart-page">
    <div style="height: var(--nav-h)"></div>
    <div class="container" style="padding-top:3rem;padding-bottom:5rem">
      <div class="section-head" style="text-align:left;margin-bottom:2rem">
        <p class="label-caps">Your Selection</p>
        <h1 class="heading-section">Shopping Bag</h1>
      </div>

      <div v-if="cart.items.length" class="cart-layout">
        <!-- Items -->
        <div class="cart-items">
          <div v-for="item in cart.items" :key="item.id" class="cart-row">
            <router-link :to="`/crystal/${item.product.slug}`" class="cart-row__img">
              <img :src="primaryImage(item.product)" :alt="item.product.name" />
            </router-link>
            <div class="cart-row__info">
              <p class="cart-row__cat">{{ item.product.category?.name }}</p>
              <router-link :to="`/crystal/${item.product.slug}`" class="cart-row__name">{{ item.product.name }}</router-link>
              <p v-if="item.product.origin" class="cart-row__origin">Origin: {{ item.product.origin }}</p>
            </div>
            <div class="cart-row__controls">
              <div class="qty-ctrl">
                <button @click="cart.updateItem(item.id, item.quantity - 1)">−</button>
                <span>{{ item.quantity }}</span>
                <button @click="cart.updateItem(item.id, item.quantity + 1)">+</button>
              </div>
              <p class="cart-row__price">₹{{ (item.product.price * item.quantity).toLocaleString('en-IN') }}</p>
              <button class="cart-row__remove" @click="cart.removeItem(item.id)">Remove</button>
            </div>
          </div>
        </div>

        <!-- Summary -->
        <div class="cart-summary">
          <h3>Order Summary</h3>
          <div class="summary-row"><span>Subtotal</span><span>₹{{ cart.subtotal.toLocaleString('en-IN') }}</span></div>
          <div class="summary-row">
            <span>Shipping</span>
            <span :class="{ 'text-gold': cart.shipping === 0 }">{{ cart.shipping === 0 ? 'Free' : '₹' + cart.shipping }}</span>
          </div>
          <div v-if="cart.shipping > 0" class="free-notice">
            Add ₹{{ (999 - cart.subtotal).toLocaleString('en-IN') }} more for free shipping
          </div>
          <div class="summary-row summary-total"><span>Total</span><span>₹{{ cart.total.toLocaleString('en-IN') }}</span></div>
          <router-link to="/checkout" class="btn btn-gold w-full"><span>Proceed to Checkout</span></router-link>
          <router-link to="/shop" class="continue-link">← Continue Shopping</router-link>
        </div>
      </div>

      <div v-else class="empty-state">
        <div style="font-size:3.5rem;color:var(--gold-dim);animation:float 3s ease-in-out infinite">✦</div>
        <p style="color:var(--ivory-dim);opacity:0.5;font-family:var(--font-serif);font-size:1.3rem">Your bag is empty</p>
        <router-link to="/shop" class="btn btn-outline"><span>Explore Crystals</span></router-link>
      </div>
    </div>
  </main>
</template>

<script setup>
import { useCartStore } from '@/store/cart'
const cart = useCartStore()
const primaryImage = p =>
  p.images?.find(i => i.is_primary)?.url || p.images?.[0]?.url ||
  'https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=300'
</script>

<style scoped>
.cart-layout { display: grid; grid-template-columns: 1fr 340px; gap: 3rem; align-items: start; }
.cart-items { display: flex; flex-direction: column; gap: 0; }
.cart-row {
  display: grid; grid-template-columns: 100px 1fr auto;
  gap: 1.5rem; align-items: center;
  padding: 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.06);
}
.cart-row__img { width: 100px; height: 100px; overflow: hidden; background: var(--charcoal); display: block; }
.cart-row__img img { width: 100%; height: 100%; object-fit: cover; }
.cart-row__cat { font-size: 0.6rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--gold-dim); margin-bottom: 0.25rem; }
.cart-row__name { font-family: var(--font-serif); font-size: 1.1rem; color: var(--ivory); display: block; margin-bottom: 0.25rem; }
.cart-row__name:hover { color: var(--gold); }
.cart-row__origin { font-size: 0.72rem; color: var(--ivory-dim); opacity: 0.4; }
.cart-row__controls { display: flex; flex-direction: column; align-items: flex-end; gap: 0.75rem; }
.qty-ctrl { display: flex; align-items: center; border: 1px solid rgba(201,168,76,0.2); }
.qty-ctrl button { width: 32px; height: 32px; color: var(--gold-dim); font-size: 1rem; transition: all 0.2s; }
.qty-ctrl button:hover { color: var(--gold); background: rgba(201,168,76,0.08); }
.qty-ctrl span { width: 36px; text-align: center; font-size: 0.85rem; color: var(--ivory); border-left: 1px solid rgba(201,168,76,0.2); border-right: 1px solid rgba(201,168,76,0.2); line-height: 32px; }
.cart-row__price { font-family: var(--font-serif); font-size: 1.1rem; color: var(--gold); }
.cart-row__remove { font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(255,255,255,0.2); transition: color 0.2s; }
.cart-row__remove:hover { color: #e07070; }

.cart-summary { position: sticky; top: calc(var(--nav-h) + 2rem); background: var(--charcoal); border: 1px solid rgba(201,168,76,0.12); padding: 2rem; }
.cart-summary h3 { font-family: var(--font-serif); font-size: 1.2rem; font-weight: 300; color: var(--ivory); margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.06); }
.summary-row { display: flex; justify-content: space-between; font-size: 0.82rem; color: var(--ivory-dim); padding: 0.4rem 0; }
.summary-total { font-family: var(--font-serif); font-size: 1.1rem; color: var(--ivory); border-top: 1px solid rgba(255,255,255,0.08); margin-top: 0.5rem; padding-top: 0.75rem; }
.free-notice { font-size: 0.65rem; letter-spacing: 0.08em; color: var(--gold-dim); text-align: center; padding: 0.4rem; border: 1px dashed rgba(201,168,76,0.2); margin: 0.5rem 0; }
.w-full { width: 100%; margin-top: 1.25rem; }
.continue-link { display: block; text-align: center; margin-top: 0.75rem; font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--gold-dim); transition: color 0.2s; }
.continue-link:hover { color: var(--gold); }

.empty-state { display: flex; flex-direction: column; align-items: center; gap: 1.5rem; padding: 5rem 0; text-align: center; }

@media (max-width: 768px) { .cart-layout { grid-template-columns: 1fr; } .cart-row { grid-template-columns: 80px 1fr; } .cart-row__controls { grid-column: 1 / -1; flex-direction: row; align-items: center; justify-content: space-between; } }
</style>
