<template>
  <div class="login-container">
    <div v-if="!showMoodCheck && !showAuthForm" class="welcome-animation">
      <h1 class="fade-in-text">欢迎来到研心合一 – 你的考研心灵伙伴</h1>
      <button @click="startJourney" class="start-button">开始旅程</button>
    </div>

    <div v-if="showMoodCheck" class="mood-check-section">
      <h1 class="page-title">心情快照 – 记录此刻的你</h1>
      <div class="mood-check-modal">
        <h2>快速心情打卡</h2>
        <select v-model="moodKeyword">
          <option disabled value="">请选择情绪</option>

          <option value="happy">开心</option>
          <option value="calm">平静</option>
          <option value="anxious">焦虑</option>
          <option value="stressed">压力</option>
          <option value="sad">难过</option>
          <option value="excited">兴奋</option>
          <option value="tired">疲惫</option>
          <option value="focused">专注</option>
        </select>
        <input type="range" min="1" max="10" v-model="stressScore" />
        <p>压力评分: {{ stressScore }}</p>
        <button @click="submitMood">提交</button>
      </div>
    </div>

    <div v-if="showAuthForm" class="auth-section">
      <h1 class="page-title">{{ isRegistering ? '加入我们 – 开启心灵成长之旅' : '欢迎回来 – 继续你的学习旅程' }}</h1>
      <div class="auth-form">
      <h2>{{ isRegistering ? '注册' : '登录' }}</h2>
      
      <!-- 错误消息提示 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      
      <input type="email" v-model="email" placeholder="邮箱" />
      <input type="password" v-model="password" placeholder="密码" />
      <input v-if="isRegistering" type="text" v-model="username" placeholder="用户名" />
      <button @click="submitAuth">{{ isRegistering ? '注册' : '登录' }}</button>
      <!-- 开发测试用：模拟登录按钮 -->
      <button @click="mockLogin" style="margin-top: 10px; background-color: #4CAF50; color: white;">开发测试：跳过登录</button>
      <p @click="toggleAuthMode">
        {{ isRegistering ? '已有账号？去登录' : '没有账号？去注册' }}
      </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const showMoodCheck = ref(false)
    const showAuthForm = ref(false)
    const isRegistering = ref(false)

    const moodKeyword = ref('')
    const stressScore = ref(5)
    const email = ref('')
    const password = ref('')
    const username = ref('')
    const errorMessage = ref('')

    const startJourney = () => {
      showMoodCheck.value = true
    }

    const submitMood = async () => {
      if (!moodKeyword.value) {
        alert('请选择一个情绪')
        return
      }
      
      try {
        // 将情绪数据临时存储到localStorage，登录后再提交
        const moodData = {
          mood: moodKeyword.value,
          stress_level: parseInt(stressScore.value),
          timestamp: new Date().toISOString()
        }
        localStorage.setItem('pendingMoodData', JSON.stringify(moodData))
        console.log('情绪数据已临时保存:', moodData)
        
        // 更温和的过渡，不使用alert
        showMoodCheck.value = false
        // 短暂延迟让用户看到过渡效果
        setTimeout(() => {
          showAuthForm.value = true
        }, 300) // 0.3秒的短暂过渡
      } catch (error) {
        console.error('保存情绪数据失败:', error)
        alert('保存失败，请重试')
      }
    }

    const toggleAuthMode = () => {
      isRegistering.value = !isRegistering.value
      errorMessage.value = '' // 清除错误消息
    }

    // 模拟登录方法
    const mockLogin = () => {
      console.log('执行模拟登录')
      authStore.mockLogin()
      // 模拟登录后直接跳转到仪表盘
      router.push('/dashboard')
    }
    
    const submitAuth = async () => {
      errorMessage.value = '' // 清除之前的错误消息
      
      if (isRegistering.value) {
        const result = await authStore.register(email.value, password.value, username.value)
        if (result.success) {
          // 注册成功后，检查是否有待提交的情绪数据
          const pendingMoodData = localStorage.getItem('pendingMoodData')
          if (pendingMoodData) {
            try {
              const moodData = JSON.parse(pendingMoodData)
              console.log('检测到待提交的情绪数据:', moodData)
              
              // 发送情绪数据到后端
              const token = localStorage.getItem('token') // 修正：使用正确的key
              console.log('使用token提交情绪数据:', token ? '有token' : '无token')
              
              const response = await fetch('http://localhost:8000/api/v1/moods/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(moodData)
              })
              
              console.log('情绪数据提交响应状态:', response.status)
              if (response.ok) {
                const responseData = await response.json()
                console.log('情绪数据提交成功:', responseData)
                localStorage.removeItem('pendingMoodData') // 删除临时数据
              } else {
                const errorData = await response.text()
                console.error('情绪数据提交失败:', response.status, errorData)
              }
            } catch (error) {
              console.error('处理待提交情绪数据时出错:', error)
            }
          }
          
          // 注册成功，跳转到入门指导
          router.push('/onboarding')
        } else if (result.error === 'EMAIL_EXISTS') {
          // 邮箱已存在，显示消息并自动跳转到登录
          errorMessage.value = result.message
          setTimeout(() => {
            isRegistering.value = false // 切换到登录模式
            errorMessage.value = '请使用该邮箱登录'
          }, 800) // 改为0.8秒
        } else {
          // 其他错误
          errorMessage.value = result.message || '注册失败，请重试。'
        }
      } else {
        const success = await authStore.login(email.value, password.value)
        if (success) {
          // 登录成功后，检查是否有待提交的情绪数据
          const pendingMoodData = localStorage.getItem('pendingMoodData')
          if (pendingMoodData) {
            try {
              const moodData = JSON.parse(pendingMoodData)
              console.log('检测到待提交的情绪数据:', moodData)
              
              // 发送情绪数据到后端
              const token = localStorage.getItem('token') // 修正：使用正确的key
              console.log('使用token提交情绪数据:', token ? '有token' : '无token')
              
              const response = await fetch('http://localhost:8000/api/v1/moods/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(moodData)
              })
              
              console.log('情绪数据提交响应状态:', response.status)
              if (response.ok) {
                const responseData = await response.json()
                console.log('情绪数据提交成功:', responseData)
                localStorage.removeItem('pendingMoodData') // 删除临时数据
              } else {
                const errorData = await response.text()
                console.error('情绪数据提交失败:', response.status, errorData)
              }
            } catch (error) {
              console.error('处理待提交情绪数据时出错:', error)
            }
          }
          
          router.push('/dashboard')
        } else {
          errorMessage.value = '登录失败，请检查邮箱和密码。'
        }
      }
    }

    return {
      showMoodCheck,
      showAuthForm,
      isRegistering,
      moodKeyword,
      stressScore,
      email,
      password,
      username,
      errorMessage,
      startJourney,
      submitMood,
      submitAuth,
      toggleAuthMode,
      mockLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); /* 蓝绿渐变 */
  color: #333;
  font-family: 'Arial', sans-serif;
}

.welcome-animation {
  text-align: center;
  animation: fadeIn 2s ease-out;
}

.fade-in-text {
  font-size: 2.5em;
  margin-bottom: 20px;
  opacity: 0;
  animation: textFadeIn 2s forwards;
  animation-delay: 0.5s;
}

.start-button {
  padding: 12px 25px;
  font-size: 1.2em;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  opacity: 0;
  animation: buttonFadeIn 2s forwards;
  animation-delay: 2.5s;
}

.start-button:hover {
  background-color: #45a049;
}

.mood-check-modal,
.auth-form {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  text-align: center;
  opacity: 0;
  animation: fadeIn 0.5s forwards;
  animation-delay: 3s;
}

.mood-check-modal h2,
.auth-form h2 {
  color: #333;
  margin-bottom: 20px;
}

.mood-check-modal select,
.mood-check-modal input[type="range"],
.auth-form input {
  width: 80%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.mood-check-modal button,
.auth-form button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.mood-check-modal button:hover,
.auth-form button:hover {
  background-color: #0056b3;
}

.auth-form p {
  margin-top: 15px;
  color: #007bff;
  cursor: pointer;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 15px;
  font-size: 14px;
}

.mood-check-section,
.auth-section {
  text-align: center;
  animation: fadeIn 0.5s ease-out;
}

.page-title {
  font-size: 2.2em;
  margin-bottom: 30px;
  color: #333;
  opacity: 0;
  animation: textFadeIn 1s forwards;
  font-weight: 300;
  letter-spacing: 1px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes textFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes buttonFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

