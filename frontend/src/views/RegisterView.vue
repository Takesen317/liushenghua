<template>
  <div class="auth-page">
    <div class="auth-container">
      <!-- Logo -->
      <div class="auth-logo" @click="$router.push('/')">留声画</div>

      <!-- Card -->
      <div class="auth-card">
        <div class="auth-header">
          <h2>注册</h2>
          <p class="auth-subtitle">创建新账户</p>
        </div>

        <form class="auth-form" @submit.prevent="handleRegister">
          <div class="form-group">
            <input
              v-model="form.nickname"
              type="text"
              class="input-underline"
              placeholder="昵称"
              required
            />
          </div>

          <div class="form-group">
            <input
              v-model="form.email"
              type="email"
              class="input-underline"
              placeholder="邮箱"
              required
            />
          </div>

          <div class="form-group">
            <input
              v-model="form.password"
              type="password"
              class="input-underline"
              placeholder="密码"
              required
            />
          </div>

          <div class="form-group">
            <input
              v-model="form.confirmPassword"
              type="password"
              class="input-underline"
              placeholder="确认密码"
              required
            />
          </div>

          <button type="submit" class="btn-submit" :class="{ loading }">
            <span v-if="!loading">注册</span>
            <span v-else class="loading-dots">...</span>
          </button>
        </form>

        <div class="auth-footer">
          <span class="text-muted">已有账号？</span>
          <router-link to="/login" class="link-underline">
            立即登录
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)

const form = reactive({
  nickname: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  if (!form.nickname || !form.email || !form.password) return

  if (form.password !== form.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }

  if (form.password.length < 6) {
    ElMessage.error('密码至少6位')
    return
  }

  loading.value = true
  try {
    const success = await userStore.register({
      email: form.email,
      password: form.password,
      nickname: form.nickname
    })
    if (success) {
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
}

.auth-container {
  width: 100%;
  max-width: 380px;
}

.auth-logo {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  text-align: center;
  letter-spacing: 0.2em;
  margin-bottom: 60px;
  cursor: pointer;
  transition: color 0.3s ease;
}

.auth-logo:hover {
  color: var(--accent);
}

.auth-card {
  background: rgba(10, 10, 10, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 4px;
  padding: 48px 40px;
  backdrop-filter: blur(20px);
}

.auth-header {
  text-align: center;
  margin-bottom: 40px;
}

.auth-header h2 {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
  letter-spacing: 0.1em;
}

.auth-subtitle {
  color: var(--text-secondary);
  font-size: 14px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.form-group {
  position: relative;
}

.input-underline {
  width: 100%;
  padding: 16px 0;
  background: transparent;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  color: var(--text-primary);
  font-size: 16px;
  font-family: var(--font-body);
  transition: border-color 0.3s ease;
}

.input-underline::placeholder {
  color: var(--text-muted);
}

.input-underline:focus {
  outline: none;
  border-bottom-color: var(--accent);
}

.btn-submit {
  width: 100%;
  padding: 18px 24px;
  background: var(--accent);
  border: none;
  border-radius: 2px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: all 0.3s var(--ease-out-expo);
  margin-top: 16px;
}

.btn-submit:hover {
  background: #ff4444;
  transform: translateY(-2px);
}

.btn-submit:active {
  transform: translateY(0);
}

.loading-dots {
  animation: dots 1s infinite;
}

@keyframes dots {
  0%, 20% { content: '.'; }
  40% { content: '..'; }
  60%, 100% { content: '...'; }
}

.auth-footer {
  margin-top: 40px;
  text-align: center;
  font-size: 14px;
  display: flex;
  justify-content: center;
  gap: 8px;
}

.link-underline {
  position: relative;
  color: var(--text-secondary);
  transition: color 0.3s ease;
}

.link-underline::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: var(--accent);
  transition: width 0.3s var(--ease-out-expo);
}

.link-underline:hover {
  color: var(--accent);
}

.link-underline:hover::after {
  width: 100%;
}
</style>
