<template>
  <main class="checkout-page">
    <div style="height: var(--nav-h)"></div>

    <div class="container checkout-layout">
      <!-- Left: Form -->
      <div class="checkout-form">
        <div class="checkout-header">
          <router-link to="/" class="checkout-logo">✦ Crystal Luxe</router-link>
          <div class="checkout-steps">
            <span :class="['step', { active: step >= 1, done: step > 1 }]">Address</span>
            <span class="step-line"></span>
            <span :class="['step', { active: step >= 2, done: step > 2 }]">Review</span>
            <span class="step-line"></span>
            <span :class="['step', { active: step >= 3 }]">Payment</span>
          </div>
        </div>

        <!-- Step 1: Shipping -->
        <div v-if="step === 1" class="form-section">
          <h2>Shipping Address</h2>
          <div class="form-grid">
            <div class="field span-2">
              <label class="input-label">Full Name</label>
              <input v-model="address.full_name" class="input-field" required />
            </div>
            <div class="field">
              <label class="input-label">Email</label>
              <input v-model="address.email" type="email" class="input-field" />
            </div>
            <div class="field">
              <label class="input-label">Phone</label>
              <input v-model="address.phone" type="tel" class="input-field" required />
            </div>
            <div class="field span-2">
              <label class="input-label">Address Line 1</label>
              <input v-model="address.line1" class="input-field" required placeholder="House / Flat / Street" />
            </div>
            <div class="field span-2">
              <label class="input-label">Address Line 2 (optional)</label>
              <input v-model="address.line2" class="input-field" placeholder="Area / Landmark" />
            </div>
            <div class="field">
              <label class="input-label">City</label>
              <input v-model="address.city" class="input-field" required />
            </div>
            <div class="field">
              <label class="input-label">State</label>
              <input v-model="address.state" class="input-field" required />
            </div>
            <div class="field">
              <label class="input-label">PIN Code</label>
              <input v-model="address.pincode" class="input-field" required maxlength="6" />
            </div>
            <div class="field">
              <label class="input-label">Country</label>
              <input v-model="address.country" class="input-field" />
            </div>
          </div>
          <button class="btn btn-gold step-btn" @click="step = 2"><span>Continue to Review</span></button>
        </div>

        <!-- Step 2: Review -->
        <div v-if="step === 2" class="form-section">
          <h2>Review Your Order</h2>
          <div class="review-items">
            <div v-for="item in cart.items" :key="item.id" class="review-item">
              <img :src="primaryImage(item.product)" :alt="item.product.name" />
              <div class="review-item__info">
                <p class="review-item__name">{{ item.product.name }}</p>
                <p class="review-item__cat">{{ item.product.category?.name }}</p>
                <p class="review-item__qty">Qty: {{ item.quantity }}</p>
              </div>
              <p class="review-item__price">₹{{ (item.product.price * item.quantity).toLocaleString('en-IN') }}</p>
            </div>
          </div>
          <div class="address-review">
            <p class="label-caps" style="margin-bottom:0.5rem">Delivering to</p>
            <p>{{ address.full_name }}</p>
            <p>{{ address.line1 }}<span v-if="address.line2">, {{ address.line2 }}</span></p>
            <p>{{ address.city }}, {{ address.state }} — {{ address.pincode }}</p>
            <p>{{ address.phone }}</p>
          </div>
          <div class="step-buttons">
            <button class="btn btn-ghost" @click="step = 1"><span>← Edit Address</span></button>
            <button class="btn btn-gold" @click="step = 3"><span>Proceed to Payment</span></button>
          </div>
        </div>

        <!-- Step 3: Payment -->
        <div v-if="step === 3" class="form-section">
          <h2>Payment</h2>
          <div class="payment-methods">
            <label v-for="m in paymentMethods" :key="m.value" :class="['payment-method', { selected: paymentMethod === m.value }]">
              <input type="radio" :value="m.value" v-model="paymentMethod" name="payment" />
              <span class="payment-icon">{{ m.icon }}</span>
              <div>
                <span class="payment-name">{{ m.name }}</span>
                <span class="payment-sub">{{ m.sub }}</span>
              </div>
            </label>
          </div>
          <div class="field" style="margin-top:1.5rem">
            <label class="input-label">Order Notes (optional)</label>
            <textarea v-model="notes" class="input-field" rows="3" placeholder="Any special instructions for your order…"></textarea>
          </div>
          <div class="step-buttons">
            <button class="btn btn-ghost" @click="step = 2"><span>← Back</span></button>
            <button class="btn btn-gold" @click="placeOrder" :disabled="placing">
              <span>{{ placing ? 'Placing Order…' : 'Place Order' }}</span>
            </button>
          </div>
        </div>

        <!-- Step 4: Success -->
        <div v-if="step === 4" class="success-panel">
          <div class="success-icon">✦</div>
          <h2>Order Placed!</h2>
          <p>Your order <strong>{{ placedOrderNumber }}</strong> has been received.</p>
          <p style="margin-top:0.5rem;opacity:0.6;font-size:0.85rem">
            We'll send you a confirmation and dispatch details shortly.
          </p>
          <div class="success-actions">
            <router-link to="/account/orders" class="btn btn-gold"><span>Track My Order</span></router-link>
            <router-link to="/shop" class="btn btn-ghost"><span>Continue Shopping</span></router-link>
          </div>
        </div>
      </div>

      <!-- Right: Summary -->
      <div class="checkout-summary" v-if="step < 4">
        <h3>Order Summary</h3>
        <div class="summary-items">
          <div v-for="item in cart.items" :key="item.id" class="summary-item">
            <div class="summary-item__img">
              <img :src="primaryImage(item.product)" :alt="item.product.name" />
              <span class="summary-item__qty">{{ item.quantity }}</span>
            </div>
            <div class="summary-item__info">
              <p>{{ item.product.name }}</p>
              <p class="summary-item__price">₹{{ (item.product.price * item.quantity).toLocaleString('en-IN') }}</p>
            </div>
          </div>
        </div>
        <div class="summary-totals">
          <div class="summary-row">
            <span>Subtotal</span>
            <span>₹{{ cart.subtotal.toLocaleString('en-IN') }}</span>
          </div>
          <div class="summary-row">
            <span>Shipping</span>
            <span :class="{ 'text-gold': cart.shipping === 0 }">
              {{ cart.shipping === 0 ? 'Free' : '₹' + cart.shipping }}
            </span>
          </div>
          <div class="summary-row summary-row--total">
            <span>Total</span>
            <span>₹{{ cart.total.toLocaleString('en-IN') }}</span>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify'
import { useCartStore } from '@/store/cart'
import { useAuthStore } from '@/store/auth'
import { orderApi } from '@/api'

const cart = useCartStore()
const auth = useAuthStore()
const router = useRouter()

const step = ref(1)
const placing = ref(false)
const paymentMethod = ref('cod')
const notes = ref('')
const placedOrderNumber = ref('')

const address = reactive({
  full_name: auth.user?.full_name || '',
  email: auth.user?.email || '',
  phone: auth.user?.phone || '',
  line1: '', line2: '', city: '', state: '', pincode: '', country: 'India'
})

const paymentMethods = [
  { value: 'cod',      icon: '💵', name: 'Cash on Delivery', sub: 'Pay when you receive your order' },
  { value: 'razorpay', icon: '💳', name: 'Online Payment',   sub: 'UPI, Cards, Net Banking via Razorpay' },
  { value: 'upi',      icon: '📱', name: 'UPI',              sub: 'Google Pay, PhonePe, Paytm' },
]

const primaryImage = p =>
  p.images?.find(i => i.is_primary)?.url || p.images?.[0]?.url ||
  'https://images.unsplash.com/photo-1599707367072-cd6ada2bc375?w=200'

// async function placeOrder() {
//   if (!cart.items.length) { toast.error('Your cart is empty'); return }
//   placing.value = true
//   try {
//     const { data } = await orderApi.place({
//       shipping_name: address.full_name,
//       shipping_phone: address.phone,
//       shipping_line1: address.line1,
//       shipping_line2: address.line2,
//       shipping_city: address.city,
//       shipping_state: address.state,
//       shipping_pincode: address.pincode,
//       shipping_country: address.country,
//       payment_method: paymentMethod.value,
//       notes: notes.value
//     })
//     placedOrderNumber.value = data.order_number
//     step.value = 4
//     toast.success('Order placed successfully!')
//     await cart.fetchCart()
//   } catch (e) {
//     toast.error(e.response?.data?.detail || 'Failed to place order')
//   } finally { placing.value = false }
// }

async function placeOrder() {
  if (!auth.token) {
    toast.error('Session expired. Please login again.')
    auth.logout()
    router.push('/?login=1')
    return
  }

  if (!cart.items.length) {
    toast.error('Your cart is empty')
    return
  }

  placing.value = true

  try {
    const { data } = await orderApi.place({
      shipping_name: address.full_name,
      shipping_phone: address.phone,
      shipping_line1: address.line1,
      shipping_line2: address.line2,
      shipping_city: address.city,
      shipping_state: address.state,
      shipping_pincode: address.pincode,
      shipping_country: address.country,
      payment_method: paymentMethod.value,
      notes: notes.value
    })

    placedOrderNumber.value = data.order_number
    step.value = 4
    toast.success('Order placed successfully!')
    await cart.fetchCart()

  } catch (e) {
    toast.error(e.response?.data?.detail || 'Failed to place order')
  } finally {
    placing.value = false
  }
}
</script>

<style scoped>
.checkout-page { min-height: 100vh; background: var(--black); }
.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 4rem;
  padding-top: 3rem;
  padding-bottom: 5rem;
  align-items: start;
}
.checkout-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 2.5rem; padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(201,168,76,0.12);
}
.checkout-logo {
  font-family: var(--font-serif); font-size: 1.2rem;
  letter-spacing: 0.1em; color: var(--gold);
}
.checkout-steps { display: flex; align-items: center; gap: 0.5rem; }
.step {
  font-size: 0.62rem; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--ivory-dim); opacity: 0.3;
  transition: all 0.3s;
}
.step.active { color: var(--gold); opacity: 1; }
.step.done { color: var(--gold-dim); opacity: 0.7; }
.step-line { width: 20px; height: 1px; background: rgba(201,168,76,0.2); }

.form-section h2 {
  font-family: var(--font-serif); font-size: 1.8rem; font-weight: 300;
  color: var(--ivory); margin-bottom: 1.75rem;
}
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem; }
.field { display: flex; flex-direction: column; }
.span-2 { grid-column: 1 / -1; }

.review-items { margin-bottom: 1.5rem; }
.review-item {
  display: flex; align-items: center; gap: 1rem;
  padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.review-item img { width: 60px; height: 60px; object-fit: cover; background: var(--charcoal); }
.review-item__info { flex: 1; }
.review-item__name { font-family: var(--font-serif); font-size: 0.95rem; color: var(--ivory); }
/* .review-item__cat { font-size: 0.62rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--gold-dim); } */
/* .review-item__qty { font-size: 0.75rem; color: var(--ivory-dim); opacity: 0.5; margin-top: 0.2rem; } */
.review-item__qty {
  font-size: 0.75rem;
  color: rgba(255,248,240,0.75);   /* readable */
  margin-top: 0.2rem;
}

.review-item__cat {
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(201,168,76,0.85);   /* brighter gold */
}
.review-item__price { font-family: var(--font-serif); color: var(--gold); }

/* .address-review {
  padding: 1.25rem; background: var(--charcoal);
  border: 1px solid rgba(201,168,76,0.1);
  font-size: 0.85rem; color: var(--ivory-dim);
  line-height: 1.7; margin-bottom: 1.5rem;
} */

.address-review {
  padding: 1.25rem;

  background: rgba(40, 34, 30, 0.95);   /* softer, less dead */
  border: 1px solid rgba(201,168,76,0.2);

  font-size: 0.9rem;
  color: rgba(255,248,240,0.9);         /* 🔥 readable */

  line-height: 1.75;
  margin-bottom: 1.5rem;
}

.payment-methods { display: flex; flex-direction: column; gap: 0.75rem; }
.payment-method {
  display: flex; align-items: center; gap: 1rem;
  padding: 1rem 1.25rem;
  border: 1px solid rgba(201,168,76,0.15);
  cursor: pointer; transition: border-color 0.2s;
}
.payment-method.selected { border-color: var(--gold); }
.payment-method input { accent-color: var(--gold); }
.payment-icon { font-size: 1.4rem; }
.payment-name { display: block; font-size: 0.85rem; color: var(--ivory); }
/* .payment-sub { font-size: 0.68rem; color: var(--ivory-dim); opacity: 0.45; } */

.payment-sub {
  font-size: 0.7rem;
  color: rgba(255,248,240,0.7);   /* readable */
}

.step-btn, .step-buttons .btn { min-width: 200px; }
.step-buttons { display: flex; gap: 1rem; margin-top: 2rem; }

/* Summary */
/* .checkout-summary {
  position: sticky; top: calc(var(--nav-h) + 2rem);
  background: var(--charcoal);
  border: 1px solid rgba(201,168,76,0.12);
  padding: 2rem;
} */

.checkout-summary {
  position: sticky;
  top: calc(var(--nav-h) + 2rem);

  background: linear-gradient(
    180deg,
    rgba(71, 59, 50, 0.96),
    rgba(104, 80, 60, 0.98)
  );

  border: 1px solid rgba(201,168,76,0.22);
  padding: 2rem;

  box-shadow: 0 10px 40px rgba(0,0,0,0.35); /* depth = readability */
}

.checkout-summary h3 {
  font-family: var(--font-serif); font-size: 1.2rem; font-weight: 300;
  /* color: var(--ivory); margin-bottom: 1.5rem; */
  color: var(--gold); margin-bottom: 1.5rem;
  /* padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.06); */
  padding-bottom: 1rem; border-bottom: 1px solid rgba(201,168,76,0.15);
}
.summary-items { margin-bottom: 1.5rem; }
/* .summary-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.75rem 0; border-bottom: 1px solid rgba(255,255,255,0.04);
} */
.summary-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.9rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
.summary-item__img { position: relative; flex-shrink: 0; }
.summary-item__img img { width: 56px; height: 56px; object-fit: cover; background: var(--warm-dark); }
.summary-item__qty {
  position: absolute; top: -6px; right: -6px;
  width: 18px; height: 18px; border-radius: 50%;
  background: var(--gold); color: var(--black);
  font-size: 0.55rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
/* .summary-item__info p:first-child { font-size: 0.82rem; color: var(--ivory); line-height: 1.3; }
.summary-item__price { font-size: 0.82rem; color: var(--gold-dim); margin-top: 0.2rem; } */
.summary-item__info p:first-child {
  font-size: 0.88rem;
  color: #ffffff;                 /* 🔥 pure white */
  line-height: 1.45;
  font-weight: 500;
}

.summary-item__price {
  font-size: 0.85rem;
  color: #e6c27a;   /* brighter gold */
}

/* .summary-totals { border-top: 1px solid rgba(201,168,76,0.12); padding-top: 1rem; } */
.summary-totals { border-top: 1px solid rgba(201,168,76,0.15); padding-top: 1rem; }
/* .summary-row { display: flex; justify-content: space-between; font-size: 0.82rem; color: var(--ivory-dim); padding: 0.35rem 0; } */
.summary-row {
  display: flex;
  justify-content: space-between;

  font-size: 0.85rem;
  color: rgba(255,255,255,0.92);   /* readable */

  padding: 0.4rem 0;
}
/* .summary-row--total {
  border-top: 1px solid rgba(255,255,255,0.08); margin-top: 0.5rem; padding-top: 0.75rem;
  font-family: var(--font-serif); font-size: 1.1rem; color: var(--ivory);
} */

.summary-row--total {
  border-top: 1px solid rgba(255,255,255,0.12);
  margin-top: 0.6rem;
  padding-top: 0.9rem;

  font-size: 1.15rem;
}

.summary-row--total span:last-child {
  color: #e6c27a;   /* gold highlight */
  font-weight: 600;
}

.summary-row span:first-child {
  color: rgba(255,255,255,0.75);  /* label */
}

.summary-row span:last-child {
  color: #ffffff;                /* value */
  font-weight: 500;
}

/* Success */
.success-panel {
  display: flex; flex-direction: column; align-items: center;
  text-align: center; padding: 3rem 0;
}
.success-icon { font-size: 3rem; color: var(--gold); margin-bottom: 1.5rem; animation: pulse-gold 2s ease-in-out infinite; }
.success-panel h2 { font-family: var(--font-serif); font-size: 2.5rem; font-weight: 300; color: var(--ivory); margin-bottom: 0.75rem; }
.success-panel p { color: var(--ivory-dim); }
.success-panel strong { color: var(--gold); }
.success-actions { display: flex; gap: 1rem; margin-top: 2rem; flex-wrap: wrap; justify-content: center; }

@media (max-width: 900px) {
  .checkout-layout { grid-template-columns: 1fr; }
  .checkout-summary { position: static; }
  .form-grid { grid-template-columns: 1fr; }
  .span-2 { grid-column: auto; }
}
</style>
