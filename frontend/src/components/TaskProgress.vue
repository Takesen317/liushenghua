<template>
  <div class="task-progress">
    <el-progress
      :percentage="progress"
      :status="getStatus()"
      :stroke-width="10"
    />
    <div class="step-info">
      <span class="step-text">{{ currentStep || '等待处理...' }}</span>
      <span class="percentage">{{ progress }}%</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  progress: {
    type: Number,
    default: 0
  },
  currentStep: {
    type: String,
    default: ''
  },
  status: {
    type: String,
    default: 'pending'
  }
})

const getStatus = () => {
  if (props.status === 'completed') return 'success'
  if (props.status === 'failed') return 'exception'
  if (props.progress >= 100) return 'success'
  return undefined
}
</script>

<style scoped>
.task-progress {
  padding: 10px 0;
}

.step-info {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
}

.step-text {
  flex: 1;
}

.percentage {
  min-width: 40px;
  text-align: right;
}
</style>
