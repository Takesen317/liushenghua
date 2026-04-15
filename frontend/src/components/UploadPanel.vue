<template>
  <div class="upload-panel">
    <div class="panel-header">
      <h3>上传照片</h3>
    </div>

    <!-- Upload Zone -->
    <div
      class="upload-zone"
      :class="{ 'drag-over': isDragOver, 'has-file': file }"
      @dragover.prevent="isDragOver = true"
      @dragleave="isDragOver = false"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      <input
        ref="fileInputRef"
        type="file"
        accept="image/*"
        class="file-input"
        @change="handleFileChange"
      />

      <!-- Empty State -->
      <div v-if="!file" class="upload-placeholder">
        <div class="upload-icon">+</div>
        <p class="upload-text">拖拽照片到这里</p>
        <p class="upload-subtext">或点击选择文件</p>
      </div>

      <!-- Preview State -->
      <div v-else class="upload-preview">
        <img :src="previewUrl" alt="Preview" class="preview-image" @load="onImageLoad" />
        <p class="file-name">{{ file.name }}</p>
      </div>
    </div>

    <!-- Options (show after file selected) -->
    <div v-if="file" class="style-options">
      <div class="option-group">
        <label class="option-label">解说风格</label>
        <select v-model="options.style" class="select">
          <option value="warm">温暖</option>
          <option value="lively">活泼</option>
          <option value="lyrical">抒情</option>
          <option value="documentary">记录</option>
        </select>
      </div>

      <div class="option-group">
        <label class="option-label">语音</label>
        <select v-model="options.voice" class="select">
          <option value="xiaoxiao">小晓 (女声)</option>
          <option value="yunyang">云扬 (男声)</option>
          <option value="yunxia">云夏 (女声)</option>
        </select>
      </div>

      <div class="option-group">
        <label class="option-label">音乐风格</label>
        <select v-model="options.musicStyle" class="select">
          <option value="gentle">轻柔</option>
          <option value="cheerful">欢快</option>
          <option value="melancholy">忧伤</option>
          <option value="epic">史诗</option>
        </select>
      </div>

      <button class="btn-submit" :class="{ loading: uploading }" @click.stop="handleUpload">
        {{ uploading ? '上传中...' : '开始生成' }}
      </button>
    </div>

    <p class="upload-tip">支持 JPG、PNG、WebP，最大 20MB</p>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const emit = defineEmits(['upload-success'])

const fileInputRef = ref()
const file = ref(null)
const uploading = ref(false)
const previewUrl = ref('')
const isDragOver = ref(false)

const options = reactive({
  style: 'warm',
  voice: 'xiaoxiao',
  musicStyle: 'gentle'
})

const triggerFileInput = () => {
  fileInputRef.value?.click()
}

const handleFileChange = (event) => {
  const selectedFile = event.target.files?.[0]
  if (selectedFile) {
    setFile(selectedFile)
  }
}

const handleDrop = (event) => {
  isDragOver.value = false
  const droppedFile = event.dataTransfer?.files?.[0]
  if (droppedFile && droppedFile.type.startsWith('image/')) {
    setFile(droppedFile)
  } else {
    ElMessage.warning('请上传图片文件')
  }
}

const setFile = (selectedFile) => {
  if (selectedFile.size > 20 * 1024 * 1024) {
    ElMessage.warning('文件大小不能超过 20MB')
    return
  }
  file.value = selectedFile
  previewUrl.value = URL.createObjectURL(selectedFile)
}

const onImageLoad = () => {
  // Add loaded class for reveal animation if needed
}

const handleUpload = async () => {
  if (!file.value) {
    ElMessage.warning('请先选择照片')
    return
  }

  uploading.value = true
  try {
    const response = await api.uploadFile(file.value)
    const fileId = response.data.file_id
    emit('upload-success', fileId)

    // Reset
    file.value = null
    previewUrl.value = ''
    fileInputRef.value.value = ''
  } catch (error) {
    ElMessage.error('上传失败，请重试')
  } finally {
    uploading.value = false
  }
}
</script>

<style scoped>
.upload-panel {
  background: rgba(10, 10, 10, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 32px;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  position: relative;
}

/* Top gradient overlay for text readability */
.upload-panel::before {
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
  margin-bottom: 24px;
}

.panel-header h3 {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
}

/* Upload Zone */
.upload-zone {
  position: relative;
  border: 1px dashed rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  padding: 48px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s var(--ease-out-expo);
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-zone:hover {
  border-color: rgba(255, 51, 51, 0.3);
  background: rgba(255, 51, 51, 0.02);
}

.upload-zone.drag-over {
  border-color: var(--accent);
  background: rgba(255, 51, 51, 0.05);
  transform: scale(1.01);
}

.upload-zone.has-file {
  border-style: solid;
  border-color: rgba(255, 255, 255, 0.1);
}

.file-input {
  display: none;
}

.upload-placeholder {
  pointer-events: none;
}

.upload-icon {
  font-size: 40px;
  font-weight: 300;
  color: var(--text-muted);
  margin-bottom: 16px;
  transition: all 0.3s var(--ease-out-expo);
}

.upload-zone:hover .upload-icon {
  color: var(--accent);
  transform: scale(1.1);
}

.upload-text {
  color: var(--text-secondary);
  font-size: 15px;
  margin-bottom: 4px;
}

.upload-subtext {
  color: var(--text-muted);
  font-size: 13px;
}

/* Preview */
.upload-preview {
  width: 100%;
}

.preview-image {
  width: 100%;
  max-height: 180px;
  object-fit: cover;
  border-radius: 2px;
  margin-bottom: 12px;
  animation: img-in 0.4s var(--ease-out-expo);
}

@keyframes img-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.file-name {
  color: var(--text-secondary);
  font-size: 13px;
  word-break: break-all;
}

/* Options */
.style-options {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.option-label {
  color: var(--text-muted);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.select {
  width: 100%;
  padding: 12px 0;
  background: transparent;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
  font-size: 14px;
  font-family: var(--font-body);
  cursor: pointer;
  transition: border-color 0.3s ease;
  appearance: none;
}

.select:hover,
.select:focus {
  outline: none;
  border-bottom-color: var(--accent);
}

.btn-submit {
  width: 100%;
  padding: 16px 24px;
  background: var(--accent);
  border: none;
  border-radius: 2px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.3s var(--ease-out-expo);
  margin-top: 12px;
}

.btn-submit:hover {
  background: #ff4444;
  transform: translateY(-2px);
}

.btn-submit.loading {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.upload-tip {
  margin-top: 20px;
  color: var(--text-muted);
  font-size: 12px;
  text-align: center;
}
</style>
