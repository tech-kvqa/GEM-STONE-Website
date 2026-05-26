<template>
  <header :class="['navbar', { 'navbar--scrolled': scrolled, 'navbar--hidden': hidden }]">
    <div class="navbar__inner">

      <!-- Left Nav -->
      <nav class="navbar__links">
        <router-link to="/shop" class="nav-link">Collections</router-link>

        <!-- Crystals mega -->
        <div class="nav-mega" @mouseenter="megaOpen = 'crystals'" @mouseleave="megaOpen = null">
          <span class="nav-link nav-link--has-arrow">Crystals <span class="nav-arrow">›</span></span>
          <div :class="['mega-panel', { 'mega-panel--open': megaOpen === 'crystals' }]">
            <div class="mega-grid">
              <router-link
                v-for="cat in categories" :key="cat.slug"
                :to="`/shop/${cat.slug}`"
                class="mega-item" @click="megaOpen = null"
              >
                <div class="mega-item__img">
                  <img :src="cat.image_url" :alt="cat.name" loading="lazy" />
                </div>
                <span class="mega-item__name">{{ cat.name }}</span>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Premium Collection mega — NEW -->
        <div class="nav-mega" @mouseenter="megaOpen = 'premium'" @mouseleave="megaOpen = null">
          <span class="nav-link nav-link--premium nav-link--has-arrow">
            Premium Collection <span class="nav-arrow">›</span>
          </span>
          <div :class="['mega-panel mega-panel--premium', { 'mega-panel--open': megaOpen === 'premium' }]">
            <div class="premium-grid">
              <div v-for="col in premiumCollections" :key="col.label" class="premium-col">
                <div class="premium-col__header">
                  <span class="premium-col__icon">{{ col.icon }}</span>
                  <h4 class="premium-col__title">{{ col.label }}</h4>
                </div>
                <p class="premium-col__desc">{{ col.desc }}</p>
                <div class="premium-col__items">
                  <router-link
                    v-for="item in col.items" :key="item.name"
                    :to="item.to"
                    class="premium-item"
                    @click="megaOpen = null"
                  >
                    <span class="premium-item__dot" :style="{ background: item.color }"></span>
                    <span>{{ item.name }}</span>
                  </router-link>
                </div>
              </div>
            </div>
            <div class="premium-footer">
              <router-link to="/consultation" class="premium-consult-cta" @click="megaOpen = null">
                ✦ Book a Free Crystal Consultation — Find Your Perfect Stone
              </router-link>
            </div>
          </div>
        </div>

        <router-link to="/consultation" class="nav-link nav-link--consult">Consultation</router-link>
        <router-link to="/our-story" class="nav-link">Our Story</router-link>
        <router-link to="/crystal-guide" class="nav-link">Crystal Guide</router-link>
      </nav>

      <!-- Logo -->
      <router-link to="/" class="navbar__logo">
        <div class="logo-wrapper">
          <img src="/logo.png" alt="Glow With Ritz" class="logo-img" />
        </div>
      </router-link>

      <!-- Right Actions -->
      <div class="navbar__actions">
        <button class="action-btn" @click="openSearch" title="Search">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        </button>
        <button class="action-btn" @click="handleAccount" title="Account">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </button>
        <router-link v-if="auth.isLoggedIn" to="/wishlist" class="action-btn" title="Wishlist">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          <span v-if="wishlist.count" class="action-badge">{{ wishlist.count }}</span>
        </router-link>
        <button class="action-btn" @click="cart.toggleCart()" title="Cart">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
          <span v-if="cart.count" class="action-badge">{{ cart.count }}</span>
        </button>
        <button class="mobile-menu-btn" @click="mobileOpen = !mobileOpen">
          <span :class="['hamburger', { open: mobileOpen }]"></span>
        </button>
      </div>
    </div>

    <!-- Search Bar -->
    <div :class="['search-bar', { 'search-bar--open': searchOpen }]">
      <div class="search-bar__inner">
        <input
          ref="searchInput"
          v-model="searchQuery"
          type="text"
          placeholder="Search crystals by name, chakra, or intention…"
          @keyup.enter="doSearch"
          @keyup.escape="searchOpen = false"
        />
        <button class="search-bar__close" @click="searchOpen = false">✕</button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div :class="['mobile-menu', { 'mobile-menu--open': mobileOpen }]">
      <router-link to="/" @click="mobileOpen = false">Home</router-link>
      <router-link to="/shop" @click="mobileOpen = false">All Crystals</router-link>
      <router-link v-for="cat in categories" :key="cat.slug" :to="`/shop/${cat.slug}`" @click="mobileOpen = false">{{ cat.name }}</router-link>
      <div class="mobile-divider-label">Premium Collection</div>
      <router-link to="/shop/jewellery" @click="mobileOpen = false">Jewellery Designs</router-link>
      <router-link to="/shop/crystal-designs" @click="mobileOpen = false">Crystal Designs</router-link>
      <!-- <router-link to="/shop/lab-diamonds" @click="mobileOpen = false">Lab Diamonds</router-link> -->
      <div class="mobile-menu__divider"></div>
      <router-link to="/consultation" @click="mobileOpen = false" class="mobile-consult-link">✦ Book Consultation</router-link>
      <router-link to="/our-story" @click="mobileOpen = false">Our Story</router-link>
      <router-link to="/crystal-guide" @click="mobileOpen = false">Crystal Guide</router-link>
      <div class="mobile-menu__divider"></div>
      <button v-if="!auth.isLoggedIn" @click="handleAccount">Sign In / Register</button>
      <router-link v-else to="/account" @click="mobileOpen = false">My Account</router-link>
      <router-link v-if="auth.isLoggedIn" to="/wishlist" @click="mobileOpen = false">Wishlist</router-link>
    </div>
  </header>

  <AuthModal v-if="authModalOpen" @close="authModalOpen = false" />
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useCartStore } from '@/store/cart'
import { useWishlistStore } from '@/store/wishlist'
import { categoryApi } from '@/api'
import AuthModal from '@/components/common/AuthModal.vue'

const auth = useAuthStore()
const cart = useCartStore()
const wishlist = useWishlistStore()
const router = useRouter()

const scrolled    = ref(false)
const hidden      = ref(false)
const megaOpen    = ref(null)
const mobileOpen  = ref(false)
const searchOpen  = ref(false)
const searchQuery = ref('')
const searchInput = ref(null)
const authModalOpen = ref(false)
const categories  = ref([])
let lastY = 0

const premiumCollections = [
  {
    icon: '💍',
    label: 'Jewellery Designs',
    desc: 'Wearable crystal energy — hand-crafted into elegant pieces.',
    items: [
      { name: 'Crystal Pendants',    to: '/shop/jewellery', color: '#c4876a' },
      { name: 'Chakra Bracelets',    to: '/shop/jewellery', color: '#9b72cf' },
      { name: 'Crystal Rings',       to: '/shop/jewellery', color: '#e07b54' },
      { name: 'Healing Necklaces',   to: '/shop/jewellery', color: '#6dba82' },
    ]
  },
  {
    icon: '🔮',
    label: 'Crystal Designs',
    desc: 'Sacred forms and bespoke crystal artistry for your space.',
    items: [
      { name: 'Crystal Spheres',     to: '/shop/crystal-designs', color: '#5b9dd4' },
      { name: 'Crystal Towers',      to: '/shop/crystal-designs', color: '#c0392b' },
      { name: 'Geometric Sets',      to: '/shop/crystal-designs', color: '#e8b84b' },
      { name: 'Altar Pieces',        to: '/shop/crystal-designs', color: '#c4876a' },
    ]
  },
  // {
  //   icon: '✦',
  //   label: 'Lab Diamonds',
  //   desc: 'Ethically created, optically perfect — brilliance without compromise.',
  //   items: [
  //     { name: 'Loose Lab Diamonds',  to: '/shop/lab-diamonds', color: '#c8a8d8' },
  //     { name: 'Diamond Pendants',    to: '/shop/lab-diamonds', color: '#5b9dd4' },
  //     { name: 'Diamond Rings',       to: '/shop/lab-diamonds', color: '#e8b84b' },
  //     { name: 'Custom Jewellery',    to: '/shop/lab-diamonds', color: '#c4876a' },
  //   ]
  // }
]

async function openSearch() {
  searchOpen.value = true
  await nextTick()
  searchInput.value?.focus()
}
function doSearch() {
  if (searchQuery.value.trim()) {
    router.push({ name: 'Shop', query: { search: searchQuery.value.trim() } })
    searchOpen.value = false
    searchQuery.value = ''
  }
}
function handleAccount() {
  mobileOpen.value = false
  if (auth.isLoggedIn) router.push('/account')
  else authModalOpen.value = true
}
function onScroll() {
  const y = window.scrollY
  scrolled.value = y > 50
  hidden.value   = y > lastY && y > 300
  lastY = y
}
onMounted(async () => {
  window.addEventListener('scroll', onScroll, { passive: true })
  const { data } = await categoryApi.list()
  categories.value = data
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.navbar {
  position: fixed; top: 0; left: 0; right: 0;
  z-index: 900;
  transition: transform 0.4s ease, background 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
  border-bottom: 1px solid transparent;
}
.navbar--scrolled {
  background: rgba(253, 248, 245, 0.97);
  backdrop-filter: blur(20px);
  border-bottom-color: var(--blush);
  box-shadow: 0 2px 20px rgba(196, 135, 106, 0.08);
}
.navbar--hidden { transform: translateY(-100%); }

.navbar__inner {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  height: var(--nav-h);
  padding: 0 2rem;
  max-width: var(--max-w);
  margin: 0 auto;
}

/* ── Logo — FIX #10: blend mode removes white bg ── */
.navbar__logo { display: flex; align-items: center; justify-content: center; }
.logo-wrapper {
  background: transparent;
  display: flex; align-items: center;
}
.logo-img {
  height: 58px; width: auto; object-fit: contain;
  mix-blend-mode: multiply;         /* blends white bg away on cream navbar */
  transition: transform 0.3s var(--ease-silk);
}
.navbar--scrolled .logo-img { /* already on cream bg, multiply works perfectly */ }
.navbar__logo:hover .logo-img { transform: scale(1.04); }

/* ── Nav links ── */
.navbar__links { display: flex; align-items: center; gap: 1.8rem; }
.nav-link {
  font-size: 0.62rem; font-weight: 500; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--warm-brown);
  transition: color 0.2s; cursor: pointer; white-space: nowrap;
}
.nav-link:hover, .router-link-active.nav-link { color: var(--rose-gold); }
.nav-link--has-arrow .nav-arrow { display: inline-block; transition: transform 0.2s; }
.nav-mega:hover .nav-link--has-arrow .nav-arrow { transform: rotate(90deg); }

/* Extra hover safety for premium dropdown */
.nav-mega::before {
  content: '';
  position: absolute;
  top: 100%;
  left: -60px;
  right: -60px;
  height: 50px;
}

/* Premium nav link — golden accent */
.nav-link--premium {
  color: var(--rose-gold);
  padding: 0.25rem 0.6rem;
  border: 1px solid var(--blush-mid);
  background: var(--blush-light);
}
.nav-link--premium:hover { background: var(--rose-gold); color: #fff; border-color: var(--rose-gold); }

/* Consultation — stands out */
.nav-link--consult {
  color: var(--rose-gold-deep);
  font-weight: 600;
}
.nav-link--consult:hover { color: var(--rose-gold); }

/* ── Mega menu ── */
/* .nav-mega { position: relative; }
.mega-panel {
  position: absolute; top: calc(100% + 1.5rem);
  left: 50%; transform: translateX(-50%) translateY(-8px);
  width: 680px; background: rgba(253,248,245,0.98);
  border: 1px solid var(--blush); backdrop-filter: blur(20px);
  box-shadow: 0 20px 60px rgba(196,135,106,0.12);
  padding: 2rem; opacity: 0; pointer-events: none;
  transition: opacity 0.3s ease, transform 0.3s ease;
} */
/* .mega-panel--open { opacity: 1; pointer-events: all; 
  transform: translateX(-50%) translateY(0); 
  transform: translateY(0);
} */
/* .mega-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.mega-item { display: flex; flex-direction: column; gap: 0.5rem; cursor: pointer; transition: opacity 0.2s; }
.mega-item:hover { opacity: 0.75; }
.mega-item__img { aspect-ratio: 1; overflow: hidden; background: var(--blush-light); }
.mega-item__img img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.mega-item:hover .mega-item__img img { transform: scale(1.08); }
.mega-item__name { font-size: 0.6rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--warm-brown); } */

/* ── Premium Collection mega panel ── */
/* .mega-panel--premium { width: 860px; left: 0; transform: translateX(0) translateY(-8px); }
.mega-panel--premium.mega-panel--open { transform: translateX(0) translateY(0); } */

/* ── Mega menu UX FIX ───────────────────────────────────────────── */

/* Larger hover bridge so dropdown doesn't vanish while moving cursor */
.nav-mega {
  position: relative;
  /* padding-bottom: 2.5rem;
  margin-bottom: -2.5rem; */
}

/* Invisible hover-safe corridor */
.nav-mega::after {
  content: '';
  position: absolute;
  top: 100%;
  left: -40px;
  right: -40px;
  height: 45px;
}

/* Base panel */
.mega-panel {
  position: absolute;
  top: calc(100% + 1rem);

  /* Better screen fit */
  left: clamp(-140px, -10vw, -30px);

  width: min(92vw, 820px);
  max-width: 820px;

  background: rgba(253,248,245,0.985);
  border: 1px solid var(--blush);
  backdrop-filter: blur(22px);
  box-shadow: 0 20px 60px rgba(196,135,106,0.14);

  padding: 2rem;

  opacity: 0;
  visibility: hidden;
  pointer-events: none;

  transform: translateY(-8px);
  transition:
    opacity 0.28s ease,
    transform 0.28s ease,
    visibility 0.28s ease;
}

/* Open state */
.mega-panel--open {
  opacity: 1;
  visibility: visible;
  pointer-events: all;
  transform: translateY(0);
}

/* Grid fix for full desktop visibility */
.mega-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 1rem;
}

/* Item card */
.mega-item {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  cursor: pointer;
  transition: transform 0.25s ease, opacity 0.25s ease;
}

.mega-item:hover {
  opacity: 0.88;
  transform: translateY(-3px);
}

.mega-item__img {
  aspect-ratio: 1;
  max-height: 130px;
  overflow: hidden;
  background: var(--blush-light);
  border: 1px solid rgba(196,135,106,0.08);
}

.mega-item__img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.mega-item:hover .mega-item__img img {
  transform: scale(1.06);
}

.mega-item__name {
  font-size: 0.62rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--warm-brown);
}

/* ── Premium Collection ─────────────────────────────────────────── */

/* .mega-panel--premium {
  width: min(95vw, 1100px);
  max-width: 1100px;

  left: 50%;
  transform: translateX(-50%) translateY(-8px);
  transform: translateY(-8px);
}

.mega-panel--premium.mega-panel--open {
  transform: translateX(-50%) translateY(0);
} */

/* ── Premium Collection UX FIX ─────────────────────────────────── */
.mega-panel--premium {
  width: min(95vw, 1100px);
  max-width: 1100px;

  left: 50%;
  transform: translateX(-50%) translateY(-8px);

  opacity: 0;
  visibility: hidden;
  pointer-events: none;

  transition:
    opacity 0.28s ease,
    transform 0.28s ease,
    visibility 0.28s ease;
}

.mega-panel--premium.mega-panel--open {
  opacity: 1;
  visibility: visible;
  pointer-events: all;
  transform: translateX(-30%) translateY(0);
}
/* .premium-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 1.25rem; } */
.premium-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.25rem;
}
.premium-col { padding: 1rem; border: 1px solid var(--blush); background: var(--cream); }
.premium-col__header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }
.premium-col__icon { font-size: 1.2rem; }
.premium-col__title { font-family: var(--font-serif); font-size: 1rem; font-weight: 400; color: var(--ink); }
.premium-col__desc { font-size: 0.7rem; color: var(--muted); line-height: 1.5; margin-bottom: 0.85rem; }
.premium-col__items { display: flex; flex-direction: column; gap: 0.4rem; }
.premium-item {
  display: flex; align-items: center; gap: 0.5rem;
  font-size: 0.72rem; color: var(--warm-brown); transition: color 0.2s, padding-left 0.2s;
}
.premium-item:hover { color: var(--rose-gold); padding-left: 4px; }
.premium-item__dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.premium-footer { border-top: 1px solid var(--blush); padding-top: 1rem; text-align: center; }
.premium-consult-cta {
  font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase;
  color: var(--rose-gold); transition: color 0.2s;
}
.premium-consult-cta:hover { color: var(--rose-gold-deep); }

/* ── Actions ── */
.navbar__actions { display: flex; align-items: center; justify-content: flex-end; gap: 1.1rem; }
.action-btn { position: relative; color: var(--warm-brown); transition: color 0.2s; display: flex; align-items: center; }
.action-btn:hover { color: var(--rose-gold); }
.action-badge {
  position: absolute; top: -6px; right: -8px;
  background: var(--rose-gold); color: #fff;
  font-size: 0.52rem; font-weight: 700;
  width: 15px; height: 15px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}

/* ── Search Bar ── */
.search-bar {
  position: absolute; top: 100%; left: 0; right: 0;
  background: rgba(253,248,245,0.99);
  border-bottom: 1px solid var(--blush);
  padding: 1.25rem 2.5rem;
  transform: translateY(-100%); opacity: 0; pointer-events: none;
  transition: transform 0.35s ease, opacity 0.35s ease;
  box-shadow: 0 8px 30px rgba(196,135,106,0.08);
}
.search-bar--open { transform: translateY(0); opacity: 1; pointer-events: all; }
.search-bar__inner {
  max-width: 600px; margin: 0 auto;
  display: flex; align-items: center; gap: 1rem;
  border-bottom: 1px solid var(--blush-mid); padding-bottom: 0.75rem;
}
.search-bar__inner input {
  flex: 1; background: none; border: none; outline: none;
  color: var(--ink); font-family: var(--font-serif); font-size: 1.15rem; font-weight: 300;
}
.search-bar__inner input::placeholder { color: var(--light-muted); }
.search-bar__close { color: var(--rose-gold-dim); font-size: 0.9rem; transition: color 0.2s; }
.search-bar__close:hover { color: var(--rose-gold); }

/* ── Mobile ── */
.mobile-menu-btn { display: none; }
.hamburger { display: block; width: 22px; height: 1.5px; background: var(--warm-brown); position: relative; transition: background 0.2s; }
.hamburger::before, .hamburger::after {
  content: ''; position: absolute; left: 0;
  width: 100%; height: 1.5px; background: var(--warm-brown); transition: transform 0.3s ease;
}
.hamburger::before { top: -7px; }
.hamburger::after  { top: 7px; }
.hamburger.open { background: transparent; }
.hamburger.open::before { transform: rotate(45deg) translate(5px, 5px); }
.hamburger.open::after  { transform: rotate(-45deg) translate(5px, -5px); }

.mobile-menu {
  display: none; flex-direction: column;
  background: var(--cream); border-top: 1px solid var(--blush);
  max-height: 0; overflow: hidden; transition: max-height 0.4s ease;
}
.mobile-menu--open { max-height: 700px; }
.mobile-menu a, .mobile-menu button {
  padding: 0.9rem 2rem; font-size: 0.72rem; letter-spacing: 0.15em; text-transform: uppercase;
  color: var(--warm-brown); border-bottom: 1px solid var(--blush-light); text-align: left; width: 100%;
  transition: color 0.2s, padding-left 0.2s;
}
.mobile-menu a:hover, .mobile-menu button:hover { color: var(--rose-gold); padding-left: 2.5rem; }
.mobile-menu__divider { height: 1px; background: var(--blush); margin: 0.25rem 0; }
.mobile-divider-label {
  padding: 0.5rem 2rem; font-size: 0.55rem; letter-spacing: 0.2em;
  text-transform: uppercase; color: var(--rose-gold); background: var(--blush-light);
}
.mobile-consult-link { color: var(--rose-gold) !important; font-weight: 600; }

@media (max-width: 1100px) {
  .navbar__links { gap: 1.2rem; }
  .nav-link { font-size: 0.58rem; }
}
@media (max-width: 900px) {
  .navbar__links { display: none; }
  .mobile-menu-btn { display: flex; }
  .mobile-menu { display: flex; }
  .navbar__inner { padding: 0 1.25rem; }
  .logo-img { height: 48px; }
}
</style>
