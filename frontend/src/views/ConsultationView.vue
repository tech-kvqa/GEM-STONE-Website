<template>
  <main class="consult-page" :style="{ paddingTop: 'var(--nav-h)' }">

    <!-- Hero -->
    <section class="consult-hero">
      <div class="consult-hero__bg">
        <img src="https://images.unsplash.com/photo-1610890690846-4a7e5adacce8?w=1600&q=90" alt="Crystal Consultation" />
        <div class="consult-hero__overlay"></div>
      </div>
      <div class="consult-hero__content">
        <p class="label-caps" style="color:var(--dusty-rose)">One-on-One with Ritz</p>
        <h1 class="consult-hero__title">Book Your<br/><em>Crystal Consultation</em></h1>
        <p class="consult-hero__sub">
          A personal 45-minute session with Ritz — your intentions, your energy, your perfect crystals.
        </p>
      </div>
    </section>

    <!-- Booking UI -->
    <section class="section" style="background: var(--bg-main)">
      <div class="container">
        <div class="booking-layout">

          <!-- Left: Info -->
          <div class="booking-info">
            <h2 class="booking-info__title">What to Expect</h2>
            <div class="booking-features">
              <div v-for="f in features" :key="f.title" class="booking-feature">
                <div class="booking-feature__icon">{{ f.icon }}</div>
                <div>
                  <h4>{{ f.title }}</h4>
                  <p>{{ f.desc }}</p>
                </div>
              </div>
            </div>
            <div class="booking-price-box">
              <div class="booking-price-box__label label-caps">Session Details</div>
              <div class="booking-price-box__row"><span>Duration</span><strong>45 minutes</strong></div>
              <div class="booking-price-box__row"><span>Format</span><strong>Video Call (Google Meet)</strong></div>
              <div class="booking-price-box__row"><span>Investment</span><strong class="text-gold">₹999 / session</strong></div>
              <div class="booking-price-box__row"><span>Availability</span><strong>Mon–Sat, 10 AM – 6 PM IST</strong></div>
              <p class="booking-price-box__note">✦ A crystal worth ₹500+ is gifted to every new client.</p>
            </div>
          </div>

          <!-- Right: Booking Form -->
          <div class="booking-form-wrap">
            <h2 class="booking-form__title">Select a Date & Time</h2>

            <!-- Step 1: Pick Date -->
            <div class="step" v-if="step === 1">
              <p class="step__label label-caps">Step 1 — Choose a Date</p>
              <div class="calendar-grid">
                <button
                  v-for="d in availableDates" :key="d.iso"
                  :class="['cal-day', { selected: selectedDate === d.iso, disabled: d.disabled }]"
                  :disabled="d.disabled"
                  @click="selectDate(d.iso)"
                >
                  <span class="cal-day__dow">{{ d.dow }}</span>
                  <span class="cal-day__num">{{ d.num }}</span>
                  <span class="cal-day__mon">{{ d.mon }}</span>
                </button>
              </div>
              <div class="step-nav">
                <button class="btn btn-gold w-full" :disabled="!selectedDate" @click="step = 2">
                  <span>Continue to Time Slots →</span>
                </button>
              </div>
            </div>

            <!-- Step 2: Pick Time -->
            <div class="step" v-if="step === 2">
              <p class="step__label label-caps">Step 2 — Choose a Time (IST)</p>
              <p class="step__date-chosen">{{ formattedDate }}</p>
              <div class="time-grid">
                <button
                  v-for="slot in timeSlots" :key="slot.value"
                  :class="['time-slot', { selected: selectedTime === slot.value, booked: slot.booked }]"
                  :disabled="slot.booked"
                  @click="selectedTime = slot.value"
                >
                  <span class="time-slot__time">{{ slot.label }}</span>
                  <span class="time-slot__status">{{ slot.booked ? 'Booked' : 'Available' }}</span>
                </button>
              </div>
              <div class="step-nav">
                <button class="btn btn-ghost" @click="step = 1"><span>← Back</span></button>
                <button class="btn btn-gold" :disabled="!selectedTime" @click="step = 3"><span>Continue →</span></button>
              </div>
            </div>

            <!-- Step 3: Your Details -->
            <div class="step" v-if="step === 3">
              <p class="step__label label-caps">Step 3 — Your Details</p>
              <div class="booking-summary-mini">
                📅 {{ formattedDate }} &nbsp;&nbsp; 🕐 {{ selectedTime }}
                <button class="change-link" @click="step = 1">Change</button>
              </div>
              <div class="fields">
                <div class="field">
                  <label class="input-label">Full Name *</label>
                  <input v-model="form.name" type="text" class="input-field" placeholder="Your name" required />
                </div>
                <div class="field">
                  <label class="input-label">Email *</label>
                  <input v-model="form.email" type="email" class="input-field" placeholder="your@email.com" required />
                </div>
                <div class="field">
                  <label class="input-label">Phone (WhatsApp) *</label>
                  <input v-model="form.phone" type="tel" class="input-field" placeholder="+91 00000 00000" required />
                </div>
                <div class="field">
                  <label class="input-label">Your Intention / What you're seeking</label>
                  <textarea v-model="form.intention" class="input-field" rows="3"
                    placeholder="E.g. I'm looking for healing around grief, or I want crystals to support my meditation practice…"></textarea>
                </div>
              </div>
              <p v-if="formError" class="error-msg">{{ formError }}</p>
              <div class="step-nav">
                <button class="btn btn-ghost" @click="step = 2"><span>← Back</span></button>
                <button class="btn btn-gold" @click="submitBooking" :disabled="submitting">
                  <span>{{ submitting ? 'Confirming…' : 'Confirm Booking' }}</span>
                </button>
              </div>
            </div>

            <!-- Step 4: Confirmed -->
            <div class="step step--success" v-if="step === 4">
              <div class="success-icon">✦</div>
              <h3>Booking Confirmed!</h3>
              <p class="success-msg">
                Thank you, {{ form.name.split(' ')[0] }}. Ritz will reach out to you at <strong>{{ form.email }}</strong>
                with your Google Meet link within 2 hours.
              </p>
              <div class="booking-recap">
                <div>📅 {{ formattedDate }}</div>
                <div>🕐 {{ selectedTime }}</div>
                <div>📧 Confirmation sent to {{ form.email }}</div>
              </div>
              <router-link to="/shop" class="btn btn-gold" style="margin-top:1.5rem"><span>Explore Crystals While You Wait</span></router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="section faq-section" style="background:var(--bg-section)">
      <div class="container">
        <div class="section-head">
          <p class="label-caps">Common Questions</p>
          <h2 class="heading-section">Before You Book</h2>
        </div>
        <div class="faq-grid">
          <div v-for="q in faqs" :key="q.q" class="faq-item">
            <h4>{{ q.q }}</h4>
            <p>{{ q.a }}</p>
          </div>
        </div>
      </div>
    </section>

  </main>
</template>

<script setup>
import { ref, computed } from 'vue'
import { toast } from 'vue3-toastify'

const step         = ref(1)
const selectedDate = ref('')
const selectedTime = ref('')
const submitting   = ref(false)
const formError    = ref('')
const form = ref({ name: '', email: '', phone: '', intention: '' })

// Generate next 14 working days (Mon–Sat), skip Sundays
const availableDates = computed(() => {
  const days = []
  const now = new Date()
  const dows = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
  const mons = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  let d = new Date(now)
  d.setDate(d.getDate() + 1) // start tomorrow
  while (days.length < 14) {
    if (d.getDay() !== 0) { // skip Sunday
      days.push({
        iso: d.toISOString().split('T')[0],
        dow: dows[d.getDay()],
        num: d.getDate(),
        mon: mons[d.getMonth()],
        disabled: false,
      })
    }
    d.setDate(d.getDate() + 1)
  }
  return days
})

// Time slots 10 AM – 6 PM, 45-min sessions
const allSlots = [
  '10:00 AM','10:45 AM','11:30 AM','12:15 PM',
  '02:00 PM','02:45 PM','03:30 PM','04:15 PM','05:00 PM','05:45 PM'
]
// Pseudo-random "booked" slots based on selected date
const timeSlots = computed(() => {
  const seed = selectedDate.value ? selectedDate.value.charCodeAt(9) : 0
  return allSlots.map((t, i) => ({
    label: t,
    value: t,
    booked: ((seed + i * 3) % 7) === 0 // deterministic pseudo-random booking
  }))
})

const formattedDate = computed(() => {
  if (!selectedDate.value) return ''
  const d = new Date(selectedDate.value + 'T12:00:00')
  return d.toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
})

function selectDate(iso) {
  selectedDate.value = iso
  selectedTime.value = ''
}

function submitBooking() {
  formError.value = ''
  if (!form.value.name || !form.value.email || !form.value.phone) {
    formError.value = 'Please fill in all required fields.'
    return
  }
  submitting.value = true
  setTimeout(() => {
    submitting.value = false
    step.value = 4
    toast.success('Booking confirmed! Check your email ✦')
  }, 1200)
}

const features = [
  { icon: '💎', title: 'Personalised Crystal Curation', desc: 'Ritz handpicks crystals based on your unique energy and intentions.' },
  { icon: '🌸', title: 'Healing & Intention Guidance', desc: 'Learn exactly how to work with each crystal for maximum benefit.' },
  { icon: '🔮', title: 'Chakra Assessment', desc: 'A gentle exploration of which energy centres need support right now.' },
  { icon: '🎁', title: 'Free Crystal Gift', desc: 'Every new client receives a curated crystal worth ₹500+ as a welcome gift.' },
]

const faqs = [
  { q: 'Do I need to know anything about crystals beforehand?', a: 'Not at all. The consultation is designed for complete beginners and seasoned collectors alike.' },
  { q: 'What platform do we use?', a: 'All consultations are held via Google Meet. You\'ll receive a link in your confirmation email.' },
  { q: 'Can I reschedule?', a: 'Yes — up to 6 hours before your session. Just email us or WhatsApp Ritz directly.' },
  { q: 'Is payment taken now?', a: 'A booking confirmation email is sent first. Payment is made via Razorpay link 24 hours before your session.' },
]
</script>

<style scoped>
.consult-hero {
  position: relative; height: 55vh; min-height: 360px;
  display: flex; align-items: center; justify-content: center; text-align: center;
  overflow: hidden;
}
.consult-hero__bg { position: absolute; inset: 0; }
.consult-hero__bg img { width: 100%; height: 100%; object-fit: cover; }
.consult-hero__overlay {
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(42,31,26,0.45), rgba(42,31,26,0.7));
}
.consult-hero__content { position: relative; z-index: 2; padding: 0 1.5rem; }
.consult-hero__title {
  font-family: var(--font-serif); font-size: clamp(2.5rem, 6vw, 5rem);
  font-weight: 300; color: #fff; line-height: 1.1; margin: 0.75rem 0;
}
.consult-hero__title em { color: var(--dusty-rose); font-style: italic; }
.consult-hero__sub { color: rgba(255,255,255,0.8); font-size: 1rem; max-width: 500px; margin: 0 auto; }

.booking-layout { display: grid; grid-template-columns: 1fr 1.4fr; gap: 4rem; align-items: start; }

.booking-info__title {
  font-family: var(--font-serif); font-size: 1.8rem; font-weight: 300;
  color: var(--ink); margin-bottom: 1.75rem;
}
.booking-features { display: flex; flex-direction: column; gap: 1.25rem; margin-bottom: 2rem; }
.booking-feature { display: flex; gap: 1rem; }
.booking-feature__icon { font-size: 1.5rem; flex-shrink: 0; }
.booking-feature h4 { font-family: var(--font-serif); font-size: 0.95rem; font-weight: 400; color: var(--ink); margin-bottom: 0.2rem; }
.booking-feature p { font-size: 0.8rem; color: var(--muted); line-height: 1.6; }

.booking-price-box {
  border: 1px solid var(--blush-mid); padding: 1.5rem; background: var(--blush-light);
}
.booking-price-box__label { margin-bottom: 1rem; }
.booking-price-box__row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.5rem 0; border-bottom: 1px solid var(--blush); font-size: 0.82rem;
}
.booking-price-box__row span { color: var(--muted); }
.booking-price-box__row strong { color: var(--ink); font-weight: 500; }
.booking-price-box__note { font-size: 0.72rem; color: var(--rose-gold); margin-top: 0.85rem; }

.booking-form-wrap {
  background: #fff; border: 1px solid var(--blush);
  padding: 2.5rem; box-shadow: 0 4px 30px rgba(196,135,106,0.08);
}
.booking-form__title {
  font-family: var(--font-serif); font-size: 1.6rem; font-weight: 300;
  color: var(--ink); margin-bottom: 2rem;
}
.step__label { margin-bottom: 1.25rem; display: block; }
.step__date-chosen { font-family: var(--font-serif); font-size: 1rem; color: var(--rose-gold); margin-bottom: 1.25rem; }

.calendar-grid {
  display: grid; grid-template-columns: repeat(7, 1fr); gap: 0.5rem; margin-bottom: 1.5rem;
}
.cal-day {
  display: flex; flex-direction: column; align-items: center; gap: 0.15rem;
  padding: 0.65rem 0.25rem; border: 1px solid var(--blush); background: #fff;
  cursor: pointer; transition: all 0.2s;
}
.cal-day:hover:not(.disabled) { border-color: var(--rose-gold); background: var(--blush-light); }
.cal-day.selected { background: var(--rose-gold); border-color: var(--rose-gold); }
.cal-day.selected .cal-day__dow,
.cal-day.selected .cal-day__num,
.cal-day.selected .cal-day__mon { color: #fff; }
.cal-day.disabled { opacity: 0.35; cursor: not-allowed; }
.cal-day__dow { font-size: 0.5rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--rose-gold-dim); }
.cal-day__num { font-family: var(--font-serif); font-size: 1.15rem; font-weight: 300; color: var(--ink); }
.cal-day__mon { font-size: 0.48rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }

.time-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.6rem; margin-bottom: 1.5rem; }
.time-slot {
  padding: 0.75rem 1rem; border: 1px solid var(--blush); background: #fff;
  display: flex; justify-content: space-between; align-items: center;
  cursor: pointer; transition: all 0.2s; text-align: left;
}
.time-slot:hover:not(.booked) { border-color: var(--rose-gold); background: var(--blush-light); }
.time-slot.selected { background: var(--rose-gold); border-color: var(--rose-gold); }
.time-slot.selected .time-slot__time,
.time-slot.selected .time-slot__status { color: #fff; }
.time-slot.booked { opacity: 0.45; cursor: not-allowed; }
.time-slot__time { font-family: var(--font-serif); font-size: 0.95rem; color: var(--ink); }
.time-slot__status { font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--rose-gold-dim); }
.time-slot.booked .time-slot__status { color: #c07070; }

.fields { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.25rem; }
.field {}
.input-field textarea { resize: vertical; min-height: 80px; }
.booking-summary-mini {
  background: var(--blush-light); border: 1px solid var(--blush);
  padding: 0.75rem 1rem; font-size: 0.8rem; color: var(--warm-brown);
  margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;
}
.change-link {
  color: var(--rose-gold); font-size: 0.68rem; text-decoration: underline;
  cursor: pointer; margin-left: auto;
}
.error-msg { font-size: 0.76rem; color: #b05050; padding: 0.6rem; background: rgba(176,80,80,0.06); border: 1px solid rgba(176,80,80,0.2); margin-bottom: 1rem; }

.step-nav { display: flex; gap: 0.75rem; margin-top: 1rem; }
.w-full { width: 100%; }

.step--success { text-align: center; padding: 1rem 0; }
.success-icon { font-size: 2.5rem; color: var(--rose-gold); animation: float 3s ease-in-out infinite; margin-bottom: 1rem; }
.step--success h3 { font-family: var(--font-serif); font-size: 1.8rem; font-weight: 300; color: var(--ink); margin-bottom: 0.75rem; }
.success-msg { font-size: 0.88rem; color: var(--muted); line-height: 1.7; margin-bottom: 1.5rem; }
.booking-recap {
  background: var(--blush-light); border: 1px solid var(--blush);
  padding: 1rem 1.25rem; font-size: 0.82rem; color: var(--warm-brown);
  display: flex; flex-direction: column; gap: 0.4rem; text-align: left;
}

.faq-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
.faq-item { padding: 1.5rem; border: 1px solid var(--blush); background: #fff; }
.faq-item h4 { font-family: var(--font-serif); font-size: 1rem; font-weight: 400; color: var(--ink); margin-bottom: 0.5rem; }
.faq-item p { font-size: 0.82rem; color: var(--muted); line-height: 1.7; }

@media (max-width: 900px) {
  .booking-layout { grid-template-columns: 1fr; gap: 2rem; }
  .calendar-grid { grid-template-columns: repeat(5, 1fr); }
}
@media (max-width: 600px) {
  .calendar-grid { grid-template-columns: repeat(4, 1fr); }
  .faq-grid { grid-template-columns: 1fr; }
  .time-grid { grid-template-columns: 1fr; }
}
</style>
