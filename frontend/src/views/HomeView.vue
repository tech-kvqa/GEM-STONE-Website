<template>
  <main class="home">

    <!-- ── Hero ──────────────────────────────────────────────────────────── -->
    <section class="hero">
      <div class="hero__bg">
        <img src="https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=1800&q=90" alt="Crystal Collection" />
        <div class="hero__overlay"></div>
      </div>
      <div class="hero__content">
        <p class="label-caps hero__pre animate-fade-up" style="animation-delay:0.1s">✦ Hand-Sourced · Ethically Obtained · Certified Natural</p>
        <h1 class="hero__title animate-fade-up" style="animation-delay:0.25s">
          Glow with<br/><em>the Earth's Light</em>
        </h1>
        <p class="hero__desc animate-fade-up" style="animation-delay:0.4s">
          Each crystal a story. Each stone a journey across continents and millennia.
          Discover the world's finest hand-sourced crystals, curated with love by Ritz.
        </p>
        <div class="hero__ctas animate-fade-up" style="animation-delay:0.55s">
          <router-link to="/shop" class="btn btn-gold"><span>Explore Collection</span></router-link>
          <router-link to="/our-story" class="btn btn-ghost"><span>Our Story</span></router-link>
        </div>
      </div>
      <div class="hero__scroll-hint">
        <span>Discover</span>
        <div class="scroll-line"></div>
      </div>
    </section>

    <!-- ── Brand pillars ──────────────────────────────────────────────────── -->
    <section class="pillars">
      <div class="container">
        <div class="pillars__grid">
          <div v-for="p in pillars" :key="p.label" class="pillar">
            <div class="pillar__icon">{{ p.icon }}</div>
            <h4>{{ p.label }}</h4>
            <p>{{ p.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Brand Story Banner ─────────────────────────────────────────────── -->
    <section class="story-banner">
      <div class="story-banner__img">
        <img src="https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=1000&q=85" alt="Rose Quartz Story" loading="lazy" />
      </div>
      <div class="story-banner__text">
        <p class="label-caps">The Glow With Ritz Story</p>
        <h2>Born from a Belief<br/><em>in Gentle Power</em></h2>
        <div class="divider-gold"><span>✦</span></div>
        <p class="story-body">
          We believe that the earth speaks — in colour, in weight, in the cool smoothness of
          a rose quartz sphere or the flash of light inside a labradorite. Glow With Ritz was
          founded to bring these voices home to you.
        </p>
        <p class="story-body" style="margin-top:1rem">
          Every crystal is hand-selected by Ritz herself — held, felt, and approved before
          it ever reaches your hands. This is not a warehouse. This is a curation.
        </p>
        <router-link to="/our-story" class="btn btn-outline" style="margin-top:2rem"><span>Read Our Full Story</span></router-link>
      </div>
    </section>

    <!-- ── Bestsellers ────────────────────────────────────────────────────── -->
    <section class="section">
      <div class="container">
        <div class="section-head">
          <p class="label-caps">Most Beloved</p>
          <h2 class="heading-section">Our Bestsellers</h2>
        </div>
        <div v-if="bestsellers.length" class="product-grid">
          <ProductCard v-for="p in bestsellers" :key="p.id" :product="p" />
        </div>
        <div v-else class="product-grid">
          <div v-for="i in 4" :key="i" class="skeleton" style="aspect-ratio:4/5"></div>
        </div>
      </div>
    </section>

    <!-- ── CHAKRA Section ─────────────────────────────────────────────────── -->
    <section class="chakra-section">
      <div class="chakra-section__header">
        <p class="label-caps" style="color:var(--blush)">Find Your Glow</p>
        <h2 class="chakra-section__title">Shop by <em>Chakra</em></h2>
        <p class="chakra-section__sub">Every crystal carries a frequency. Find yours.</p>
      </div>
      <div class="chakra-river">
        <router-link
          v-for="c in chakras" :key="c.name"
          :to="`/shop?chakra=${encodeURIComponent(c.name)}`"
          class="chakra-pill" :style="{ '--cc': c.color, '--cc-soft': c.soft }"
        >
          <div class="chakra-pill__orb">
            <span class="chakra-pill__symbol">{{ c.symbol }}</span>
          </div>
          <div class="chakra-pill__body">
            <div class="chakra-pill__name">{{ c.name }}</div>
            <div class="chakra-pill__crystal">{{ c.crystal }}</div>
            <div class="chakra-pill__intent">{{ c.intent }}</div>
          </div>
          <div class="chakra-pill__arrow">→</div>
        </router-link>
      </div>
    </section>

    <!-- ── New Arrivals ───────────────────────────────────────────────────── -->
    <section class="section" style="background: var(--bg-section)">
      <div class="container">
        <div class="section-head section-head--between">
          <div>
            <p class="label-caps">Fresh from the Earth</p>
            <h2 class="heading-section">New Arrivals</h2>
          </div>
          <router-link to="/shop?new_arrival=true" class="btn btn-outline"><span>View All</span></router-link>
        </div>
        <div v-if="newArrivals.length" class="product-grid">
          <ProductCard v-for="p in newArrivals" :key="p.id" :product="p" />
        </div>
      </div>
    </section>

    <!-- ── Sacred Knowledge — VIDEO section ──────────────────────────────── -->
    <section class="sacred-section">
      <div class="sacred-section__left">
        <p class="label-caps" style="color:var(--rose-gold)">Sacred Knowledge</p>
        <h2 class="sacred-section__title">The Glow With Ritz<br/><em>Crystal Guide</em></h2>
        <p class="sacred-body">
          New to crystals? Our guide walks you through every stone's story,
          healing properties, and the intentions they serve best — written with love.
        </p>
        <router-link to="/crystal-guide" class="btn btn-gold" style="margin-top:2rem"><span>Read the Guide</span></router-link>
      </div>
      <div class="sacred-section__video">
        <div class="video-wrapper">
          <iframe
            src="https://www.youtube.com/embed/dTd6sL0EVq8?rel=0&modestbranding=1&showinfo=0"
            title="Crystal Healing Guide — Glow With Ritz"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>
        <div class="video-caption">✦ A gentle introduction to the world of crystals</div>
      </div>
    </section>

    <!-- ── Testimonials ───────────────────────────────────────────────────── -->
    <section class="section testimonials">
      <div class="container">
        <div class="section-head">
          <p class="label-caps">From the Glow Circle</p>
          <h2 class="heading-section">What Our Collectors Say</h2>
        </div>
        <div class="testimonials__grid">
          <div v-for="t in testimonials" :key="t.name" class="testimonial-card">
            <div class="stars"><span v-for="i in 5" :key="i">★</span></div>
            <blockquote>{{ t.quote }}</blockquote>
            <div class="testimonial-card__author">
              <div class="author-avatar">{{ t.name[0] }}</div>
              <div>
                <div class="author-name">{{ t.name }}</div>
                <div class="author-loc">{{ t.location }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Trust Badges ───────────────────────────────────────────────────── -->
    <section class="trust-bar">
      <div class="container">
        <div class="trust-grid">
          <div v-for="t in trustBadges" :key="t.label" class="trust-item">
            <span class="trust-icon">{{ t.icon }}</span>
            <div>
              <div class="trust-label">{{ t.label }}</div>
              <div class="trust-sub">{{ t.sub }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ProductCard from '@/components/product/ProductCard.vue'
import { productApi, categoryApi } from '@/api'

const categories  = ref([])
const bestsellers = ref([])
const newArrivals = ref([])

const pillars = [
  { icon: '🌍', label: 'Ethically Sourced',  desc: 'Every crystal traced to its origin with fair-trade commitments to every miner.' },
  { icon: '🔬', label: 'Lab Certified',       desc: 'All crystals tested and certified natural — no dyed, treated, or synthetic pieces.' },
  { icon: '💎', label: 'Hand Selected',       desc: 'Each piece personally held and approved by Ritz before it reaches your hands.' },
  { icon: '🎀', label: 'Gift Packaging',      desc: 'Delivered in beautiful, eco-conscious packaging with a crystal story card.' },
]

const chakras = [
  { name: 'Root',         color: '#c0392b', soft: 'rgba(192,57,43,0.12)',  symbol: '᯼', crystal: 'Black Tourmaline', intent: 'Safety & Grounding' },
  { name: 'Sacral',       color: '#e07b54', soft: 'rgba(224,123,84,0.12)', symbol: '᯽', crystal: 'Carnelian',        intent: 'Passion & Creativity' },
  { name: 'Solar Plexus', color: '#e8b84b', soft: 'rgba(232,184,75,0.12)', symbol: '᯾', crystal: 'Citrine',          intent: 'Confidence & Power' },
  { name: 'Heart',        color: '#6dba82', soft: 'rgba(109,186,130,0.12)',symbol: '♡', crystal: 'Rose Quartz',      intent: 'Love & Compassion' },
  { name: 'Throat',       color: '#5b9dd4', soft: 'rgba(91,157,212,0.12)', symbol: '◯', crystal: 'Lapis Lazuli',     intent: 'Truth & Expression' },
  { name: 'Third Eye',    color: '#9b72cf', soft: 'rgba(155,114,207,0.12)',symbol: '✦', crystal: 'Amethyst',         intent: 'Intuition & Wisdom' },
  { name: 'Crown',        color: '#c8a8d8', soft: 'rgba(200,168,216,0.12)',symbol: '☽', crystal: 'Clear Quartz',     intent: 'Divine Connection' },
]

const testimonials = [
  { name: 'Priya Sharma',   location: 'Mumbai',    quote: 'The Rose Quartz sphere I ordered is absolutely breathtaking. The quality is unlike anything I\'ve found locally — and the packaging felt like receiving a gift from a dear friend.' },
  { name: 'Arjun Mehta',    location: 'Delhi',     quote: 'I\'ve been collecting crystals for years. Glow With Ritz is in a different league entirely. The Labradorite freeform shows the most spectacular flash I\'ve ever seen in person.' },
  { name: 'Kavitha Nair',   location: 'Bangalore', quote: 'Ordered the starter set as a gift. The crystals are exceptional and each came with a beautiful card explaining its story. My sister was moved to tears.' },
  { name: 'Rohan Gupta',    location: 'Pune',      quote: 'The Amethyst cluster on my bedside table has genuinely transformed the energy of my room. Whether you believe in the metaphysics or not — it\'s simply stunning.' },
]

const trustBadges = [
  { icon: '🛡️', label: 'Authenticity Guaranteed', sub: 'Every crystal certified natural' },
  { icon: '🚚', label: 'Free Shipping ₹999+',      sub: 'Pan-India delivery' },
  { icon: '↩️', label: '7-Day Easy Returns',        sub: 'No questions asked' },
  { icon: '🔒', label: 'Secure Payments',           sub: 'Razorpay & COD' },
]

onMounted(async () => {
  const [cats, best, newA] = await Promise.all([
    categoryApi.list(),
    productApi.bestsellers(),
    productApi.newArrivals(),
  ])
  categories.value  = cats.data
  bestsellers.value = best.data
  newArrivals.value = newA.data
})
</script>

<style scoped>
/* ── Hero ──────────────────────────────────────────────────────────────────── */
.hero {
  position: relative; /* min-height: 92vh; */
  min-height: 72vh;
  display: flex; align-items: center; justify-content: center; text-align: center; overflow: hidden;
}
.hero__bg { position: absolute; inset: 0; }
.hero__bg img {
  width: 100%; height: 100%; object-fit: cover;
  /* transform: scale(1.05); */
  transform: scale(1);
  animation: heroKen 20s ease-in-out infinite alternate;
}
@keyframes heroKen {
  from { transform: scale(1.05) translate(0, 0); }
  to   { transform: scale(1.12) translate(-1%, -1%); }
}
.hero__overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom,
    rgba(253,240,236,0.35) 0%,
    rgba(253,240,236,0.55) 40%,
    rgba(253,240,236,0.82) 100%
  );
}
.hero__content {
  position: relative; z-index: 2;
  max-width: 780px; padding: 0 1.5rem;
  padding-top: var(--nav-h);
}
.hero__pre { margin-bottom: 1.5rem; }
.hero__title {
  font-family: var(--font-serif);
  font-size: clamp(2.8rem, 7vw, 6.5rem);
  font-weight: 300; line-height: 1.05; color: var(--ink);
  margin-bottom: 1.5rem;
}
.hero__title em { color: var(--rose-gold); font-style: italic; }
/* .hero__desc {
  font-family: var(--font-serif);
  font-size: clamp(0.95rem, 1.6vw, 1.1rem);
  color: var(--warm-brown); max-width: 520px; margin: 0 auto 2.5rem;
  line-height: 1.8; opacity: 0.9;
} */
.hero__desc {
  font-family: var(--font-serif);
  font-size: clamp(0.95rem, 1.6vw, 1.1rem);
  color: var(--ink);
  font-weight: 400;
  max-width: 520px;
  margin: 0 auto 2.5rem;
  line-height: 1.8;
}
.hero__ctas { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
.hero__scroll-hint {
  position: absolute; bottom: 2rem; left: 50%; transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center; gap: 0.5rem; z-index: 2;
}
.hero__scroll-hint span { font-size: 0.58rem; letter-spacing: 0.25em; text-transform: uppercase; color: var(--rose-gold-dim); }
.scroll-line {
  width: 1px; height: 50px;
  background: linear-gradient(to bottom, var(--rose-gold-dim), transparent);
  animation: scrollPulse 2s ease-in-out infinite;
}
@keyframes scrollPulse {
  0%,100% { opacity: 0.4; transform: scaleY(0.8); }
  50%      { opacity: 1;   transform: scaleY(1); }
}

/* ── Pillars ───────────────────────────────────────────────────────────────── */
.pillars { padding: 3rem 0; border-bottom: 1px solid var(--blush); background: var(--cream); }
.pillars__grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; }
.pillar { text-align: center; padding: 1.5rem; }
.pillar__icon { font-size: 1.8rem; margin-bottom: 0.75rem; }
.pillar h4 { font-family: var(--font-serif); font-size: 1rem; font-weight: 400; color: var(--ink); margin-bottom: 0.4rem; }
.pillar p { font-size: 0.78rem; color: var(--muted); line-height: 1.7; }

/* ── Section head ──────────────────────────────────────────────────────────── */
.section-head { text-align: center; margin-bottom: 3.5rem; }
.section-head .label-caps { margin-bottom: 0.75rem; }
.section-head .heading-section em { color: var(--rose-gold); font-style: italic; }
.section-head--between {
  text-align: left; display: flex; align-items: flex-end; justify-content: space-between;
}

/* ── Story Banner ──────────────────────────────────────────────────────────── */
.story-banner { display: grid; grid-template-columns: 1fr 1fr; min-height: 520px; }
.story-banner__img { overflow: hidden; }
.story-banner__img img { width: 100%; height: 100%; object-fit: cover; }
.story-banner__text {
  background: var(--blush-light); padding: 4rem 3.5rem;
  display: flex; flex-direction: column; justify-content: center;
}
.story-banner__text h2 {
  font-family: var(--font-serif); font-size: clamp(1.8rem, 3vw, 2.8rem);
  font-weight: 300; color: var(--ink); margin: 0.75rem 0 1rem; line-height: 1.2;
}
.story-banner__text h2 em { color: var(--rose-gold); font-style: italic; }
/* FIX #2: readable body text — dark colour instead of warm-brown */
/* .story-body {
  font-family: var(--font-serif);
  font-size: 1rem;
  font-weight: 300;
  line-height: 1.85;
  color: var(--ink);
} */

.story-body {
  font-family: var(--font-serif);
  font-size: 1.05rem;
  font-weight: 400;
  line-height: 1.9;
  color: var(--ink);
}

/* ── CHAKRA Section — dramatically highlighted ─────────────────────────────── */
/* .chakra-section {
  background: linear-gradient(135deg, #1a1018 0%, #2a1f2e 40%, #1e1826 70%, #16101a 100%);
  padding: 5rem 0;
  position: relative;
  overflow: hidden;
} */
.chakra-section {
  background: linear-gradient(
    135deg,
    #1a1018 0%,
    #2a1f2e 40%,
    #1e1826 70%,
    #16101a 100%
  );
  padding: 5rem 0;
  position: relative;
  overflow: hidden;
}
.chakra-section::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(196,135,106,0.15) 0%, transparent 60%),
              radial-gradient(ellipse at 20% 80%, rgba(155,114,207,0.1) 0%, transparent 50%),
              radial-gradient(ellipse at 80% 90%, rgba(91,157,212,0.08) 0%, transparent 50%);
  pointer-events: none;
}
.chakra-section::after {
  content: '✦ ✦ ✦';
  position: absolute; top: 1.5rem; left: 50%; transform: translateX(-50%);
  font-size: 0.7rem; letter-spacing: 1rem; color: rgba(196,135,106,0.3);
  pointer-events: none;
}

.chakra-section__header {
  text-align: center;
  margin-bottom: 3rem;
  position: relative; z-index: 1;
}
.chakra-section__title {
  font-family: var(--font-serif);
  font-size: clamp(2rem, 4vw, 3.5rem);
  font-weight: 300; color: var(--cream); margin: 0.5rem 0;
}
.chakra-section__title em { color: var(--rose-gold-bright); font-style: italic; }
.chakra-section__sub {
  font-size: 0.82rem; color: rgba(255,255,255,0.45);
  letter-spacing: 0.08em; margin-top: 0.5rem;
}

.chakra-river {
  display: flex; flex-direction: column; gap: 0;
  max-width: 780px; margin: 0 auto; padding: 0 2rem;
  position: relative; z-index: 1;
}
.chakra-pill {
  display: grid; grid-template-columns: 72px 1fr auto;
  align-items: center; gap: 1.25rem;
  padding: 1.1rem 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  transition: all 0.3s ease;
  text-decoration: none;
  border-radius: 0;
  position: relative;
}
.chakra-pill::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(135deg, var(--cc-soft, rgba(196,135,106,0.08)), transparent);
  opacity: 0; transition: opacity 0.3s ease;
  border-radius: 4px;
}
.chakra-pill:hover::before { opacity: 1; }
/* .chakra-pill:hover {
  transform: translateX(6px);
  border-bottom-color: rgba(var(--cc), 0.3);
} */
.chakra-pill:hover {
  transform: translateX(6px);
  box-shadow: 0 0 24px rgba(196,135,106,0.25);
}
.chakra-pill:hover .chakra-pill__orb {
  transform: scale(1.15);
  box-shadow: 0 0 24px var(--cc), 0 0 48px color-mix(in srgb, var(--cc) 30%, transparent);
}
.chakra-pill:hover .chakra-pill__arrow { color: var(--cc); transform: translateX(4px); }

.chakra-pill__orb {
  width: 52px; height: 52px; border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, color-mix(in srgb, var(--cc) 80%, white), var(--cc));
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 16px color-mix(in srgb, var(--cc) 50%, transparent),
              inset 0 0 8px rgba(255,255,255,0.2);
  transition: all 0.4s ease;
  flex-shrink: 0;
}
.chakra-pill__symbol { font-size: 1.3rem; color: rgba(255,255,255,0.9); }

.chakra-pill__body {}
.chakra-pill__name {
  font-size: 0.65rem; font-weight: 600; letter-spacing: 0.2em;
  text-transform: uppercase; color: rgba(255,255,255,0.9); margin-bottom: 0.2rem;
}
.chakra-pill__crystal {
  font-family: var(--font-serif); font-size: 1rem; font-weight: 300;
  color: rgba(255,255,255,0.7); margin-bottom: 0.15rem;
}
.chakra-pill__intent {
  font-size: 0.68rem; color: rgba(255,255,255,0.35); letter-spacing: 0.05em;
}
.chakra-pill__arrow {
  font-size: 1rem; color: rgba(255,255,255,0.2);
  transition: all 0.3s ease; flex-shrink: 0;
}

/* ── Sacred Knowledge — Video ──────────────────────────────────────────────── */
.sacred-section {
  display: grid; grid-template-columns: 1fr 1fr;
  min-height: 480px; background: var(--blush-light);
}
.sacred-section__left {
  padding: 5rem 4rem;
  display: flex; flex-direction: column; justify-content: center;
}
.sacred-section__title {
  font-family: var(--font-serif); font-size: clamp(2rem, 3.5vw, 3.2rem);
  font-weight: 300; color: var(--ink); margin: 0.75rem 0;
}
.sacred-section__title em { color: var(--rose-gold); font-style: italic; }
/* FIX #2: readable description text */
.sacred-body {
  font-family: var(--font-serif); font-size: 1rem;
  font-weight: 300; line-height: 1.85; color: var(--ink);
  max-width: 440px; margin-top: 1.25rem;
}
.sacred-section__video {
  display: flex; flex-direction: column; justify-content: center;
  padding: 3rem 3rem 3rem 2rem; gap: 1rem;
}
.video-wrapper {
  position: relative; padding-bottom: 56.25%; height: 0;
  overflow: hidden; border: 3px solid var(--blush-mid);
  box-shadow: 0 12px 40px rgba(196,135,106,0.18);
}
.video-wrapper iframe {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
}
.video-caption {
  font-size: 0.68rem; letter-spacing: 0.12em;
  color: var(--rose-gold-dim); text-align: center;
}

/* ── Testimonials ──────────────────────────────────────────────────────────── */
.testimonials { background: var(--cream); }
.testimonials__grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
.testimonial-card {
  padding: 2rem; border: 1px solid var(--blush); background: #fff;
  display: flex; flex-direction: column; gap: 1rem;
  transition: box-shadow 0.3s;
}
.testimonial-card:hover { box-shadow: 0 8px 32px rgba(196,135,106,0.1); }
.testimonial-card blockquote {
  font-family: var(--font-serif); font-size: 1rem; font-weight: 300;
  color: var(--ink); line-height: 1.85; flex: 1;
}
.testimonial-card__author { display: flex; align-items: center; gap: 0.75rem; }
.author-avatar {
  width: 40px; height: 40px; border-radius: 50%;
  background: var(--blush); border: 1px solid var(--blush-mid);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-serif); font-size: 1.1rem; color: var(--rose-gold);
}
.author-name { font-size: 0.8rem; font-weight: 500; color: var(--ink); }
.author-loc  { font-size: 0.68rem; color: var(--rose-gold-dim); }

/* ── Trust Bar ─────────────────────────────────────────────────────────────── */
.trust-bar { border-top: 1px solid var(--blush); background: var(--bg-section); padding: 3rem 0; }
.trust-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; }
.trust-item { display: flex; align-items: center; gap: 1rem; justify-content: center; }
.trust-icon { font-size: 1.5rem; }
.trust-label { font-size: 0.78rem; font-weight: 500; color: var(--ink); margin-bottom: 0.15rem; }
.trust-sub   { font-size: 0.68rem; color: var(--rose-gold-dim); }

/* ── Responsive ────────────────────────────────────────────────────────────── */
@media (max-width: 1100px) {
  .chakra-river { max-width: 600px; }
}
@media (max-width: 900px) {
  .sacred-section { grid-template-columns: 1fr; }
  .sacred-section__left { padding: 3rem 2rem 1.5rem; }
  .sacred-section__video { padding: 1.5rem 2rem 3rem; }
  .story-banner { grid-template-columns: 1fr; }
  .story-banner__img { height: 300px; }
  .story-banner__text { padding: 3rem 2rem; }
  .pillars__grid { grid-template-columns: repeat(2, 1fr); }
  .chakra-pill { grid-template-columns: 56px 1fr auto; gap: 1rem; padding: 0.9rem 1rem; }
}
@media (max-width: 768px) {
  .testimonials__grid { grid-template-columns: 1fr; }
  .trust-grid { grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
}
@media (max-width: 520px) {
  .trust-grid { grid-template-columns: 1fr; }
  .pillars__grid { grid-template-columns: 1fr; }
  .chakra-river { padding: 0 1rem; }
  .chakra-pill__orb { width: 44px; height: 44px; }
}
</style>
