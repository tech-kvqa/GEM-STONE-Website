<template>
  <main>
    <div style="height: var(--nav-h)"></div>
    <div class="container" style="padding-top:3rem;padding-bottom:5rem">
      <div class="section-head">
        <p class="label-caps">Your Saved Crystals</p>
        <h1 class="heading-section">Wishlist</h1>
      </div>
      <div v-if="wishlist.items.length" class="product-grid">
        <ProductCard v-for="item in wishlist.items" :key="item.id" :product="item.product" />
      </div>
      <div v-else class="empty-state">
        <div style="font-size:3rem;color:var(--gold-dim);animation:float 3s ease-in-out infinite">✦</div>
        <p style="color:var(--ivory-dim);opacity:0.5">Your wishlist is empty</p>
        <router-link to="/shop" class="btn btn-outline"><span>Explore Crystals</span></router-link>
      </div>
    </div>
  </main>
</template>
<script setup>
import ProductCard from '@/components/product/ProductCard.vue'
import { useWishlistStore } from '@/store/wishlist'
const wishlist = useWishlistStore()
</script>
<style scoped>
.empty-state { display:flex;flex-direction:column;align-items:center;gap:1.5rem;padding:5rem 0;text-align:center; }
.section-head { text-align:center;margin-bottom:3rem; }
.section-head .heading-section { margin-top:0.5rem; }
</style>
