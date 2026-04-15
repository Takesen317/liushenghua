<template>
  <div class="flowing-wave-bg">
    <!-- Main Wave -->
    <svg class="wave-svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
      <defs>
        <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ff6b35" />
          <stop offset="50%" stop-color="#ff3333" />
          <stop offset="100%" stop-color="#ff6b35" />
        </linearGradient>
        <linearGradient id="waveGradient2" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ff4444" />
          <stop offset="50%" stop-color="#ff6666" />
          <stop offset="100%" stop-color="#ff4444" />
        </linearGradient>
      </defs>

      <!-- Primary Wave -->
      <path
        class="wave wave-1"
        fill="url(#waveGradient)"
        d="M0,192L48,176C96,160,192,128,288,138.7C384,149,480,203,576,208C672,213,768,171,864,154.7C960,139,1056,149,1152,165.3C1248,181,1344,203,1392,213.3L1440,224L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
      />

      <!-- Secondary Wave (smaller) -->
      <path
        class="wave wave-2"
        fill="url(#waveGradient2)"
        opacity="0.6"
        d="M0,256L48,240C96,224,192,192,288,181.3C384,171,480,181,576,192C672,203,768,213,864,197.3C960,181,1056,139,1152,128C1248,117,1344,139,1392,149.3L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
      />

      <!-- Accent Line -->
      <path
        class="wave wave-3"
        fill="none"
        stroke="#ff6b35"
        stroke-width="2"
        opacity="0.4"
        d="M0,200C240,120,480,280,720,200C960,120,1200,240,1440,160"
      />
    </svg>

    <!-- Ambient Glow -->
    <div class="ambient-glow"></div>

    <!-- Floating Particles -->
    <div class="particles">
      <div v-for="i in 6" :key="i" class="particle" :class="`particle-${i}`"></div>
    </div>
  </div>
</template>

<script setup>
// No props needed for this static design
</script>

<style scoped>
.flowing-wave-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
  background: linear-gradient(
    180deg,
    #050505 0%,
    #0a0a0a 30%,
    #0f0f0f 60%,
    #050505 100%
  );
}

/* Wave SVG */
.wave-svg {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 65vh;
  min-height: 400px;
  max-height: 600px;
}

/* Wave Animations */
.wave {
  transform-origin: center;
}

.wave-1 {
  animation: wave-float 8s ease-in-out infinite;
}

.wave-2 {
  animation: wave-float 6s ease-in-out infinite reverse;
  animation-delay: -2s;
}

.wave-3 {
  animation: dash-flow 3s linear infinite;
  stroke-dasharray: 10, 15;
}

@keyframes wave-float {
  0%, 100% {
    transform: translateX(0) translateY(0);
  }
  25% {
    transform: translateX(-5px) translateY(3px);
  }
  50% {
    transform: translateX(0) translateY(0);
  }
  75% {
    transform: translateX(5px) translateY(-3px);
  }
}

@keyframes dash-flow {
  0% {
    stroke-dashoffset: 0;
  }
  100% {
    stroke-dashoffset: -50;
  }
}

/* Ambient Glow */
.ambient-glow {
  position: absolute;
  bottom: 20%;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 300px;
  background: radial-gradient(
    ellipse at center,
    rgba(255, 51, 51, 0.15) 0%,
    rgba(255, 51, 51, 0.05) 40%,
    transparent 70%
  );
  filter: blur(40px);
  animation: glow-pulse 4s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% {
    opacity: 0.6;
    transform: translateX(-50%) scale(1);
  }
  50% {
    opacity: 1;
    transform: translateX(-50%) scale(1.1);
  }
}

/* Floating Particles */
.particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 107, 53, 0.6);
  border-radius: 50%;
  animation: float-up 12s linear infinite;
}

.particle-1 {
  left: 10%;
  animation-delay: 0s;
  animation-duration: 15s;
}

.particle-2 {
  left: 25%;
  animation-delay: -3s;
  animation-duration: 12s;
}

.particle-3 {
  left: 45%;
  animation-delay: -6s;
  animation-duration: 18s;
}

.particle-4 {
  left: 65%;
  animation-delay: -2s;
  animation-duration: 14s;
}

.particle-5 {
  left: 80%;
  animation-delay: -8s;
  animation-duration: 16s;
}

.particle-6 {
  left: 90%;
  animation-delay: -5s;
  animation-duration: 13s;
}

@keyframes float-up {
  0% {
    transform: translateY(100vh) scale(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
    transform: translateY(90vh) scale(1);
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-10vh) scale(0.5);
    opacity: 0;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .wave-svg {
    height: 50vh;
    min-height: 300px;
  }

  .ambient-glow {
    width: 100%;
    bottom: 25%;
  }

  .particle {
    width: 3px;
    height: 3px;
  }
}
</style>
