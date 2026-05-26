<template>
  <main class="admin-login">
    <div class="login-bg">
      <img src="https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=1800&q=90" alt="" />
      <div class="login-bg__overlay"></div>
    </div>

    <div class="login-card card-glass">
      <div class="login-card__top">
        <p class="label-caps" style="color:var(--dusty-rose)">✦ Glow With Ritz</p>
        <h1 class="login-card__title">Admin <em>Portal</em></h1>
        <p class="login-card__sub">Restricted access. Authorised personnel only.</p>
      </div>

      <div class="divider-gold"><span>✦</span></div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="field">
          <label class="input-label">Email Address</label>
          <input v-model="form.email" type="email" required class="input-field"
            placeholder="admin@glowwithritz.com" autocomplete="username" />
        </div>
        <div class="field">
          <label class="input-label">Password</label>
          <div class="pwd-wrap">
            <input v-model="form.password" :type="showPwd ? 'text' : 'password'"
              required class="input-field" placeholder="••••••••" autocomplete="current-password" />
            <button type="button" class="pwd-toggle" @click="showPwd = !showPwd">
              {{ showPwd ? '✕' : '○' }}
            </button>
          </div>
        </div>

        <div v-if="error" class="login-error">{{ error }}</div>

        <button type="submit" :disabled="loading" class="btn btn-gold w-full">
          <span>{{ loading ? 'Signing in…' : 'Enter Admin Panel' }}</span>
        </button>
      </form>

      <p class="login-footer">
        Consumer store →
        <a href="/" style="color:var(--rose-gold)">glowwithritz.com</a>
      </p>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminAuthStore } from '@/store/adminAuth'

const router    = useRouter()
const adminAuth = useAdminAuthStore()
const form      = ref({ email: '', password: '' })
const loading   = ref(false)
const error     = ref('')
const showPwd   = ref(false)

async function handleLogin() {
  error.value   = ''
  loading.value = true
  try {
    await adminAuth.login(form.value.email, form.value.password)
    router.push({ name: 'AdminDashboard' })
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Invalid credentials. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.admin-login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 2rem;
}
.login-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
}
.login-bg img {
  width: 100%; height: 100%;
  object-fit: cover;
  filter: brightness(0.35) saturate(0.6);
}
.login-bg__overlay {
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(42,31,26,0.7) 0%, rgba(90,64,56,0.4) 100%);
}

.login-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 440px;
  padding: 3rem 2.5rem;
  background: rgba(253,248,245,0.08);
  border: 1px solid rgba(196,135,106,0.25);
  backdrop-filter: blur(20px);
}

.login-card__top { text-align: center; margin-bottom: 1.5rem; }
.login-card__title {
  font-family: var(--font-serif);
  font-size: 2.2rem;
  font-weight: 300;
  color: var(--cream);
  margin: 0.4rem 0 0.6rem;
  letter-spacing: 0.02em;
}
.login-card__title em { font-style: italic; color: var(--rose-gold); }
.login-card__sub { font-size: 0.75rem; color: var(--light-muted); letter-spacing: 0.08em; }

.login-form { display: flex; flex-direction: column; gap: 1.2rem; margin-top: 1.5rem; }
.field { display: flex; flex-direction: column; gap: 0.4rem; }

.input-field {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(196,135,106,0.25);
  color: var(--cream);
}
.input-field::placeholder { color: rgba(196,168,152,0.4); }
.input-field:focus { border-color: var(--rose-gold); background: rgba(255,255,255,0.09); }

.pwd-wrap { position: relative; }
.pwd-wrap .input-field { padding-right: 2.5rem; }
.pwd-toggle {
  position: absolute; right: 0.9rem; top: 50%;
  transform: translateY(-50%);
  font-size: 0.7rem; color: var(--rose-gold-dim);
  transition: color 0.2s;
}
.pwd-toggle:hover { color: var(--rose-gold); }

.login-error {
  font-size: 0.75rem;
  color: #e07070;
  border: 1px solid rgba(224,112,112,0.25);
  padding: 0.6rem 0.9rem;
  letter-spacing: 0.04em;
}

.w-full { width: 100%; margin-top: 0.5rem; }

.login-footer {
  text-align: center;
  font-size: 0.68rem;
  color: var(--light-muted);
  margin-top: 1.5rem;
  letter-spacing: 0.06em;
}
</style>
