<template>
  <main class="guide-page">
    <div style="height: var(--nav-h)"></div>
    <div class="guide-hero">
      <p class="label-caps">Sacred Knowledge</p>
      <h1 class="heading-display">The Crystal<br/><em>Beginner's Guide</em></h1>
      <p class="body-serif" style="margin-top:1rem;max-width:580px">
        Everything you need to know to begin your crystal journey — from choosing your first stone 
        to understanding the ancient wisdom behind each piece.
      </p>
    </div>

    <div class="container guide-body">
      <div v-for="chapter in chapters" :key="chapter.title" class="guide-chapter">
        <div class="guide-chapter__num">{{ chapter.num }}</div>
        <div class="guide-chapter__content">
          <h2>{{ chapter.title }}</h2>
          <p class="body-serif">{{ chapter.content }}</p>
          <div v-if="chapter.crystals" class="guide-crystals">
            <span v-for="c in chapter.crystals" :key="c" class="crystal-tag">{{ c }}</span>
          </div>
        </div>
      </div>

      <!-- Chakra Guide Table -->
      <div class="guide-table-section">
        <div class="divider-gold"><span>✦</span></div>
        <h2 style="text-align:center;margin:2rem 0;font-family:var(--font-serif);font-size:2.5rem;font-weight:300;color:var(--ivory)">
          Chakra & Crystal Reference
        </h2>
        <div class="chakra-table">
          <div class="chakra-row chakra-row--head">
            <span>Chakra</span><span>Colour</span><span>Location</span><span>Crystals</span><span>Intention</span>
          </div>
          <div v-for="row in chakraTable" :key="row.chakra" class="chakra-row" :style="{'--accent': row.color}">
            <span class="chakra-name"><span class="dot" :style="{background: row.color}"></span>{{ row.chakra }}</span>
            <span>{{ row.colour }}</span>
            <span>{{ row.location }}</span>
            <span>{{ row.crystals }}</span>
            <span>{{ row.intention }}</span>
          </div>
        </div>
      </div>

      <div class="guide-cta">
        <h3>Ready to Begin?</h3>
        <p class="body-serif">Explore our full collection of hand-sourced, certified crystals.</p>
        <router-link to="/shop" class="btn btn-gold" style="margin-top:1.5rem"><span>Shop All Crystals</span></router-link>
      </div>
    </div>
  </main>
</template>

<script setup>
const chapters = [
  {
    num: '01',
    title: 'What Are Crystals?',
    content: 'Crystals are solid materials whose atoms are arranged in a highly ordered, repeating pattern extending in all three spatial dimensions — a crystal lattice. This perfect atomic order is what gives crystals their extraordinary physical properties: their hardness, their ability to conduct electricity, their optical clarity, and — many believe — their energetic qualities. Every crystal began as liquid or gas, cooled and compressed over millions of years until its atoms settled into this perfect mathematical pattern.',
    crystals: ['Clear Quartz', 'Amethyst', 'Rose Quartz', 'Labradorite']
  },
  {
    num: '02',
    title: 'How to Choose Your First Crystal',
    content: 'The oldest advice is the most reliable: let the crystal choose you. Pick up a crystal and notice how it feels — not just its texture, but your own response to it. Do you feel drawn to it? Does something settle in you when you hold it? Trust that response. Beyond intuition, consider your current intention. Are you seeking calm? (Amethyst, Selenite) Protection? (Black Tourmaline) Love? (Rose Quartz) Clarity? (Clear Quartz) Abundance? (Citrine) Each crystal tradition associates stones with specific energetic qualities, and these associations have been remarkably consistent across cultures and centuries.',
    crystals: ['Amethyst', 'Black Tourmaline', 'Rose Quartz', 'Clear Quartz', 'Citrine']
  },
  {
    num: '03',
    title: 'How to Cleanse Your Crystals',
    content: 'Crystals are thought to absorb energy from their environments and the people who handle them. Regular cleansing resets them to their natural state. The most effective methods: Moonlight (place crystals outside or on a windowsill during a full moon overnight). Selenite (place your crystals on a Selenite plate — one of the only crystals that cleanses others). Sound (use a singing bowl or tuning fork near your crystals). Running water (for hardy crystals like Quartz — never for soft stones like Selenite). Smoke cleansing (pass crystals through the smoke of sacred herbs). Never cleanse in salt water — it can damage many crystals permanently.',
  },
  {
    num: '04',
    title: 'Working with Your Crystals',
    content: 'Crystals are tools for intention. The simplest practice: hold your crystal in your non-dominant hand (your receiving hand), close your eyes, and state your intention clearly — either silently or aloud. You might carry it in your pocket or bag throughout the day, place it on your desk or bedside table, use it during meditation (hold it, or place it on the relevant chakra point on your body), or create a crystal grid — an arrangement of multiple crystals in a geometric pattern around a central stone.',
  },
]

const chakraTable = [
  { chakra: 'Root',         colour: 'Red / Black',  color: '#c0392b', location: 'Base of spine',  crystals: 'Black Tourmaline, Red Jasper', intention: 'Safety, grounding, security' },
  { chakra: 'Sacral',       colour: 'Orange',       color: '#e67e22', location: 'Lower abdomen',  crystals: 'Carnelian, Citrine',           intention: 'Creativity, pleasure, flow' },
  { chakra: 'Solar Plexus', colour: 'Yellow',       color: '#f1c40f', location: 'Upper abdomen',  crystals: 'Citrine, Tiger\'s Eye',        intention: 'Confidence, will, identity' },
  { chakra: 'Heart',        colour: 'Green / Pink', color: '#27ae60', location: 'Centre of chest', crystals: 'Rose Quartz, Green Aventurine', intention: 'Love, compassion, healing' },
  { chakra: 'Throat',       colour: 'Blue',         color: '#2980b9', location: 'Throat',          crystals: 'Lapis Lazuli, Blue Topaz',     intention: 'Truth, expression, clarity' },
  { chakra: 'Third Eye',    colour: 'Indigo',       color: '#8e44ad', location: 'Between brows',   crystals: 'Amethyst, Labradorite',        intention: 'Intuition, insight, vision' },
  { chakra: 'Crown',        colour: 'Violet / White',color: '#bdc3c7',location: 'Top of head',    crystals: 'Clear Quartz, Selenite',       intention: 'Connection, consciousness' },
]
</script>

<style scoped>
.guide-hero {
  text-align: center; padding: 5rem 2rem 3rem;
  display: flex; flex-direction: column; align-items: center;
}
.guide-hero .heading-display em { color: var(--gold); font-style: italic; }

.guide-body { max-width: 860px; padding-bottom: 5rem; }

.guide-chapter {
  display: grid; grid-template-columns: 80px 1fr; gap: 2rem;
  padding: 3rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.guide-chapter__num {
  font-family: var(--font-serif); font-size: 3.5rem; font-weight: 300;
  color: rgba(201,168,76,0.15); line-height: 1; padding-top: 0.25rem;
}
.guide-chapter__content h2 {
  font-family: var(--font-serif); font-size: 1.8rem; font-weight: 300;
  color: var(--ivory); margin-bottom: 1rem;
}
.guide-crystals { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1.25rem; }
.crystal-tag {
  font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase;
  border: 1px solid rgba(201,168,76,0.2); color: var(--gold-dim);
  padding: 0.25rem 0.6rem;
}

.guide-table-section { padding: 3rem 0 4rem; }
.chakra-table { display: flex; flex-direction: column; border: 1px solid rgba(201,168,76,0.12); overflow: auto; }
.chakra-row {
  display: grid; grid-template-columns: 1.2fr 1fr 1fr 1.5fr 1.5fr;
  gap: 1rem; padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  font-size: 0.8rem; color: var(--ivory-dim);
  transition: background 0.2s;
}
.chakra-row:hover { background: rgba(255,255,255,0.02); }
.chakra-row--head { background: var(--charcoal); font-size: 0.62rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--gold-dim); }
.chakra-name { display: flex; align-items: center; gap: 0.5rem; color: var(--ivory); }
.dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }

.guide-cta { text-align: center; padding: 4rem 0; }
.guide-cta h3 { font-family: var(--font-serif); font-size: 2.5rem; font-weight: 300; color: var(--ivory); margin-bottom: 0.5rem; }

@media (max-width: 600px) { .guide-chapter { grid-template-columns: 1fr; } }
</style>
