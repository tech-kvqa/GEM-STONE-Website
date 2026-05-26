<template>
  <teleport to="body">
    <transition name="drawer">
      <div v-if="cart.open" class="drawer-overlay" @click.self="cart.open = false">
        <div class="drawer">
          <div class="drawer__head">
            <div>
              <p class="label-caps">Your Selection</p>
              <h3>Shopping Bag <span v-if="cart.count">({{ cart.count }})</span></h3>
            </div>
            <button class="drawer__close" @click="cart.open = false">✕</button>
          </div>

          <div class="drawer__body">
            <div v-if="cart.loading" class="drawer__loading">
              <div v-for="i in 3" :key="i" class="skeleton" style="height:90px;margin-bottom:1rem"></div>
            </div>
            <div v-else-if="!cart.items.length" class="drawer__empty">
              <div class="empty-icon">✦</div>
              <p>Your bag is empty</p>
              <router-link to="/shop" class="btn btn-outline" @click="cart.open = false"><span>Explore Crystals</span></router-link>
            </div>
            <div v-else class="drawer__items">
              <TransitionGroup name="item">
                <div v-for="item in cart.items" :key="item.id" class="cart-item">
                  <router-link :to="`/crystal/${item.product.slug}`" class="cart-item__img" @click="cart.open = false">
                    <img :src="primaryImage(item.product)" :alt="item.product.name" />
                  </router-link>
                  <div class="cart-item__info">
                    <router-link :to="`/crystal/${item.product.slug}`" class="cart-item__name" @click="cart.open = false">{{ item.product.name }}</router-link>
                    <p class="cart-item__cat">{{ item.product.category?.name }}</p>
                    <div class="cart-item__foot">
                      <div class="qty-ctrl">
                        <button @click="cart.updateItem(item.id, item.quantity - 1)">−</button>
                        <span>{{ item.quantity }}</span>
                        <button @click="cart.updateItem(item.id, item.quantity + 1)">+</button>
                      </div>
                      <span class="cart-item__price">₹{{ (item.product.price * item.quantity).toLocaleString('en-IN') }}</span>
                    </div>
                  </div>
                  <button class="cart-item__remove" @click="cart.removeItem(item.id)" title="Remove">✕</button>
                </div>
              </TransitionGroup>
            </div>
          </div>

          <div v-if="cart.items.length" class="drawer__foot">
            <div class="drawer__summary">
              <div class="summary-row"><span>Subtotal</span><span>₹{{ cart.subtotal.toLocaleString('en-IN') }}</span></div>
              <div class="summary-row">
                <span>Shipping</span>
                <span :class="{ 'text-gold': cart.shipping === 0 }">{{ cart.shipping === 0 ? 'Free' : '₹' + cart.shipping }}</span>
              </div>
              <div v-if="cart.shipping > 0" class="free-shipping-notice">
                Add ₹{{ (999 - cart.subtotal).toLocaleString('en-IN') }} more for free shipping
              </div>
              <div class="summary-row summary-row--total">
                <span>Total</span><span>₹{{ cart.total.toLocaleString('en-IN') }}</span>
              </div>
            </div>
            <router-link to="/checkout" class="btn btn-gold w-full" @click="cart.open = false"><span>Proceed to Checkout</span></router-link>
            <button class="drawer__continue" @click="cart.open = false">Continue Shopping</button>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { getImageUrl } from '@/utils/image'
import { useCartStore } from '@/store/cart'
const cart = useCartStore()
// const primaryImage = p =>
//   p.images?.find(i => i.is_primary)?.url || p.images?.[0]?.url ||
//   'https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=200'
const primaryImage = (p) => {
  const img =
    p.images?.find(i => i.is_primary)?.url ||
    p.images?.[0]?.url

  return img
    ? getImageUrl(img)
    : 'https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=200'
}
</script>

<style scoped>
.drawer-overlay {
  position: fixed; inset: 0; background: rgba(42,31,26,0.4);
  backdrop-filter: blur(4px); z-index: 1000; display: flex; justify-content: flex-end;
}
.drawer {
  width: 100%; max-width: 420px; height: 100vh;
  background: var(--cream); border-left: 1px solid var(--blush);
  display: flex; flex-direction: column;
  box-shadow: -8px 0 40px rgba(196,135,106,0.12);
}
.drawer__head {
  display: flex; align-items: flex-start; justify-content: space-between;
  padding: 2rem 1.75rem 1.5rem; border-bottom: 1px solid var(--blush);
}
.drawer__head h3 {
  font-family: var(--font-serif); font-size: 1.35rem; font-weight: 300;
  color: var(--ink); margin-top: 0.25rem;
}
.drawer__close { color: var(--rose-gold-dim); font-size: 0.85rem; transition: color 0.2s; padding: 0.25rem; }
.drawer__close:hover { color: var(--rose-gold); }

.drawer__body { flex: 1; overflow-y: auto; padding: 1.5rem 1.75rem; }
.drawer__loading, .drawer__empty {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  height: 100%; gap: 1rem; text-align: center;
}
.empty-icon { font-size: 2.5rem; color: var(--blush-deep); animation: float 3s ease-in-out infinite; }
.drawer__empty p { color: var(--muted); font-size: 0.9rem; }

.cart-item {
  display: grid; grid-template-columns: 75px 1fr auto; gap: 0.85rem;
  align-items: start; padding: 1.1rem 0; border-bottom: 1px solid var(--blush-light);
}
.cart-item__img { width: 75px; height: 75px; overflow: hidden; background: var(--blush-light); }
.cart-item__img img { width: 100%; height: 100%; object-fit: cover; }
.cart-item__name {
  font-family: var(--font-serif); font-size: 0.95rem; font-weight: 400;
  color: var(--ink); line-height: 1.3; display: block; margin-bottom: 0.2rem;
}
.cart-item__cat { font-size: 0.6rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--rose-gold); margin-bottom: 0.6rem; }
.cart-item__foot { display: flex; align-items: center; justify-content: space-between; }
.qty-ctrl { display: flex; align-items: center; border: 1px solid var(--blush); }
.qty-ctrl button { width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; color: var(--rose-gold-dim); font-size: 1rem; transition: all 0.2s; }
.qty-ctrl button:hover { color: var(--rose-gold); background: var(--blush-light); }
.qty-ctrl span { width: 30px; text-align: center; font-size: 0.82rem; color: var(--ink); border-left: 1px solid var(--blush); border-right: 1px solid var(--blush); line-height: 26px; }
.cart-item__price { font-family: var(--font-serif); font-size: 0.95rem; color: var(--rose-gold); }
.cart-item__remove { color: var(--blush-mid); font-size: 0.65rem; transition: color 0.2s; padding: 0.2rem; }
.cart-item__remove:hover { color: #c0605a; }

.drawer__foot { border-top: 1px solid var(--blush); padding: 1.5rem 1.75rem; }
.drawer__summary { margin-bottom: 1.25rem; }
.summary-row { display: flex; justify-content: space-between; font-size: 0.82rem; color: var(--muted); padding: 0.35rem 0; }
.summary-row--total { font-family: var(--font-serif); font-size: 1.05rem; color: var(--ink); border-top: 1px solid var(--blush); margin-top: 0.5rem; padding-top: 0.75rem; }
.free-shipping-notice {
  font-size: 0.62rem; letter-spacing: 0.08em; color: var(--rose-gold-dim);
  text-align: center; padding: 0.4rem; border: 1px dashed var(--blush-mid); margin: 0.4rem 0;
}
.w-full { width: 100%; }
.drawer__continue {
  width: 100%; margin-top: 0.65rem; font-size: 0.65rem; letter-spacing: 0.15em;
  text-transform: uppercase; color: var(--rose-gold-dim); text-align: center; padding: 0.5rem; transition: color 0.2s;
}
.drawer__continue:hover { color: var(--rose-gold); }

.drawer-enter-active, .drawer-leave-active { transition: opacity 0.3s ease; }
.drawer-enter-from, .drawer-leave-to { opacity: 0; }
.drawer-enter-active .drawer, .drawer-leave-active .drawer { transition: transform 0.35s ease; }
.drawer-enter-from .drawer, .drawer-leave-to .drawer { transform: translateX(100%); }
.item-enter-active, .item-leave-active { transition: all 0.3s ease; }
.item-enter-from { opacity: 0; transform: translateX(20px); }
.item-leave-to   { opacity: 0; transform: translateX(-20px); }
</style>
