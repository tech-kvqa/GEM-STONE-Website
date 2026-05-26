<template>
  <main class="shop-page">
    <div style="height: var(--nav-h)"></div>

    <!-- Category Banner -->
    <div v-if="currentCat" class="cat-banner">
      <img :src="currentCat.banner_url || currentCat.image_url" :alt="currentCat.name" />
      <div class="cat-banner__overlay">
        <p class="label-caps">Crystal Collection</p>
        <h1>{{ currentCat.name }}</h1>
        <p class="cat-banner__desc">{{ currentCat.description }}</p>
      </div>
    </div>
    <div v-else class="shop-hero">
      <p class="label-caps">The Complete Edit</p>
      <h1>All Crystals</h1>
    </div>

    <!-- Category Story -->
    <div v-if="currentCat?.story" class="cat-story">
      <div class="container">
        <div class="cat-story__inner">
          <div class="divider-gold"><span>✦</span></div>
          <p class="cat-story__text body-serif">{{ currentCat.story }}</p>
          <div class="divider-gold"><span>✦</span></div>
        </div>
      </div>
    </div>

    <div class="container shop-layout">
      <!-- Sidebar Filters -->
      <aside class="filters" :class="{ 'filters--open': filtersOpen }">
        <div class="filters__head">
          <h3>Refine</h3>
          <button class="filters__close" @click="filtersOpen = false">✕</button>
        </div>

        <!-- Categories -->
        <div class="filter-group">
          <h4 class="filter-group__title">Collection</h4>
          <router-link to="/shop" class="filter-option" :class="{ active: !$route.params.category }">All Crystals</router-link>
          <router-link
            v-for="cat in categories"
            :key="cat.slug"
            :to="`/shop/${cat.slug}`"
            class="filter-option"
            :class="{ active: $route.params.category === cat.slug }"
          >{{ cat.name }}</router-link>
        </div>

        <!-- Price Range -->
        <div class="filter-group">
          <h4 class="filter-group__title">Price Range</h4>
          <div class="price-inputs">
            <input v-model.number="filters.min_price" type="number" placeholder="Min ₹" class="input-field" style="font-size:0.8rem;padding:0.5rem 0.75rem" @change="applyFilters" />
            <span>—</span>
            <input v-model.number="filters.max_price" type="number" placeholder="Max ₹" class="input-field" style="font-size:0.8rem;padding:0.5rem 0.75rem" @change="applyFilters" />
          </div>
        </div>

        <!-- Chakra -->
        <div class="filter-group">
          <h4 class="filter-group__title">Chakra</h4>
          <label v-for="chakra in chakras" :key="chakra" class="filter-check">
            <input type="radio" name="chakra" :value="chakra" v-model="filters.chakra" @change="applyFilters" />
            <span>{{ chakra }}</span>
          </label>
          <button v-if="filters.chakra" class="clear-filter" @click="filters.chakra = ''; applyFilters()">Clear</button>
        </div>

        <!-- Type -->
        <div class="filter-group">
          <h4 class="filter-group__title">Type</h4>
          <label class="filter-check">
            <input type="checkbox" v-model="filters.featured" @change="applyFilters" />
            <span>Featured</span>
          </label>
          <label class="filter-check">
            <input type="checkbox" v-model="filters.bestseller" @change="applyFilters" />
            <span>Bestsellers</span>
          </label>
          <label class="filter-check">
            <input type="checkbox" v-model="filters.new_arrival" @change="applyFilters" />
            <span>New Arrivals</span>
          </label>
        </div>

        <button class="btn btn-outline w-full" style="margin-top:1rem" @click="resetFilters">Reset All</button>
      </aside>

      <!-- Product Area -->
      <div class="shop-main">
        <!-- Toolbar -->
        <div class="shop-toolbar">
          <button class="filter-toggle-btn" @click="filtersOpen = true">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="4" y1="6" x2="20" y2="6"/><line x1="8" y1="12" x2="20" y2="12"/><line x1="12" y1="18" x2="20" y2="18"/></svg>
            Filters
          </button>
          <span class="result-count">{{ total }} {{ total === 1 ? 'Crystal' : 'Crystals' }}</span>
          <select v-model="filters.sort" @change="applyFilters" class="sort-select">
            <option value="created_at_desc">Newest First</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="name_asc">Name A–Z</option>
          </select>
        </div>

        <!-- Grid -->
        <div v-if="loading" class="product-grid">
          <div v-for="i in 12" :key="i" class="skeleton" style="aspect-ratio:4/5"></div>
        </div>
        <div v-else-if="products.length" class="product-grid">
          <ProductCard v-for="p in products" :key="p.id" :product="p" />
        </div>
        <div v-else class="empty-state">
          <div class="empty-icon">✦</div>
          <p>No crystals found for this search.</p>
          <button class="btn btn-outline" @click="resetFilters"><span>Clear Filters</span></button>
        </div>

        <!-- Pagination -->
        <div v-if="pages > 1" class="pagination">
          <button
            v-for="pg in pages"
            :key="pg"
            :class="['page-btn', { active: pg === currentPage }]"
            @click="goToPage(pg)"
          >{{ pg }}</button>
        </div>
      </div>
    </div>

    <!-- Overlay for mobile filters -->
    <div v-if="filtersOpen" class="filters-overlay" @click="filtersOpen = false"></div>
  </main>
</template>

<script setup>
import { ref, reactive, watch, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import ProductCard from '@/components/product/ProductCard.vue'
import { productApi, categoryApi } from '@/api'

const route = useRoute()
const products   = ref([])
const categories = ref([])
const total      = ref(0)
const pages      = ref(1)
const currentPage = ref(1)
const loading    = ref(false)
const filtersOpen = ref(false)

const filters = reactive({
  sort: 'created_at_desc',
  min_price: null,
  max_price: null,
  chakra: '',
  featured: !!route.query.featured,
  bestseller: !!route.query.bestseller,
  new_arrival: !!route.query.new_arrival,
  search: route.query.search || ''
})

const chakras = ['Root', 'Sacral', 'Solar Plexus', 'Heart', 'Throat', 'Third Eye', 'Crown', 'All Chakras']

const currentCat = computed(() => {
  if (!route.params.category) return null
  return categories.value.find(c => c.slug === route.params.category)
})

async function fetchProducts() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: 12,
      sort: filters.sort,
      ...(route.params.category && { category: route.params.category }),
      ...(filters.min_price && { min_price: filters.min_price }),
      ...(filters.max_price && { max_price: filters.max_price }),
      ...(filters.chakra && { chakra: filters.chakra }),
      ...(filters.featured && { featured: true }),
      ...(filters.bestseller && { bestseller: true }),
      ...(filters.new_arrival && { new_arrival: true }),
      ...(filters.search && { search: filters.search }),
    }
    const { data } = await productApi.list(params)
    products.value = data.items
    total.value = data.total
    pages.value = data.pages
  } finally { loading.value = false }
}

function applyFilters() { currentPage.value = 1; fetchProducts() }

function resetFilters() {
  Object.assign(filters, { sort: 'created_at_desc', min_price: null, max_price: null, chakra: '', featured: false, bestseller: false, new_arrival: false, search: '' })
  applyFilters()
}

function goToPage(pg) { currentPage.value = pg; fetchProducts(); window.scrollTo({ top: 0, behavior: 'smooth' }) }

watch(() => route.params.category, () => { currentPage.value = 1; fetchProducts() })
watch(() => route.query.search, (v) => { filters.search = v || ''; applyFilters() })

onMounted(async () => {
  const { data } = await categoryApi.list()
  categories.value = data
  if (route.query.search) filters.search = route.query.search
  fetchProducts()
})
</script>

<style scoped>
.cat-banner {
  position: relative; height: 420px; overflow: hidden;
}
.cat-banner img {
  width: 100%; height: 100%; object-fit: cover;
  filter: brightness(0.45);
}
.cat-banner__overlay {
  position: absolute; inset: 0;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center; padding: 2rem;
}
.cat-banner__overlay .label-caps { margin-bottom: 0.75rem; }
.cat-banner__overlay h1 {
  font-family: var(--font-serif);
  font-size: clamp(2.5rem, 6vw, 5rem);
  font-weight: 300; color: var(--ivory);
  margin-bottom: 0.75rem;
}
/* .cat-banner__desc {
  font-family: var(--font-serif);
  font-size: 1.1rem; color: var(--ivory-dim);
  max-width: 500px; opacity: 0.75;
} */

.cat-banner__desc {
  font-family: var(--font-serif);
  font-size: 1.1rem;
  color: rgba(255,255,255,0.92);
  max-width: 500px;
  opacity: 1;
  line-height: 1.8;
}

.shop-hero {
  text-align: center; padding: 4rem 1.5rem 2rem;
}
.shop-hero .label-caps { margin-bottom: 0.5rem; }
/* .shop-hero h1 {
  font-family: var(--font-serif);
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 300; color: var(--ivory);
} */

.shop-hero h1 {
  font-family: var(--font-serif);
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 300;
  color: var(--ink);
}

/* .cat-story { padding: 3rem 0; background: var(--charcoal); }
.cat-story__inner { max-width: 720px; margin: 0 auto; text-align: center; }
.cat-story__text { margin: 1.5rem 0; } */

/* .cat-story {
  padding: 3rem 0;
  background: linear-gradient(
    180deg,
    rgba(20, 18, 16, 0.95),
    rgba(30, 26, 22, 0.98)
  );
} */

.cat-story {
  padding: 3rem 0;
  background: linear-gradient(
    180deg,
    var(--blush-light) 0%,
    var(--bg-section) 100%
  );
  border-top: 1px solid var(--blush);
  border-bottom: 1px solid var(--blush);
}

/* .cat-story__text {
  margin: 1.5rem 0;
  color: rgba(255, 248, 240, 0.85);
  font-size: 1.05rem;
  line-height: 1.8;
  letter-spacing: 0.02em;
} */

.cat-story__text {
  margin: 1.5rem 0;
  color: var(--ink);
  font-size: 1.08rem;
  line-height: 1.9;
  letter-spacing: 0.015em;
  font-weight: 400;
}
/* .cat-story__inner { max-width: 720px; margin: 0 auto; text-align: center; } */
.cat-story__inner {
  max-width: 820px;
  margin: 0 auto;
  text-align: center;
}

.shop-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 3rem;
  padding-top: 3rem;
  padding-bottom: 5rem;
  align-items: start;
}

/* Filters */
.filters { position: sticky; top: calc(var(--nav-h) + 1rem); }
.filters__head {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 1.5rem;
}
.filters__head h3 {
  font-family: var(--font-serif); font-size: 1.2rem; font-weight: 400; color: var(--ivory);
}
.filters__close { display: none; color: var(--gold-dim); }

.filter-group { margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 1.5rem; }
.filter-group__title {
  font-size: 0.62rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--gold-dim); margin-bottom: 0.9rem;
}
.filter-option {
  display: block; font-size: 0.82rem; color: var(--ivory-dim);
  opacity: 0.55; padding: 0.3rem 0;
  transition: opacity 0.2s, color 0.2s, padding-left 0.2s;
}
.filter-option:hover, .filter-option.active { opacity: 1; color: var(--gold); padding-left: 4px; }
.filter-option.router-link-active { color: var(--gold); opacity: 1; }

.filter-check {
  display: flex; align-items: center; gap: 0.6rem;
  font-size: 0.82rem; color: var(--ivory-dim); opacity: 0.65;
  padding: 0.3rem 0; cursor: pointer;
  transition: opacity 0.2s;
}
.filter-check:hover { opacity: 1; }
.filter-check input[type="checkbox"],
.filter-check input[type="radio"] { accent-color: var(--gold); }

.price-inputs { display: flex; align-items: center; gap: 0.5rem; }
.clear-filter {
  font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--gold-dim); margin-top: 0.4rem; transition: color 0.2s;
}
.clear-filter:hover { color: var(--gold); }

/* Toolbar */
/* .shop-toolbar {
  display: flex; align-items: center; gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
} */

.shop-toolbar {
  display: flex;
  align-items: center;
  gap: 1rem;

  margin-bottom: 1.5rem;
  padding-bottom: 1rem;

  border-bottom: 1px solid rgba(201,168,76,0.15);  /* gold tint */
}
/* .filter-toggle-btn {
  display: none;
  align-items: center; gap: 0.4rem;
  font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--gold-dim); border: 1px solid rgba(201,168,76,0.2);
  padding: 0.5rem 0.9rem;
  transition: all 0.2s;
}
.filter-toggle-btn:hover { color: var(--gold); border-color: var(--gold); } */

.filter-toggle-btn {
  display: none;
  align-items: center;
  gap: 0.4rem;

  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;

  color: rgba(255,248,240,0.75);
  border: 1px solid rgba(201,168,76,0.25);

  padding: 0.55rem 1rem;

  background: rgba(40,34,30,0.6);   /* subtle background */
  transition: all 0.25s ease;
}

.filter-toggle-btn:hover {
  color: var(--gold);
  border-color: var(--gold);
  background: rgba(201,168,76,0.08);
}

/* .result-count { font-size: 0.78rem; color: var(--ivory-dim); opacity: 0.5; margin-right: auto; } */
/* .sort-select {
  background: var(--charcoal); border: 1px solid rgba(201,168,76,0.15);
  color: var(--ivory-dim); font-size: 0.78rem; padding: 0.5rem 0.75rem;
  outline: none; cursor: pointer;
} */

.result-count {
  font-size: 0.8rem;
  color: rgba(255, 248, 240, 0.8);   /* brighter */
  opacity: 0.9;
  margin-right: auto;
  letter-spacing: 0.04em;
}

.sort-select {
  background: rgba(40, 34, 30, 0.95);   /* softer than charcoal */
  border: 1px solid rgba(201,168,76,0.25);

  color: rgba(255,248,240,0.9);         /* readable text */
  font-size: 0.8rem;
  padding: 0.55rem 0.8rem;

  outline: none;
  cursor: pointer;

  transition: all 0.2s ease;
}

/* Hover */
.sort-select:hover {
  border-color: var(--gold);
}

/* Focus */
.sort-select:focus {
  border-color: var(--gold);
  box-shadow: 0 0 0 1px rgba(201,168,76,0.3);
}

/* Dropdown options */
.sort-select option {
  background: #1e1a16;
  color: rgba(255,248,240,0.9);
}

/* Pagination */
.pagination { display: flex; gap: 0.5rem; justify-content: center; margin-top: 3rem; }
.page-btn {
  width: 36px; height: 36px;
  border: 1px solid rgba(201,168,76,0.15);
  color: var(--ivory-dim); font-size: 0.8rem;
  transition: all 0.2s;
}
.page-btn:hover, .page-btn.active {
  background: var(--gold); border-color: var(--gold);
  color: var(--black);
}

/* Empty state */
.empty-state {
  display: flex; flex-direction: column; align-items: center;
  gap: 1rem; padding: 5rem 0; text-align: center;
}
.empty-icon { font-size: 3rem; color: var(--gold-dim); animation: float 3s ease-in-out infinite; }
.empty-state p { color: var(--ivory-dim); opacity: 0.5; }

.w-full { width: 100%; }

/* Mobile */
.filters-overlay { display: none; }
@media (max-width: 900px) {
  .shop-layout { grid-template-columns: 1fr; }
  .filters {
    position: fixed; top: 0; left: 0; bottom: 0;
    width: 300px; background: var(--ink);
    border-right: 1px solid rgba(201,168,76,0.15);
    z-index: 800; overflow-y: auto;
    padding: 1.5rem;
    transform: translateX(-110%);
    transition: transform 0.35s ease;
  }
  .filters--open { transform: translateX(0); }
  .filters__close { display: flex; }
  .filter-toggle-btn { display: flex; }
  .filters-overlay {
    display: block;
    position: fixed; inset: 0;
    background: rgba(5,4,3,0.6);
    z-index: 799;
  }
}
</style>
