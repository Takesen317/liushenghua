<template>
  <div class="infinite-scroll-grid">
    <div class="grid-container" :style="{ transform: `rotate(${rotation}deg) scale(${scale})` }">
      <!-- Column 1 - Moving Down -->
      <div class="column col-1">
        <div class="column-inner" :style="{ animationDuration: `${duration1}s`, animationDirection: 'normal' }">
          <div v-for="(img, i) in imagesCol1" :key="`1-${i}`" class="image-card">
            <img :src="img.url" :alt="img.alt" loading="lazy" />
            <div class="image-overlay"></div>
          </div>
        </div>
        <!-- Clone for seamless loop -->
        <div class="column-inner clone" :style="{ animationDuration: `${duration1}s`, animationDirection: 'normal' }">
          <div v-for="(img, i) in imagesCol1" :key="`1-clone-${i}`" class="image-card">
            <img :src="img.url" :alt="img.alt" loading="lazy" />
            <div class="image-overlay"></div>
          </div>
        </div>
      </div>

      <!-- Column 2 - Moving Up -->
      <div class="column col-2">
        <div class="column-inner" :style="{ animationDuration: `${duration2}s`, animationDirection: 'reverse' }">
          <div v-for="(img, i) in imagesCol2" :key="`2-${i}`" class="image-card large">
            <img :src="img.url" :alt="img.alt" loading="lazy" />
            <div class="image-overlay"></div>
          </div>
        </div>
        <div class="column-inner clone" :style="{ animationDuration: `${duration2}s`, animationDirection: 'reverse' }">
          <div v-for="(img, i) in imagesCol2" :key="`2-clone-${i}`" class="image-card large">
            <img :src="img.url" :alt="img.alt" loading="lazy" />
            <div class="image-overlay"></div>
          </div>
        </div>
      </div>

      <!-- Column 3 - Moving Down -->
      <div class="column col-3">
        <div class="column-inner" :style="{ animationDuration: `${duration3}s`, animationDirection: 'normal' }">
          <div v-for="(img, i) in imagesCol3" :key="`3-${i}`" class="image-card medium">
            <img :src="img.url" :alt="img.alt" loading="lazy" />
            <div class="image-overlay"></div>
          </div>
        </div>
        <div class="column-inner clone" :style="{ animationDuration: `${duration3}s`, animationDirection: 'normal' }">
          <div v-for="(img, i) in imagesCol3" :key="`3-clone-${i}`" class="image-card medium">
            <img :src="img.url" :alt="img.alt" loading="lazy" />
            <div class="image-overlay"></div>
          </div>
        </div>
      </div>

      <!-- Column 4 - Moving Up -->
      <div class="column col-4">
        <div class="column-inner" :style="{ animationDuration: `${duration4}s`, animationDirection: 'reverse' }">
          <div v-for="(img, i) in imagesCol4" :key="`4-${i}`" class="image-card">
            <img :src="img.url" :alt="img.alt" loading="lazy" />
            <div class="image-overlay"></div>
          </div>
        </div>
        <div class="column-inner clone" :style="{ animationDuration: `${duration4}s`, animationDirection: 'reverse' }">
          <div v-for="(img, i) in imagesCol4" :key="`4-clone-${i}`" class="image-card">
            <img :src="img.url" :alt="img.alt" loading="lazy" />
            <div class="image-overlay"></div>
          </div>
        </div>
      </div>

      <!-- Column 5 - Moving Down -->
      <div class="column col-5">
        <div class="column-inner" :style="{ animationDuration: `${duration5}s`, animationDirection: 'normal' }">
          <div v-for="(img, i) in imagesCol5" :key="`5-${i}`" class="image-card small">
            <img :src="img.url" :alt="img.alt" loading="lazy" />
            <div class="image-overlay"></div>
          </div>
        </div>
        <div class="column-inner clone" :style="{ animationDuration: `${duration5}s`, animationDirection: 'normal' }">
          <div v-for="(img, i) in imagesCol5" :key="`5-clone-${i}`" class="image-card small">
            <img :src="img.url" :alt="img.alt" loading="lazy" />
            <div class="image-overlay"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Global Overlay -->
    <div class="global-overlay"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  rotation: {
    type: Number,
    default: -12
  },
  scale: {
    type: Number,
    default: 1.3
  }
})

// Picsum placeholder images with different sizes
const generateImages = (count, minSize, maxSize) => {
  const images = []
  for (let i = 0; i < count; i++) {
    const width = Math.floor(Math.random() * (maxSize - minSize) + minSize)
    const height = Math.floor(Math.random() * (maxSize - minSize) + minSize)
    const id = Math.floor(Math.random() * 200)
    images.push({
      url: `https://picsum.photos/seed/${id + i}/${width}/${height}`,
      alt: `Image ${i}`,
      size: { width, height }
    })
  }
  return images
}

// Generate images for each column with different seeds for variety
const imagesCol1 = generateImages(8, 300, 500)
const imagesCol2 = generateImages(6, 400, 600)
const imagesCol3 = generateImages(7, 350, 550)
const imagesCol4 = generateImages(5, 450, 650)
const imagesCol5 = generateImages(9, 280, 450)

// Different durations for staggered effect (20-40s range)
const duration1 = 25
const duration2 = 35
const duration3 = 30
const duration4 = 40
const duration5 = 28
</script>

<style scoped>
.infinite-scroll-grid {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
}

.grid-container {
  position: absolute;
  top: -20%;
  left: -20%;
  right: -20%;
  bottom: -20%;
  display: flex;
  gap: 20px;
  padding: 0 20px;
  transform-origin: center center;
}

/* Column */
.column {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.column-inner {
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: scroll-down linear infinite;
  will-change: transform;
}

.column-inner.clone {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
}

/* Scroll Animation */
@keyframes scroll-down {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(-50%);
  }
}

/* Image Cards */
.image-card {
  position: relative;
  border-radius: 4px;
  overflow: hidden;
  flex-shrink: 0;
  will-change: transform;
}

.image-card img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: cover;
}

.image-card.large {
  transform: scale(1.1);
}

.image-card.medium {
  transform: scale(0.95);
}

.image-card.small {
  transform: scale(0.9);
}

/* Image Overlay - semi-transparent */
.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(5, 5, 5, 0.4) 0%,
    rgba(5, 5, 5, 0.2) 50%,
    rgba(5, 5, 5, 0.5) 100%
  );
  /* Noise texture effect */
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.6;
  mix-blend-mode: overlay;
}

/* Global Overlay - darkens everything */
.global-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    ellipse at center,
    rgba(5, 5, 5, 0.3) 0%,
    rgba(5, 5, 5, 0.7) 70%,
    rgba(5, 5, 5, 0.9) 100%
  );
  pointer-events: none;
}

/* Mobile Responsive */
@media (max-width: 1024px) {
  .grid-container {
    gap: 12px;
  }

  .column-inner {
    gap: 12px;
  }
}

@media (max-width: 768px) {
  .infinite-scroll-grid {
    opacity: 0.5;
  }

  .grid-container {
    gap: 8px;
    top: -30%;
    bottom: -30%;
  }

  .column-inner {
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .grid-container {
    gap: 6px;
  }

  .column-inner {
    gap: 6px;
  }
}
</style>
