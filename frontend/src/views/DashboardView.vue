<template>
  <div class="dashboard">
    <!-- Header -->
    <header class="header">
      <div class="header-logo">◉ 留声画</div>
      <div class="header-user">
        <span class="user-email">{{ userStore.user?.email || '用户' }}</span>
        <button class="btn-text" @click="handleLogout">
          退出
          <span class="arrow">↗</span>
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main">
      <el-row :gutter="24">
        <!-- Upload Panel -->
        <el-col :xs="24" :sm="24" :md="8">
          <upload-panel @upload-success="handleUploadSuccess" />
        </el-col>

        <!-- Task List -->
        <el-col :xs="24" :sm="24" :md="16">
          <task-list :tasks="tasks" @refresh="fetchTasks" />
        </el-col>
      </el-row>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'
import api from '../api'
import UploadPanel from '../components/UploadPanel.vue'
import TaskList from '../components/TaskList.vue'

const router = useRouter()
const userStore = useUserStore()
const tasks = ref([])
let pollInterval = null

onMounted(async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  await userStore.fetchUser()
  await fetchTasks()
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})

const startPolling = () => {
  // Poll every 3 seconds for task status updates
  pollInterval = setInterval(pollTaskStatuses, 3000)
}

const stopPolling = () => {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

const pollTaskStatuses = async () => {
  // Find tasks that are pending or processing
  const activeTasks = tasks.value.filter(t => t.status === 'pending' || t.status === 'processing')

  if (activeTasks.length === 0) {
    return // No active tasks, nothing to poll
  }

  try {
    for (const task of activeTasks) {
      const response = await api.getTaskStatus(task.id)
      const newStatus = response.data.status

      // Update task in local state
      const taskIndex = tasks.value.findIndex(t => t.id === task.id)
      if (taskIndex !== -1) {
        const oldStatus = tasks.value[taskIndex].status
        tasks.value[taskIndex] = {
          ...tasks.value[taskIndex],
          status: newStatus,
          progress: response.data.progress || tasks.value[taskIndex].progress,
          current_step: response.data.current_step
        }

        // If task just completed, do a full refresh to get result_data
        if (oldStatus !== 'completed' && newStatus === 'completed') {
          ElMessage.success('任务已完成！')
          await fetchTasks() // Full refresh to get result_data
          return
        }

        // If task failed
        if (oldStatus !== 'failed' && newStatus === 'failed') {
          ElMessage.error('任务处理失败')
        }
      }
    }
  } catch (error) {
    console.error('Failed to poll task statuses:', error)
  }
}

const fetchTasks = async () => {
  try {
    const response = await api.getTasks()
    tasks.value = response.data.tasks || []
  } catch (error) {
    console.error('Failed to fetch tasks:', error)
    tasks.value = []
  }
}

const handleUploadSuccess = async (fileId) => {
  ElMessage.success('文件上传成功，正在创建任务...')
  try {
    await api.createTask(fileId, 'warm', 'xiaoxiao', 'gentle')
    ElMessage.success('任务已创建')
    await fetchTasks()
  } catch (error) {
    ElMessage.error('创建任务失败')
  }
}

const handleLogout = () => {
  stopPolling()
  userStore.logout()
  router.push('/')
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
}

/* Header */
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 48px;
  background: rgba(5, 5, 5, 0.98);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
}

.header-logo {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
}

.header-user {
  display: flex;
  align-items: center;
  gap: 32px;
}

.user-email {
  color: var(--text-secondary);
  font-size: 14px;
}

.arrow {
  display: inline-block;
  transition: transform 0.3s var(--ease-out-expo);
}

.btn-text:hover .arrow {
  transform: translate(2px, -2px);
}

/* Main Content */
.main {
  padding: 60px 48px 40px;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* Responsive */
@media (max-width: 768px) {
  .header {
    padding: 20px 24px;
  }

  .main {
    padding: 24px;
  }
}
</style>
