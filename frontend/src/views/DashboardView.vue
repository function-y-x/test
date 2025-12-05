<template>
  <div class="healing-dashboard">
    <!-- 背景动画层 -->
    <div class="background-waves">
      <div class="wave wave-1"></div>
      <div class="wave wave-2"></div>
      <div class="wave wave-3"></div>
    </div>
    
    <!-- 顶部欢迎区域 -->
    <header class="welcome-section">
      <!-- 左上角提示气泡 -->
      <div class="tip-bubble">
        <div class="tip-content">
          <span class="tip-text">点击心情气泡可更新当前的心情哦~</span>
        </div>
        <div class="tip-arrow"></div>
      </div>
      
      <!-- 右上角退出按钮 -->
      <button @click="logout" class="healing-logout-btn">轻松退出</button>
      
      <h1 class="healing-title">欢迎回来，{{ user?.username || 'jtb' }}!</h1>
      
      <!-- 状态气泡群 -->
      <div class="stats-cloud">
        <!-- 考试倒计时气泡 -->
        <div class="bubble-float exam-bubble">
          <div class="bubble-content">
            <div class="bubble-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12,6 12,12 16,14"/>
              </svg>
            </div>
            <span class="stat-number">{{ daysUntilExam }}</span>
            <span class="stat-label">考试倒计时(天)</span>
          </div>
        </div>
        
        <!-- 当前心情气泡 -->
        <div class="bubble-float mood-bubble" @click="showMoodQuickCheck" title="点击快速记录心情">
          <div class="bubble-content">
            <div class="bubble-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
            </div>
            <span class="stat-number">{{ currentMood }}</span>
            <span class="stat-label">当前心情</span>
          </div>
        </div>
        
        <!-- 在线学习时长气泡 -->
        <div class="bubble-float time-bubble">
          <div class="bubble-content">
            <div class="bubble-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"/>
              </svg>
            </div>
            <span class="stat-number">{{ formattedStudyTime }}</span>
            <span class="stat-label">在线学习时长</span>
          </div>
        </div>
        
        <!-- 压力指数气泡 -->
        <div class="bubble-float stress-bubble" @click="showMoodQuickCheck" title="点击更新压力指数">
          <div class="bubble-content">
            <div class="bubble-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
            </div>
            <span class="stat-number">{{ stressLevel }}/10</span>
            <span class="stat-label">压力指数</span>
          </div>
        </div>
      </div>
    </header>

    <!-- 情绪快照弹窗 -->
    <div v-if="showMoodModal" class="mood-overlay" @click="closeMoodModal">
      <div class="mood-bubble-modal" @click.stop>
        <div class="modal-header">
          <h3>心情快照 - 记录此刻的你</h3>
          <div class="close-ripple" @click="closeMoodModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </div>
        </div>
        
        <div class="healing-form">
          <div class="mood-selection">
            <label class="form-label">快速心情打卡</label>
            <div class="mood-grid">
              <div 
                v-for="mood in moodOptions" 
                :key="mood.value"
                class="mood-option"
                :class="{ active: selectedMood === mood.value }"
                @click="selectedMood = mood.value"
              >
                <div class="mood-text">{{ mood.label }}</div>
              </div>
            </div>
          </div>
          
          <div class="stress-section">
            <label class="form-label">压力评分: {{ tempStressLevel }}</label>
            <div class="stress-track">
              <input 
                type="range" 
                min="1" 
                max="10" 
                v-model="tempStressLevel" 
                class="healing-slider"
              />
              <div class="stress-labels">
                <span>轻松</span>
                <span>适中</span>
                <span>紧张</span>
              </div>
            </div>
          </div>
          
          <div class="modal-actions">
            <button @click="submitMoodData" class="submit-bubble">记录心情</button>
            <button @click="closeMoodModal" class="cancel-bubble">稍后再说</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 - 左右分栏布局 -->
    <div class="main-content-layout">
      <!-- 左侧：任务气泡链条区域 -->
      <section class="left-panel task-bubbles-section">
        <div class="task-cloud">
          <h2 class="section-title todolist-title">ToDoList</h2>
          
          <div class="task-input-bubble">
            <div class="input-wrapper">
              <input 
                v-model="newTodo" 
                @keyup.enter="addTodo"
                placeholder="种下一个新目标..."
                class="healing-input"
              />
              <button @click="addTodo" class="add-task-ripple">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"/>
                  <line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
              </button>
            </div>
          </div>
          
          <div class="tasks-flow">
            <div 
              v-for="todo in todos" 
              :key="todo.id"
              class="task-bubble"
              :class="{ 'completed': todo.completed }"
              @click="toggleTodo(todo.id)"
            >
              <div class="task-content">
                <div class="task-check">
                  <svg v-if="todo.completed" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                  </svg>
                  <div v-else class="check-circle"></div>
                </div>
                <span class="task-text">{{ todo.text }}</span>
              </div>
              <div class="completion-glow" v-if="todo.completed"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- 右侧：功能气泡星座 -->
      <main class="right-panel modules-constellation">
      <div class="floating-modules">
        <div class="module-bubble stress-module" @click="navigateTo('/stress-radar')">
          <div class="bubble-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 3v18h18"/>
              <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
            </svg>
          </div>
          <h3>压力雷达</h3>
          <p>监测学习压力</p>
          <div class="ripple-effect"></div>
        </div>

        <div class="module-bubble flow-module" @click="navigateTo('/flow-training')">
          <div class="bubble-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 9V5a3 3 0 0 0-6 0v4"/>
              <rect x="2" y="9" width="20" height="12" rx="2" ry="2"/>
            </svg>
          </div>
          <h3>心流训练</h3>
          <p>专注力提升</p>
          <div class="ripple-effect"></div>
        </div>

        <div class="module-bubble emotional-module" @click="navigateTo('/emotional-aid')">
          <div class="bubble-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
          </div>
          <h3>情绪急救</h3>
          <p>快速情绪调节和心理支持</p>
          <div class="ripple-effect"></div>
        </div>

        <div class="module-bubble painting-module" @click="navigateTo('/mind-painting')">
          <div class="bubble-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 19l7-7 3 3-7 7-3-3z"/>
              <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
              <path d="M2 2l7.586 7.586"/>
              <circle cx="11" cy="11" r="2"/>
            </svg>
          </div>
          <h3>心灵画语</h3>
          <p>艺术疗愈</p>
          <div class="ripple-effect"></div>
        </div>

        <div class="module-bubble messenger-module" @click="navigateTo('/messenger')">
          <div class="bubble-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <h3>心语信使</h3>
          <p>内心对话</p>
          <div class="ripple-effect"></div>
        </div>

        <div class="module-bubble review-module" @click="navigateTo('/error-review')">
          <div class="bubble-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14,2 14,8 20,8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10,9 9,9 8,9"/>
            </svg>
          </div>
          <h3>错题复盘表</h3>
          <p>学习反思和总结提升</p>
          <div class="ripple-effect"></div>
        </div>

        <div class="module-bubble report-module" @click="navigateTo('/weekly-report')">
          <div class="bubble-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
          </div>
          <h3>我的周报</h3>
          <p>学习报告</p>
          <div class="ripple-effect"></div>
        </div>
      </div>
      </main>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import axios from 'axios'

export default {
  name: 'DashboardView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const user = computed(() => authStore.getUser)
    const examDate = ref('2025-12-20') // Placeholder, should come from user profile
    const currentMood = ref('平静') // 将从最新情绪记录获取
    
    // 学习时长计时器
    const studyStartTime = ref(Date.now())
    const currentTime = ref(Date.now())
    const stressLevel = ref(5) // 将从最新情绪记录获取，范围 1-10
    
    // 情绪快照弹窗相关
    const showMoodModal = ref(false)
    const selectedMood = ref('calm')
    const tempStressLevel = ref(5)
    
    // 情绪选项数据
    const moodOptions = ref([
      { value: 'happy', label: '开心' },
      { value: 'calm', label: '平静' },
      { value: 'anxious', label: '焦虑' },
      { value: 'stressed', label: '压力' },
      { value: 'sad', label: '难过' },
      { value: 'excited', label: '兴奋' },
      { value: 'tired', label: '疲惫' },
      { value: 'focused', label: '专注' }
    ])
    
    // Todo List 相关
    const newTodo = ref('')
    const todos = ref([]) // 从空数组开始，将从API加载

    // 计算在线学习时长（格式化显示）
    const formattedStudyTime = computed(() => {
      const diffMs = currentTime.value - studyStartTime.value
      const hours = Math.floor(diffMs / (1000 * 60 * 60))
      const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
      
      if (hours > 0) {
        return `${hours}h${minutes}m`
      } else {
        return `${minutes}m`
      }
    })

    const daysUntilExam = computed(() => {
      const today = new Date()
      const exam = new Date(examDate.value)
      const diffTime = Math.abs(exam - today)
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    })

    let timeInterval = null

    // 更新时间的函数
    const updateTime = () => {
      currentTime.value = Date.now()
    }

    // 获取今日任务
    const fetchTodayTasks = async () => {
      try {
        const token = authStore.getToken
        if (!token) return

        const response = await axios.get('/tasks/today', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.data) {
          todos.value = response.data.map(task => ({
            id: task.id,
            text: task.text,
            completed: task.completed
          }))
        }
      } catch (error) {
        console.error('获取今日任务失败:', error)
      }
    }

    // 添加新任务
    const addTodo = async () => {
      if (!newTodo.value.trim()) return

      try {
        const token = authStore.getToken
        console.log('当前token:', token) // 调试信息
        if (!token) {
          alert('请先登录')
          return
        }

        const response = await axios.post('/tasks/', {
          text: newTodo.value.trim()
        }, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (response.status === 200 || response.status === 201) {
          // 添加到本地列表
          todos.value.push({
            id: response.data.id,
            text: response.data.text,
            completed: response.data.completed
          })
          newTodo.value = ''
        }
      } catch (error) {
        console.error('添加任务失败:', error)
        console.error('错误详情:', error.response?.data)
        if (error.response?.status === 401) {
          alert('登录已过期，请重新登录')
          authStore.logout()
          router.push('/login')
        } else {
          alert('添加任务失败，请稍后重试')
        }
      }
    }

    // 切换任务完成状态
    const toggleTodo = async (id) => {
      try {
        const token = authStore.getToken
        console.log('切换任务token:', token) // 调试信息
        if (!token) return

        const todo = todos.value.find(t => t.id === id)
        if (!todo) return

        const newCompletedStatus = !todo.completed

        const response = await axios.put(`/tasks/${id}`, {
          completed: newCompletedStatus
        }, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (response.status === 200) {
          // 更新本地状态
          todo.completed = newCompletedStatus
        }
      } catch (error) {
        console.error('更新任务状态失败:', error)
        console.error('错误详情:', error.response?.data)
        if (error.response?.status === 401) {
          alert('登录已过期，请重新登录')
          authStore.logout()
          router.push('/login')
        } else {
          alert('更新任务状态失败')
        }
      }
    }

    // 获取最新的情绪数据
    const fetchLatestMoodData = async () => {
      try {
        const token = authStore.getToken
        if (!token) {
          console.log('未找到认证token，跳过情绪数据获取')
          return
        }

        console.log('正在获取最新情绪数据...')
        // 获取最新的情绪记录
        const response = await axios.get('/moods/latest', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        console.log('API响应:', response.data)
        
        if (response.data) {
          const moodData = response.data
          
          // 情绪映射：将后端的情绪值映射为中文显示
          const moodMapping = {
            'happy': '开心',
            'calm': '平静', 
            'anxious': '焦虑',
            'stressed': '压力',
            'sad': '难过',
            'excited': '兴奋',
            'tired': '疲惫',
            'focused': '专注'
          }
          
          // 更新当前心情显示
          currentMood.value = moodMapping[moodData.mood] || moodData.mood || '平静'
          console.log('更新心情显示为:', currentMood.value)
          
          // 更新压力指数（如果后端有压力评分字段）
          if (moodData.stress_level !== undefined) {
            stressLevel.value = moodData.stress_level
            console.log('更新压力指数为:', stressLevel.value)
          } else if (moodData.mood === 'stressed' || moodData.mood === 'anxious') {
            stressLevel.value = 7 // 如果心情是压力或焦虑，设置较高的压力值
          } else if (moodData.mood === 'calm' || moodData.mood === 'happy') {
            stressLevel.value = 3 // 如果心情是平静或开心，设置较低的压力值
          }
        } else {
          console.log('API返回空数据，可能还没有情绪记录')
        }
      } catch (error) {
        console.error('获取情绪数据失败:', error)
        console.error('错误详情:', error.response?.data)
        // 如果获取失败，保持默认值
        currentMood.value = '平静'
        stressLevel.value = 5
      }
    }

    // 显示情绪快照弹窗
    const showMoodQuickCheck = () => {
      // 初始化弹窗数据为当前值
      selectedMood.value = getCurrentMoodKey()
      tempStressLevel.value = stressLevel.value
      showMoodModal.value = true
    }

    // 关闭情绪快照弹窗
    const closeMoodModal = () => {
      showMoodModal.value = false
    }

    // 获取当前心情对应的英文key
    const getCurrentMoodKey = () => {
      const moodKeyMapping = {
        '开心': 'happy',
        '平静': 'calm',
        '焦虑': 'anxious', 
        '压力': 'stressed',
        '难过': 'sad',
        '兴奋': 'excited',
        '疲惫': 'tired',
        '专注': 'focused'
      }
      return moodKeyMapping[currentMood.value] || 'calm'
    }

    // 提交情绪数据
    const submitMoodData = async () => {
      try {
        const token = authStore.getToken
        if (!token) {
          alert('请先登录')
          return
        }

        const moodData = {
          mood: selectedMood.value,
          stress_level: parseInt(tempStressLevel.value),
          notes: null  // 可以留空，用户以后可以添加备注功能
        }

        const response = await axios.post('/moods/', moodData, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (response.status === 200 || response.status === 201) {
          // 提交成功，更新显示
          await fetchLatestMoodData()
          closeMoodModal()
          
          // 显示成功提示
          const moodMapping = {
            'happy': '开心',
            'calm': '平静', 
            'anxious': '焦虑',
            'stressed': '压力',
            'sad': '难过',
            'excited': '兴奋',
            'tired': '疲惫',
            'focused': '专注'
          }
          alert(`心情记录成功！当前心情：${moodMapping[selectedMood.value]}，压力指数：${tempStressLevel.value}`)
        }
      } catch (error) {
        console.error('提交情绪数据失败:', error)
        alert('心情记录失败，请稍后重试')
      }
    }

    const navigateTo = (path) => {
      router.push(path)
    }

    const logout = async () => {
      try {
        // 清理计时器
        if (timeInterval) {
          clearInterval(timeInterval)
        }
        authStore.logout()
        await router.push('/')
      } catch (error) {
        console.error('Logout error:', error)
        // 强制跳转
        window.location.href = '/'
      }
    }

    onMounted(() => {
      // 启动计时器，每分钟更新一次时间显示
      timeInterval = setInterval(updateTime, 60000)
      
      // 获取最新的情绪数据
      fetchLatestMoodData()
      
      // 获取今日任务
      fetchTodayTasks()
      
      // 可以设置定期刷新情绪数据（例如每5分钟）
      const moodInterval = setInterval(fetchLatestMoodData, 5 * 60 * 1000)
      
      // 在组件卸载时清理这个间隔
      onUnmounted(() => {
        clearInterval(moodInterval)
      })
      
      // Fetch user specific data like exam date from backend
      // For now, using placeholders
    })

    onUnmounted(() => {
      // 清理计时器
      if (timeInterval) {
        clearInterval(timeInterval)
      }
    })

    return {
      user,
      daysUntilExam,
      currentMood,
      formattedStudyTime,
      stressLevel,
      newTodo,
      todos,
      showMoodModal,
      selectedMood,
      tempStressLevel,
      moodOptions,
      addTodo,
      toggleTodo,
      fetchTodayTasks,
      showMoodQuickCheck,
      closeMoodModal,
      submitMoodData,
      navigateTo,
      logout
    }
  }
}
</script>

<style scoped>
/* === 核心疗愈主题 === */
.healing-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  font-family: 'PingFang SC', 'Arial', sans-serif;
  padding: 20px;
  position: relative;
  overflow-x: hidden;
}

/* === 背景动画层 === */
.background-waves {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.wave {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle at center, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: float 6s ease-in-out infinite;
}

.wave-1 {
  width: 300px;
  height: 300px;
  top: 10%;
  left: -10%;
  animation-delay: 0s;
}

.wave-2 {
  width: 200px;
  height: 200px;
  top: 60%;
  right: -5%;
  animation-delay: 2s;
}

.wave-3 {
  width: 150px;
  height: 150px;
  bottom: 20%;
  left: 30%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(-45deg); opacity: 0.3; }
  50% { transform: translateY(-20px) rotate(45deg); opacity: 0.6; }
}

/* === 欢迎区域 === */
.welcome-section {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
  z-index: 1;
}

/* 左上角提示气泡 */
.tip-bubble {
  position: absolute;
  top: 90px;
  left: 120px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 15px 20px;
  box-shadow: 0 8px 32px rgba(184, 169, 201, 0.3);
  border: 2px solid rgba(184, 169, 201, 0.2);
  animation: tipFloat 3s ease-in-out infinite;
  z-index: 10;
  max-width: 280px;
  transform: rotate(-15deg);
}

.tip-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.tip-icon {
  font-size: 1.2em;
  animation: tipGlow 2s ease-in-out infinite;
}

.tip-text {
  font-family: 'Fredoka One', '方正童趣体', cursive, sans-serif;
  font-size: 0.9em;
  color: #8B7AA8;
  font-weight: 500;
  line-height: 1.3;
}

.tip-arrow {
  position: absolute;
  bottom: -8px;
  right: 20px;
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 8px solid rgba(255, 255, 255, 0.9);
}

@keyframes tipFloat {
  0%, 100% { 
    transform: rotate(-15deg) translateY(0px); 
  }
  33% { 
    transform: rotate(-13deg) translateY(-5px); 
  }
  66% { 
    transform: rotate(-17deg) translateY(3px); 
  }
}

@keyframes tipGlow {
  0%, 100% { 
    opacity: 0.8; 
    transform: scale(1); 
  }
  50% { 
    opacity: 1; 
    transform: scale(1.1); 
  }
}

.healing-title {
  font-family: 'Fredoka One', 'Bubblegum Sans', '方正童趣体', '华文琥珀', cursive, fantasy;
  font-size: 3.8em;
  font-weight: 400;
  background: linear-gradient(135deg, #B8A9C9, #C8B2DB, #D4BBDD, #E0C3FC);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  margin: 20px 0 40px 0;
  letter-spacing: 2px;
  text-shadow: 2px 2px 6px rgba(184, 169, 201, 0.3),
               4px 4px 12px rgba(200, 178, 219, 0.2),
               6px 6px 18px rgba(212, 187, 221, 0.15);
  transform: rotate(-0.5deg);
  animation: sweetBounce 5s ease-in-out infinite;
  position: relative;
  text-align: center;
  filter: drop-shadow(0 3px 6px rgba(184, 169, 201, 0.15));
}

.healing-title::after {
  content: '🧡';
  position: absolute;
  top: -15px;
  right: 10px;
  font-size: 0.6em;
  animation: gentleSparkle 3s ease-in-out infinite;
}

@keyframes sweetBounce {
  0%, 100% { 
    transform: rotate(-0.5deg) translateY(0px) scale(1); 
  }
  20% { 
    transform: rotate(0deg) translateY(-8px) scale(1.05); 
  }
  40% { 
    transform: rotate(-0.3deg) translateY(4px) scale(0.98); 
  }
  60% { 
    transform: rotate(0.2deg) translateY(-6px) scale(1.03); 
  }
  80% { 
    transform: rotate(-0.1deg) translateY(2px) scale(1.01); 
  }
}

@keyframes welcomeHandwriting {
  0%, 100% { 
    transform: rotate(-1deg) translateY(0px) scale(1); 
  }
  25% { 
    transform: rotate(-0.5deg) translateY(-5px) scale(1.02); 
  }
  50% { 
    transform: rotate(-1.5deg) translateY(2px) scale(0.99); 
  }
  75% { 
    transform: rotate(-0.8deg) translateY(-3px) scale(1.01); 
  }
}

@keyframes gentleSparkle {
  0%, 100% { 
    opacity: 0.6; 
    transform: scale(1) rotate(0deg); 
  }
  50% { 
    opacity: 1; 
    transform: scale(1.2) rotate(180deg); 
  }
}

/* === 状态气泡群 === */
.stats-cloud {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
  animation: bubblesRise 1s ease-out 0.5s both;
}

.bubble-float {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 50px;
  padding: 20px 30px;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  animation: float 4s ease-in-out infinite;
}

.bubble-float:nth-child(1) { animation-delay: 0s; }
.bubble-float:nth-child(2) { animation-delay: 0.5s; }
.bubble-float:nth-child(3) { animation-delay: 1s; }
.bubble-float:nth-child(4) { animation-delay: 1.5s; }

.bubble-float:hover {
  transform: scale(1.1);
  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.bubble-float:before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s;
}

.bubble-float:hover:before {
  left: 100%;
}

.bubble-content {
  position: relative;
  z-index: 2;
}

.bubble-icon {
  width: 24px;
  height: 24px;
  margin: 0 auto 8px;
  color: #4A90E2;
}

.stat-number {
  display: block;
  font-size: 1.8em;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9em;
  color: #7f8c8d;
  font-weight: 300;
}

/* 不同气泡的特色颜色 */
.exam-bubble { border: 2px solid rgba(241, 196, 15, 0.3); }
.mood-bubble { border: 2px solid rgba(231, 76, 60, 0.3); }
.time-bubble { border: 2px solid rgba(52, 152, 219, 0.3); }
.stress-bubble { border: 2px solid rgba(155, 89, 182, 0.3); }

.healing-logout-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: linear-gradient(135deg, #ff7675, #fd79a8);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 0.9em;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 118, 117, 0.3);
  z-index: 100;
}

.healing-logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 118, 117, 0.4);
}

/* === 主要内容区域布局 === */
.main-content-layout {
  display: flex;
  gap: 30px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px 0;
  position: relative;
  z-index: 1;
}

.left-panel {
  flex: 1;
  min-width: 400px;
  max-width: 500px;
}

.right-panel {
  flex: 2;
  min-width: 600px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content-layout {
    flex-direction: column;
    gap: 20px;
  }
  
  .left-panel,
  .right-panel {
    min-width: auto;
    max-width: none;
  }
}

@keyframes bubblesRise {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}

/* === 情绪弹窗样式 === */
.mood-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.mood-bubble-modal {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 30px;
  padding: 40px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  animation: bubbleIn 0.5s ease;
  position: relative;
}

@keyframes bubbleIn {
  from { opacity: 0; transform: scale(0.8) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.modal-header h3 {
  color: #2c3e50;
  font-size: 1.5em;
  font-weight: 300;
  margin: 0;
}

.close-ripple {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-ripple:hover {
  background: rgba(255, 118, 117, 0.2);
  transform: scale(1.1);
}

.close-ripple svg {
  width: 20px;
  height: 20px;
  color: #7f8c8d;
}

.form-label {
  display: block;
  color: #2c3e50;
  font-weight: 500;
  margin-bottom: 15px;
  font-size: 1.1em;
}

.mood-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 25px;
}

.mood-option {
  background: rgba(255, 255, 255, 0.7);
  border: 2px solid rgba(74, 144, 226, 0.2);
  border-radius: 20px;
  padding: 15px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.mood-option:hover {
  background: rgba(74, 144, 226, 0.1);
  transform: translateY(-2px);
}

.mood-option.active {
  background: linear-gradient(135deg, #4A90E2, #7ED321);
  color: white;
  border-color: #4A90E2;
  box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
}

.mood-text {
  font-weight: 500;
  font-size: 1em;
}

.stress-section {
  margin-bottom: 25px;
}

.stress-track {
  position: relative;
  margin-top: 15px;
}

.healing-slider {
  width: 100%;
  height: 8px;
  border-radius: 5px;
  background: linear-gradient(to right, #7ED321, #F5A623, #ff7675);
  outline: none;
  cursor: pointer;
  margin-bottom: 10px;
}

.healing-slider::-webkit-slider-thumb {
  appearance: none;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
}

.healing-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.stress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.9em;
  color: #7f8c8d;
}

.modal-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 30px;
}

.submit-bubble, .cancel-bubble {
  padding: 12px 30px;
  border: none;
  border-radius: 25px;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.submit-bubble {
  background: linear-gradient(135deg, #7ED321, #4A90E2);
  color: white;
  box-shadow: 0 4px 15px rgba(126, 211, 33, 0.3);
}

.submit-bubble:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(126, 211, 33, 0.4);
}

.cancel-bubble {
  background: rgba(255, 255, 255, 0.8);
  color: #7f8c8d;
  border: 1px solid rgba(127, 140, 141, 0.3);
}

.cancel-bubble:hover {
  background: rgba(127, 140, 141, 0.1);
}

/* === 任务气泡链条 === */
.task-bubbles-section {
  position: relative;
  z-index: 1;
}

.task-cloud {
  width: 100%;
}

.section-title {
  text-align: center;
  color: #2c3e50;
  font-size: 2em;
  font-weight: 300;
  margin-bottom: 30px;
  animation: fadeInDown 1s ease;
}

/* 手绘风格的ToDoList标题 */
.todolist-title {
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-size: 2.5em;
  font-weight: bold;
  color: #9B59B6;
  text-align: center;
  margin-bottom: 30px;
  position: relative;
  text-shadow: 2px 2px 0px #E8D5E8, 
               4px 4px 0px #D4B5D4,
               6px 6px 8px rgba(155, 89, 182, 0.3);
  transform: rotate(-2deg);
  animation: handDrawn 3s ease-in-out infinite;
}

.todolist-title::before {
  content: '';
  position: absolute;
  top: -10px;
  left: -20px;
  right: -20px;
  bottom: -5px;
  border: 3px solid #9B59B6;
  border-radius: 20px;
  transform: rotate(1deg);
  z-index: -1;
  opacity: 0.6;
  border-style: dashed;
}

.todolist-title::after {
  content: '✨';
  position: absolute;
  top: -15px;
  right: -15px;
  font-size: 1.2em;
  animation: sparkle 2s ease-in-out infinite;
}

@keyframes handDrawn {
  0%, 100% { 
    transform: rotate(-2deg) translateY(0px); 
  }
  25% { 
    transform: rotate(-1deg) translateY(-2px); 
  }
  50% { 
    transform: rotate(-2.5deg) translateY(1px); 
  }
  75% { 
    transform: rotate(-1.5deg) translateY(-1px); 
  }
}

@keyframes sparkle {
  0%, 100% { 
    opacity: 0.6; 
    transform: scale(1) rotate(0deg); 
  }
  50% { 
    opacity: 1; 
    transform: scale(1.2) rotate(180deg); 
  }
}

.task-input-bubble {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(15px);
  border-radius: 30px;
  padding: 20px;
  margin-bottom: 25px;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.1);
}

.input-wrapper {
  display: flex;
  gap: 15px;
  align-items: center;
}

.healing-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 1.1em;
  padding: 15px 20px;
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.8);
  outline: none;
  transition: all 0.3s ease;
}

.healing-input:focus {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 0 20px rgba(74, 144, 226, 0.2);
}

.healing-input::placeholder {
  color: #b2bec3;
  font-style: italic;
}

.add-task-ripple {
  width: 50px;
  height: 50px;
  border: none;
  border-radius: 50%;
  background: linear-gradient(135deg, #7ED321, #4A90E2);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.add-task-ripple:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 20px rgba(126, 211, 33, 0.4);
}

.add-task-ripple:before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transition: all 0.3s;
  transform: translate(-50%, -50%);
}

.add-task-ripple:active:before {
  width: 60px;
  height: 60px;
}

.add-task-ripple svg {
  width: 24px;
  height: 24px;
  z-index: 1;
}

.tasks-flow {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.task-bubble {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 25px;
  padding: 20px 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border: 2px solid transparent;
  animation: slideInLeft 0.5s ease;
}

.task-bubble:hover {
  transform: translateX(10px);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.task-bubble.completed {
  background: linear-gradient(135deg, rgba(126, 211, 33, 0.2), rgba(74, 144, 226, 0.2));
  border-color: rgba(126, 211, 33, 0.5);
}

.task-content {
  display: flex;
  align-items: center;
  gap: 15px;
  position: relative;
  z-index: 2;
}

.task-check {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.task-bubble.completed .task-check {
  background: linear-gradient(135deg, #7ED321, #4A90E2);
  border-color: #7ED321;
  color: white;
}

.check-circle {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: transparent;
  transition: all 0.3s ease;
}

.task-bubble:hover .check-circle {
  background: rgba(74, 144, 226, 0.3);
}

.task-check svg {
  width: 16px;
  height: 16px;
}

.task-text {
  flex: 1;
  font-size: 1.1em;
  color: #2c3e50;
  transition: all 0.3s ease;
}

.task-bubble.completed .task-text {
  text-decoration: line-through;
  color: #7f8c8d;
}

.completion-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, rgba(126, 211, 33, 0.1), rgba(74, 144, 226, 0.1));
  border-radius: 25px;
  opacity: 0;
  animation: glowPulse 2s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-50px); }
  to { opacity: 1; transform: translateX(0); }
}

/* === 功能模块星座 === */
.modules-constellation {
  position: relative;
  z-index: 1;
}

.floating-modules {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 0;
}

.module-bubble {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(15px);
  border-radius: 25px;
  padding: 25px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.5);
  animation: moduleFloat 6s ease-in-out infinite;
}

.module-bubble:nth-child(1) { animation-delay: 0s; }
.module-bubble:nth-child(2) { animation-delay: 1s; }
.module-bubble:nth-child(3) { animation-delay: 2s; }
.module-bubble:nth-child(4) { animation-delay: 3s; }
.module-bubble:nth-child(5) { animation-delay: 4s; }
.module-bubble:nth-child(6) { animation-delay: 5s; }
.module-bubble:nth-child(7) { animation-delay: 6s; }

@keyframes moduleFloat {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-10px) rotate(0.3deg); }
  66% { transform: translateY(5px) rotate(-0.3deg); }
}

.module-bubble:hover {
  transform: scale(1.05) translateY(-10px);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
  border-color: rgba(74, 144, 226, 0.5);
}

.module-bubble .bubble-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 20px;
  padding: 15px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4A90E2, #7ED321);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

/* 各模块的特定颜色主题 */
.stress-module .bubble-icon {
  background: linear-gradient(135deg, #87CEEB, #B0E0E6); /* 浅蓝色 - 压力监测 */
}

.flow-module .bubble-icon {
  background: linear-gradient(135deg, #98FB98, #90EE90); /* 浅绿色 - 心流训练 */
}

.emotional-module .bubble-icon {
  background: linear-gradient(135deg, #FFB6C1, #FFC0CB); /* 浅粉色 - 情绪急救 */
}

.painting-module .bubble-icon {
  background: linear-gradient(135deg, #DDA0DD, #E6E6FA); /* 浅紫色 - 心灵画语 */
}

.messenger-module .bubble-icon {
  background: linear-gradient(135deg, #F0E68C, #FFFFE0); /* 浅黄色 - 心语信使 */
}

.review-module .bubble-icon {
  background: linear-gradient(135deg, #FFA07A, #FFEFD5); /* 浅橙色 - 错题复盘 */
}

.report-module .bubble-icon {
  background: linear-gradient(135deg, #20B2AA, #AFEEEE); /* 浅青色 - 我的周报 */
}

.module-bubble:hover .bubble-icon {
  transform: rotate(360deg) scale(1.1);
}

/* 各模块hover状态的特定颜色增强 */
.stress-module:hover .bubble-icon {
  background: linear-gradient(135deg, #6AB7FF, #87CEEB);
  box-shadow: 0 8px 25px rgba(135, 206, 235, 0.4);
}

.flow-module:hover .bubble-icon {
  background: linear-gradient(135deg, #7FFF7F, #98FB98);
  box-shadow: 0 8px 25px rgba(152, 251, 152, 0.4);
}

.emotional-module:hover .bubble-icon {
  background: linear-gradient(135deg, #FF91A4, #FFB6C1);
  box-shadow: 0 8px 25px rgba(255, 182, 193, 0.4);
}

.painting-module:hover .bubble-icon {
  background: linear-gradient(135deg, #DA70D6, #DDA0DD);
  box-shadow: 0 8px 25px rgba(221, 160, 221, 0.4);
}

.messenger-module:hover .bubble-icon {
  background: linear-gradient(135deg, #FFD700, #F0E68C);
  box-shadow: 0 8px 25px rgba(240, 230, 140, 0.4);
}

.review-module:hover .bubble-icon {
  background: linear-gradient(135deg, #FF7F50, #FFA07A);
  box-shadow: 0 8px 25px rgba(255, 160, 122, 0.4);
}

.report-module:hover .bubble-icon {
  background: linear-gradient(135deg, #00CED1, #20B2AA);
  box-shadow: 0 8px 25px rgba(32, 178, 170, 0.4);
}

.module-bubble h3 {
  color: #2c3e50;
  font-size: 1.3em;
  font-weight: 500;
  margin: 0 0 10px 0;
  transition: all 0.3s ease;
}

.module-bubble p {
  color: #7f8c8d;
  font-size: 0.95em;
  line-height: 1.5;
  margin: 0;
  transition: all 0.3s ease;
}

.module-bubble:hover h3 {
  color: #4A90E2;
}

.module-bubble:hover p {
  color: #2c3e50;
}

.ripple-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(74, 144, 226, 0.3);
  transform: translate(-50%, -50%);
  transition: all 0.6s ease;
  pointer-events: none;
}

.module-bubble:active .ripple-effect {
  width: 300px;
  height: 300px;
  opacity: 0;
}

/* 模块特色边框 */
.stress-module { border-left: 4px solid #F5A623; }
.flow-module { border-left: 4px solid #4A90E2; }
.emotional-module { border-left: 4px solid #ff7675; }
.painting-module { border-left: 4px solid #fd79a8; }
.messenger-module { border-left: 4px solid #00b894; }
.review-module { border-left: 4px solid #6c5ce7; }
.report-module { border-left: 4px solid #fdcb6e; }

/* === 响应式设计 === */
@media (max-width: 768px) {
  .healing-title {
    font-size: 2em;
  }
  
  .stats-cloud {
    flex-direction: column;
    align-items: center;
  }
  
  .bubble-float {
    width: 100%;
    max-width: 300px;
  }
  
  .floating-modules {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .input-wrapper {
    flex-direction: column;
  }
  
  .mood-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .healing-dashboard {
    padding: 15px;
  }
  
  .mood-bubble-modal {
    padding: 25px;
  }
  
  .module-bubble {
    padding: 20px;
  }
}

/* === 通用动画 === */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* === 滚动条美化 === */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #4A90E2, #7ED321);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #357ABD, #5FA617);
}

/* === 原有样式兼容 === */

.stat-item.clickable {
  cursor: pointer;
}

.stat-item.clickable:hover {
  transform: translateY(-2px) scale(1.02);
  background: rgba(255, 255, 255, 0.9);
}

.stat-number {
  display: block;
  font-size: 1.8em;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9em;
  color: #666;
}

.logout-button {
  position: absolute;
  top: 0;
  right: 0;
  background: rgba(231, 76, 60, 0.9);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  animation: fadeIn 1s ease-out 0.6s both;
}

.logout-button:hover {
  background: rgba(192, 57, 43, 0.9);
  transform: scale(1.05);
}

/* Todo List 区域 */
.todo-section {
  max-width: 1200px;
  margin: 0 auto 40px auto;
  animation: fadeInUp 1s ease-out 0.9s both;
}

.todo-container {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 25px;
  padding: 30px;
  backdrop-filter: blur(15px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.todo-container h2 {
  color: #2c3e50;
  margin: 0 0 20px 0;
  font-size: 1.8em;
  font-weight: 600;
  text-align: center;
}

.todo-input-area {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
}

.todo-input {
  flex: 1;
  padding: 12px 20px;
  border: 2px solid rgba(168, 237, 234, 0.5);
  border-radius: 25px;
  font-size: 1em;
  outline: none;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.8);
}

.todo-input:focus {
  border-color: rgba(168, 237, 234, 1);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 0 0 3px rgba(168, 237, 234, 0.2);
}

.add-todo-btn {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #2c3e50;
  border: none;
  padding: 12px 25px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.add-todo-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.todo-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px 20px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.todo-item:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: translateX(5px);
}

.todo-item.completed {
  background: rgba(200, 230, 201, 0.6);
  border-color: rgba(76, 175, 80, 0.3);
}

.todo-item.completed .todo-text {
  text-decoration: line-through;
  color: #666;
}

.todo-checkbox {
  width: 24px;
  height: 24px;
  border: 2px solid #a8edea;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.todo-item.completed .todo-checkbox {
  background: #4CAF50;
  border-color: #4CAF50;
}

.checkmark {
  color: white;
  font-weight: bold;
  font-size: 0.9em;
}

.todo-text {
  flex: 1;
  font-size: 1.1em;
  color: #2c3e50;
  transition: all 0.3s ease;
}

/* 气泡容器 */
.bubbles-container {
  max-width: 1200px;
  margin: 0 auto;
}

.bubbles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
  padding: 20px 0;
}

/* 气泡样式 */
.bubble-item {
  background: rgba(255, 255, 255, 0.85);
  border-radius: 25px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  backdrop-filter: blur(15px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
  position: relative;
  overflow: hidden;
  animation: bubbleFloat 1s ease-out both;
}

/* 不同大小的气泡 */
.bubble-item.large {
  grid-column: span 2;
  padding: 40px;
}

.bubble-item.medium {
  grid-column: span 1;
}

/* 气泡悬浮动画 */
.bubble-item:nth-child(1) { animation-delay: 0.1s; }
.bubble-item:nth-child(2) { animation-delay: 0.2s; }
.bubble-item:nth-child(3) { animation-delay: 0.3s; }
.bubble-item:nth-child(4) { animation-delay: 0.4s; }
.bubble-item:nth-child(5) { animation-delay: 0.5s; }
.bubble-item:nth-child(6) { animation-delay: 0.6s; }
.bubble-item:nth-child(7) { animation-delay: 0.7s; }
.bubble-item:nth-child(8) { animation-delay: 0.8s; }

/* 气泡悬停效果 */
.bubble-item:hover {
  transform: translateY(-10px) scale(1.02);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

/* 气泡内容 */
.bubble-icon {
  font-size: 3em;
  margin-bottom: 15px;
  display: block;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.bubble-item h3 {
  color: #2c3e50;
  margin: 15px 0 10px 0;
  font-size: 1.4em;
  font-weight: 600;
}

.bubble-item p {
  color: #666;
  font-size: 1em;
  line-height: 1.5;
  margin: 0;
}

.bubble-item.large h3 {
  font-size: 1.6em;
}

.bubble-item.large p {
  font-size: 1.1em;
}

/* 气泡渐变背景效果 */
.bubble-item:nth-child(1)::before { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); }
.bubble-item:nth-child(2)::before { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); }
.bubble-item:nth-child(3)::before { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); }
.bubble-item:nth-child(4)::before { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }
.bubble-item:nth-child(5)::before { background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%); }
.bubble-item:nth-child(6)::before { background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%); }
.bubble-item:nth-child(7)::before { background: linear-gradient(135deg, #fdbb2d 0%, #22c1c3 100%); }
.bubble-item:nth-child(8)::before { background: linear-gradient(135deg, #ff9a56 0%, #ffad56 100%); }

.bubble-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 25px;
  z-index: -1;
}

.bubble-item:hover::before {
  opacity: 0.1;
}

/* 动画定义 */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translate3d(0, -30px, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translate3d(0, 30px, 0);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes bubbleFloat {
  from {
    opacity: 0;
    transform: translate3d(0, 50px, 0) scale(0.8);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0) scale(1);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 15px;
  }

  .welcome-title {
    font-size: 1.8em;
  }

  .header-stats {
    flex-wrap: wrap;
    gap: 15px;
  }

  .stat-item {
    flex: 1;
    min-width: 120px;
  }

  .todo-container {
    padding: 20px;
  }

  .todo-input-area {
    flex-direction: column;
    gap: 10px;
  }

  .todo-input {
    width: 100%;
  }

  .bubbles-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .bubble-item.large {
    grid-column: span 1;
    padding: 25px;
  }

  .logout-button {
    position: static;
    margin-top: 20px;
  }
}

@media (max-width: 480px) {
  .bubble-item {
    padding: 20px;
  }

  .bubble-icon {
    font-size: 2.5em;
  }

  .bubble-item h3 {
    font-size: 1.2em;
  }
}

/* 情绪快照弹窗样式 */
.mood-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.mood-modal {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 25px;
  padding: 30px;
  min-width: 400px;
  max-width: 500px;
  backdrop-filter: blur(15px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.mood-modal h3 {
  color: #2c3e50;
  margin: 0 0 25px 0;
  text-align: center;
  font-size: 1.5em;
  font-weight: 600;
}

.mood-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.mood-selector label,
.stress-slider label {
  display: block;
  margin-bottom: 8px;
  color: #2c3e50;
  font-weight: 600;
  font-size: 1.1em;
}

.mood-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid rgba(168, 237, 234, 0.5);
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.8);
  font-size: 1em;
  outline: none;
  transition: all 0.3s ease;
}

.mood-select:focus {
  border-color: rgba(168, 237, 234, 1);
  background: rgba(255, 255, 255, 1);
}

.slider {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(to right, #4CAF50, #FFC107, #FF5722);
  outline: none;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.slider:hover {
  opacity: 1;
}

.slider::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2c3e50;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2c3e50;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.modal-buttons {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 20px;
}

.cancel-btn,
.submit-btn {
  padding: 12px 25px;
  border: none;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 100px;
}

.cancel-btn {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
  border: 2px solid rgba(108, 117, 125, 0.3);
}

.cancel-btn:hover {
  background: rgba(108, 117, 125, 0.2);
  transform: translateY(-1px);
}

.submit-btn {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #2c3e50;
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

@media (max-width: 480px) {
  .mood-modal {
    min-width: 300px;
    margin: 20px;
    padding: 20px;
  }
  
  .modal-buttons {
    flex-direction: column;
  }
}
</style>

