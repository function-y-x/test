<template>
  <div class="login-container">
    <!-- 花瓣飘落背景 -->
    <div class="falling-petals">
      <div v-for="i in 12" :key="i" class="petal-bg" :class="`petal-bg-${i}`">
        <img :src="i % 2 === 0 ? '/花瓣1.png' : '/花瓣2.png'" alt="飘落花瓣" />
      </div>
    </div>
    
    <div v-if="!showMoodCheck && !showAuthForm" class="welcome-animation">
      <!-- 书本元素 - 放在标题上方 -->
      <div class="book-container">
        <img src="/书.png" alt="心研领航书本" class="book-image" />
      </div>
      
      <!-- 标题 -->
      <h1 class="fade-in-text">欢迎来到心研领航 – 你的考研心灵伙伴</h1>
      
      <!-- 粒子群 - 独立定位 -->
      <div class="particles-container">
        <!-- 桌面端显示12个粒子 -->
        <div 
          v-for="i in 12" 
          :key="`desktop-${i}`" 
          class="heart-flow-particle hidden md:block"
          :style="getParticleStyle(i)"
        >
          <img 
            :src="i % 2 === 0 ? '/粒子1.png' : '/粒子2.png'" 
            alt="心流粒子" 
            class="object-contain"
            style="width: 100%; height: 100%;"
          />
        </div>
        
        <!-- 移动端显示6个粒子 -->
        <div 
          v-for="i in 6" 
          :key="`mobile-${i}`" 
          class="heart-flow-particle block md:hidden"
          :style="getMobileParticleStyle(i)"
        >
          <img 
            :src="i % 2 === 0 ? '/粒子1.png' : '/粒子2.png'" 
            alt="心流粒子" 
            class="object-contain"
            style="width: 100%; height: 100%;"
          />
        </div>
      </div>
      
      <!-- 开始按钮 -->
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

    // 粒子动态样式生成方法 - 从书本上方升空
    const getParticleStyle = (index) => {
      // 粒子从书本上方开始，随机分布在书本区域
      const bookCenterX = 50 // 书本中心X坐标
      const bookTopY = 8 // 书本位置，考虑margin-top: -40px的影响
      
      // 粒子起始位置的随机范围
      const offsetRange = 15 // X轴±8%范围，更集中在书本附近
      const startX = bookCenterX + (Math.random() - 0.5) * offsetRange
      const startY = bookTopY + (Math.random() - 0.5) * 2 // Y轴很小范围，紧贴书本上方
      
      // 粒子尺寸
      const particleSize = '14px'
      
      // 延迟：每个粒子错开，营造连续升空效果
      const delay = index * 0.5 + Math.random() * 1
      
      return {
        left: `${startX}%`,
        top: `${startY}%`,
        width: particleSize,
        height: particleSize,
        animationDelay: `${delay}s`
      }
    }

    const getMobileParticleStyle = (index) => {
      // 移动端粒子从书本上方升空
      const bookCenterX = 50
      const bookTopY = 8 // 书本位置，考虑margin-top: -40px的影响
      
      // 移动端起始范围
      const offsetRange = 15
      const startX = bookCenterX + (Math.random() - 0.5) * offsetRange
      const startY = bookTopY + (Math.random() - 0.5) * 2
      
      // 移动端粒子尺寸
      const particleSize = '12px'
      
      // 移动端延迟
      const delay = index * 0.4 + Math.random() * 0.8
      
      return {
        left: `${startX}%`,
        top: `${startY}%`,
        width: particleSize,
        height: particleSize,
        animationDelay: `${delay}s`
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
      getParticleStyle,
      getMobileParticleStyle
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
  position: relative;
  overflow: hidden;
}

/* 花瓣背景 */
.falling-petals {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

.petal-bg {
  position: absolute;
  animation: fall linear infinite;
  opacity: 0;
  top: -100px;
  /* 初始位置设置在屏幕外更高处 */
}

.petal-bg img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: transparent;
  /* 确保透明背景显示 */
}

/* 动态花瓣样式 */
.petal-bg-1 { width: 15px; height: 15px; left: 10%; animation-duration: 8s; animation-delay: -2s; }
.petal-bg-2 { width: 12px; height: 12px; left: 20%; animation-duration: 12s; animation-delay: -1s; }
.petal-bg-3 { width: 18px; height: 18px; left: 30%; animation-duration: 10s; animation-delay: -3s; }
.petal-bg-4 { width: 14px; height: 14px; left: 40%; animation-duration: 15s; animation-delay: -0.5s; }
.petal-bg-5 { width: 16px; height: 16px; left: 50%; animation-duration: 9s; animation-delay: -4s; }
.petal-bg-6 { width: 13px; height: 13px; left: 60%; animation-duration: 11s; animation-delay: -1.5s; }
.petal-bg-7 { width: 17px; height: 17px; left: 70%; animation-duration: 13s; animation-delay: -2.5s; }
.petal-bg-8 { width: 15px; height: 15px; left: 80%; animation-duration: 14s; animation-delay: -3.5s; }
.petal-bg-9 { width: 19px; height: 19px; left: 90%; animation-duration: 16s; animation-delay: -5s; }
.petal-bg-10 { width: 14px; height: 14px; left: 15%; animation-duration: 18s; animation-delay: -4.5s; }
.petal-bg-11 { width: 16px; height: 16px; left: 35%; animation-duration: 20s; animation-delay: -6s; }
.petal-bg-12 { width: 18px; height: 18px; left: 75%; animation-duration: 22s; animation-delay: -7s; }

/* 花瓣下降动画 */
@keyframes fall {
  0% { 
    top: -100px; 
    transform: rotate(0deg) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  25% {
    transform: rotate(90deg) translateX(-10px);
    opacity: 0.9;
  }
  50% {
    transform: rotate(180deg) translateX(5px);
    opacity: 1;
  }
  75% {
    transform: rotate(270deg) translateX(-15px);
    opacity: 0.7;
  }
  100% { 
    top: 100vh; 
    transform: rotate(360deg) translateX(10px);
    opacity: 0;
  }
}

/* 花瓣飘落关键帧动画 */
@keyframes petalFall1 {
  0% { 
    top: -50px; 
    transform: rotate(0deg) translateX(0);
    opacity: 0.8;
  }
  100% { 
    top: 100vh; 
    transform: rotate(360deg) translateX(30px);
    opacity: 0;
  }
}

@keyframes petalFall2 {
  0% { 
    top: -50px; 
    transform: rotate(0deg) translateX(0);
    opacity: 0.8;
  }
  50% {
    transform: rotate(180deg) translateX(-20px);
  }
  100% { 
    top: 100vh; 
    transform: rotate(360deg) translateX(10px);
    opacity: 0;
  }
}

@keyframes petalFall3 {
  0% { 
    top: -50px; 
    transform: rotate(0deg) translateX(0);
    opacity: 0.8;
  }
  30% {
    transform: rotate(120deg) translateX(15px);
  }
  70% {
    transform: rotate(240deg) translateX(-10px);
  }
  100% { 
    top: 100vh; 
    transform: rotate(360deg) translateX(20px);
    opacity: 0;
  }
}

@keyframes petalFall4 {
  0% { 
    top: -50px; 
    transform: rotate(0deg);
    opacity: 0.8;
  }
  100% { 
    top: 100vh; 
    transform: rotate(270deg);
    opacity: 0;
  }
}

@keyframes petalFall5 {
  0% { 
    top: -50px; 
    transform: rotate(0deg) translateX(0);
    opacity: 0.8;
  }
  25% {
    transform: rotate(90deg) translateX(-25px);
  }
  75% {
    transform: rotate(270deg) translateX(25px);
  }
  100% { 
    top: 100vh; 
    transform: rotate(360deg) translateX(0);
    opacity: 0;
  }
}

@keyframes petalFall6 {
  0% { 
    top: -50px; 
    transform: rotate(0deg);
    opacity: 0.8;
  }
  100% { 
    top: 100vh; 
    transform: rotate(180deg);
    opacity: 0;
  }
}

/* 其他花瓣使用简化动画 */
@keyframes petalFall7 { 
  0% { top: -50px; transform: rotate(0deg); opacity: 0.8; }
  100% { top: 100vh; transform: rotate(360deg); opacity: 0; }
}
@keyframes petalFall8 { 
  0% { top: -50px; transform: rotate(0deg); opacity: 0.8; }
  100% { top: 100vh; transform: rotate(450deg); opacity: 0; }
}
@keyframes petalFall9 { 
  0% { top: -50px; transform: rotate(0deg); opacity: 0.8; }
  100% { top: 100vh; transform: rotate(315deg); opacity: 0; }
}
@keyframes petalFall10 { 
  0% { top: -50px; transform: rotate(0deg); opacity: 0.8; }
  100% { top: 100vh; transform: rotate(540deg); opacity: 0; }
}
@keyframes petalFall11 { 
  0% { top: -50px; transform: rotate(0deg); opacity: 0.8; }
  100% { top: 100vh; transform: rotate(270deg); opacity: 0; }
}
@keyframes petalFall12 { 
  0% { top: -50px; transform: rotate(0deg); opacity: 0.8; }
  100% { top: 100vh; transform: rotate(405deg); opacity: 0; }
}

.welcome-animation {
  text-align: center;
  animation: fadeIn 2s ease-out;
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 书本容器 - 简化设计 */
.book-container {
  position: relative;
  margin-top: -40px; /* 负的上边距让书本往上移动 */
  margin-bottom: 5px; /* 减少底部间距，让标题更靠近书本 */
  display: flex;
  justify-content: center;
  align-items: center;
  animation: iconFadeIn 1s ease-out;
  animation-delay: 1s;
  animation-fill-mode: both;
  filter: drop-shadow(0 8px 24px rgba(0,0,0,0.15));
  order: 1; /* 确保书本在第一位 */
}

.book-image {
  width: 240px;
  height: 240px;
  object-fit: contain;
  background: transparent !important;
  animation: bookFlutter 6s ease-in-out infinite;
  margin: 0 auto;
  display: block;
}

/* 粒子容器 - 覆盖整个屏幕用于粒子升空 */
.particles-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  pointer-events: none;
  z-index: 1;
  overflow: visible;
}

/* 心流粒子emanation容器 */
.particles-emanation {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  background: transparent;
}

/* 心流粒子样式 - 增强版 */
.heart-flow-particle {
  position: absolute;
  background: transparent;
  background-size: contain;
  background-repeat: no-repeat;
  filter: drop-shadow(0 0 8px rgba(74, 144, 226, 0.9)) 
          drop-shadow(0 0 16px rgba(0, 255, 127, 0.8))
          drop-shadow(0 0 4px rgba(255, 255, 255, 0.9))
          drop-shadow(0 2px 8px rgba(0, 0, 0, 0.2));
  animation: heartFlowEmanation 6s ease-out infinite;
  animation-fill-mode: both;
  transform-origin: center center;
  will-change: transform, opacity;
  pointer-events: none;
  z-index: 20;
}

/* 心流粒子emanation动画 - 从书本上方由小到大升空淡出 */
@keyframes heartFlowEmanation {
  0% { 
    transform: scale(0.1) rotate(0deg);
    opacity: 0;
  }
  5% {
    transform: translateY(-10px) scale(0.2) rotate(2deg);
    opacity: 0.3;
  }
  15% {
    transform: translateY(-40px) scale(0.5) rotate(-5deg);
    opacity: 0.7;
  }
  25% {
    transform: translateY(-80px) scale(0.8) rotate(8deg);
    opacity: 1;
  }
  35% {
    transform: translateY(-130px) scale(1.1) rotate(-3deg);
    opacity: 1;
  }
  45% {
    transform: translateY(-190px) scale(1.4) rotate(10deg);
    opacity: 0.9;
  }
  55% {
    transform: translateY(-260px) scale(1.7) rotate(-7deg);
    opacity: 0.8;
  }
  65% {
    transform: translateY(-340px) scale(2.0) rotate(12deg);
    opacity: 0.7;
  }
  75% {
    transform: translateY(-430px) scale(2.3) rotate(-5deg);
    opacity: 0.5;
  }
  85% {
    transform: translateY(-530px) scale(2.6) rotate(8deg);
    opacity: 0.3;
  }
  95% {
    transform: translateY(-640px) scale(2.8) rotate(-3deg);
    opacity: 0.1;
  }
  100% { 
    transform: translateY(-750px) scale(3.0) rotate(0deg);
    opacity: 0;
  }
}

/* 书本翻页动画 */
@keyframes bookFlutter {
  0%, 100% { transform: rotate(0deg) scale(1); }
  25% { transform: rotate(-1deg) scale(1.02); }
  50% { transform: rotate(0deg) scale(1.01); }
  75% { transform: rotate(1deg) scale(1.02); }
}



.fade-in-text {
  font-size: 2.5em;
  margin-top: -30px; /* 负的上边距让标题更靠近书本 */
  margin-bottom: 20px;
  opacity: 0;
  animation: textFadeIn 2s forwards;
  animation-delay: 0.5s;
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 1.2;
  order: 2; /* 确保标题在书本后面 */
}

.title-line-1 {
  font-size: 1em;
  font-weight: 700;
  color: #2c3e50;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 8px;
  background: linear-gradient(135deg, #2c3e50, #34495e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-line-2 {
  font-size: 0.75em;
  font-weight: 400;
  color: #7f8c8d;
  font-style: italic;
  opacity: 0;
  animation: titleLine2FadeIn 2s forwards;
  animation-delay: 1.2s;
  letter-spacing: 1px;
}

.start-button {
  padding: 20px 40px;
  font-size: 2.0em;
  background: linear-gradient(135deg, #81C784, #A5D6A7);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  opacity: 0;
  animation: buttonFadeIn 2s forwards;
  animation-delay: 2.5s;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 6px 16px rgba(129, 199, 132, 0.3);
  order: 3; /* 确保按钮在最后 */
}

.start-button:hover {
  background: linear-gradient(135deg, #66BB6A, #81C784);
  transform: translateY(-3px);
  box-shadow: 0 12px 28px rgba(129, 199, 132, 0.5);
}

.mood-check-modal {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 40px;
  border-radius: 24px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.12),
    0 2px 16px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
  margin: 20px auto 0; /* 使用auto确保水平居中 */
  text-align: center;
  opacity: 0;
  animation: fadeIn 0.5s forwards;
  animation-delay: 3s;
  max-width: 420px;
  width: 90%;
  position: relative;
  overflow: hidden;
  box-sizing: border-box; /* 确保padding包含在width内 */
}

.mood-check-modal::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.6) 50%, 
    transparent 100%);
}

.mood-check-modal h2 {
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 1.8rem;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.5px;
}

.mood-check-modal select {
  width: 100%;
  padding: 16px 20px;
  margin-bottom: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: #2c3e50;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  appearance: none;
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23666"><path d="M7 10l5 5 5-5z"/></svg>');
  background-repeat: no-repeat;
  background-position: right 16px center;
  background-size: 20px;
  box-sizing: border-box; /* 确保padding包含在width内 */
}

.mood-check-modal select:focus {
  outline: none;
  border-color: rgba(74, 144, 226, 0.6);
  background: rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 0 0 3px rgba(74, 144, 226, 0.1),
    0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.mood-check-modal input[type="range"] {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.3);
  outline: none;
  border-radius: 20px;
  margin: 20px 0;
  appearance: none;
  backdrop-filter: blur(10px);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.mood-check-modal input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #4a90e2, #357abd);
  cursor: pointer;
  border-radius: 50%;
  box-shadow: 
    0 4px 12px rgba(74, 144, 226, 0.4),
    0 2px 6px rgba(0, 0, 0, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.8);
  transition: all 0.2s ease;
}

.mood-check-modal input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 
    0 6px 20px rgba(74, 144, 226, 0.5),
    0 3px 8px rgba(0, 0, 0, 0.3);
}

.mood-check-modal input[type="range"]::-moz-range-thumb {
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #4a90e2, #357abd);
  cursor: pointer;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.8);
  box-shadow: 
    0 4px 12px rgba(74, 144, 226, 0.4),
    0 2px 6px rgba(0, 0, 0, 0.2);
}

.mood-check-modal p {
  color: #34495e;
  font-size: 16px;
  font-weight: 500;
  margin: 15px 0 25px 0;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.mood-check-modal button {
  background: linear-gradient(135deg, #4a90e2, #357abd);
  color: white;
  padding: 16px 32px;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 
    0 4px 16px rgba(74, 144, 226, 0.3),
    0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-transform: none;
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
}

.mood-check-modal button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.2), 
    transparent);
  transition: left 0.5s ease;
}

.mood-check-modal button:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 24px rgba(74, 144, 226, 0.4),
    0 4px 12px rgba(0, 0, 0, 0.2);
  background: linear-gradient(135deg, #5ba0f2, #4080cd);
}

.mood-check-modal button:hover::before {
  left: 100%;
}

.mood-check-modal button:active {
  transform: translateY(0);
  box-shadow: 
    0 4px 16px rgba(74, 144, 226, 0.3),
    0 2px 8px rgba(0, 0, 0, 0.1);
}

.auth-form {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 40px;
  border-radius: 24px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.12),
    0 2px 16px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
  margin: 20px auto 0; /* 使用auto确保水平居中 */
  text-align: center;
  opacity: 0;
  animation: fadeIn 0.5s forwards;
  animation-delay: 3s;
  max-width: 420px;
  width: 90%;
  position: relative;
  overflow: hidden;
  box-sizing: border-box; /* 确保padding包含在width内 */
}

.auth-form::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.6) 50%, 
    transparent 100%);
}

.auth-form h2 {
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 1.8rem;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.5px;
}

.auth-form input {
  width: 100%;
  padding: 16px 20px;
  margin-bottom: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  color: #2c3e50;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-sizing: border-box; /* 确保padding包含在width内 */
}

.auth-form input:focus {
  outline: none;
  border-color: rgba(74, 144, 226, 0.6);
  background: rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 0 0 3px rgba(74, 144, 226, 0.1),
    0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.auth-form input::placeholder {
  color: rgba(44, 62, 80, 0.6);
}

.auth-form button {
  background: linear-gradient(135deg, #4a90e2, #357abd);
  color: white;
  padding: 16px 32px;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 
    0 4px 16px rgba(74, 144, 226, 0.3),
    0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-transform: none;
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
  width: 100%;
  margin-top: 10px;
  box-sizing: border-box; /* 确保padding包含在width内 */
}

.auth-form button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.2), 
    transparent);
  transition: left 0.5s ease;
}

.auth-form button:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 24px rgba(74, 144, 226, 0.4),
    0 4px 12px rgba(0, 0, 0, 0.2);
  background: linear-gradient(135deg, #5ba0f2, #4080cd);
}

.auth-form button:hover::before {
  left: 100%;
}

.auth-form button:active {
  transform: translateY(0);
  box-shadow: 
    0 4px 16px rgba(74, 144, 226, 0.3),
    0 2px 8px rgba(0, 0, 0, 0.1);
}

.auth-form p {
  margin-top: 20px;
  color: #4a90e2;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  text-decoration: none;
  position: relative;
}

.auth-form p:hover {
  color: #357abd;
  text-shadow: 0 2px 4px rgba(74, 144, 226, 0.2);
  transform: translateY(-1px);
}

.auth-form p::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(135deg, #4a90e2, #357abd);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.auth-form p:hover::after {
  width: 100%;
}

/* 花瓣动画性能优化 */
@media (prefers-reduced-motion: reduce) {
  .petal {
    animation: none;
    display: none;
  }
}

/* 移动端优化 */
@media (max-width: 768px) {
  .petal:nth-child(n+7) {
    display: none; /* 移动端只显示前6个花瓣 */
  }
  
  .petal {
    width: 8px;
    height: 8px; /* 移动端花瓣更小 */
  }
  
  .fade-in-text {
    font-size: 2em; /* 移动端字体稍小 */
  }
  
  .title-line-1 {
    font-size: 1em;
  }
  
  .title-line-2 {
    font-size: 0.7em;
  }
}

@media (max-width: 480px) {
  .petal:nth-child(n+5) {
    display: none; /* 小屏幕只显示前4个花瓣 */
  }
  
  .fade-in-text {
    font-size: 1.8em; /* 小屏幕字体更小 */
  }
  
  .title-line-1 {
    font-size: 1em;
  }
  
  .title-line-2 {
    font-size: 0.65em;
  }
  
  .hero-icon svg {
    width: 120px;
    height: 120px;
  }
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
  width: 100%;
  max-width: 500px;
  margin: 0 auto; /* 添加水平居中 */
  position: relative;
  z-index: 2;
}

.page-title {
  font-size: 2.2em;
  margin-bottom: 30px;
  color: #2c3e50;
  opacity: 0;
  animation: textFadeIn 1s forwards;
  font-weight: 300;
  letter-spacing: 1px;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: linear-gradient(135deg, #2c3e50, #34495e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes iconFadeIn {
  from { 
    opacity: 0; 
    transform: translateY(-20px) scale(0.8); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0) scale(1); 
  }
}

@keyframes textFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes buttonFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 响应式设计 - Tailwind CSS 媒体查询 */
@media (max-width: 768px) {
  .book-particles-container {
    width: 240px;
    height: 240px;
  }
  
  .book-center {
    width: 180px;
    height: 180px;
  }
  
  .fade-in-text {
    font-size: 1.8em;
  }
  
  /* 移动端粒子效果优化 */
  .heart-flow-particle {
    filter: drop-shadow(0 0 6px rgba(74, 144, 226, 0.8)) 
            drop-shadow(0 0 12px rgba(0, 255, 127, 0.7))
            drop-shadow(0 0 3px rgba(255, 255, 255, 0.8));
  }
}

@media (max-width: 480px) {
  .book-container {
    width: 200px;
    height: 200px;
  }
  
  .book-center {
    width: 150px;
    height: 150px;
  }
  
  .fade-in-text {
    font-size: 1.5em;
  }
  
  /* 小屏幕粒子效果进一步优化 */
  .heart-flow-particle {
    filter: drop-shadow(0 0 4px rgba(74, 144, 226, 0.7)) 
            drop-shadow(0 0 8px rgba(0, 255, 127, 0.6))
            drop-shadow(0 0 2px rgba(255, 255, 255, 0.7));
  }
}
</style>

