/* eslint-disable */
import { defineStore } from 'pinia'
import axios from 'axios'

// 配置axios基础URL
// 将baseURL设为空字符串，以便在API调用中直接使用完整路径
axios.defaults.baseURL = ''
axios.defaults.timeout = 60000 // 进一步延长超时时间到60秒，以适应AI分析需要
axios.defaults.withCredentials = true // 允许发送cookies

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    isAuthenticated: !!localStorage.getItem('token')
  }),
  getters: {
    getToken: (state) => state.token,
    getUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated
  },
  actions: {
    // 模拟登录方法，用于开发测试
    mockLogin() {
      console.log('使用模拟登录进行开发测试')
      // 设置模拟的token和用户信息
      this.token = 'mock-token-for-development'
      this.user = {
        id: '1',
        email: 'developer@example.com',
        username: '开发者',
        exam_date: '2024-12-31',
        selected_subjects: ['数学', '英语', '专业课'],
        ai_companion_style: '鼓励型',
        created_at: new Date().toISOString()
      }
      this.isAuthenticated = true
      localStorage.setItem('token', this.token)
      localStorage.setItem('user', JSON.stringify(this.user))
      return true
    },
    
    async login(email, password) {
      try {
        // 后端使用OAuth2PasswordRequestForm，需要用form格式发送数据
        const formData = new FormData()
        formData.append('username', email)  // OAuth2使用username字段
        formData.append('password', password)
        
        const response = await axios.post('/api/v1/auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        this.token = response.data.access_token
        this.user = response.data.user
        this.isAuthenticated = true
        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))
        return true
      } catch (error) {
        console.error('Login failed:', error)
        console.error('Error details:', error.response?.data)
        this.logout()
        return false
      }
    },
    async register(email, password, username) {
      try {
        const response = await axios.post('/api/v1/auth/register', { 
          email, 
          password, 
          username 
        })
        // 注册成功后自动设置token和用户信息
        this.token = response.data.access_token
        this.user = response.data.user
        this.isAuthenticated = true
        localStorage.setItem('token', this.token)
        localStorage.setItem('user', JSON.stringify(this.user))
        return { success: true }
      } catch (error) {
        console.error('Registration failed:', error)
        console.error('Error details:', error.response?.data)
        
        // 检查是否是邮箱已注册的错误
        if (error.response?.status === 400 && error.response?.data?.detail === 'Email already registered') {
          return { 
            success: false, 
            error: 'EMAIL_EXISTS',
            message: '该邮箱已被注册，请使用其他邮箱或前往登录页面'
          }
        }
        
        return { 
          success: false, 
          error: 'UNKNOWN_ERROR',
          message: '注册失败，请重试'
        }
      }
    },
    logout() {
      this.token = null
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})

