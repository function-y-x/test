/* eslint-disable */
import { defineStore } from 'pinia'
import axios from 'axios'

// 配置axios基础URL
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/api/v1'
axios.defaults.timeout = 10000 // 设置10秒超时
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
    async login(email, password) {
      try {
        // 后端使用OAuth2PasswordRequestForm，需要用form格式发送数据
        const formData = new FormData()
        formData.append('username', email)  // OAuth2使用username字段
        formData.append('password', password)
        
        const response = await axios.post('/auth/login', formData, {
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
        const response = await axios.post('/auth/register', { 
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

