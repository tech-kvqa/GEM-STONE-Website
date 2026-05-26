<template>
  <main style="min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:2rem;background:var(--bg-main)">
    <div>
      <div style="font-size:4rem;color:var(--blush-deep);animation:float 3s ease-in-out infinite;margin-bottom:1.5rem">✦</div>
      <h1 style="font-family:var(--font-serif);font-size:clamp(3rem,8vw,6rem);font-weight:300;color:var(--ink);line-height:1">404</h1>
      <p style="font-family:var(--font-serif);font-size:1.2rem;color:var(--muted);margin:0.75rem 0 2rem">This page has gently returned to the earth.</p>
      <router-link to="/" class="btn btn-gold"><span>Return Home</span></router-link>
    </div>
  </main>
</template>
<script setup></script>
