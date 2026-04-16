<template>
  <div class="task-list">
    <div class="panel-header">
      <h3>最近创作</h3>
      <button class="btn-text" @click="$emit('refresh')">
        刷新 ↻
      </button>
    </div>

    <!-- Empty State -->
    <div v-if="tasks.length === 0" class="empty-state">
      <div class="empty-icon">+</div>
      <p>还没有创作</p>
      <p class="empty-sub">上传照片开始你的第一个创作</p>
    </div>

    <!-- Task Grid -->
    <div v-else class="task-grid">
      <div
        v-for="task in tasks"
        :key="task.id"
        class="task-card"
        :class="`status-${task.status}`"
      >
        <div class="task-image">
          <div class="image-placeholder">
            <span>{{ getStatusIcon(task.status) }}</span>
          </div>
        </div>

        <div class="task-info">
          <div class="task-header">
            <span class="task-filename">{{ task.filename || '照片' }}</span>
            <span class="status-indicator" :class="task.status"></span>
          </div>

          <!-- Status Content -->
          <div class="task-status">
            <span class="status-text" :class="task.status">
              {{ getStatusText(task.status) }}
            </span>

            <!-- Progress Bar -->
            <div v-if="task.status === 'processing'" class="progress-wrap">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${task.progress || 0}%` }"></div>
              </div>
              <span class="progress-text">{{ task.progress || 0 }}%</span>
            </div>

            <!-- Actions for completed -->
            <div v-if="task.status === 'completed'" class="task-actions">
              <button class="action-btn" title="播放" @click="playVideo(task)">▶</button>
              <button class="action-btn" title="下载" @click="downloadVideo(task)">↓</button>
              <button class="action-btn" title="分享" @click="shareTask(task)">↗</button>
              <button class="action-btn delete-btn" title="删除" @click="deleteTask(task)">×</button>
            </div>

            <!-- Retry for failed -->
            <button v-if="task.status === 'failed'" class="retry-btn" @click="retryTask(task)">
              重试
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Video Player Modal -->
    <div v-if="showPlayer" class="video-modal" @click.self="closePlayer">
      <div class="video-container">
        <button class="video-close" @click="closePlayer">×</button>
        <video
          v-if="videoUrl"
          :src="videoUrl"
          controls
          autoplay
          class="video-player"
        ></video>
        <div v-else class="video-error">
          <p>视频文件不存在</p>
          <p class="video-error-sub">{{ videoUrl }}</p>
        </div>
      </div>
    </div>

    <!-- Share Modal -->
    <div v-if="showShare" class="video-modal" @click.self="closeShare">
      <div class="share-container">
        <button class="video-close" @click="closeShare">×</button>
        <h3>分享视频</h3>
        <div v-if="shareUrl" class="share-content">
          <p class="share-label">分享链接</p>
          <div class="share-link-box">
            <input type="text" :value="shareUrl" readonly class="share-input" />
            <button class="copy-btn" @click="copyShareLink">复制</button>
          </div>
          <p class="share-tip">复制链接后可直接分享给好友</p>
        </div>
        <div v-else class="share-loading">生成分享链接中...</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const { tasks } = defineProps({
  tasks: {
    type: Array,
    default: () => []
  }
})

defineEmits(['refresh'])

const showPlayer = ref(false)
const showShare = ref(false)
const videoUrl = ref('')
const shareUrl = ref('')

const getStatusIcon = (status) => {
  const icons = {
    pending: '○',
    processing: '◐',
    completed: '●',
    failed: '✕'
  }
  return icons[status] || '?'
}

const getStatusText = (status) => {
  const texts = {
    pending: '等待中',
    processing: '处理中',
    completed: '已完成',
    failed: '失败'
  }
  return texts[status] || status
}

const playVideo = async (task) => {
  // Get full task details for video URL
  try {
    const response = await api.getTask(task.id)
    const resultData = response.data.result_data
    if (resultData?.video_url) {
      const videoPath = resultData.video_url.replace(/\\/g, '/')
      // Handle paths like "tsk_xxx/file.mp4" or "results/tsk_xxx/file.mp4"
      const parts = videoPath.split('/').filter(p => p)
      let taskId = ''
      let filename = ''
      if (parts.length >= 2 && parts[0] === 'results') {
        taskId = parts[1]
        filename = parts.slice(2).join('/')
      } else if (parts.length >= 2) {
        taskId = parts[0]
        filename = parts.slice(1).join('/')
      } else if (parts.length === 1) {
        filename = parts[0]
      }
      if (taskId && filename) {
        videoUrl.value = `/results/${taskId}/${filename}`
        showPlayer.value = true
      } else {
        ElMessage.error('视频路径格式错误')
      }
    } else {
      ElMessage.error('视频文件不存在')
    }
  } catch (error) {
    console.error('Failed to get task:', error)
    ElMessage.error('获取视频信息失败')
  }
}

const closePlayer = () => {
  showPlayer.value = false
  videoUrl.value = ''
}

const downloadVideo = async (task) => {
  try {
    const response = await api.getTask(task.id)
    const resultData = response.data.result_data
    if (resultData?.video_url) {
      const videoPath = resultData.video_url.replace(/\\/g, '/')
      // Handle paths like "tsk_xxx/file.mp4" or "results/tsk_xxx/file.mp4"
      const parts = videoPath.split('/').filter(p => p)
      let taskId = ''
      let filename = ''
      if (parts.length >= 2 && parts[0] === 'results') {
        taskId = parts[1]
        filename = parts.slice(2).join('/')
      } else if (parts.length >= 2) {
        taskId = parts[0]
        filename = parts.slice(1).join('/')
      } else if (parts.length === 1) {
        filename = parts[0]
      }
      if (taskId && filename) {
        const downloadUrl = `/results/${taskId}/${filename}`
        // Create download link
        const link = document.createElement('a')
        link.href = downloadUrl
        link.download = `留声画_${task.id}.mp4`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        ElMessage.success('开始下载')
      }
    } else {
      ElMessage.error('视频文件不存在')
    }
  } catch (error) {
    console.error('Failed to download:', error)
    ElMessage.error('下载失败')
  }
}

const shareTask = async (task) => {
  showShare.value = true
  shareUrl.value = ''
  try {
    const response = await api.createShare(task.id)
    shareUrl.value = window.location.origin + response.data.url
  } catch (error) {
    console.error('Failed to create share:', error)
    ElMessage.error('生成分享链接失败')
  }
}

const closeShare = () => {
  showShare.value = false
  shareUrl.value = ''
}

const copyShareLink = async () => {
  try {
    await navigator.clipboard.writeText(shareUrl.value)
    ElMessage.success('链接已复制到剪贴板')
  } catch {
    ElMessage.error('复制失败，请手动复制')
  }
}

const retryTask = async (task) => {
  try {
    await api.retryTask(task.id)
    ElMessage.success('任务已重新提交')
    // Update task status locally using splice for reactivity
    const taskIndex = tasks.value.findIndex(t => t.id === task.id)
    if (taskIndex !== -1) {
      tasks.value.splice(taskIndex, 1, {
        ...tasks.value[taskIndex],
        status: 'pending',
        progress: 0
      })
    }
  } catch (error) {
    console.error('Failed to retry task:', error)
    ElMessage.error('重试失败')
  }
}

const deleteTask = async (task) => {
  if (!confirm('确定要删除这个任务吗？')) {
    return
  }
  try {
    await api.deleteTask(task.id)
    ElMessage.success('任务已删除')
    // Directly remove from local list - no need to wait for parent refresh
    const taskIndex = tasks.findIndex(t => t.id === task.id)
    if (taskIndex !== -1) {
      tasks.splice(taskIndex, 1)
    }
  } catch (error) {
    console.error('Failed to delete task:', error)
    ElMessage.error('删除失败')
  }
}
</script>

<style scoped>
.task-list {
  background: rgba(10, 10, 10, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 32px;
  min-height: 400px;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  position: relative;
}

/* Top gradient overlay for text readability */
.task-list::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: linear-gradient(
    to bottom,
    rgba(10, 10, 10, 0.95) 0%,
    transparent 100%
  );
  pointer-events: none;
  border-radius: 8px 8px 0 0;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.panel-header h3 {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  font-weight: 300;
  color: var(--text-muted);
  margin-bottom: 16px;
}

.empty-state p {
  color: var(--text-secondary);
  font-size: 15px;
}

.empty-sub {
  color: var(--text-muted) !important;
  font-size: 13px !important;
  margin-top: 4px;
}

/* Task Grid */
.task-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

/* Task Card */
.task-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  overflow: hidden;
  transition: all 0.3s var(--ease-out-expo);
}

.task-card:hover {
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.task-image {
  aspect-ratio: 16/9;
  background: rgba(255, 255, 255, 0.03);
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-placeholder {
  font-size: 24px;
  color: var(--text-muted);
}

.task-info {
  padding: 16px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.task-filename {
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 120px;
}

/* Status Indicator */
.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-indicator.pending {
  background: var(--text-muted);
}

.status-indicator.processing {
  background: var(--accent);
  animation: pulse 1.5s infinite;
}

.status-indicator.completed {
  background: #22c55e;
}

.status-indicator.failed {
  background: #ef4444;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* Status Text */
.task-status {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-text {
  font-size: 12px;
  color: var(--text-muted);
}

.status-text.completed {
  color: #22c55e;
}

.status-text.failed {
  color: #ef4444;
}

/* Progress */
.progress-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex: 1;
  height: 2px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 1px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--accent);
  transition: width 0.5s var(--ease-out-expo);
}

.progress-text {
  font-size: 11px;
  color: var(--text-muted);
  min-width: 32px;
}

/* Actions */
.task-actions {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.action-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  color: var(--text-secondary);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.action-btn:first-child {
  background: var(--accent);
  border-color: var(--accent);
  color: white;
}

.action-btn:first-child:hover {
  background: #ff4444;
  border-color: #ff4444;
}

.action-btn.delete-btn {
  margin-left: auto;
  color: var(--text-muted);
}

.action-btn.delete-btn:hover {
  border-color: #ef4444;
  color: #ef4444;
}

/* Retry */
.retry-btn {
  padding: 6px 12px;
  background: transparent;
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 2px;
  color: #ef4444;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  align-self: flex-start;
}

.retry-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
}

/* Video Modal */
.video-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.video-container {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.video-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 32px;
  cursor: pointer;
  padding: 4px 12px;
  transition: opacity 0.2s;
}

.video-close:hover {
  opacity: 0.7;
}

.video-player {
  max-width: 100%;
  max-height: 80vh;
  border-radius: 4px;
}

.video-error {
  color: white;
  text-align: center;
  padding: 60px 40px;
}

.video-error p {
  font-size: 18px;
  margin-bottom: 8px;
}

.video-error-sub {
  font-size: 12px !important;
  color: var(--text-muted) !important;
  word-break: break-all;
}

/* Share Modal */
.share-container {
  background: rgba(20, 20, 20, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 40px;
  min-width: 400px;
  max-width: 90vw;
}

.share-container h3 {
  color: var(--text-primary);
  font-size: 18px;
  margin-bottom: 24px;
  text-align: center;
}

.share-content {
  text-align: center;
}

.share-label {
  color: var(--text-muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 12px;
}

.share-link-box {
  display: flex;
  gap: 8px;
}

.share-input {
  flex: 1;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: var(--text-primary);
  font-size: 14px;
}

.copy-btn {
  padding: 12px 24px;
  background: var(--accent);
  border: none;
  border-radius: 4px;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.copy-btn:hover {
  background: #ff4444;
}

.share-tip {
  color: var(--text-muted);
  font-size: 12px;
  margin-top: 16px;
}

.share-loading {
  color: var(--text-muted);
  text-align: center;
  padding: 20px;
}

/* Responsive */
@media (max-width: 640px) {
  .task-grid {
    grid-template-columns: 1fr;
  }

  .share-container {
    min-width: auto;
    width: 90vw;
    padding: 24px;
  }

  .share-link-box {
    flex-direction: column;
  }
}
</style>
