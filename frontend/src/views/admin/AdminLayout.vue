<template>
  <div class="admin-shell">

    <!-- Sidebar -->
    <aside class="admin-sidebar" :class="{ 'admin-sidebar--collapsed': collapsed }">
      <!-- Brand -->
      <div class="sidebar-brand">
        <div class="sidebar-brand__gem">✦</div>
        <div v-if="!collapsed" class="sidebar-brand__text">
          <span class="sidebar-brand__name">Glow With Ritz</span>
          <span class="sidebar-brand__role label-caps">Admin</span>
        </div>
      </div>

      <!-- Nav -->
      <nav class="sidebar-nav">
        <router-link v-for="item in navItems" :key="item.name"
          :to="{ name: item.route }"
          class="sidebar-link"
          active-class="sidebar-link--active">
          <span class="sidebar-link__icon">{{ item.icon }}</span>
          <span v-if="!collapsed" class="sidebar-link__label">{{ item.label }}</span>
        </router-link>
      </nav>

      <!-- Admin info -->
      <div class="sidebar-footer">
        <div class="sidebar-admin">
          <div class="sidebar-admin__avatar">{{ adminAuth.user?.name?.[0]?.toUpperCase() || 'A' }}</div>
          <div v-if="!collapsed" class="sidebar-admin__info">
            <p class="sidebar-admin__name">{{ adminAuth.user?.name }}</p>
            <p class="sidebar-admin__role label-caps">{{ adminAuth.user?.role || 'admin' }}</p>
          </div>
        </div>
        <button v-if="!collapsed" class="sidebar-logout" @click="logout">
          <span>Sign Out</span>
        </button>
      </div>
    </aside>

    <!-- Main -->
    <div class="admin-main">

      <!-- Topbar -->
      <header class="admin-topbar">
        <button class="topbar-toggle" @click="collapsed = !collapsed">
          <span>{{ collapsed ? '▶' : '◀' }}</span>
        </button>
        <div class="topbar-breadcrumb">
          <span class="label-caps" style="color:var(--rose-gold)">Admin</span>
          <span class="topbar-sep">·</span>
          <span class="topbar-page">{{ currentTitle }}</span>
        </div>
        <div class="topbar-right">
          <a href="/" target="_blank" class="topbar-store-link">
            <span>View Store</span>
            <span>↗</span>
          </a>
          <div class="topbar-live"><span class="live-dot"></span>Live</div>
        </div>
      </header>

      <!-- Page -->
      <div class="admin-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAdminAuthStore } from '@/store/adminAuth'

const router    = useRouter()
const route     = useRoute()
const adminAuth = useAdminAuthStore()
const collapsed = ref(false)

const navItems = [
  { icon: '◈', label: 'Dashboard',     route: 'AdminDashboard' },
  { icon: '◇', label: 'Products',      route: 'AdminProducts' },
  { icon: '◻', label: 'Orders',        route: 'AdminOrders' },
  { icon: '◉', label: 'Users',         route: 'AdminUsers' },
  { icon: '✦', label: 'Consultations', route: 'AdminConsultations' },
  { icon: '★', label: 'Reviews',       route: 'AdminReviews' },
  { icon: '▣', label: 'Inventory',     route: 'AdminInventory' },
  { icon: '⊙', label: 'Settings',      route: 'AdminSettings' },
]

const titles = {
  AdminDashboard: 'Dashboard', AdminProducts: 'Products',
  AdminOrders: 'Orders', AdminOrderDetail: 'Order Detail',
  AdminUsers: 'Users', AdminConsultations: 'Consultations',
  AdminReviews: 'Reviews', AdminInventory: 'Inventory', AdminSettings: 'Settings',
}
const currentTitle = computed(() => titles[route.name] || 'Admin Panel')

function logout() {
  adminAuth.logout()
  router.push({ name: 'AdminLogin' })
}
</script>

<style scoped>
/* ── Shell ──────────────────────────────────────────────────────────────────── */
.admin-shell {
  display: flex;
  min-height: 100vh;
  background: var(--bg-section);
  font-family: var(--font-sans);
}

/* ── Sidebar ────────────────────────────────────────────────────────────────── */
.admin-sidebar {
  width: 240px;
  min-height: 100vh;
  background: var(--bg-dark);
  border-right: 1px solid rgba(196,135,106,0.12);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: width var(--dur-mid) var(--ease-silk);
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: hidden;
}
.admin-sidebar--collapsed { width: 64px; }

/* Brand */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem 1.2rem;
  border-bottom: 1px solid rgba(196,135,106,0.12);
  min-height: 72px;
}
.sidebar-brand__gem {
  width: 34px; height: 34px;
  background: linear-gradient(135deg, var(--rose-gold), var(--rose-gold-deep));
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem; color: #fff;
  flex-shrink: 0;
}
.sidebar-brand__text { display: flex; flex-direction: column; overflow: hidden; }
.sidebar-brand__name {
  font-family: var(--font-serif);
  font-size: 0.95rem; font-weight: 300;
  color: var(--cream);
  white-space: nowrap;
}
.sidebar-brand__role { color: var(--rose-gold-dim); font-size: 0.55rem; margin-top: 0.1rem; }

/* Nav */
.sidebar-nav {
  flex: 1;
  padding: 1rem 0.6rem;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  overflow-y: auto;
}
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.65rem 0.75rem;
  color: var(--light-muted);
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  transition: all var(--dur-fast) var(--ease-silk);
  white-space: nowrap;
  overflow: hidden;
  border-left: 2px solid transparent;
}
.sidebar-link:hover {
  color: var(--cream);
  background: rgba(196,135,106,0.08);
  border-left-color: rgba(196,135,106,0.3);
}
.sidebar-link--active {
  color: var(--rose-gold);
  background: rgba(196,135,106,0.1);
  border-left-color: var(--rose-gold);
}
.sidebar-link__icon { font-size: 1rem; flex-shrink: 0; width: 18px; text-align: center; }

/* Footer */
.sidebar-footer {
  padding: 1rem 0.75rem;
  border-top: 1px solid rgba(196,135,106,0.12);
}
.sidebar-admin {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 0.75rem;
  overflow: hidden;
}
.sidebar-admin__avatar {
  width: 32px; height: 32px;
  background: linear-gradient(135deg, var(--rose-gold-deep), var(--mauve));
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-serif);
  font-size: 0.9rem; color: #fff;
  flex-shrink: 0;
}
.sidebar-admin__name {
  font-size: 0.8rem;
  color: var(--cream);
  font-weight: 300;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sidebar-admin__role { color: var(--rose-gold-dim); font-size: 0.55rem; }
.sidebar-logout {
  width: 100%;
  padding: 0.5rem;
  font-size: 0.62rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--muted);
  border: 1px solid rgba(196,135,106,0.15);
  transition: all var(--dur-fast);
}
.sidebar-logout:hover { color: var(--rose-gold); border-color: var(--rose-gold); }

/* ── Main area ──────────────────────────────────────────────────────────────── */
.admin-main { flex: 1; display: flex; flex-direction: column; min-width: 0; }

/* Topbar */
.admin-topbar {
  height: 60px;
  background: var(--bg-card);
  border-bottom: 1px solid rgba(196,135,106,0.12);
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 10;
}
.topbar-toggle {
  font-size: 0.7rem;
  color: var(--muted);
  padding: 0.4rem;
  transition: color 0.2s;
}
.topbar-toggle:hover { color: var(--rose-gold); }
.topbar-breadcrumb { display: flex; align-items: center; gap: 0.5rem; }
.topbar-sep { color: var(--blush-mid); }
.topbar-page { font-family: var(--font-serif); font-size: 1rem; color: var(--ink); font-weight: 300; }
.topbar-right { margin-left: auto; display: flex; align-items: center; gap: 1rem; }
.topbar-store-link {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--rose-gold);
  border: 1px solid rgba(196,135,106,0.3);
  padding: 0.35rem 0.8rem;
  transition: all 0.2s;
}
.topbar-store-link:hover { background: var(--rose-gold); color: #fff; }
.topbar-live {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #66bb6a;
}
.live-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #66bb6a;
  animation: pulse-rose 2s infinite;
}

/* Content */
.admin-content { flex: 1; padding: 2rem 1.5rem; overflow-y: auto; }
</style>
