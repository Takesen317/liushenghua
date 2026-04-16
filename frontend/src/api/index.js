import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000
})

// Request interceptor for auth token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // Auth
  register(data) {
    return api.post('/auth/register', data)
  },
  login(email, password) {
    const params = new URLSearchParams()
    params.append('username', email)
    params.append('password', password)
    return api.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  getMe() {
    return api.get('/auth/me')
  },

  // Files
  uploadFile(file, onProgress) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/files/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: onProgress
    })
  },
  getFile(fileId) {
    return api.get(`/files/${fileId}`)
  },
  deleteFile(fileId) {
    return api.delete(`/files/${fileId}`)
  },

  // Tasks
  createTask(fileId, style, voice, musicStyle) {
    return api.post('/tasks', {
      file_id: fileId,
      style: style || 'warm',
      voice: voice || 'xiaoxiao',
      music_style: musicStyle || 'gentle'
    })
  },
  getTask(taskId) {
    return api.get(`/tasks/${taskId}`)
  },
  getTasks() {
    return api.get('/tasks')
  },
  getTaskStatus(taskId) {
    return api.get(`/tasks/${taskId}/status`)
  },
  cancelTask(taskId) {
    return api.post(`/tasks/${taskId}/cancel`)
  },
  retryTask(taskId) {
    return api.post(`/tasks/${taskId}/retry`)
  },
  deleteTask(taskId) {
    return api.delete(`/tasks/${taskId}`)
  },

  // Share
  createShare(taskId) {
    return api.post('/share', { task_id: taskId })
  },
  getShare(shareCode) {
    return api.get(`/share/${shareCode}`)
  }
}
