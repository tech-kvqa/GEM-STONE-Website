<template>
  <main class="story-page">
    <div style="height: var(--nav-h)"></div>

    <!-- Hero -->
    <section class="story-hero">
      <img src="https://images.unsplash.com/photo-1535412833400-40b4f58cbf04?w=1600" alt="Our Story" />
      <div class="story-hero__overlay">
        <p class="label-caps">The Crystal Luxe Story</p>
        <h1>Born from a Belief<br/><em>in the Earth's Wisdom</em></h1>
      </div>
    </section>

    <!-- Story Body -->
    <section class="section">
      <div class="container story-body">
        <div class="story-block">
          <div class="story-block__mark">✦</div>
          <p class="label-caps" style="text-align:center;margin-bottom:1rem">Our Origin</p>
          <h2>The Beginning</h2>
          <p class="body-serif">
            Crystal Luxe was born in 2019 from a single obsession: the belief that the earth's most beautiful
            creations deserve to be experienced, not just collected. Our founder, a geologist and long-time
            crystal enthusiast, grew tired of the market's compromise — dyed stones, synthetic fakes,
            and crystals sourced without regard for the communities that mine them.
          </p>
          <p class="body-serif" style="margin-top:1rem">
            She set out on a different path — traveling to Madagascar, Uruguay, Brazil, and the high-altitude
            mines of Himachal Pradesh to find what she described as "the crystals that speak when you hold them."
            The ones you don't put down.
          </p>
        </div>

        <div class="story-image-break">
          <img src="https://images.unsplash.com/photo-1567225557594-88d73398014a?w=1200" alt="Crystal Collection" />
        </div>

        <div class="story-block">
          <div class="story-block__mark">✦</div>
          <p class="label-caps" style="text-align:center;margin-bottom:1rem">Our Logo</p>
          <h2>The Six-Pointed Star <em>✦</em></h2>
          <p class="body-serif">
            Our brand mark is not decoration — it is a declaration. The six-pointed crystal star (✦) 
            represents the perfect lattice structure found in all crystalline matter: the orderly, 
            repeating pattern through which atoms arrange themselves into the stones we carry.
          </p>
          <p class="body-serif" style="margin-top:1rem">
            It is also the shape of a snowflake, of a water molecule viewed under a microscope — the 
            geometry of nature at its most precise. At Crystal Luxe, we believe in this precision. 
            Every crystal we carry has been formed by these same perfect mathematical forces, 
            over millions of years, in the dark heart of the earth.
          </p>
          <p class="body-serif" style="margin-top:1rem">
            The ✦ is our promise: that what you receive from us is as genuine, as precisely formed, 
            and as honestly presented as the crystal it represents.
          </p>
        </div>

        <!-- Values -->
        <div class="story-values">
          <div class="divider-gold"><span>✦</span></div>
          <p class="label-caps" style="text-align:center;margin-bottom:2rem;margin-top:1.5rem">What We Stand For</p>
          <div class="values-grid">
            <div v-for="v in values" :key="v.title" class="value-card">
              <div class="value-card__icon">{{ v.icon }}</div>
              <h4>{{ v.title }}</h4>
              <p>{{ v.desc }}</p>
            </div>
          </div>
        </div>

        <div class="story-block">
          <div class="story-block__mark">✦</div>
          <p class="label-caps" style="text-align:center;margin-bottom:1rem">Our Promise</p>
          <h2>The Crystal Luxe Guarantee</h2>
          <p class="body-serif">
            Every single crystal in our collection is 100% natural — no treatments, no dyes, no synthetics, 
            ever. We work with independent gemological labs to verify authenticity, and we provide 
            certificates for all significant pieces on request.
          </p>
          <p class="body-serif" style="margin-top:1rem">
            We pay fair prices to our mining partners. We use biodegradable packaging. We plant a tree 
            for every order above ₹5,000. And we will always, always tell you the truth about what you 
            are buying — including its limitations, its country of origin, and any natural variations 
            you should expect.
          </p>
          <p class="body-serif" style="margin-top:1rem;font-style:italic;color:var(--gold-dim)">
            This is not just a business. It is a calling. We hope you feel the difference.
          </p>
        </div>

        <div class="story-cta">
          <router-link to="/shop" class="btn btn-gold"><span>Explore the Collection</span></router-link>
          <router-link to="/crystal-guide" class="btn btn-ghost"><span>Read the Crystal Guide</span></router-link>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
const values = [
  { icon: '🌍', title: 'Ethical Sourcing', desc: 'We visit our mines personally. We know who digs our crystals, and we pay them fairly.' },
  { icon: '🔬', title: 'Scientific Authenticity', desc: 'Every stone is verified natural. No heat treatment unless stated. No synthetics. Ever.' },
  { icon: '✦',  title: 'Intentional Curation', desc: 'We don\'t carry thousands of SKUs. We carry the crystals we would keep ourselves.' },
  { icon: '🌱', title: 'Environmental Commitment', desc: 'Biodegradable packaging, carbon-offset shipping, and a tree planted for every large order.' },
]
</script>

<style scoped>
.story-hero { position: relative; height: 70vh; overflow: hidden; }
.story-hero img { width: 100%; height: 100%; object-fit: cover; filter: brightness(0.4); }
.story-hero__overlay {
  position: absolute; inset: 0;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center; padding: 2rem;
}
.story-hero__overlay .label-caps { margin-bottom: 1rem; }
.story-hero__overlay h1 {
  font-family: var(--font-serif);
  font-size: clamp(2.5rem, 6vw, 5.5rem);
  font-weight: 300; color: var(--ivory); line-height: 1.15;
}
.story-hero__overlay h1 em { color: var(--gold); font-style: italic; }

.story-body { max-width: 780px; }
.story-block { text-align: center; margin-bottom: 4rem; }
.story-block__mark { font-size: 1.5rem; color: var(--gold-dim); margin-bottom: 1rem; }
.story-block h2 {
  font-family: var(--font-serif); font-size: clamp(2rem, 3.5vw, 3rem);
  font-weight: 300; color: var(--ivory); margin-bottom: 1.5rem;
}
.story-block h2 em { color: var(--gold); font-style: italic; }

.story-image-break {
  width: 100vw; margin-left: calc(50% - 50vw);
  height: 500px; margin-bottom: 4rem; overflow: hidden;
}
.story-image-break img { width: 100%; height: 100%; object-fit: cover; }

.values-grid {
  display: grid; grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem; margin-bottom: 4rem;
}
.value-card {
  padding: 2rem; text-align: left;
  border: 1px solid rgba(201,168,76,0.1);
  background: var(--charcoal);
}
.value-card__icon { font-size: 1.6rem; margin-bottom: 0.75rem; }
.value-card h4 { font-family: var(--font-serif); font-size: 1.1rem; color: var(--ivory); margin-bottom: 0.5rem; }
.value-card p { font-size: 0.82rem; color: var(--ivory-dim); opacity: 0.6; line-height: 1.7; }

.story-cta { display: flex; gap: 1rem; justify-content: center; margin-top: 3rem; flex-wrap: wrap; }

@media (max-width: 600px) { .values-grid { grid-template-columns: 1fr; } }
</style>
