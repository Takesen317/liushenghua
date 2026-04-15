<template>
  <div class="video-player">
    <video
      ref="videoRef"
      :src="videoUrl"
      controls
      :poster="poster"
      @play="handlePlay"
      @pause="handlePause"
      @ended="handleEnded"
    />
    <div v-if="!videoUrl" class="placeholder">
      <el-icon :size="48"><video-play /></el-icon>
      <p>暂无视频</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { VideoPlay } from '@element-plus/icons-vue'

const props = defineProps({
  videoUrl: {
    type: String,
    default: ''
  },
  poster: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['play', 'pause', 'ended'])

const videoRef = ref()

const handlePlay = () => emit('play')
const handlePause = () => emit('pause')
const handleEnded = () => emit('ended')
</script>

<style scoped>
.video-player {
  position: relative;
  width: 100%;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

video {
  width: 100%;
  display: block;
}

.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  background: #f5f5f5;
  color: #909399;
}

.placeholder p {
  margin-top: 10px;
}
</style>
