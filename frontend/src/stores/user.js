import { defineStore } from 'pinia'
import api from '../api'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null,
    isLoggedIn: !!localStorage.getItem('access_token')
  }),

  actions: {
    async register(data) {
      try {
        const response = await api.register(data)
        console.log('Register success:', response.data)
        ElMessage.success('注册成功！')
        return true
      } catch (error) {
        const message = error.response?.data?.detail || '注册失败'
        console.error('Register failed:', error.response?.data)
        ElMessage.error(message)
        return false
      }
    },

    async login(username, password) {
      try {
        const response = await api.login(username, password)
        this.token = response.data.access_token
        this.isLoggedIn = true
        localStorage.setItem('access_token', this.token)
        await this.fetchUser()
        return true
      } catch (error) {
        console.error('Login failed:', error)
        ElMessage.error('登录失败，请检查邮箱和密码')
        return false
      }
    },

    async fetchUser() {
      try {
        const response = await api.getMe()
        this.user = response.data
      } catch (error) {
        console.error('Failed to fetch user:', error)
        this.logout()
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isLoggedIn = false
      localStorage.removeItem('access_token')
    }
  }
})
