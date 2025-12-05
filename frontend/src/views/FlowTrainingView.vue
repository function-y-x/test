<template>
  <div class="flow-training-container">
    <!-- 顶部栏 -->
    <div class="top-bar">
      <button class="back-button" @click="goBack" title="返回主界面">
        <span class="back-icon">←</span>
        返回主界面
      </button>
      <div class="motivation-quote">
        <span class="quote-mark">"</span>
        <span class="quote-text">{{ motivationText }}</span>
        <span class="quote-mark">"</span>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 左侧今日计划 -->
      <div class="left-panel">
        <div class="panel-header">
          <h3>📋 今日计划</h3>
        </div>
        <div class="today-tasks">
          <div v-for="(task, index) in todayTasks" :key="index" class="task-item" :class="{ completed: task.completed }">
            <div class="task-icon">{{ task.icon }}</div>
            <div class="task-content">
              <div class="task-title">{{ task.title }}</div>
              <div class="task-time">{{ task.estimatedTime }}</div>
            </div>
            <button class="task-toggle" @click="toggleTask(index)">
              {{ task.completed ? '✓' : '○' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 中央计时器区域 -->
      <div class="center-panel">
        <!-- 时间设定界面 -->
        <div v-if="!hasStarted" class="time-setting">
          <h2>设置专注时间</h2>
          <div class="time-presets">
            <button v-for="preset in timePresets" :key="preset.value" 
                    class="preset-btn" 
                    :class="{ active: selectedTime === preset.value }"
                    @click="selectTime(preset.value)">
              {{ preset.label }}
            </button>
          </div>
          <div class="custom-time">
            <label>自定义时间（分钟）：</label>
            <input type="number" v-model="customMinutes" min="1" max="120" />
            <button @click="selectCustomTime">确定</button>
          </div>
          <button class="start-btn" @click="startSession" :disabled="selectedTime === 0">
            开始专注
          </button>
        </div>

        <!-- 计时器界面 -->
        <div v-else class="timer-section">
          <div class="session-label">{{ sessionLabel }}</div>
          <div class="timer-circle" :style="{ background: `conic-gradient(rgba(255,255,255,0.8) ${progress}%, rgba(255,255,255,0.1) ${progress}%)` }">
            <div class="timer-inner">
              <div class="timer-display">{{ formattedTime }}</div>
              <div class="focus-text">{{ focusText }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧长期计划 -->
      <div class="right-panel">
        <div class="panel-header">
          <h3>🎯 长期计划</h3>
        </div>
        <div class="long-term-goals">
          <div v-for="(goal, index) in longTermGoals" :key="index" class="goal-card" :style="{ background: goal.color }">
            <div class="goal-content">
              <div class="goal-title">{{ goal.title }}</div>
              <div class="goal-description">{{ goal.description }}</div>
              <div class="goal-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: goal.progress + '%' }"></div>
                </div>
                <span class="progress-text">{{ goal.progress }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部控制按钮 -->
    <div v-if="hasStarted" class="bottom-controls">
      <button class="control-btn brightness-btn" @click="adjustBrightness" title="亮度调整">
        <span class="icon">☀️</span>
      </button>
      <button class="control-btn pause-btn" @click="toggleTimer" title="暂停/继续">
        <span class="icon">{{ isRunning ? '⏸️' : '▶️' }}</span>
      </button>
      <button class="control-btn music-btn" @click="toggleMusic" title="音乐">
        <span class="icon">{{ isMusicPlaying ? '🔊' : '🔇' }}</span>
      </button>
      <button class="control-btn stop-btn" @click="stopSession" title="结束">
        <span class="icon">⏹️</span>
      </button>
      <button class="control-btn toolbox-btn" @click="openToolbox" title="工具箱">
        <span class="icon">🧰</span>
      </button>
      <button class="control-btn share-btn" @click="shareSession" title="分享">
        <span class="icon">📤</span>
      </button>
    </div>

    <!-- 工具箱弹窗 -->
    <div v-if="showToolbox" class="toolbox-modal" @click="closeToolbox">
      <div class="toolbox-content" @click.stop>
        <h3>学习工具箱</h3>
        <div class="tool-buttons">
          <button class="tool-btn tool-btn-1" @click="openDictionary">📖 查单词</button>
          <button class="tool-btn tool-btn-2" @click="openCalculator">🧮 计算器</button>
          <button class="tool-btn tool-btn-3" @click="openNotes">📝 笔记</button>
          <button class="tool-btn tool-btn-4" @click="openTimer">⏰ 其他计时器</button>
        </div>
        <button class="close-btn" @click="closeToolbox">关闭</button>
      </div>
    </div>

    <!-- 分享 & 奖励悬浮窗口 -->
    <div v-if="showShareModal" class="share-modal" @click="closeShareModal">
      <div class="share-content" id="shareCard" @click.stop>
        <div class="share-header">
          <div class="badge-display">
            <div class="badge-icon">{{ badgeIcon }}</div>
            <div class="badge-text">
              <div class="badge-name">{{ badgeName }}</div>
              <div class="badge-desc">{{ badgeDesc }}</div>
            </div>
          </div>
          <button class="close-mini" @click="closeShareModal">×</button>
        </div>
        <div class="share-body">
          <div class="stat-line">本次设定：<strong>{{ originalMinutes }} 分钟</strong></div>
          <div class="stat-line" v-if="isRunning">已进行：{{ elapsedMinutes }} 分钟</div>
          <div class="stat-line" v-else-if="originalTime && !isRunning">已完成：{{ originalMinutes }} 分钟专注</div>
          <div class="quote-inline">“ {{ motivationText }} ”</div>
          <div class="reward-progress">
            <div class="reward-bar">
              <div class="reward-fill" :style="{ width: rewardProgress + '%' }"></div>
            </div>
            <span class="reward-progress-text">{{ rewardProgress }}%</span>
          </div>
          <div class="next-badge" v-if="nextBadgeName">距离下一枚徽章：{{ nextBadgeName }} ({{ nextBadgeMinutes }} 分钟总时长)</div>
        </div>
        <div class="share-actions">
          <button class="download-btn" @click="downloadShareCard">下载分享卡片</button>
          <button class="close-btn alt" @click="closeShareModal">关闭</button>
        </div>
        <div class="share-footer">考研心理教练 · 专注打卡</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'

export default {
  name: 'FlowTrainingView',
  setup() {
    const timer = ref(0)
    const selectedTime = ref(0)
    const originalTime = ref(0)
    const isRunning = ref(false)
    const isMusicPlaying = ref(false)
    const showToolbox = ref(false)
  const showShareModal = ref(false)
    const hasStarted = ref(false)
    const customMinutes = ref(25)
    const sessionLabel = ref('加油 💪')
    const focusText = ref('准备开始')
    let interval = null

    // 时间预设选项
    const timePresets = [
      { label: '25分钟', value: 25 * 60 },
      { label: '45分钟', value: 45 * 60 },
      { label: '60分钟', value: 60 * 60 },
      { label: '90分钟', value: 90 * 60 }
    ]

    // 励志话语数组
    const motivationTexts = [
      '你像把无销刃伴利敌说，但好刃应在刃销里。',
      '成功的秘诀在于坚持自己的目标。',
      '每一个不曾起舞的日子，都是对生命的辜负。',
      '志不强者智不达，言不信者行不果。',
      '路虽远行则将至，事虽难做则必成。'
    ]
    
    const motivationText = ref('')

    // 今日计划数据
    const todayTasks = ref([
      { icon: '📚', title: '复习高等数学', estimatedTime: '2小时', completed: false },
      { icon: '📖', title: '英语阅读练习', estimatedTime: '1小时', completed: true },
      { icon: '✍️', title: '政治选择题', estimatedTime: '30分钟', completed: false },
      { icon: '🔬', title: '专业课笔记', estimatedTime: '1.5小时', completed: false },
      { icon: '📝', title: '作文练习', estimatedTime: '45分钟', completed: false },
      { icon: '🧮', title: '数学真题', estimatedTime: '2小时', completed: false },
      { icon: '📱', title: '单词背诵', estimatedTime: '30分钟', completed: true },
      { icon: '📊', title: '错题整理', estimatedTime: '40分钟', completed: false }
    ])

    // 长期计划数据
    const longTermGoals = ref([
      {
        title: '数学目标',
        description: '复习完高等数学全部章节',
        progress: 65,
        color: 'linear-gradient(135deg, rgba(168, 237, 234, 0.3) 0%, rgba(179, 229, 252, 0.3) 100%)'
      },
      {
        title: '英语目标',
        description: '词汇量达到8000+',
        progress: 45,
        color: 'linear-gradient(135deg, rgba(254, 214, 227, 0.3) 0%, rgba(255, 238, 173, 0.3) 100%)'
      },
      {
        title: '政治目标',
        description: '考研政治目标90+',
        progress: 30,
        color: 'linear-gradient(135deg, rgba(179, 229, 252, 0.3) 0%, rgba(198, 219, 239, 0.3) 100%)'
      },
      {
        title: '最终目标',
        description: '上岸南开大学',
        progress: 55,
        color: 'linear-gradient(135deg, rgba(198, 246, 213, 0.3) 0%, rgba(168, 237, 234, 0.3) 100%)'
      },
      {
        title: '专业课目标',
        description: '专业课达到130+',
        progress: 40,
        color: 'linear-gradient(135deg, rgba(255, 230, 230, 0.3) 0%, rgba(255, 238, 173, 0.3) 100%)'
      },
      {
        title: '综合目标',
        description: '总分超过380分',
        progress: 50,
        color: 'linear-gradient(135deg, rgba(230, 220, 250, 0.3) 0%, rgba(254, 214, 227, 0.3) 100%)'
      }
    ])

    const formattedTime = computed(() => {
      const minutes = Math.floor(timer.value / 60)
        .toString()
        .padStart(2, '0')
      const seconds = (timer.value % 60).toString().padStart(2, '0')
      return `${minutes}:${seconds}`
    })

    const progress = computed(() => {
      if (originalTime.value === 0) return 0
      return ((originalTime.value - timer.value) / originalTime.value) * 360
    })

    // 统计/奖励相关
    const elapsedSeconds = computed(() => originalTime.value - timer.value)
    const elapsedMinutes = computed(() => Math.max(0, Math.floor(elapsedSeconds.value / 60)))
    const originalMinutes = computed(() => Math.floor(originalTime.value / 60))

    // 奖励等级定义（示例）
    const badgeLevels = [
      { minutes: 25, name: '初始芽', icon: '🌱', desc: '迈出专注第一步' },
      { minutes: 45, name: '稳步苗', icon: '🌿', desc: '专注渐入佳境' },
      { minutes: 60, name: '成长叶', icon: '🍀', desc: '持续专注表现' },
      { minutes: 90, name: '绽放花', icon: '🌸', desc: '高强度专注者' },
      { minutes: 120, name: '璀璨星', icon: '⭐', desc: '专注力杰出' }
    ]

    const currentBadge = computed(() => {
      if (!originalMinutes.value) return null
      let earned = null
      for (const b of badgeLevels) {
        if (originalMinutes.value >= b.minutes) earned = b
      }
      return earned || badgeLevels[0]
    })

    const badgeName = computed(() => currentBadge.value ? currentBadge.value.name : '未开始')
    const badgeIcon = computed(() => currentBadge.value ? currentBadge.value.icon : '⏳')
    const badgeDesc = computed(() => currentBadge.value ? currentBadge.value.desc : '设置一个专注时长开始挑战')

    const nextBadge = computed(() => {
      if (!originalMinutes.value) return badgeLevels[0]
      return badgeLevels.find(b => b.minutes > originalMinutes.value)
    })
    const nextBadgeName = computed(() => nextBadge.value ? nextBadge.value.name : '')
    const nextBadgeMinutes = computed(() => nextBadge.value ? nextBadge.value.minutes : 0)

    const rewardProgress = computed(() => {
      if (!currentBadge.value) return 0
      const base = currentBadge.value.minutes
      const next = nextBadge.value ? nextBadge.value.minutes : base
      if (!next || next === base) return 100
      const span = next - base
      const within = originalMinutes.value - base
      return Math.min(100, Math.max(0, Math.round(within / span * 100)))
    })

    // 随机选择励志话语
    const setRandomMotivation = () => {
      const randomIndex = Math.floor(Math.random() * motivationTexts.length)
      motivationText.value = motivationTexts[randomIndex]
    }

    const selectTime = (timeInSeconds) => {
      selectedTime.value = timeInSeconds
    }

    const selectCustomTime = () => {
      if (customMinutes.value > 0 && customMinutes.value <= 120) {
        selectedTime.value = customMinutes.value * 60
      }
    }

    const startSession = () => {
      if (selectedTime.value > 0) {
        timer.value = selectedTime.value
        originalTime.value = selectedTime.value
        hasStarted.value = true
        startTimer()
      }
    }

    const toggleTimer = () => {
      if (isRunning.value) {
        pauseTimer()
      } else {
        startTimer()
      }
    }

    const startTimer = () => {
      if (!isRunning.value) {
        isRunning.value = true
        focusText.value = '专注中'
        interval = setInterval(() => {
          if (timer.value > 0) {
            timer.value--
          } else {
            clearInterval(interval)
            isRunning.value = false
            focusText.value = '已完成'
            alert('🎉 专注时间结束！你做得很棒！')
            // 重置状态
            resetSession()
          }
        }, 1000)
      }
    }

    const pauseTimer = () => {
      clearInterval(interval)
      isRunning.value = false
      focusText.value = '已暂停'
    }

    const stopSession = () => {
      clearInterval(interval)
      resetSession()
    }

    const resetSession = () => {
      isRunning.value = false
      hasStarted.value = false
      timer.value = 0
      selectedTime.value = 0
      originalTime.value = 0
      focusText.value = '准备开始'
      setRandomMotivation()
    }

    const toggleTask = (index) => {
      todayTasks.value[index].completed = !todayTasks.value[index].completed
    }

    const toggleMusic = () => {
      isMusicPlaying.value = !isMusicPlaying.value
      if (isMusicPlaying.value) {
        console.log('播放背景音乐')
      } else {
        console.log('停止背景音乐')
      }
    }

    const adjustBrightness = () => {
      const container = document.querySelector('.flow-training-container')
      container.classList.toggle('dark-mode')
    }

    const openToolbox = () => {
      showToolbox.value = true
    }

    const closeToolbox = () => {
      showToolbox.value = false
    }

    const shareSession = () => {
      showShareModal.value = true
    }

    const closeShareModal = () => {
      showShareModal.value = false
    }

    const downloadShareCard = () => {
      // 简易导出：将 shareCard 转为图片 (无需外部库，使用 svg foreignObject 方案)
      const node = document.getElementById('shareCard')
      if (!node) return
      const rect = node.getBoundingClientRect()
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
      svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
      svg.setAttribute('width', rect.width)
      svg.setAttribute('height', rect.height)
      const fo = document.createElementNS('http://www.w3.org/2000/svg', 'foreignObject')
      fo.setAttribute('x', '0')
      fo.setAttribute('y', '0')
      fo.setAttribute('width', '100%')
      fo.setAttribute('height', '100%')
      // 克隆节点
      const clone = node.cloneNode(true)
      clone.classList.add('exporting')
      fo.appendChild(clone)
      svg.appendChild(fo)
      const serializer = new XMLSerializer()
      const svgStr = serializer.serializeToString(svg)
      const img = new Image()
      const url = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgStr)
      img.onload = function () {
        const canvas = document.createElement('canvas')
        canvas.width = rect.width * 2
        canvas.height = rect.height * 2
        const ctx = canvas.getContext('2d')
        ctx.scale(2, 2)
        ctx.fillStyle = 'white'
        ctx.fillRect(0, 0, rect.width, rect.height)
        ctx.drawImage(img, 0, 0)
        const a = document.createElement('a')
        a.download = `专注分享卡-${Date.now()}.png`
        a.href = canvas.toDataURL('image/png')
        a.click()
      }
      img.src = url
    }

    const openDictionary = () => {
      window.open('https://dict.youdao.com/', '_blank')
      closeToolbox()
    }

    const openCalculator = () => {
      window.open('https://www.calculator.net/', '_blank')
      closeToolbox()
    }

    const openNotes = () => {
      alert('笔记功能开发中...')
      closeToolbox()
    }

    const openTimer = () => {
      alert('其他计时器功能开发中...')
      closeToolbox()
    }

    const goBack = () => {
      // 返回到主页面
      window.history.back()
    }

    onMounted(() => {
      setRandomMotivation()
    })

    onUnmounted(() => {
      clearInterval(interval)
    })

    return {
      timer,
      selectedTime,
      isRunning,
      isMusicPlaying,
      showToolbox,
  showShareModal,
      hasStarted,
      customMinutes,
      sessionLabel,
      focusText,
      motivationText,
      timePresets,
      todayTasks,
      longTermGoals,
      formattedTime,
      progress,
  elapsedMinutes,
  originalMinutes,
  badgeName,
  badgeIcon,
  badgeDesc,
  rewardProgress,
  nextBadgeName,
  nextBadgeMinutes,
      selectTime,
      selectCustomTime,
      startSession,
      toggleTimer,
      startTimer,
      pauseTimer,
      stopSession,
      resetSession,
      toggleTask,
      toggleMusic,
      adjustBrightness,
      openToolbox,
      closeToolbox,
      shareSession,
  closeShareModal,
  downloadShareCard,
      openDictionary,
      openCalculator,
      openNotes,
      openTimer,
      goBack
    }
  }
}
</script>

<style scoped>
.flow-training-container {
  padding: 0;
  margin: 0;
  min-height: 100vh;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  font-family: 'Noto Sans SC', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #2c3e50;
  position: relative;
  overflow-x: hidden;
}

/* 深色模式 */
.flow-training-container.dark-mode {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 50%, #4a5568 100%);
}

/* 顶部栏 */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  position: relative;
  z-index: 10;
}

.back-button {
  background: rgba(255, 255, 255, 0.4);
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 25px;
  padding: 10px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #2c3e50;
  transition: all 0.3s ease;
  backdrop-filter: blur(15px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.8);
}

.back-icon {
  font-size: 1.2em;
  font-weight: bold;
}

.motivation-quote {
  display: flex;
  align-items: center;
  gap: 8px;
  max-width: 60%;
  text-align: center;
}

.quote-mark {
  font-size: 32px;
  font-family: 'Times New Roman', serif;
  font-style: italic;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1;
}

.quote-text {
  font-size: 16px;
  font-weight: 500;
  color: #2c3e50;
  line-height: 1.4;
  font-style: italic;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.5);
}

/* 主内容区域 */
.main-content {
  display: flex;
  gap: 20px;
  padding: 0 20px;
  height: calc(100vh - 200px);
  overflow: hidden;
}

/* 左侧面板 - 今日计划 */
.left-panel {
  flex: 1;
  max-width: 300px;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(25px);
  border-radius: 20px;
  padding: 20px;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  border: none;
  position: relative;
}

.panel-header h3 {
  margin: 0 0 20px 0;
  font-size: 18px;
  color: #2c3e50;
  text-align: center;
  font-weight: 600;
}

.today-tasks {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  transition: all 0.3s ease;
  border: 2px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(15px);
}

.task-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.task-item.completed {
  opacity: 0.7;
  border-color: rgba(198, 246, 213, 0.5);
  background: rgba(198, 246, 213, 0.15);
}

.task-icon {
  font-size: 22px;
  margin-right: 12px;
}

.task-content {
  flex: 1;
}

.task-title {
  font-weight: 600;
  margin-bottom: 4px;
  color: #2c3e50;
  font-size: 15px;
}

.task-time {
  font-size: 12px;
  color: #666;
  font-weight: 400;
}

.task-toggle {
  background: none;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  font-weight: bold;
}

.task-toggle:hover {
  border-color: rgba(255, 255, 255, 0.7);
  background: rgba(255, 255, 255, 0.1);
}

/* 中央面板 - 计时器 */
.center-panel {
  flex: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

/* 时间设定界面 */
.time-setting {
  text-align: center;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(30px);
  border-radius: 25px;
  padding: 45px;
  width: 100%;
  max-width: 520px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
  border: none;
  position: relative;
}

.time-setting h2 {
  margin: 0 0 35px 0;
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
}

.time-presets {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
  margin-bottom: 35px;
}

.preset-btn {
  padding: 18px 25px;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.3);
  color: #2c3e50;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(15px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.preset-btn:hover {
  background: rgba(255, 255, 255, 0.5);
  border-color: rgba(255, 255, 255, 0.7);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.preset-btn.active {
  background: rgba(255, 182, 219, 0.5);
  border-color: rgba(255, 182, 219, 0.8);
  box-shadow: 0 6px 25px rgba(255, 182, 219, 0.4);
}

.custom-time {
  margin-bottom: 35px;
  color: #2c3e50;
}

.custom-time label {
  display: block;
  margin-bottom: 12px;
  font-weight: 500;
}

.custom-time input {
  padding: 12px 15px;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.3);
  color: #2c3e50;
  width: 90px;
  margin-right: 12px;
  font-size: 14px;
  backdrop-filter: blur(15px);
}

.custom-time button {
  padding: 12px 25px;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.3);
  color: #2c3e50;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  backdrop-filter: blur(15px);
}

.custom-time button:hover {
  background: rgba(255, 255, 255, 0.5);
  border-color: rgba(255, 255, 255, 0.7);
}

.start-btn {
  padding: 18px 45px;
  border: none;
  border-radius: 30px;
  background: linear-gradient(135deg, rgba(255, 182, 219, 0.6), rgba(255, 168, 219, 0.6));
  color: #2c3e50;
  font-size: 20px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.start-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(255, 182, 219, 0.5);
  background: linear-gradient(135deg, rgba(255, 182, 219, 0.8), rgba(255, 168, 219, 0.8));
}

.start-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 计时器界面 */
.timer-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.session-label {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 35px;
  color: #2c3e50;
}

.timer-circle {
  width: 300px;
  height: 300px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  margin-bottom: 50px;
  box-shadow: 0 0 60px rgba(168, 237, 234, 0.4), 0 0 100px rgba(254, 214, 227, 0.3);
}

.timer-inner {
  width: 260px;
  height: 260px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(30px);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 12px 50px rgba(0, 0, 0, 0.3),
    inset 0 0 30px rgba(255, 255, 255, 0.1);
  border: 3px solid rgba(255, 255, 255, 0.25);
}

.timer-display {
  font-size: 3.8rem;
  font-weight: 300;
  color: #2c3e50;
  margin-bottom: 12px;
  letter-spacing: 3px;
  font-family: 'Roboto Mono', monospace;
}

.focus-text {
  font-size: 18px;
  color: #555;
  font-weight: 600;
}

/* 右侧面板 - 长期计划 */
.right-panel {
  flex: 1;
  max-width: 300px;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(25px);
  border-radius: 20px;
  padding: 20px;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  border: none;
  position: relative;
}

.long-term-goals {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.goal-card {
  padding: 22px;
  border-radius: 18px;
  color: #2c3e50;
  transition: all 0.3s ease;
  backdrop-filter: blur(15px);
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.goal-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
}

.goal-title {
  font-size: 17px;
  font-weight: 700;
  margin-bottom: 10px;
}

.goal-description {
  font-size: 14px;
  margin-bottom: 18px;
  opacity: 0.95;
  line-height: 1.4;
}

.goal-progress {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 13px;
  font-weight: 700;
}

/* 底部控制按钮 */
.bottom-controls {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 15px;
  padding: 18px 30px;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(30px);
  border-radius: 40px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(255, 255, 255, 0.15);
}

.control-btn {
  width: 60px;
  height: 60px;
  border: none;
  border-radius: 30px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.3);
}

.control-btn:active {
  transform: translateY(-2px);
}

.control-btn .icon {
  font-size: 26px;
}

/* 特殊按钮样式 */
.pause-btn {
  background: linear-gradient(135deg, rgba(198, 246, 213, 0.6), rgba(168, 237, 234, 0.6));
}

.pause-btn:hover {
  background: linear-gradient(135deg, rgba(198, 246, 213, 0.75), rgba(168, 237, 234, 0.75));
  box-shadow: 0 8px 25px rgba(198, 246, 213, 0.4);
}

.stop-btn {
  background: linear-gradient(135deg, rgba(255, 230, 230, 0.6), rgba(254, 214, 227, 0.6));
}

.stop-btn:hover {
  background: linear-gradient(135deg, rgba(255, 230, 230, 0.75), rgba(254, 214, 227, 0.75));
  box-shadow: 0 8px 25px rgba(255, 230, 230, 0.4);
}

.music-btn {
  background: linear-gradient(135deg, rgba(230, 220, 250, 0.6), rgba(198, 219, 239, 0.6));
}

.music-btn:hover {
  background: linear-gradient(135deg, rgba(230, 220, 250, 0.75), rgba(198, 219, 239, 0.75));
  box-shadow: 0 8px 25px rgba(230, 220, 250, 0.4);
}

.brightness-btn {
  background: linear-gradient(135deg, rgba(255, 238, 173, 0.6), rgba(255, 248, 220, 0.6));
}

.brightness-btn:hover {
  background: linear-gradient(135deg, rgba(255, 238, 173, 0.75), rgba(255, 248, 220, 0.75));
  box-shadow: 0 8px 25px rgba(255, 238, 173, 0.4);
}

.toolbox-btn {
  background: linear-gradient(135deg, rgba(179, 229, 252, 0.6), rgba(168, 237, 234, 0.6));
}

.toolbox-btn:hover {
  background: linear-gradient(135deg, rgba(179, 229, 252, 0.75), rgba(168, 237, 234, 0.75));
  box-shadow: 0 8px 25px rgba(179, 229, 252, 0.4);
}

.share-btn {
  background: linear-gradient(135deg, rgba(254, 214, 227, 0.6), rgba(255, 238, 173, 0.6));
}

.share-btn:hover {
  background: linear-gradient(135deg, rgba(254, 214, 227, 0.75), rgba(255, 238, 173, 0.75));
  box-shadow: 0 8px 25px rgba(254, 214, 227, 0.4);
}

/* 工具箱弹窗 */
.toolbox-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(15px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.toolbox-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(25px);
  border-radius: 20px;
  padding: 30px;
  max-width: 350px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.toolbox-content h3 {
  color: #2c3e50;
  margin: 0 0 20px 0;
  text-align: center;
  font-size: 22px;
  font-weight: 600;
}

.tool-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 25px;
}

.tool-btn {
  padding: 15px 10px;
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.tool-btn-1 {
  background: linear-gradient(135deg, rgba(168, 237, 234, 0.7) 0%, rgba(179, 229, 252, 0.7) 100%);
}

.tool-btn-1:hover {
  background: linear-gradient(135deg, rgba(168, 237, 234, 0.85) 0%, rgba(179, 229, 252, 0.85) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(168, 237, 234, 0.4);
}

.tool-btn-2 {
  background: linear-gradient(135deg, rgba(254, 214, 227, 0.7) 0%, rgba(255, 238, 173, 0.7) 100%);
}

.tool-btn-2:hover {
  background: linear-gradient(135deg, rgba(254, 214, 227, 0.85) 0%, rgba(255, 238, 173, 0.85) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(254, 214, 227, 0.4);
}

.tool-btn-3 {
  background: linear-gradient(135deg, rgba(230, 220, 250, 0.7) 0%, rgba(198, 219, 239, 0.7) 100%);
}

.tool-btn-3:hover {
  background: linear-gradient(135deg, rgba(230, 220, 250, 0.85) 0%, rgba(198, 219, 239, 0.85) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(230, 220, 250, 0.4);
}

.tool-btn-4 {
  background: linear-gradient(135deg, rgba(198, 246, 213, 0.7) 0%, rgba(179, 229, 252, 0.7) 100%);
}

.tool-btn-4:hover {
  background: linear-gradient(135deg, rgba(198, 246, 213, 0.85) 0%, rgba(179, 229, 252, 0.85) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(198, 246, 213, 0.4);
}

.close-btn {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  background: transparent;
  color: #666;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #f5f5f5;
  border-color: #ccc;
}

/* 分享悬浮窗口 */
.share-modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.55);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1200;
}

.share-content {
  width: 360px;
  max-width: 92%;
  background: linear-gradient(145deg, rgba(255,255,255,0.85), rgba(255,255,255,0.65));
  border-radius: 26px;
  padding: 24px 24px 18px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.25);
  position: relative;
  font-family: 'Noto Sans SC', sans-serif;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.share-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.badge-display {
  display: flex;
  gap: 12px;
  align-items: center;
}

.badge-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg,#ffd89b,#f7b733);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.badge-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.badge-name {
  font-size: 18px;
  font-weight: 700;
}

.badge-desc {
  font-size: 12px;
  color: #555;
}

.close-mini {
  background: rgba(0,0,0,0.08);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all .25s ease;
}

.close-mini:hover { background: rgba(0,0,0,0.15); }

.share-body { display: flex; flex-direction: column; gap: 10px; }

.stat-line { font-size: 14px; }
.stat-line strong { font-weight: 600; }

.quote-inline {
  margin-top: 4px;
  font-style: italic;
  font-size: 13px;
  color: #444;
  line-height: 1.4;
}

.reward-progress { display:flex; align-items:center; gap:10px; }
.reward-bar { flex:1; height:8px; background:rgba(0,0,0,0.1); border-radius:4px; overflow:hidden; }
.reward-fill { height:100%; background:linear-gradient(90deg,#7ED321,#4A90E2); transition:width .4s ease; }
.reward-progress-text { font-size:12px; font-weight:600; }

.next-badge { font-size:12px; color:#666; }

.share-actions { display:flex; gap:12px; margin-top:6px; }
.download-btn {
  flex:1;
  padding:12px 16px;
  background: linear-gradient(135deg,#7ED321,#4A90E2);
  color:#fff;
  border:none;
  border-radius:14px;
  font-weight:600;
  cursor:pointer;
  box-shadow:0 6px 18px rgba(74,144,226,.3);
  transition:all .3s ease;
}
.download-btn:hover { transform:translateY(-2px); box-shadow:0 10px 25px rgba(74,144,226,.45); }

.close-btn.alt { flex:0.6; background:#fff; border:2px solid #eee; color:#333; }
.close-btn.alt:hover { background:#fafafa; }

.share-footer { text-align:center; margin-top:4px; font-size:11px; letter-spacing:1px; color:#777; }

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    flex-direction: column;
    height: auto;
    gap: 20px;
  }
  
  .left-panel, .right-panel {
    max-width: none;
    max-height: 200px;
  }
  
  .timer-circle {
    width: 240px;
    height: 240px;
  }
  
  .timer-inner {
    width: 200px;
    height: 200px;
  }
  
  .timer-display {
    font-size: 2.8rem;
  }
}

@media (max-width: 768px) {
  .motivation-text {
    font-size: 14px;
  }
  
  .bottom-controls {
    gap: 15px;
    padding: 12px 20px;
  }
  
  .control-btn {
    width: 50px;
    height: 50px;
  }
  
  .left-panel, .right-panel {
    padding: 15px;
  }
  
  .time-setting {
    padding: 25px;
  }
  
  .time-presets {
    grid-template-columns: 1fr;
  }
}

/* 动画效果 */
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}

.timer-circle {
  animation: pulse 4s ease-in-out infinite;
}

/* 滚动条样式 */
.left-panel::-webkit-scrollbar,
.right-panel::-webkit-scrollbar {
  width: 6px;
}

.left-panel::-webkit-scrollbar-track,
.right-panel::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.left-panel::-webkit-scrollbar-thumb,
.right-panel::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.left-panel::-webkit-scrollbar-thumb:hover,
.right-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>

