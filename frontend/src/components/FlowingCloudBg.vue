<template>
  <div class="flowing-cloud-bg">
    <!-- Upper Flowing Section -->
    <div class="cloud-section">
      <!-- Mist Layer 1 -->
      <div class="cloud-layer layer-1">
        <div class="mist-wrapper">
          <svg class="cloud-svg" viewBox="0 0 1440 200" preserveAspectRatio="none">
            <defs>
              <filter id="mist-blur">
                <feGaussianBlur stdDeviation="20" />
              </filter>
              <linearGradient id="mist-grad-1" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#ff5533" stop-opacity="0" />
                <stop offset="20%" stop-color="#ff5533" stop-opacity="0.3" />
                <stop offset="80%" stop-color="#ff6644" stop-opacity="0.25" />
                <stop offset="100%" stop-color="#ff5533" stop-opacity="0" />
              </linearGradient>
            </defs>
            <path
              fill="url(#mist-grad-1)"
              filter="url(#mist-blur)"
              d="M0,100 Q180,50 360,80 T720,60 T1080,90 T1440,70 L1440,200 L0,200 Z"
            />
          </svg>
          <!-- Duplicate for seamless loop -->
          <svg class="cloud-svg clone" viewBox="0 0 1440 200" preserveAspectRatio="none">
            <defs>
              <filter id="mist-blur">
                <feGaussianBlur stdDeviation="20" />
              </filter>
              <linearGradient id="mist-grad-1" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#ff5533" stop-opacity="0" />
                <stop offset="20%" stop-color="#ff5533" stop-opacity="0.3" />
                <stop offset="80%" stop-color="#ff6644" stop-opacity="0.25" />
                <stop offset="100%" stop-color="#ff5533" stop-opacity="0" />
              </linearGradient>
            </defs>
            <path
              fill="url(#mist-grad-1)"
              filter="url(#mist-blur)"
              d="M0,100 Q180,50 360,80 T720,60 T1080,90 T1440,70 L1440,200 L0,200 Z"
            />
          </svg>
        </div>
      </div>

      <!-- Mist Layer 2 -->
      <div class="cloud-layer layer-2">
        <div class="mist-wrapper">
          <svg class="cloud-svg" viewBox="0 0 1440 200" preserveAspectRatio="none">
            <defs>
              <filter id="mist-blur-2">
                <feGaussianBlur stdDeviation="15" />
              </filter>
              <linearGradient id="mist-grad-2" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#ff6644" stop-opacity="0" />
                <stop offset="30%" stop-color="#ff5533" stop-opacity="0.35" />
                <stop offset="70%" stop-color="#ff7755" stop-opacity="0.3" />
                <stop offset="100%" stop-color="#ff6644" stop-opacity="0" />
              </linearGradient>
            </defs>
            <path
              fill="url(#mist-grad-2)"
              filter="url(#mist-blur-2)"
              d="M0,120 Q200,60 400,95 T800,65 T1200,100 T1440,75 L1440,200 L0,200 Z"
            />
          </svg>
          <svg class="cloud-svg clone" viewBox="0 0 1440 200" preserveAspectRatio="none">
            <defs>
              <filter id="mist-blur-2">
                <feGaussianBlur stdDeviation="15" />
              </filter>
              <linearGradient id="mist-grad-2" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#ff6644" stop-opacity="0" />
                <stop offset="30%" stop-color="#ff5533" stop-opacity="0.35" />
                <stop offset="70%" stop-color="#ff7755" stop-opacity="0.3" />
                <stop offset="100%" stop-color="#ff6644" stop-opacity="0" />
              </linearGradient>
            </defs>
            <path
              fill="url(#mist-grad-2)"
              filter="url(#mist-blur-2)"
              d="M0,120 Q200,60 400,95 T800,65 T1200,100 T1440,75 L1440,200 L0,200 Z"
            />
          </svg>
        </div>
      </div>

      <!-- Solid Flow Line -->
      <div class="flow-line layer-3">
        <div class="line-wrapper">
          <svg class="flow-svg" viewBox="0 0 1440 80" preserveAspectRatio="none">
            <defs>
              <linearGradient id="line-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#ff6b35" stop-opacity="0" />
                <stop offset="15%" stop-color="#ff6b35" stop-opacity="1" />
                <stop offset="85%" stop-color="#ff6b35" stop-opacity="1" />
                <stop offset="100%" stop-color="#ff6b35" stop-opacity="0" />
              </linearGradient>
            </defs>
            <path
              fill="none"
              stroke="url(#line-grad)"
              stroke-width="2"
              d="M0,40 Q180,20 360,35 T720,25 T1080,45 T1440,30"
            />
          </svg>
          <svg class="flow-svg clone" viewBox="0 0 1440 80" preserveAspectRatio="none">
            <defs>
              <linearGradient id="line-grad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#ff6b35" stop-opacity="0" />
                <stop offset="15%" stop-color="#ff6b35" stop-opacity="1" />
                <stop offset="85%" stop-color="#ff6b35" stop-opacity="1" />
                <stop offset="100%" stop-color="#ff6b35" stop-opacity="0" />
              </linearGradient>
            </defs>
            <path
              fill="none"
              stroke="url(#line-grad)"
              stroke-width="2"
              d="M0,40 Q180,20 360,35 T720,25 T1080,45 T1440,30"
            />
          </svg>
        </div>
      </div>

      <!-- Dashed Flow Line -->
      <div class="flow-line layer-4">
        <div class="line-wrapper">
          <svg class="flow-svg" viewBox="0 0 1440 60" preserveAspectRatio="none">
            <path
              fill="none"
              stroke="#ff8888"
              stroke-width="1.5"
              stroke-dasharray="10,15"
              d="M0,30 Q200,15 400,28 T800,18 T1200,32 T1440,22"
            />
          </svg>
          <svg class="flow-svg clone" viewBox="0 0 1440 60" preserveAspectRatio="none">
            <path
              fill="none"
              stroke="#ff8888"
              stroke-width="1.5"
              stroke-dasharray="10,15"
              d="M0,30 Q200,15 400,28 T800,18 T1200,32 T1440,22"
            />
          </svg>
        </div>
      </div>

      <!-- Floating Particles -->
      <div class="particles">
        <div v-for="i in 8" :key="i" class="particle" :class="`particle-${i}`"></div>
      </div>
    </div>

    <!-- Bottom Wave Section -->
    <div class="wave-section">
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

        <path
          class="wave wave-1"
          fill="url(#waveGradient)"
          d="M0,192L48,176C96,160,192,128,288,138.7C384,149,480,203,576,208C672,213,768,171,864,154.7C960,139,1056,149,1152,165.3C1248,181,1344,203,1392,213.3L1440,224L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
        />

        <path
          class="wave wave-2"
          fill="url(#waveGradient2)"
          opacity="0.6"
          d="M0,256L48,240C96,224,192,192,288,181.3C384,171,480,181,576,192C672,203,768,213,864,197.3C960,181,1056,139,1152,128C1248,117,1344,139,1392,149.3L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
        />
      </svg>

      <div class="ambient-glow"></div>

      <div class="particles-bottom">
        <div v-for="i in 6" :key="i" class="particle-b" :class="`particle-b-${i}`"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.flowing-cloud-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  pointer-events: none;
  background: #050505;
}

/* ==================== */
/* Upper Cloud Section */
/* ==================== */
.cloud-section {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 55vh;
  min-height: 320px;
  overflow: hidden;
}

/* Mist Wrapper - Handles the infinite scroll */
.mist-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 200%;
  height: 100%;
  display: flex;
  will-change: transform;
}

.cloud-svg {
  width: 50%;
  height: 100%;
  flex-shrink: 0;
}

.cloud-svg.clone {
  /* Clone is placed right after the original */
}

/* Mist Layer Animations */
.layer-1 .mist-wrapper {
  animation: flow-horizontal 35s linear infinite;
}

.layer-2 .mist-wrapper {
  animation: flow-horizontal 25s linear infinite reverse;
  opacity: 0.85;
}

/* Flow Line Wrapper */
.flow-line {
  position: absolute;
  left: 0;
  width: 100%;
  overflow: hidden;
}

.layer-3 {
  bottom: 35%;
  height: 80px;
}

.layer-4 {
  bottom: 25%;
  height: 60px;
}

.line-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 200%;
  height: 100%;
  display: flex;
  will-change: transform;
}

.flow-svg {
  width: 50%;
  height: 100%;
  flex-shrink: 0;
}

.layer-3 .line-wrapper {
  animation: flow-horizontal 20s linear infinite;
}

.layer-4 .line-wrapper {
  animation: flow-horizontal 15s linear infinite reverse;
}

.layer-4 .flow-svg path {
  stroke-dashoffset: 0;
  animation: dash-flow 8s linear infinite;
}

/* Seamless Horizontal Flow - key is translateX(-50%) */
@keyframes flow-horizontal {
  0% {
    transform: translate3d(0, 0, 0);
  }
  100% {
    transform: translate3d(-50%, 0, 0);
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

/* Particles - Drift from right to left */
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
  width: 3px;
  height: 3px;
  background: rgba(255, 107, 53, 0.7);
  border-radius: 50%;
  will-change: transform, opacity;
}

.particle-1 { top: 20%; animation: drift 18s linear infinite; }
.particle-2 { top: 35%; animation: drift 22s linear infinite; animation-delay: -5s; }
.particle-3 { top: 50%; animation: drift 20s linear infinite; animation-delay: -10s; }
.particle-4 { top: 15%; animation: drift 25s linear infinite; animation-delay: -3s; }
.particle-5 { top: 40%; animation: drift 19s linear infinite; animation-delay: -8s; }
.particle-6 { top: 55%; animation: drift 23s linear infinite; animation-delay: -12s; }
.particle-7 { top: 25%; animation: drift 21s linear infinite; animation-delay: -6s; }
.particle-8 { top: 45%; animation: drift 17s linear infinite; animation-delay: -14s; }

@keyframes drift {
  0% {
    transform: translate3d(100vw, 0, 0);
    opacity: 0;
  }
  5% {
    opacity: 1;
  }
  95% {
    opacity: 1;
  }
  100% {
    transform: translate3d(-100vw, 0, 0);
    opacity: 0;
  }
}

/* ==================== */
/* Bottom Wave Section */
/* ==================== */
.wave-section {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 65vh;
  min-height: 400px;
  max-height: 600px;
  overflow: hidden;
}

.wave-svg {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.wave {
  will-change: transform;
}

.wave-1 {
  animation: wave-float 8s ease-in-out infinite;
}

.wave-2 {
  animation: wave-float 6s ease-in-out infinite reverse;
  animation-delay: -2s;
}

@keyframes wave-float {
  0%, 100% {
    transform: translate3d(0, 0, 0);
  }
  25% {
    transform: translate3d(-3px, 2px, 0);
  }
  50% {
    transform: translate3d(0, 0, 0);
  }
  75% {
    transform: translate3d(3px, -2px, 0);
  }
}

.ambient-glow {
  position: absolute;
  bottom: 15%;
  left: 50%;
  width: 80%;
  height: 250px;
  background: radial-gradient(
    ellipse at center,
    rgba(255, 51, 51, 0.15) 0%,
    rgba(255, 51, 51, 0.05) 40%,
    transparent 70%
  );
  filter: blur(40px);
  animation: glow-pulse 4s ease-in-out infinite;
  will-change: opacity, transform;
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

/* Bottom Particles */
.particles-bottom {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.particle-b {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 107, 53, 0.6);
  border-radius: 50%;
  will-change: transform, opacity;
  animation: float-up 15s linear infinite;
}

.particle-b-1 { left: 10%; animation-delay: 0s; animation-duration: 15s; }
.particle-b-2 { left: 25%; animation-delay: -3s; animation-duration: 12s; }
.particle-b-3 { left: 45%; animation-delay: -6s; animation-duration: 18s; }
.particle-b-4 { left: 65%; animation-delay: -2s; animation-duration: 14s; }
.particle-b-5 { left: 80%; animation-delay: -8s; animation-duration: 16s; }
.particle-b-6 { left: 90%; animation-delay: -5s; animation-duration: 13s; }

@keyframes float-up {
  0% {
    transform: translate3d(0, 100vh, 0) scale(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
    transform: translate3d(0, 90vh, 0) scale(1);
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translate3d(0, -20vh, 0) scale(0.5);
    opacity: 0;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .cloud-section {
    height: 45vh;
    min-height: 250px;
  }

  .wave-section {
    height: 55vh;
    min-height: 300px;
  }

  .particle,
  .particle-b {
    width: 2px;
    height: 2px;
  }
}
</style>
