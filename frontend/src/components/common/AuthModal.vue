<template>
  <teleport to="body">
    <div class="modal-overlay" @click.self="$emit('close')">
      <div class="modal">
        <button class="modal__close" @click="$emit('close')">✕</button>
        <div class="modal__logo">
          <img src="/logo.png" alt="Glow With Ritz" class="modal__logo-img" />
        </div>
        <div class="modal__tabs">
          <button :class="{ active: tab === 'login' }" @click="tab = 'login'">Sign In</button>
          <button :class="{ active: tab === 'register' }" @click="tab = 'register'">Create Account</button>
        </div>

        <form v-if="tab === 'login'" @submit.prevent="doLogin" class="modal__form">
          <h2>Welcome Back</h2>
          <p class="modal__sub">Sign in to your Glow With Ritz account</p>
          <div class="field">
            <label class="input-label">Email</label>
            <input v-model="loginData.email" type="email" class="input-field" required placeholder="you@example.com" />
          </div>
          <div class="field">
            <label class="input-label">Password</label>
            <input v-model="loginData.password" type="password" class="input-field" required placeholder="••••••••" />
          </div>
          <p v-if="error" class="error-msg">{{ error }}</p>
          <button type="submit" class="btn btn-gold w-full" :disabled="loading"><span>{{ loading ? 'Signing In…' : 'Sign In' }}</span></button>
        </form>

        <form v-else @submit.prevent="doRegister" class="modal__form">
          <h2>Join the Circle</h2>
          <p class="modal__sub">Begin your crystal journey with Ritz</p>
          <div class="field">
            <label class="input-label">Full Name</label>
            <input v-model="regData.full_name" type="text" class="input-field" required placeholder="Your name" />
          </div>
          <div class="field">
            <label class="input-label">Email</label>
            <input v-model="regData.email" type="email" class="input-field" required placeholder="you@example.com" />
          </div>
          <div class="field">
            <label class="input-label">Phone (optional)</label>
            <input v-model="regData.phone" type="tel" class="input-field" placeholder="+91 00000 00000" />
          </div>
          <div class="field">
            <label class="input-label">Password</label>
            <input v-model="regData.password" type="password" class="input-field" required placeholder="Min. 8 characters" />
          </div>
          <p v-if="error" class="error-msg">{{ error }}</p>
          <button type="submit" class="btn btn-gold w-full" :disabled="loading"><span>{{ loading ? 'Creating Account…' : 'Create Account' }}</span></button>
        </form>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { toast } from 'vue3-toastify'
import { useAuthStore } from '@/store/auth'
import { useCartStore } from '@/store/cart'
import { useWishlistStore } from '@/store/wishlist'

const emit = defineEmits(['close'])
const auth = useAuthStore(); const cart = useCartStore(); const wishlist = useWishlistStore()
const tab = ref('login'); const loading = ref(false); const error = ref('')
const loginData = reactive({ email: '', password: '' })
const regData   = reactive({ full_name: '', email: '', password: '', phone: '' })

async function doLogin() {
  error.value = ''; loading.value = true
  try {
    await auth.login(loginData.email, loginData.password)
    cart.fetchCart(); wishlist.fetch()
    toast.success(`Welcome back, ${auth.user.full_name.split(' ')[0]}! ✦`)
    emit('close')
  } catch (e) { error.value = e.response?.data?.detail || 'Invalid credentials' }
  finally { loading.value = false }
}
async function doRegister() {
  error.value = ''; loading.value = true
  try {
    await auth.register(regData)
    cart.fetchCart()
    toast.success(`Welcome to Glow With Ritz, ${regData.full_name.split(' ')[0]}! ✦`)
    emit('close')
  } catch (e) { error.value = e.response?.data?.detail || 'Registration failed' }
  finally { loading.value = false }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0; background: rgba(42,31,26,0.5);
  backdrop-filter: blur(8px); z-index: 1100;
  display: flex; align-items: center; justify-content: center; padding: 1rem;
}
.modal {
  background: var(--cream); border: 1px solid var(--blush);
  box-shadow: 0 20px 60px rgba(196,135,106,0.2);
  width: 100%; max-width: 400px; padding: 2.5rem 2.5rem 2rem;
  position: relative; animation: fadeInUp 0.4s ease;
}
.modal__close { position: absolute; top: 1rem; right: 1rem; color: var(--rose-gold-dim); font-size: 0.8rem; transition: color 0.2s; }
.modal__close:hover { color: var(--rose-gold); }
.modal__logo { text-align: center; margin-bottom: 1.5rem; }
.modal__logo-img { height: 60px; width: auto; margin: 0 auto; }
.modal__tabs { display: flex; border-bottom: 1px solid var(--blush); margin-bottom: 1.75rem; }
.modal__tabs button {
  flex: 1; padding: 0.6rem; font-size: 0.65rem; font-weight: 500;
  letter-spacing: 0.15em; text-transform: uppercase; color: var(--muted);
  border-bottom: 2px solid transparent; transition: all 0.2s;
}
.modal__tabs button.active { color: var(--rose-gold); border-bottom-color: var(--rose-gold); }
.modal__form h2 { font-family: var(--font-serif); font-size: 1.7rem; font-weight: 300; color: var(--ink); margin-bottom: 0.2rem; }
.modal__sub { font-size: 0.78rem; color: var(--muted); margin-bottom: 1.75rem; }
.field { margin-bottom: 1rem; }
.error-msg { font-size: 0.76rem; color: #b05050; padding: 0.6rem; background: rgba(176,80,80,0.06); border: 1px solid rgba(176,80,80,0.2); margin-bottom: 1rem; }
.w-full { width: 100%; }
</style>
