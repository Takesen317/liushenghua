<template>
  <div class="share-view">
    <!-- Header -->
    <header class="header">
      <div class="header-logo">◉ 留声画</div>
      <div class="header-actions">
        <button class="btn-text" @click="goHome">首页</button>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">!</div>
      <h2>{{ error }}</h2>
      <p>请检查链接是否正确或联系分享者</p>
      <button class="btn-primary" @click="goHome">返回首页</button>
    </div>

    <!-- Content -->
    <div v-else class="share-content">
      <div class="share-card">
        <h1 class="share-title">照片语音解说</h1>
        <p class="share-desc">{{ aiDescription }}</p>

        <!-- Video Player -->
        <div class="video-container">
          <video
            v-if="videoUrl"
            :src="videoUrl"
            controls
            autoplay
            class="video-player"
          ></video>
          <div v-else class="video-placeholder">
            <p>视频不可用</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="share-actions">
          <button class="btn-primary" @click="downloadVideo">
            ↓ 下载视频
          </button>
          <button class="btn-secondary" @click="createOwnTask">
            我也要创作
          </button>
        </div>

        <p class="share-count">已有 {{ viewCount }} 次浏览</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api'

const router = useRouter()
const route = useRoute()

const loading = ref(true)
const error = ref('')
const aiDescription = ref('')
const videoUrl = ref('')
const viewCount = ref(0)
const shareCode = route.params.code

const fetchShareContent = async () => {
  try {
    loading.value = true
    const response = await api.getShare(shareCode)
    const data = response.data

    aiDescription.value = data.ai_description || '照片语音解说'
    viewCount.value = data.view_count || 0

    if (data.result_data?.video_url) {
      const videoPath = data.result_data.video_url.replace(/\\/g, '/')
      // Handle paths like "tsk_xxx/file.mp4" or "results/tsk_xxx/file.mp4"
      const parts = videoPath.split('/').filter(p => p)
      let taskId = ''
      let filename = ''

      // Normalize: if path starts with 'results/', skip it
      const startIdx = parts[0] === 'results' ? 2 : 0

      if (parts.length >= startIdx + 2) {
        taskId = parts[startIdx]
        filename = parts.slice(startIdx + 1).join('/')
      } else if (parts.length === startIdx + 1) {
        filename = parts[startIdx]
      }

      if (taskId && filename) {
        videoUrl.value = `/results/${taskId}/${filename}`
      }
    }
  } catch (err) {
    console.error('Failed to fetch share:', err)
    loading.value = false
    if (err.response?.status === 404) {
      error.value = '分享不存在或已过期'
    } else if (err.response?.status === 410) {
      error.value = '分享链接已过期'
    } else {
      error.value = '加载失败'
    }
    return // Don't set loading to false here, keep error state
  }
  loading.value = false
}

const downloadVideo = () => {
  if (videoUrl.value) {
    const link = document.createElement('a')
    link.href = videoUrl.value
    link.download = `留声画_${shareCode}.mp4`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

const createOwnTask = () => {
  router.push('/register')
}

const goHome = () => {
  router.push('/')
}

onMounted(() => {
  fetchShareContent()
})
</script>

<style scoped>
.share-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 48px;
  background: rgba(5, 5, 5, 0.9);
  backdrop-filter: blur(20px);
}

.header-logo {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.1em;
}

.btn-text {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  padding: 8px 16px;
}

.btn-text:hover {
  color: var(--accent);
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  color: var(--text-primary);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 51, 51, 0.2);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon {
  width: 60px;
  height: 60px;
  border: 3px solid #ef4444;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: #ef4444;
  margin-bottom: 24px;
}

.error-state h2 {
  font-size: 24px;
  margin-bottom: 8px;
}

.error-state p {
  color: var(--text-muted);
  margin-bottom: 24px;
}

.share-content {
  display: flex;
  justify-content: center;
  padding: 40px 24px;
}

.share-card {
  max-width: 600px;
  width: 100%;
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 48px;
  text-align: center;
}

.share-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 16px;
}

.share-desc {
  color: var(--text-secondary);
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 32px;
}

.video-container {
  margin-bottom: 32px;
  border-radius: 8px;
  overflow: hidden;
  background: #000;
}

.video-player {
  width: 100%;
  max-height: 400px;
}

.video-placeholder {
  padding: 60px;
  color: var(--text-muted);
}

.share-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 24px;
}

.btn-primary {
  padding: 14px 32px;
  background: var(--accent);
  border: none;
  border-radius: 4px;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #ff4444;
  transform: translateY(-2px);
}

.btn-secondary {
  padding: 14px 32px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: var(--text-primary);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.share-count {
  color: var(--text-muted);
  font-size: 13px;
}

@media (max-width: 640px) {
  .header {
    padding: 20px 24px;
  }

  .share-card {
    padding: 24px;
  }

  .share-actions {
    flex-direction: column;
  }
}
</style>
