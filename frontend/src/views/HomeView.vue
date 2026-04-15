<template>
  <div class="home">
    <!-- Grid Background -->
    <div class="grid-bg"></div>

    <!-- Navigation -->
    <nav class="nav" :class="{ scrolled: isScrolled }">
      <div class="nav-logo" @click="$router.push('/')">留声画</div>
      <div class="nav-actions">
        <button class="btn-text" @click="$router.push('/login')">登录</button>
        <button class="btn-text primary" @click="$router.push('/register')">开始使用</button>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <!-- Main Title -->
        <div ref="titleRef" class="hero-title-wrap">
          <h1 class="hero-title" :class="{ visible: titleVisible }">
            <span class="title-char" v-for="(char, i) in '留声画'" :key="i" :style="{ animationDelay: `${i * 0.08}s` }">
              {{ char }}
            </span>
          </h1>
        </div>

        <!-- Subtitle -->
        <p class="hero-subtitle" :class="{ visible: subtitleVisible }">
          让每张照片都能讲述自己的故事
        </p>

        <!-- Description -->
        <p class="hero-description" :class="{ visible: descVisible }">
          上传一张照片，AI 自动分析场景并生成语音解说与背景音乐，<br>
          将静态的记忆转化为生动的视听体验。
        </p>

        <!-- CTA Buttons -->
        <div class="hero-actions" :class="{ visible: ctaVisible }">
          <button class="btn-text primary" @click="$router.push('/register')">
            开始创作
          </button>
          <button class="btn-text" @click="scrollToFeatures">
            了解更多
            <span class="arrow">↓</span>
          </button>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="scroll-indicator" :class="{ visible: scrollVisible }">
        <div class="scroll-line"></div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features" ref="featuresRef">
      <div class="features-header">
        <h2 class="section-title">智能 AI 驱动</h2>
        <p class="section-subtitle">融合多种 AI 技术，打造沉浸式体验</p>
      </div>

      <div class="features-grid">
        <div
          v-for="(feature, index) in features"
          :key="index"
          class="feature-card"
          :ref="el => featureCards[index] = el"
        >
          <div class="feature-number">0{{ index + 1 }}</div>
          <h3 class="feature-title">{{ feature.title }}</h3>
          <p class="feature-desc">{{ feature.desc }}</p>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <div class="cta-content">
        <h2 class="cta-title">让回忆"声"动起来</h2>
        <p class="cta-subtitle">上传一张照片，开启你的创意之旅</p>
        <button class="btn-text primary" @click="$router.push('/register')">
          立即开始
        </button>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <p>留声画 · Photo Voice Narrator</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isScrolled = ref(false)
const titleRef = ref(null)

// Animation states
const titleVisible = ref(false)
const subtitleVisible = ref(false)
const descVisible = ref(false)
const ctaVisible = ref(false)
const scrollVisible = ref(false)

const featuresRef = ref(null)
const featureCards = ref([])

const features = [
  {
    title: '智能分析',
    desc: 'BLIP-2 视觉语言模型，准确理解照片场景与情感'
  },
  {
    title: '语音解说',
    desc: 'Edge-TTS 微软语音合成，自然流畅的中文解说'
  },
  {
    title: '背景音乐',
    desc: 'MusicGen AI 音乐生成，智能匹配场景氛围'
  }
]

// Intersection Observer for scroll animations
let observer = null

const setupObserver = () => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view')
        }
      })
    },
    { threshold: 0.2 }
  )
}

const scrollToFeatures = () => {
  featuresRef.value?.scrollIntoView({ behavior: 'smooth' })
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)

  // Staggered entrance animations
  setTimeout(() => { titleVisible.value = true }, 200)
  setTimeout(() => { subtitleVisible.value = true }, 500)
  setTimeout(() => { descVisible.value = true }, 700)
  setTimeout(() => { ctaVisible.value = true }, 900)
  setTimeout(() => { scrollVisible.value = true }, 1200)

  // Setup feature cards observer
  setTimeout(() => {
    if (featureCards.value.length) {
      featureCards.value.forEach(card => {
        if (card && observer) {
          observer.observe(card)
        }
      })
    }
  }, 100)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  if (observer) {
    observer.disconnect()
  }
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  position: relative;
}

/* Navigation */
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 48px;
  transition: all 0.4s var(--ease-out-expo);
}

.nav.scrolled {
  padding: 20px 48px;
  background: rgba(5, 5, 5, 0.8);
  backdrop-filter: blur(20px);
}

.nav-logo {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.15em;
  cursor: pointer;
  transition: color 0.3s ease;
}

.nav-logo:hover {
  color: var(--accent);
}

.nav-actions {
  display: flex;
  gap: 32px;
  align-items: center;
}

/* Hero Section */
.hero {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 120px 24px 80px;
  position: relative;
}

.hero-content {
  max-width: 900px;
  z-index: 1;
}

/* Title Animation */
.hero-title-wrap {
  margin-bottom: 32px;
}

.hero-title {
  font-family: var(--font-display);
  font-size: clamp(64px, 15vw, 160px);
  font-weight: 700;
  letter-spacing: 0.3em;
  line-height: 1;
  opacity: 0;
  transform: translateY(60px);
  transition: all 0.8s var(--ease-out-expo);
}

.hero-title.visible {
  opacity: 1;
  transform: translateY(0);
}

.title-char {
  display: inline-block;
  opacity: 0;
  transform: translateY(40px) rotateX(-90deg);
  animation: char-reveal 0.6s var(--ease-out-expo) forwards;
}

.hero-title.visible .title-char {
  opacity: 1;
  transform: translateY(0) rotateX(0);
}

@keyframes char-reveal {
  0% {
    opacity: 0;
    transform: translateY(40px) rotateX(-90deg);
  }
  100% {
    opacity: 1;
    transform: translateY(0) rotateX(0);
  }
}

/* Subtitle */
.hero-subtitle {
  font-size: clamp(16px, 2.5vw, 24px);
  font-weight: 500;
  letter-spacing: 0.2em;
  color: var(--accent);
  margin-bottom: 24px;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.7s var(--ease-out-expo);
}

.hero-subtitle.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Description */
.hero-description {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.8;
  margin-bottom: 48px;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.7s var(--ease-out-expo);
}

.hero-description.visible {
  opacity: 1;
  transform: translateY(0);
}

/* CTA */
.hero-actions {
  display: flex;
  gap: 40px;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.7s var(--ease-out-expo);
}

.hero-actions.visible {
  opacity: 1;
  transform: translateY(0);
}

.arrow {
  display: inline-block;
  animation: bounce-down 1.5s ease-in-out infinite;
}

@keyframes bounce-down {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(4px); }
}

/* Scroll Indicator */
.scroll-indicator {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.6s var(--ease-out-expo);
}

.scroll-indicator.visible {
  opacity: 1;
}

.scroll-line {
  width: 1px;
  height: 60px;
  background: linear-gradient(
    to bottom,
    var(--text-muted) 0%,
    transparent 100%
  );
  animation: scroll-pulse 2s ease-in-out infinite;
}

@keyframes scroll-pulse {
  0%, 100% { opacity: 0.3; transform: scaleY(1); }
  50% { opacity: 1; transform: scaleY(1.1); }
}

/* Features Section */
.features {
  padding: 160px 48px;
  position: relative;
  z-index: 1;
}

.features-header {
  text-align: center;
  margin-bottom: 80px;
}

.section-title {
  font-family: var(--font-display);
  font-size: clamp(32px, 5vw, 56px);
  font-weight: 700;
  letter-spacing: 0.05em;
  margin-bottom: 16px;
}

.section-subtitle {
  color: var(--text-secondary);
  font-size: 16px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Feature Card */
.feature-card {
  padding: 48px 32px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 4px;
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.6s var(--ease-out-expo);
}

.feature-card.in-view {
  opacity: 1;
  transform: translateY(0);
}

.feature-card:nth-child(2) {
  transition-delay: 0.1s;
}

.feature-card:nth-child(3) {
  transition-delay: 0.2s;
}

.feature-card:hover {
  border-color: rgba(255, 51, 51, 0.3);
  background: rgba(255, 51, 51, 0.02);
}

.feature-number {
  font-family: var(--font-display);
  font-size: 48px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.05);
  margin-bottom: 24px;
}

.feature-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 12px;
  letter-spacing: 0.02em;
}

.feature-desc {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

/* CTA Section */
.cta {
  padding: 200px 48px;
  text-align: center;
  position: relative;
  z-index: 1;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-family: var(--font-display);
  font-size: clamp(28px, 4vw, 48px);
  font-weight: 700;
  margin-bottom: 16px;
  letter-spacing: 0.05em;
}

.cta-subtitle {
  color: var(--text-secondary);
  margin-bottom: 40px;
}

/* Footer */
.footer {
  padding: 40px 48px;
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  position: relative;
  z-index: 1;
}

/* Responsive */
@media (max-width: 900px) {
  .features-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .nav {
    padding: 24px;
  }

  .features,
  .cta {
    padding: 100px 24px;
  }

  .hero-actions {
    flex-direction: column;
    gap: 24px;
  }
}
</style>
