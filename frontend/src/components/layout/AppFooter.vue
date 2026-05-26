<template>
  <footer class="footer">
    <!-- Top petal divider -->
    <div class="footer__divider">
      <span class="footer__petal">✦</span>
    </div>

    <div class="footer__top">
      <div class="footer__brand">
        <img src="/logo.png" alt="Glow With Ritz" class="footer__logo-img" />
        <p class="footer__desc">
          Born from a love of crystals and a belief in their gentle power —
          every piece we carry is hand-selected for beauty, authenticity, and energy.
          Glow with what the earth made for you.
        </p>
        <div class="footer__social">
          <a href="#" aria-label="Instagram">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.5" fill="currentColor"/></svg>
          </a>
          <a href="#" aria-label="Pinterest">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2C6.48 2 2 6.48 2 12c0 4.24 2.65 7.86 6.39 9.29-.09-.78-.17-1.98.03-2.83.2-.77 1.3-5.5 1.3-5.5s-.33-.67-.33-1.65c0-1.55.9-2.71 2.01-2.71.95 0 1.41.71 1.41 1.57 0 .96-.61 2.39-.93 3.72-.26 1.11.56 2.02 1.65 2.02 1.98 0 3.31-2.54 3.31-5.55 0-2.29-1.55-3.89-3.77-3.89-2.57 0-4.07 1.93-4.07 3.92 0 .78.3 1.61.67 2.07.07.09.08.17.06.26l-.25 1.01c-.04.16-.13.2-.3.12-1.12-.52-1.82-2.17-1.82-3.49 0-2.84 2.06-5.44 5.94-5.44 3.12 0 5.55 2.22 5.55 5.19 0 3.1-1.95 5.59-4.65 5.59-.91 0-1.76-.47-2.05-1.03l-.56 2.07c-.2.78-.75 1.75-1.12 2.34.85.26 1.74.4 2.68.4 5.52 0 10-4.48 10-10S17.52 2 12 2z"/></svg>
          </a>
          <a href="#" aria-label="YouTube">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.95-1.96C18.88 4 12 4 12 4s-6.88 0-8.59.46a2.78 2.78 0 0 0-1.95 1.96A29 29 0 0 0 1 12a29 29 0 0 0 .46 5.58A2.78 2.78 0 0 0 3.41 19.6C5.12 20 12 20 12 20s6.88 0 8.59-.46a2.78 2.78 0 0 0 1.95-1.95A29 29 0 0 0 23 12a29 29 0 0 0-.46-5.58z"/><polygon points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02"/></svg>
          </a>
        </div>
      </div>

      <div class="footer__col">
        <h4>Collections</h4>
        <router-link to="/shop/quartz">Quartz Crystals</router-link>
        <router-link to="/shop/amethyst">Amethyst</router-link>
        <router-link to="/shop/rose-quartz">Rose Quartz</router-link>
        <router-link to="/shop/black-tourmaline">Black Tourmaline</router-link>
        <router-link to="/shop/citrine">Citrine</router-link>
        <router-link to="/shop/labradorite">Labradorite</router-link>
        <router-link to="/shop/selenite">Selenite</router-link>
        <router-link to="/shop/lapis-lazuli">Lapis Lazuli</router-link>
      </div>

      <div class="footer__col">
        <h4>Explore</h4>
        <router-link to="/our-story">Our Story</router-link>
        <router-link to="/crystal-guide">Crystal Guide</router-link>
        <router-link to="/consultation">Book Consultation</router-link>
        <router-link to="/shop?featured=true">Featured</router-link>
        <router-link to="/shop?bestseller=true">Bestsellers</router-link>
        <router-link to="/shop?new_arrival=true">New Arrivals</router-link>
      </div>

      <div class="footer__col">
        <h4>Help</h4>
        <a href="#">Shipping & Delivery</a>
        <a href="#">Returns Policy</a>
        <a href="#">Crystal Care Guide</a>
        <a href="#">Track Your Order</a>
        <a href="#">Contact Us</a>
        <a href="#">FAQ</a>
      </div>
    </div>

    <div class="footer__newsletter">
      <p class="label-caps">The Glow Letter</p>
      <h3>Join the Ritz Circle</h3>
      <p>Crystal stories, rituals, and first access to rare arrivals — delivered with love.</p>
      <form class="footer__form" @submit.prevent="subscribe">
        <input v-model="email" type="email" placeholder="Your email address" required />
        <button type="submit" class="btn btn-gold"><span>Subscribe</span></button>
      </form>
    </div>

    <div class="footer__bottom">
      <p>© {{ new Date().getFullYear() }} Glow With Ritz. All rights reserved.</p>
      <div class="footer__bottom-links">
        <a href="#">Privacy Policy</a>
        <a href="#">Terms & Conditions</a>
        <a href="#">Authenticity Guarantee</a>
      </div>
      <p class="footer__certify">✦ All crystals ethically sourced &amp; certified natural</p>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'
import { toast } from 'vue3-toastify'
const email = ref('')
function subscribe() {
  toast.success('Welcome to the Ritz Circle ✦')
  email.value = ''
}
</script>

<style scoped>
.footer { background: var(--bg-section); border-top: 1px solid var(--blush); }

.footer__divider {
  text-align: center; padding: 2.5rem 0 0;
}
.footer__petal {
  font-size: 1.2rem; color: var(--rose-gold);
  display: inline-block; animation: sparkle 3s ease-in-out infinite;
}

.footer__top {
  display: grid; grid-template-columns: 1.5fr 1fr 1fr 1fr; gap: 3rem;
  max-width: var(--max-w); margin: 0 auto;
  padding: 2.5rem 2.5rem 4rem;
}
.footer__logo-img { height: 80px; width: auto; object-fit: contain; margin-bottom: 1.25rem; }
.footer__desc {
  font-size: 0.84rem; line-height: 1.85;
  color: var(--muted); margin-bottom: 1.5rem;
}
.footer__social { display: flex; gap: 1rem; }
.footer__social a { color: var(--blush-deep); transition: color 0.2s; }
.footer__social a:hover { color: var(--rose-gold); }

.footer__col h4 {
  font-size: 0.62rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--rose-gold); margin-bottom: 1.5rem;
}
.footer__col a {
  display: block; font-size: 0.82rem; color: var(--muted);
  margin-bottom: 0.65rem; transition: color 0.2s, padding-left 0.2s;
}
.footer__col a:hover { color: var(--rose-gold); padding-left: 4px; }

.footer__newsletter {
  text-align: center; padding: 4rem 2.5rem;
  border-top: 1px solid var(--blush); border-bottom: 1px solid var(--blush);
  background: var(--blush-light);
}
.footer__newsletter h3 {
  font-family: var(--font-serif); font-size: 2.2rem; font-weight: 300;
  color: var(--ink); margin: 0.5rem 0;
}
.footer__newsletter p { color: var(--muted); font-size: 0.88rem; margin-bottom: 2rem; }
.footer__form { display: flex; max-width: 420px; margin: 0 auto; }
.footer__form input {
  flex: 1; background: #fff; border: 1px solid var(--blush);
  border-right: none; color: var(--ink);
  padding: 0.85rem 1.1rem; font-family: var(--font-sans); font-size: 0.85rem; outline: none;
}
.footer__form input:focus { border-color: var(--rose-gold); }

.footer__bottom {
  max-width: var(--max-w); margin: 0 auto; padding: 1.5rem 2.5rem;
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;
  font-size: 0.7rem; color: var(--light-muted); letter-spacing: 0.05em;
}
.footer__bottom-links { display: flex; gap: 1.5rem; }
.footer__bottom-links a { color: var(--light-muted); transition: color 0.2s; }
.footer__bottom-links a:hover { color: var(--rose-gold); }
.footer__certify { color: var(--rose-gold-dim); }

@media (max-width: 900px) {
  .footer__top { grid-template-columns: 1fr 1fr; gap: 2rem; padding: 2rem 1.5rem 3rem; }
  .footer__bottom { flex-direction: column; text-align: center; }
}
@media (max-width: 520px) {
  .footer__top { grid-template-columns: 1fr; }
  .footer__form { flex-direction: column; }
  .footer__form input { border-right: 1px solid var(--blush); border-bottom: none; }
}
</style>
