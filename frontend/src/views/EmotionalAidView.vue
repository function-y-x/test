<template>
  <div class="emotional-aid-container">
    <!-- 动态气泡背景 -->
    <div class="bubbles-background">
      <div class="bubble" v-for="i in 20" :key="i" :style="getBubbleStyle()"></div>
    </div>
    
    <div class="page-header">
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span>
        返回主界面
      </button>
      <h1>情绪急救</h1>
    </div>

    <!-- 主菜单 -->
    <div v-if="currentView === 'menu'" class="aid-menu">
      <p class="intro-text">当您感到压力或情绪低落时，选择适合的方式快速调节</p>

      <div class="aid-options">
        <div class="aid-card immersive" @click="startEmergencyAid">
          <div class="card-icon">🧘‍♀️</div>
          <h3>90秒沉浸式急救</h3>
          <p>AI语音引导 + 视觉画面 + 匹配音乐</p>
          <div class="card-features">
            <span class="feature">正念模式</span>
            <span class="feature">辅助冥想</span>
          </div>
          <div class="card-border-glow"></div>
        </div>

        <div class="aid-card scenario" @click="showScenarioMenu">
          <div class="card-icon">🎯</div>
          <h3>场景模拟训练</h3>
          <p>AI引导快速进入最佳状态</p>
          <div class="card-features">
            <span class="feature">考试准备</span>
            <span class="feature">面试训练</span>
            <span class="feature">专注学习</span>
          </div>
          <div class="card-border-glow"></div>
        </div>

        <div class="aid-card quick" @click="showQuickOptions">
          <div class="card-icon">⚡</div>
          <h3>快速调节</h3>
          <p>传统的呼吸练习和微复盘</p>
          <div class="card-features">
            <span class="feature">呼吸指导</span>
            <span class="feature">情绪复盘</span>
          </div>
          <div class="card-border-glow"></div>
        </div>

        <div class="aid-card micro-action" @click="showMicroActionMenu">
          <div class="card-icon">💡</div>
          <h3>微行动挑战</h3>
          <p>用小行动打破负面循环，获得徽章奖励</p>
          <div class="card-features">
            <span class="feature">行动激励</span>
            <span class="feature">成长徽章</span>
          </div>
          <div class="card-border-glow"></div>
        </div>

        <div class="aid-card back-study" @click="showBackStudyMenu">
          <div class="card-icon">🎓</div>
          <h3>返回学习</h3>
          <p>精美鼓励话语，专为考研人设计</p>
          <div class="card-features">
            <span class="feature">考研专属鼓励</span>
            <span class="feature">心灵加油站</span>
          </div>
          <div class="card-border-glow"></div>
        </div>
      </div>
    </div>

    <!-- 返回学习鼓励浮窗 -->
    <div v-if="showBackStudy" class="back-study-overlay" @click="closeBackStudy">
      <div class="back-study-card" @click.stop>
        <button class="back-study-close" @click="closeBackStudy">×</button>
        <div class="back-study-header">
          <div class="back-study-badge">🎓</div>
          <div class="back-study-tag">考研冲刺 · 心流守护</div>
        </div>
        <div class="back-study-art">考研必胜</div>
        <p class="back-study-subtitle">Flow Mode Unlocked</p>
        <ul class="back-study-list">
          <li>“你不是一个人在奋斗，所有努力都在为梦想铺路！”</li>
          <li>“每一次坚持，都是离目标更近一步！”</li>
          <li>“考研路上，风雨兼程，你的勇气值得所有掌声！”</li>
          <li>“相信自己，未来的你会感谢现在拼搏的自己！”</li>
          <li>“累了就休息一下，调整好状态再出发！”</li>
          <li>“你已经很棒了，继续加油！”</li>
        </ul>
        <div class="back-study-footer">
          <div class="footer-badge">考研心理教练 · Study Flow</div>
          <button class="back-study-btn" @click="closeBackStudy">准备回到学习</button>
        </div>
      </div>
    </div>

    <!-- 90秒沉浸式急救 -->
    <div v-if="currentView === 'emergency'" class="emergency-session">
      <div class="session-header">
        <h2>90秒沉浸式急救</h2>
        <button class="exit-btn" @click="exitSession">退出</button>
      </div>

      <!-- 情绪评估 -->
      <div v-if="!emergencyStarted" class="emotion-assessment">
        <h3>请描述您当前的感受</h3>
        <div class="emotion-selector">
          <button v-for="emotion in emotions" :key="emotion.name" 
                  class="emotion-btn" 
                  :class="{ active: selectedEmotion === emotion.name }"
                  @click="selectEmotion(emotion)">
            <span class="emotion-icon">{{ emotion.icon }}</span>
            <span class="emotion-label">{{ emotion.name }}</span>
          </button>
        </div>
        
        <div class="intensity-slider">
          <label>强度等级: {{ emotionIntensity }}/10</label>
          <input type="range" v-model="emotionIntensity" min="1" max="10" step="1">
        </div>

        <button class="start-emergency-btn" @click="generateEmergencyGuidance" :disabled="!selectedEmotion">
          开始AI急救
        </button>
      </div>

      <!-- 沉浸式体验 -->
      <div v-if="emergencyStarted" class="immersive-experience">
        <div class="visual-area" :style="{ backgroundImage: `url(${currentVisual})` }">
          <div class="guidance-overlay">
            <div class="timer-circle">
              <div class="timer-text">{{ remainingTime }}s</div>
              <svg class="progress-ring" width="120" height="120">
                <circle class="progress-ring-circle" :style="{ strokeDashoffset: progressOffset }" 
                        cx="60" cy="60" r="54" fill="transparent" stroke="rgba(255,255,255,0.3)" 
                        stroke-width="4" stroke-dasharray="339.292"/>
              </svg>
            </div>
            <div class="voice-script">{{ currentVoiceText }}</div>
          </div>
        </div>

        <div class="session-controls">
          <button class="control-btn" @click="pauseSession" v-if="!isPaused">
            <span class="icon">⏸️</span>
          </button>
          <button class="control-btn" @click="resumeSession" v-else>
            <span class="icon">▶️</span>
          </button>
          <button class="control-btn" @click="stopEmergencySession">
            <span class="icon">⏹️</span>
          </button>
        </div>
      </div>

      <!-- 完成反馈 -->
      <div v-if="emergencyCompleted" class="completion-feedback">
        <div class="success-icon">✨</div>
        <h3>太棒了！您已完成90秒急救</h3>
        <p>感觉好一些了吗？</p>
        <div class="feedback-buttons">
          <button class="feedback-btn positive" @click="showEncouragePopup('positive')">
            😊 感觉更好了
          </button>
          <button class="feedback-btn neutral" @click="showEncouragePopup('neutral')">
            😐 没什么变化
          </button>
          <button class="feedback-btn negative" @click="showEncouragePopup('negative')">
            😔 还是不太好
          </button>
        </div>
      </div>

      <!-- 鼓励语弹窗 -->
      <div v-if="showEncourage" class="encourage-popup">
        <div class="encourage-card">
          <div class="encourage-badge">🏅</div>
          <h2 class="encourage-title">{{ encourageText }}</h2>
          <button class="encourage-btn" @click="startMicroAction">接受微行动挑战</button>
        </div>
      </div>

    </div>

    <!-- 场景模拟 -->
    <div v-if="currentView === 'scenario'" class="scenario-simulation">
      <div class="session-header">
        <h2>场景模拟训练</h2>
        <button class="exit-btn" @click="backToMenu">返回</button>
      </div>

      <div v-if="!scenarioStarted" class="scenario-selection">
        <h3>选择即将面临的场景</h3>
        <div class="scenario-cards">
          <div v-for="scenario in scenarios" :key="scenario.type" 
               class="scenario-card" 
               :class="{ active: selectedScenario === scenario.type }"
               @click="selectScenario(scenario)">
            <div class="scenario-icon">{{ scenario.icon }}</div>
            <h4>{{ scenario.name }}</h4>
            <p>{{ scenario.description }}</p>
          </div>
        </div>

        <div class="concerns-input">
          <label>您最担心的是什么？</label>
          <textarea v-model="userConcerns" placeholder="例如：担心紧张忘词、害怕发挥失常..."></textarea>
        </div>

        <button class="start-scenario-btn" @click="generateScenarioGuidance" :disabled="!selectedScenario">
          开始AI训练
        </button>
      </div>

      <div v-if="scenarioStarted" class="scenario-experience">
        <div class="scenario-content">
          <div class="preparation-phase" v-if="currentPhase === 'preparation'">
            <h3>准备阶段</h3>
            <div class="steps-list">
              <div v-for="(step, index) in scenarioData.preparation_steps" :key="index" 
                   class="step-item" :class="{ active: currentStep === index }">
                <span class="step-number">{{ index + 1 }}</span>
                <span class="step-text">{{ step }}</span>
              </div>
            </div>
            <button class="next-phase-btn" @click="nextPhase">进入心态调整</button>
          </div>

          <div class="mindset-phase" v-if="currentPhase === 'mindset'">
            <h3>心态调整</h3>
            <div class="mindset-content">{{ scenarioData.mindset_guidance }}</div>
            <button class="next-phase-btn" @click="nextPhase">开始可视化训练</button>
          </div>

          <div class="visualization-phase" v-if="currentPhase === 'visualization'">
            <h3>可视化训练</h3>
            <div class="visualization-area">
              <div class="visualization-text">{{ scenarioData.visualization_script }}</div>
              <div class="breathing-guide">
                <div class="breath-circle" :class="{ inhale: isInhaling }"></div>
                <div class="breath-text">{{ breathText }}</div>
              </div>
            </div>
            <button class="complete-scenario-btn" @click="completeScenario">完成训练</button>
          </div>
        </div>
      </div>

      <div v-if="scenarioCompleted" class="scenario-completion">
        <div class="success-icon">🎯</div>
        <h3>场景模拟完成！</h3>
        <p>您已经准备好面对 {{ selectedScenarioName }} 了</p>
        <div class="completion-actions">
          <button class="action-btn" @click="restartScenario">再次训练</button>
          <button class="action-btn primary" @click="backToMenu">返回主菜单</button>
        </div>
      </div>
    </div>

    <!-- 快速调节选项 -->
    <div v-if="currentView === 'quick'" class="quick-options">
      <div class="session-header">
        <h2>快速调节</h2>
        <button class="exit-btn" @click="backToMenu">返回</button>
      </div>

      <div class="quick-cards">
        <div class="quick-card" @click="startBreathingExercise">
          <div class="quick-icon">🫁</div>
          <h3>呼吸练习</h3>
          <p>4-7-8呼吸法，快速放松</p>
        </div>

        <div class="quick-card" @click="showMicroReview">
          <div class="quick-icon">🔍</div>
          <h3>微复盘</h3>
          <p>分析情绪来源，找到解决方案</p>
        </div>
      </div>

      <!-- 呼吸练习 -->
      <div v-if="showBreathing" class="breathing-exercise">
        <h3>4-7-8 呼吸练习</h3>
        <div class="breathing-visual">
          <div class="breathing-circle" :class="breathingPhase"></div>
          <div class="breathing-instruction">{{ breathingInstruction }}</div>
          <div class="breathing-count">{{ breathingCount }}</div>
        </div>
        <button class="stop-breathing-btn" @click="stopBreathing">停止练习</button>
      </div>

      <!-- 微复盘 -->
      <div v-if="showMicroReviewForm" class="micro-review-form">
        <h3>情绪微复盘</h3>
        <div class="review-questions">
          <div class="question-group">
            <label>什么事情触发了这种情绪？</label>
            <textarea v-model="trigger" placeholder="具体描述触发事件..."></textarea>
          </div>
          <div class="question-group">
            <label>您当时的想法是什么？</label>
            <textarea v-model="thoughts" placeholder="当时脑海中的想法..."></textarea>
          </div>
          <div class="question-group">
            <label>有什么更积极的角度来看待这件事？</label>
            <textarea v-model="reframe" placeholder="尝试从另一个角度思考..."></textarea>
          </div>
        </div>
        <button class="submit-review-btn" @click="submitMicroReview">完成复盘</button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <div class="loading-text">AI正在为您生成个性化指导...</div>
    </div>

    <!-- 微行动挑战浮窗 -->
    <div v-if="showMicroAction" class="micro-action-popup" @click="closeMicroAction">
      <div class="micro-action-card" @click.stop>
        <button class="micro-action-close" @click="closeMicroAction">×</button>
        <div class="micro-action-icon">💡</div>
        <h2 class="micro-action-title">微行动挑战</h2>
        <p class="micro-action-desc">{{ microAction }}</p>
        <div v-if="!microActionStarted">
          <button class="micro-action-btn" @click="beginMicroAction">立即出发</button>
        </div>
        <div v-else-if="!microActionCompleted">
          <div class="micro-action-timer">剩余时间：{{ microActionTime }} 秒</div>
          <button class="micro-action-btn" @click="completeMicroAction">完成并打卡</button>
        </div>
        <div v-else>
          <div class="badge-animate">🏆</div>
          <h3>恭喜获得徽章！</h3>
          <p>你已成功打破负面循环，欢迎回到学习！</p>
          <button class="micro-action-btn" @click="backToMenu">返回主菜单</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'EmotionalAidView',
  setup() {
    // 新增主菜单弹窗状态
  const showBackStudy = ref(false)

    // 主菜单弹窗方法
    const showBackStudyMenu = () => {
      showBackStudy.value = true
    }
    const closeBackStudy = () => {
      showBackStudy.value = false
    }

    // 微行动主菜单入口
    const showMicroActionMenu = () => {
      showEncourage.value = false
      showMicroAction.value = true
      microAction.value = microActionList[Math.floor(Math.random() * microActionList.length)]
      microActionStarted.value = false
      microActionCompleted.value = false
      microActionTime.value = 180 + Math.floor(Math.random() * 60)
    }
    const closeMicroAction = () => {
      if (microActionTimer) {
        clearInterval(microActionTimer)
        microActionTimer = null
      }
      showMicroAction.value = false
      microActionStarted.value = false
      microActionCompleted.value = false
      microActionTime.value = 180
    }

    // 生成气泡样式的方法  
    const getBubbleStyle = () => {
      const size = Math.random() * 80 + 40 // 40-120px
      const left = Math.random() * 100 // 0-100%
      const delay = Math.random() * 8 // 0-8s
      const duration = Math.random() * 10 + 15 // 15-25s
      return {
        width: `${size}px`,
        height: `${size}px`,
        left: `${left}%`,
        animationDelay: `${delay}s`,
        animationDuration: `${duration}s`
      }
    }
    
    const router = useRouter()
    
    // 主视图状态
    const currentView = ref('menu') // 'menu', 'emergency', 'scenario', 'quick'
    const isLoading = ref(false)

    // 90秒急救相关状态
    const emergencyStarted = ref(false)
    const emergencyCompleted = ref(false)
    
    // 鼓励语与微行动
    const showEncourage = ref(false)
    const encourageText = ref('')
    const showMicroAction = ref(false)
    const microAction = ref('')
    const microActionStarted = ref(false)
    const microActionCompleted = ref(false)
    const microActionTime = ref(180)
    let microActionTimer = null

    const selectedEmotion = ref('')
    const emotionIntensity = ref(5)
    const remainingTime = ref(90)
    const currentVoiceText = ref('')
    const currentVisual = ref('')
    const isPaused = ref(false)
    let emergencyTimer = null
    let voiceInterval = null

    // 鼓励语库
    const encourageList = [
      '你已经很棒了，继续前进！',
      '每一次努力都值得被肯定！',
      '你正在变得更强大！',
      '你的坚持终将带来美好结果！',
      '相信自己，你可以做到！',
      '今天的你已经比昨天更进步！'
    ]

    // 微行动库
    const microActionList = [
      '整理一下书桌，营造清爽学习环境',
      '喝一杯水，补充能量',
      '做3分钟简单伸展操，舒缓身体',
      '写下一个小目标并立即行动',
      '收拾一下房间的一角',
      '站起来走动一分钟，活动筋骨'
    ]

    // 场景模拟相关状态
    const scenarioStarted = ref(false)
    const scenarioCompleted = ref(false)
    const selectedScenario = ref('')
    const selectedScenarioName = ref('')
    const userConcerns = ref('')
    const currentPhase = ref('preparation') // 'preparation', 'mindset', 'visualization'
    const currentStep = ref(0)
    const scenarioData = ref({})
    const isInhaling = ref(true)
    const breathText = ref('深吸气')

    // 快速调节相关状态
    const showBreathing = ref(false)
    const showMicroReviewForm = ref(false)
    const breathingPhase = ref('inhale')
    const breathingInstruction = ref('准备深吸气')
    const breathingCount = ref(4)
    const trigger = ref('')
    const thoughts = ref('')
    const reframe = ref('')
    let breathingTimer = null

    // 情绪选项
    const emotions = ref([
      { name: '焦虑', icon: '😰', intensity: 'high' },
      { name: '紧张', icon: '😬', intensity: 'medium' },
      { name: '压力', icon: '😤', intensity: 'high' },
      { name: '沮丧', icon: '😔', intensity: 'medium' },
      { name: '愤怒', icon: '😠', intensity: 'high' },
      { name: '困惑', icon: '😕', intensity: 'low' },
      { name: '疲惫', icon: '😴', intensity: 'medium' },
      { name: '失望', icon: '😞', intensity: 'medium' }
    ])

    // 场景选项
    const scenarios = ref([
      { 
        type: 'exam', 
        name: '考试准备', 
        icon: '📝', 
        description: '重要考试前的心理准备和状态调整' 
      },
      { 
        type: 'interview', 
        name: '面试准备', 
        icon: '👔', 
        description: '面试前的自信建立和紧张缓解' 
      },
      { 
        type: 'study', 
        name: '专注学习', 
        icon: '📚', 
        description: '进入深度学习状态的心理调节' 
      }
    ])

    // 计算属性
    const progressOffset = computed(() => {
      const circumference = 2 * Math.PI * 54
      const progress = (90 - remainingTime.value) / 90
      return circumference - (progress * circumference)
    })

    // 基础方法
    const goBack = () => {
      router.push('/dashboard')
    }

    const backToMenu = () => {
      currentView.value = 'menu'
      resetAllStates()
    }

    const resetAllStates = () => {
      emergencyStarted.value = false
      emergencyCompleted.value = false
      scenarioStarted.value = false
      scenarioCompleted.value = false
      showBreathing.value = false
      showMicroReviewForm.value = false
      showEncourage.value = false
      showMicroAction.value = false
      microActionStarted.value = false
      microActionCompleted.value = false
      showBackStudy.value = false
      clearTimers()
    }

    const clearTimers = () => {
      if (emergencyTimer) clearInterval(emergencyTimer)
      if (voiceInterval) clearInterval(voiceInterval)
      if (breathingTimer) clearInterval(breathingTimer)
      if (microActionTimer) clearInterval(microActionTimer)
    }

    // 90秒沉浸式急救方法
    const startEmergencyAid = () => {
      currentView.value = 'emergency'
    }

    const selectEmotion = (emotion) => {
      selectedEmotion.value = emotion.name
    }

    const generateEmergencyGuidance = async () => {
      isLoading.value = true
      try {
        const response = await fetch('/api/v1/emotional-aid/emergency-guidance', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            emotion_state: selectedEmotion.value,
            intensity: emotionIntensity.value / 10
          })
        })
        
        if (response.ok) {
          const data = await response.json()
          startEmergencySession(data)
        } else {
          // 使用备选方案
          startEmergencySession({
            voice_script: '请深呼吸，吸气4秒，保持4秒，呼气6秒。重复这个过程，让自己平静下来。',
            visual_prompt: '一片宁静的森林，阳光透过树叶洒下斑驳的光影',
            music_type: 'nature_sounds',
            duration: 90
          })
        }
      } catch (error) {
        console.error('生成急救指导失败:', error)
        // 使用备选方案
        startEmergencySession({
          voice_script: '请深呼吸，吸气4秒，保持4秒，呼气6秒。重复这个过程，让自己平静下来。',
          visual_prompt: '一片宁静的森林，阳光透过树叶洒下斑驳的光影',
          music_type: 'nature_sounds',
          duration: 90
        })
      } finally {
        isLoading.value = false
      }
    }

    const startEmergencySession = (guidanceData) => {
      emergencyStarted.value = true
      currentVoiceText.value = guidanceData.voice_script
      // 这里可以集成真实的图像生成API或使用预设图片
      currentVisual.value = 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=600&fit=crop'
      
      // 启动倒计时
      emergencyTimer = setInterval(() => {
        if (!isPaused.value && remainingTime.value > 0) {
          remainingTime.value--
        } else if (remainingTime.value === 0) {
          completeEmergencySession()
        }
      }, 1000)

      // 语音文本轮播（模拟TTS）
      const voiceSegments = guidanceData.voice_script.split('。').filter(s => s.trim())
      let segmentIndex = 0
      voiceInterval = setInterval(() => {
        if (!isPaused.value && segmentIndex < voiceSegments.length) {
          currentVoiceText.value = voiceSegments[segmentIndex].trim() + '。'
          segmentIndex++
        }
      }, 10000) // 每10秒切换一段语音
    }

    const pauseSession = () => {
      isPaused.value = true
    }

    const resumeSession = () => {
      isPaused.value = false
    }

    const stopEmergencySession = () => {
      clearTimers()
      emergencyStarted.value = false
      remainingTime.value = 90
    }

    const completeEmergencySession = () => {
      clearTimers()
      emergencyStarted.value = false
      emergencyCompleted.value = true
      // 不自动弹出鼓励语，让用户选择反馈后再显示
    }

    // 鼓励语弹窗
    const showEncouragePopup = (feedbackType) => {
      // 根据反馈类型记录用户情绪状态（可用于后续分析）
      console.log('用户反馈:', feedbackType)
      emergencyCompleted.value = false
      encourageText.value = encourageList[Math.floor(Math.random() * encourageList.length)]
      showEncourage.value = true
    }

    // 微行动挑战弹窗
    const startMicroAction = () => {
      showEncourage.value = false
      showMicroAction.value = true
      microAction.value = microActionList[Math.floor(Math.random() * microActionList.length)]
      microActionStarted.value = false
      microActionCompleted.value = false
      microActionTime.value = 180 + Math.floor(Math.random() * 60) // 3-4分钟
    }

    const beginMicroAction = () => {
      if (microActionTimer) {
        clearInterval(microActionTimer)
        microActionTimer = null
      }
      microActionStarted.value = true
      microActionCompleted.value = false
      microActionTimer = setInterval(() => {
        if (microActionTime.value > 0) {
          microActionTime.value--
        } else {
          completeMicroAction()
        }
      }, 1000)
    }

    const completeMicroAction = () => {
      if (microActionTimer) {
        clearInterval(microActionTimer)
        microActionTimer = null
      }
      microActionStarted.value = false
      microActionCompleted.value = true
      // 可在此处增加积分或徽章存储逻辑
    }

    const exitSession = () => {
      clearTimers()
      backToMenu()
      showEncourage.value = false
      showMicroAction.value = false
      microActionStarted.value = false
      microActionCompleted.value = false
    }

    // 场景模拟方法
    const showScenarioMenu = () => {
      currentView.value = 'scenario'
    }

    const selectScenario = (scenario) => {
      selectedScenario.value = scenario.type
      selectedScenarioName.value = scenario.name
    }

    const generateScenarioGuidance = async () => {
      isLoading.value = true
      try {
        const response = await fetch('/api/v1/emotional-aid/scenario-simulation', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            scenario_type: selectedScenario.value,
            user_concerns: userConcerns.value
          })
        })
        
        if (response.ok) {
          const data = await response.json()
          startScenarioSession(data)
        } else {
          // 使用备选方案
          startScenarioSession({
            preparation_steps: ['清理桌面', '设定学习目标', '准备学习材料'],
            mindset_guidance: '每一分钟的努力都在为梦想添砖加瓦',
            visualization_script: '想象自己专注学习，逐步掌握知识的满足感',
            duration: 300
          })
        }
      } catch (error) {
        console.error('生成场景指导失败:', error)
        startScenarioSession({
          preparation_steps: ['深呼吸调整', '明确目标', '积极暗示'],
          mindset_guidance: '相信自己的能力，一步步来',
          visualization_script: '想象自己成功完成目标的场景',
          duration: 300
        })
      } finally {
        isLoading.value = false
      }
    }

    const startScenarioSession = (data) => {
      scenarioData.value = data
      scenarioStarted.value = true
      currentPhase.value = 'preparation'
      currentStep.value = 0
    }

    const nextPhase = () => {
      if (currentPhase.value === 'preparation') {
        currentPhase.value = 'mindset'
      } else if (currentPhase.value === 'mindset') {
        currentPhase.value = 'visualization'
        startBreathingGuide()
      }
    }

    const startBreathingGuide = () => {
      let cycle = 0
      const breathCycle = () => {
        // 吸气阶段
        isInhaling.value = true
        breathText.value = '深深吸气...'
        setTimeout(() => {
          // 呼气阶段
          isInhaling.value = false
          breathText.value = '缓缓呼气...'
        }, 4000)
      }
      
      breathCycle()
      const breathInterval = setInterval(() => {
        cycle++
        if (cycle < 5) { // 5个呼吸周期
          breathCycle()
        } else {
          clearInterval(breathInterval)
        }
      }, 8000)
    }

    const completeScenario = () => {
      scenarioStarted.value = false
      scenarioCompleted.value = true
    }

    const restartScenario = () => {
      scenarioCompleted.value = false
      currentPhase.value = 'preparation'
      currentStep.value = 0
      scenarioStarted.value = true
    }

    // 快速调节方法
    const showQuickOptions = () => {
      currentView.value = 'quick'
    }

    const startBreathingExercise = () => {
      showBreathing.value = true
      showMicroReviewForm.value = false
      startBreathingCycle()
    }

    const startBreathingCycle = () => {
      let phase = 0 // 0: inhale, 1: hold, 2: exhale
      let count = 4
      
      const updateBreathing = () => {
        switch(phase) {
          case 0:
            breathingPhase.value = 'inhale'
            breathingInstruction.value = '深吸气'
            break
          case 1:
            breathingPhase.value = 'hold'
            breathingInstruction.value = '屏住呼吸'
            break
          case 2:
            breathingPhase.value = 'exhale'
            breathingInstruction.value = '缓慢呼气'
            break
        }
        breathingCount.value = count
      }

      updateBreathing()
      
      breathingTimer = setInterval(() => {
        count--
        if (count === 0) {
          phase = (phase + 1) % 3
          count = phase === 1 ? 7 : (phase === 2 ? 8 : 4) // 4-7-8 呼吸法
        }
        updateBreathing()
      }, 1000)
    }

    const stopBreathing = () => {
      showBreathing.value = false
      if (breathingTimer) clearInterval(breathingTimer)
    }

    const showMicroReview = () => {
      showMicroReviewForm.value = true
      showBreathing.value = false
    }

    const submitMicroReview = () => {
      console.log('微复盘提交:', { trigger: trigger.value, thoughts: thoughts.value, reframe: reframe.value })
      // 这里可以将数据发送到后端进行AI分析
      alert('复盘已提交，AI将为您分析并提供建议')
      showMicroReviewForm.value = false
      trigger.value = ''
      thoughts.value = ''
      reframe.value = ''
    }

    // 生命周期
    onUnmounted(() => {
      clearTimers()
    })

    return {
  // 状态
  currentView,
  isLoading,
  emergencyStarted,
  emergencyCompleted,
  showEncourage,
  encourageText,
  showMicroAction,
  microAction,
  microActionStarted,
  microActionCompleted,
  microActionTime,
  selectedEmotion,
  emotionIntensity,
  remainingTime,
  currentVoiceText,
  currentVisual,
  isPaused,
  scenarioStarted,
  scenarioCompleted,
  selectedScenario,
  selectedScenarioName,
  userConcerns,
  currentPhase,
  currentStep,
  scenarioData,
  isInhaling,
  breathText,
  showBreathing,
  showMicroReviewForm,
  breathingPhase,
  breathingInstruction,
  breathingCount,
  trigger,
  thoughts,
  reframe,
  emotions,
  scenarios,
  progressOffset,
  showBackStudy,

  // 方法
  goBack,
  backToMenu,
  startEmergencyAid,
  selectEmotion,
  generateEmergencyGuidance,
  pauseSession,
  resumeSession,
  stopEmergencySession,
  showEncouragePopup,
  startMicroAction,
  beginMicroAction,
  completeMicroAction,
  exitSession,
  showScenarioMenu,
  selectScenario,
  generateScenarioGuidance,
  nextPhase,
  completeScenario,
  restartScenario,
  showQuickOptions,
  startBreathingExercise,
  stopBreathing,
  showMicroReview,
  submitMicroReview,
  showBackStudyMenu,
  closeBackStudy,
  showMicroActionMenu,
  closeMicroAction,
  getBubbleStyle
    }
  }
}

</script>

<style scoped>
.emotional-aid-container {
  padding: 20px;
  max-width: 100%;
  margin: 0 auto;
  font-family: 'Noto Sans SC', 'Arial', sans-serif;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 动态气泡背景 */
.bubbles-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
}

.bubble {
  position: absolute;
  bottom: -120px;
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.6), rgba(168, 237, 234, 0.3));
  border-radius: 50%;
  opacity: 0.6;
  animation: rise linear infinite;
  box-shadow: 
    0 0 20px rgba(255, 255, 255, 0.5),
    inset 0 0 20px rgba(255, 255, 255, 0.3);
}

/* 不同气泡的渐变色边框 */
.bubble:nth-child(5n+1) {
  border: 3px solid transparent;
  background-image: 
    radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.6), rgba(168, 237, 234, 0.3)),
    linear-gradient(135deg, rgba(168, 237, 234, 0.6), rgba(179, 229, 252, 0.6));
  background-origin: border-box;
  background-clip: padding-box, border-box;
}

.bubble:nth-child(5n+2) {
  border: 3px solid transparent;
  background-image: 
    radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.6), rgba(198, 246, 213, 0.3)),
    linear-gradient(135deg, rgba(198, 246, 213, 0.6), rgba(168, 237, 234, 0.6));
  background-origin: border-box;
  background-clip: padding-box, border-box;
}

.bubble:nth-child(5n+3) {
  border: 3px solid transparent;
  background-image: 
    radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.6), rgba(255, 238, 173, 0.3)),
    linear-gradient(135deg, rgba(255, 238, 173, 0.6), rgba(254, 214, 227, 0.6));
  background-origin: border-box;
  background-clip: padding-box, border-box;
}

.bubble:nth-child(5n+4) {
  border: 3px solid transparent;
  background-image: 
    radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.6), rgba(254, 214, 227, 0.3)),
    linear-gradient(135deg, rgba(254, 214, 227, 0.6), rgba(230, 220, 250, 0.6));
  background-origin: border-box;
  background-clip: padding-box, border-box;
}

.bubble:nth-child(5n) {
  border: 3px solid transparent;
  background-image: 
    radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.6), rgba(230, 220, 250, 0.3)),
    linear-gradient(135deg, rgba(230, 220, 250, 0.6), rgba(198, 219, 239, 0.6));
  background-origin: border-box;
  background-clip: padding-box, border-box;
}

@keyframes rise {
  0% {
    bottom: -120px;
    transform: translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    bottom: 110vh;
    transform: translateX(50px) rotate(360deg);
    opacity: 0;
  }
}

/* 通用样式 */
.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  gap: 20px;
  position: relative;
  z-index: 1;
}

.back-button {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  padding: 10px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #2c3e50;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.back-button:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
}

.back-icon {
  font-size: 1.2em;
  font-weight: bold;
}

h1 {
  color: #2c3e50;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 2.2rem;
}

.intro-text {
  color: #555;
  margin-bottom: 40px;
  font-size: 1.1rem;
  text-align: center;
}

/* 主菜单样式 */
.aid-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.aid-card {
  background: rgba(255, 255, 255, 0.95);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s ease;
  backdrop-filter: blur(15px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: visible;
}

/* 卡片边框发光效果 */
.card-border-glow {
  position: absolute;
  inset: -3px;
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
  z-index: -1;
}

.aid-card.immersive .card-border-glow {
  background: linear-gradient(135deg, 
    rgba(168, 237, 234, 0.6), 
    rgba(179, 229, 252, 0.6));
  box-shadow: 0 0 30px rgba(168, 237, 234, 0.6);
}

.aid-card.scenario .card-border-glow {
  background: linear-gradient(135deg, 
    rgba(198, 246, 213, 0.6), 
    rgba(168, 237, 234, 0.6));
  box-shadow: 0 0 30px rgba(198, 246, 213, 0.6);
}

.aid-card.quick .card-border-glow {
  background: linear-gradient(135deg, 
    rgba(255, 238, 173, 0.6), 
    rgba(255, 248, 220, 0.6));
  box-shadow: 0 0 30px rgba(255, 238, 173, 0.6);
}

.aid-card.micro-action .card-border-glow {
  background: linear-gradient(135deg, 
    rgba(254, 214, 227, 0.6), 
    rgba(255, 238, 173, 0.6));
  box-shadow: 0 0 30px rgba(254, 214, 227, 0.6);
}

.aid-card.back-study .card-border-glow {
  background: linear-gradient(135deg, 
    rgba(230, 220, 250, 0.6), 
    rgba(198, 219, 239, 0.6));
  box-shadow: 0 0 30px rgba(230, 220, 250, 0.6);
}

.aid-card:hover .card-border-glow {
  opacity: 1;
}

.aid-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.aid-card:hover::before {
  transform: scaleX(1);
}

.aid-card:hover {
  transform: translateY(-8px);
}

.aid-card.immersive {
  border: 2px solid rgba(168, 237, 234, 0.6);
  box-shadow: 0 4px 20px rgba(168, 237, 234, 0.15);
}

.aid-card.immersive:hover {
  background: linear-gradient(135deg, rgba(168, 237, 234, 0.25), rgba(179, 229, 252, 0.25));
  border-color: rgba(168, 237, 234, 0.8);
  box-shadow: 0 8px 35px rgba(168, 237, 234, 0.3);
}

.aid-card.scenario {
  border: 2px solid rgba(198, 246, 213, 0.6);
  box-shadow: 0 4px 20px rgba(198, 246, 213, 0.15);
}

.aid-card.scenario:hover {
  background: linear-gradient(135deg, rgba(198, 246, 213, 0.25), rgba(168, 237, 234, 0.25));
  border-color: rgba(198, 246, 213, 0.8);
  box-shadow: 0 8px 35px rgba(198, 246, 213, 0.3);
}

.aid-card.quick {
  border: 2px solid rgba(255, 238, 173, 0.6);
  box-shadow: 0 4px 20px rgba(255, 238, 173, 0.15);
}

.aid-card.quick:hover {
  background: linear-gradient(135deg, rgba(255, 238, 173, 0.25), rgba(255, 248, 220, 0.25));
  border-color: rgba(255, 238, 173, 0.8);
  box-shadow: 0 8px 35px rgba(255, 238, 173, 0.3);
}

.aid-card.micro-action {
  border: 2px solid rgba(254, 214, 227, 0.6);
  box-shadow: 0 4px 20px rgba(254, 214, 227, 0.15);
}

.aid-card.micro-action:hover {
  background: linear-gradient(135deg, rgba(254, 214, 227, 0.25), rgba(255, 238, 173, 0.25));
  border-color: rgba(254, 214, 227, 0.8);
  box-shadow: 0 8px 35px rgba(254, 214, 227, 0.3);
}

.aid-card.back-study {
  border: 2px solid rgba(230, 220, 250, 0.6);
  box-shadow: 0 4px 20px rgba(230, 220, 250, 0.15);
}

.aid-card.back-study:hover {
  background: linear-gradient(135deg, rgba(230, 220, 250, 0.25), rgba(198, 219, 239, 0.25));
  border-color: rgba(230, 220, 250, 0.8);
  box-shadow: 0 8px 35px rgba(230, 220, 250, 0.3);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  display: block;
  transition: transform 0.3s ease;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.1));
}

.aid-card:hover .card-icon {
  transform: scale(1.1);
  animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% { transform: scale(1.1); }
  50% { transform: scale(1.2); }
}

.aid-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 1.4rem;
  font-weight: 700;
  transition: color 0.3s ease;
}

.aid-card:hover h3 {
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.aid-card p {
  color: #666;
  font-size: 1rem;
  margin-bottom: 20px;
  line-height: 1.5;
}

.card-features {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.feature {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
}

/* 会话头部样式 */
.session-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  backdrop-filter: blur(10px);
}

.session-header h2 {
  color: #2c3e50;
  margin: 0;
  font-size: 1.6rem;
}

.exit-btn {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: 2px solid rgba(244, 67, 54, 0.3);
  border-radius: 12px;
  padding: 8px 16px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.exit-btn:hover {
  background: rgba(244, 67, 54, 0.2);
  transform: translateY(-2px);
}

/* 情绪评估样式 */
.emotion-assessment {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 20px;
  backdrop-filter: blur(15px);
}

.emotion-assessment h3 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 25px;
  font-size: 1.3rem;
}

.emotion-selector {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.emotion-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 15px;
  padding: 15px 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.emotion-btn:hover, .emotion-btn.active {
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(102, 126, 234, 0.5);
  transform: translateY(-3px);
}

.emotion-icon {
  font-size: 2rem;
}

.emotion-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #2c3e50;
}

.intensity-slider {
  margin-bottom: 30px;
  text-align: center;
}

.intensity-slider label {
  display: block;
  margin-bottom: 15px;
  color: #2c3e50;
  font-weight: 600;
}

.intensity-slider input[type="range"] {
  width: 100%;
  max-width: 300px;
  height: 8px;
  border-radius: 4px;
  background: rgba(102, 126, 234, 0.2);
  outline: none;
  appearance: none;
}

.intensity-slider input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #667eea;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.start-emergency-btn, .start-scenario-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 15px;
  padding: 15px 30px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.start-emergency-btn:hover, .start-scenario-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.start-emergency-btn:disabled, .start-scenario-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 沉浸式体验样式 */
.immersive-experience {
  background: transparent;
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  min-height: calc(100vh - 200px);
}

.visual-area {
  width: 100%;
  min-height: calc(100vh - 200px);
  height: auto;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.guidance-overlay {
  background: rgba(0, 0, 0, 0.4);
  color: white;
  padding: 40px;
  border-radius: 20px;
  text-align: center;
  backdrop-filter: blur(10px);
  max-width: 80%;
}

.timer-circle {
  position: relative;
  margin-bottom: 25px;
  filter: drop-shadow(0 0 20px rgba(168, 237, 234, 0.5));
  animation: timerBreath 4s ease-in-out infinite;
}

@keyframes timerBreath {
  0%, 100% { 
    filter: drop-shadow(0 0 20px rgba(168, 237, 234, 0.5));
  }
  50% { 
    filter: drop-shadow(0 0 40px rgba(168, 237, 234, 0.8));
  }
}

.timer-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
}

.progress-ring {
  transform: rotate(-90deg);
}

.progress-ring-circle {
  transition: stroke-dashoffset 0.5s ease;
}

.voice-script {
  font-size: 1.2rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.95);
  max-width: 600px;
  margin: 0 auto;
  padding: 25px 30px;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.25), rgba(168, 237, 234, 0.15));
  border-radius: 20px;
  backdrop-filter: blur(15px);
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.2),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
  animation: textGlow 3s ease-in-out infinite;
}

@keyframes textGlow {
  0%, 100% { 
    box-shadow: 
      0 8px 32px rgba(0, 0, 0, 0.2),
      inset 0 0 20px rgba(255, 255, 255, 0.1);
  }
  50% { 
    box-shadow: 
      0 8px 32px rgba(0, 0, 0, 0.2),
      inset 0 0 30px rgba(255, 255, 255, 0.2),
      0 0 30px rgba(168, 237, 234, 0.3);
  }
}

.session-controls {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 0;
  margin: 20px 0;
  background: none;
  /* 完全透明，按钮直接悬浮在背景上 */
}

.control-btn {
  position: relative;
  width: 60px;
  height: 60px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  backdrop-filter: blur(15px);
  border: 2px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.control-btn::after {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.control-btn:hover {
  transform: scale(1.15);
  background: rgba(255, 255, 255, 0.4);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
}

.control-btn:hover::after {
  opacity: 1;
}

/* 完成反馈样式 */
.completion-feedback {
  text-align: center;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 40px;
  backdrop-filter: blur(15px);
}

.success-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.completion-feedback h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 1.5rem;
}

.completion-feedback p {
  color: #666;
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.feedback-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
}

.feedback-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 15px;
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.feedback-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

/* 场景模拟样式 */
.scenario-selection {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 30px;
  backdrop-filter: blur(15px);
}

.scenario-selection h3 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 25px;
  font-size: 1.3rem;
}

.scenario-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.scenario-card {
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.scenario-card:hover, .scenario-card.active {
  background: rgba(76, 175, 80, 0.1);
  border-color: rgba(76, 175, 80, 0.5);
  transform: translateY(-3px);
}

.scenario-icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.scenario-card h4 {
  color: #2c3e50;
  margin-bottom: 8px;
  font-size: 1.1rem;
}

.scenario-card p {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.concerns-input {
  margin-bottom: 30px;
}

.concerns-input label {
  display: block;
  margin-bottom: 10px;
  color: #2c3e50;
  font-weight: 600;
}

.concerns-input textarea {
  width: 100%;
  padding: 15px;
  border: 2px solid rgba(76, 175, 80, 0.3);
  border-radius: 10px;
  min-height: 100px;
  font-family: inherit;
  resize: vertical;
  background: rgba(255, 255, 255, 0.8);
}

/* 场景体验样式 */
.scenario-experience {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(198, 246, 213, 0.3));
  border-radius: 20px;
  padding: 30px;
  backdrop-filter: blur(15px);
  border: 2px solid rgba(198, 246, 213, 0.5);
  box-shadow: 
    0 10px 40px rgba(0, 0, 0, 0.12),
    inset 0 0 30px rgba(255, 255, 255, 0.3);
}

.scenario-content h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 1.4rem;
  text-align: center;
  background: linear-gradient(135deg, #4caf50, #45a049);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

.steps-list {
  margin-bottom: 30px;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  margin-bottom: 10px;
  background: linear-gradient(135deg, rgba(198, 246, 213, 0.2), rgba(76, 175, 80, 0.1));
  border-radius: 10px;
  transition: all 0.3s ease;
  border: 1px solid rgba(76, 175, 80, 0.2);
  position: relative;
  overflow: hidden;
}

.step-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.step-item:hover::before {
  left: 100%;
}

.step-item.active {
  background: linear-gradient(135deg, rgba(198, 246, 213, 0.4), rgba(76, 175, 80, 0.25));
  border: 2px solid rgba(76, 175, 80, 0.6);
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
  animation: shimmer 2s ease-in-out infinite;
}

@keyframes shimmer {
  0%, 100% {
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
  }
  50% {
    box-shadow: 0 6px 25px rgba(76, 175, 80, 0.4);
  }
}

.step-number {
  width: 30px;
  height: 30px;
  background: #4caf50;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.step-text {
  flex: 1;
  color: #2c3e50;
  font-weight: 500;
}

.mindset-content {
  background: rgba(76, 175, 80, 0.1);
  border-radius: 15px;
  padding: 25px;
  color: #2c3e50;
  font-size: 1.1rem;
  line-height: 1.6;
  text-align: center;
  margin-bottom: 30px;
}

.visualization-area {
  text-align: center;
  padding: 30px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 15px;
  margin-bottom: 30px;
}

.visualization-text {
  color: #2c3e50;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 30px;
}

.breathing-guide {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.breath-circle {
  width: 80px;
  height: 80px;
  background: rgba(102, 126, 234, 0.3);
  border-radius: 50%;
  transition: all 2s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
}

.breath-circle.inhale {
  transform: scale(1.3);
  background: rgba(102, 126, 234, 0.5);
}

.breath-text {
  color: #2c3e50;
  font-weight: 600;
  font-size: 1.1rem;
}

.next-phase-btn, .complete-scenario-btn {
  position: relative;
  width: 100%;
  background: linear-gradient(135deg, #4caf50, #45a049);
  color: white;
  border: none;
  border-radius: 15px;
  padding: 15px 30px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.next-phase-btn::after, .complete-scenario-btn::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.5s, height 0.5s;
}

.next-phase-btn:hover::after, .complete-scenario-btn:hover::after {
  width: 300px;
  height: 300px;
}

.next-phase-btn:hover, .complete-scenario-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 35px rgba(76, 175, 80, 0.5);
}

/* 场景完成样式 */
.scenario-completion {
  text-align: center;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 40px;
  backdrop-filter: blur(15px);
}

.scenario-completion h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 1.5rem;
}

.scenario-completion p {
  color: #666;
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.completion-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.action-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 12px;
  padding: 12px 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: transparent;
}

.action-btn:hover {
  transform: translateY(-2px);
}

/* 快速调节样式 */
.quick-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.quick-card {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid rgba(255, 193, 7, 0.3);
  border-radius: 15px;
  padding: 25px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(15px);
}

.quick-card:hover {
  background: rgba(255, 193, 7, 0.1);
  border-color: rgba(255, 193, 7, 0.5);
  transform: translateY(-5px);
}

.quick-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.quick-card h3 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 1.2rem;
}

.quick-card p {
  color: #666;
  font-size: 0.95rem;
}

/* 呼吸练习样式 */
.breathing-exercise {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  backdrop-filter: blur(15px);
}

.breathing-exercise h3 {
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 1.4rem;
}

.breathing-visual {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.breathing-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 1s ease-in-out;
  box-shadow: 
    0 8px 30px rgba(0, 0, 0, 0.1),
    0 0 40px rgba(168, 237, 234, 0.4),
    inset 0 0 30px rgba(255, 255, 255, 0.3);
  border: 3px solid rgba(255, 255, 255, 0.5);
  animation: breathGlow 3s ease-in-out infinite;
}

@keyframes breathGlow {
  0%, 100% {
    box-shadow: 
      0 8px 30px rgba(0, 0, 0, 0.1),
      0 0 40px rgba(168, 237, 234, 0.4),
      inset 0 0 30px rgba(255, 255, 255, 0.3);
  }
  50% {
    box-shadow: 
      0 8px 30px rgba(0, 0, 0, 0.1),
      0 0 60px rgba(168, 237, 234, 0.6),
      inset 0 0 40px rgba(255, 255, 255, 0.5);
  }
}

.breathing-circle.inhale {
  background: rgba(76, 175, 80, 0.3);
  transform: scale(1.2);
}

.breathing-circle.hold {
  background: rgba(255, 193, 7, 0.3);
  transform: scale(1.2);
}

.breathing-circle.exhale {
  background: rgba(102, 126, 234, 0.3);
  transform: scale(0.8);
}

.breathing-instruction {
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
}

.breathing-count {
  color: #667eea;
  font-size: 2rem;
  font-weight: 700;
}

.stop-breathing-btn {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: 2px solid rgba(244, 67, 54, 0.3);
  border-radius: 12px;
  padding: 12px 24px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.stop-breathing-btn:hover {
  background: rgba(244, 67, 54, 0.2);
}

/* 微复盘样式 */
.micro-review-form {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(230,  220, 250, 0.3));
  border-radius: 20px;
  padding: 30px;
  backdrop-filter: blur(15px);
  border: 2px solid rgba(230, 220, 250, 0.5);
  box-shadow: 
    0 10px 40px rgba(0, 0, 0, 0.15),
    inset 0 0 30px rgba(255, 255, 255, 0.3);
}

.micro-review-form h3 {
  color: #2c3e50;
  margin-bottom: 25px;
  font-size: 1.4rem;
  text-align: center;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

.review-questions {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.question-group label {
  display: block;
  margin-bottom: 8px;
  color: #2c3e50;
  font-weight: 600;
  font-size: 1rem;
}

.question-group textarea {
  width: 100%;
  padding: 15px;
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 10px;
  min-height: 80px;
  font-family: inherit;
  resize: vertical;
  background: rgba(255, 255, 255, 0.8);
  transition: border-color 0.3s ease;
}

.question-group textarea:focus {
  outline: none;
  border-color: rgba(102, 126, 234, 0.6);
}

.submit-review-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 15px;
  padding: 15px 30px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-review-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

/* 加载状态样式 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: white;
  font-size: 1.1rem;
  font-weight: 500;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .emotional-aid-container {
    padding: 15px;
  }
  
  .aid-options {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .scenario-cards {
    grid-template-columns: 1fr;
  }
  
  .quick-cards {
    grid-template-columns: 1fr;
  }
  
  .emotion-selector {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  }
  
  .feedback-buttons {
    flex-direction: column;
  }
  
  .completion-actions {
    flex-direction: column;
  }
  
  .visual-area {
    min-height: 60vh;
    height: auto;
  }
  
  .guidance-overlay {
    padding: 20px;
  }
  
  h1 {
    font-size: 1.8rem;
  }
}

@media (max-width: 480px) {
  .session-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .visual-area {
    min-height: 50vh;
    height: auto;
  }
  
  .timer-text {
    font-size: 1.4rem;
  }
  
  .voice-script {
    font-size: 1rem;
  }
}

/* 返回学习浮窗 */
.back-study-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
}

.back-study-card {
  position: relative;
  width: min(480px, 92vw);
  border-radius: 32px;
  padding: 48px 38px 40px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 236, 210, 0.92) 50%, rgba(232, 219, 255, 0.95) 100%);
  box-shadow: 0 25px 70px rgba(118, 75, 162, 0.35);
  overflow: hidden;
  animation: popIn 0.45s ease forwards;
}

.back-study-card::before {
  content: '';
  position: absolute;
  inset: 18px;
  border-radius: 24px;
  border: 1px dashed rgba(118, 75, 162, 0.35);
  pointer-events: none;
}

.back-study-close {
  position: absolute;
  top: 18px;
  right: 22px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.85);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
  cursor: pointer;
  font-size: 1.2rem;
  color: #764ba2;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.back-study-close:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.16);
}

.back-study-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.back-study-badge {
  font-size: 3.2rem;
  animation: bounce 2.6s ease-in-out infinite;
}

.back-study-tag {
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(118, 75, 162, 0.12);
  color: #764ba2;
  font-size: 0.92rem;
  font-weight: 600;
  letter-spacing: 0.08em;
}

.back-study-art {
  font-size: clamp(2.6rem, 6vw, 3.6rem);
  font-family: 'ZCOOL KuaiLe', 'Ma Shan Zheng', 'STKaiti', serif;
  background: linear-gradient(120deg, #ff8a9a 0%, #feae65 30%, #84fab0 65%, #8fd3f4 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
  margin-bottom: 12px;
  text-shadow: 0 10px 25px rgba(132, 250, 176, 0.25);
}

.back-study-subtitle {
  text-align: center;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  font-size: 0.85rem;
  color: rgba(118, 75, 162, 0.7);
  margin-bottom: 26px;
}

.back-study-list {
  list-style: none;
  padding: 0;
  margin: 0 0 28px;
  display: grid;
  gap: 12px;
}

.back-study-list li {
  position: relative;
  padding-left: 32px;
  color: rgba(60, 52, 82, 0.9);
  font-size: 1.05rem;
  font-weight: 500;
  line-height: 1.8;
  padding: 12px 12px 12px 32px;
  margin-bottom: 8px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.5), rgba(254, 214, 227, 0.2));
  border-radius: 12px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.back-study-list li:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.8), rgba(254, 214, 227, 0.4));
  transform: translateX(12px);
  border-left-color: rgba(255, 138, 154, 0.8);
  box-shadow: 
    0 6px 20px rgba(255, 138, 154, 0.3),
    0 0 30px rgba(254, 214, 227, 0.2);
}

.back-study-list li::before {
  content: '✦';
  position: absolute;
  left: 0;
  top: 0;
  color: #ff8a9a;
}

.back-study-footer {
  display: flex;
  flex-direction: column;
  gap: 14px;
  align-items: center;
}

.footer-badge {
  padding: 6px 16px;
  border-radius: 999px;
  background: rgba(132, 250, 176, 0.25);
  color: #2c3e50;
  font-weight: 600;
  letter-spacing: 0.08em;
}

.back-study-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 28px;
  padding: 16px 32px;
  font-size: 1.05rem;
  font-weight: 700;
  color: #fff;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  box-shadow: 0 16px 35px rgba(102, 126, 234, 0.35);
}

.back-study-btn:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 20px 45px rgba(118, 75, 162, 0.4);
}

@media (max-width: 520px) {
  .back-study-card {
    padding: 38px 24px 32px;
  }

  .back-study-art {
    font-size: clamp(2.2rem, 10vw, 3rem);
  }

  .back-study-list li {
    font-size: 0.95rem;
  }
}

/* 鼓励语弹窗样式 */
.encourage-popup {
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

.encourage-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 25px;
  padding: 32px;
  text-align: center;
  max-width: 320px;
  width: 72%;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  transform: scale(0.8);
}

.encourage-badge {
  font-size: 4rem;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.encourage-title {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 30px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.encourage-btn {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 25px;
  padding: 15px 30px;
  font-size: 1.1rem;
  font-weight: 600;
  color: #667eea;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.encourage-btn:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

/* 微行动挑战弹窗样式 */
.micro-action-popup {
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

.micro-action-card {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  border-radius: 25px;
  padding: 40px;
  text-align: center;
  max-width: 450px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3), 0 0 32px rgba(254,214,227,0.18);
  border: 2px solid rgba(254,214,227,0.5);
  transform: scale(0);
  animation: popIn 0.5s ease-out forwards;
  position: relative;
}

.micro-action-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.85);
  color: #8b4513;
  font-size: 1.1rem;
  cursor: pointer;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.18);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.micro-action-close:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22);
}

.micro-action-icon {
  font-size: 3.5rem;
  margin-bottom: 20px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.micro-action-title {
  color: #8b4513;
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 15px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.micro-action-desc {
  color: #654321;
  font-size: 1.1rem;
  margin-bottom: 25px;
  line-height: 1.5;
}

.micro-action-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 25px;
  padding: 15px 30px;
  font-size: 1.1rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  margin: 10px;
}

.micro-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.micro-action-timer {
  font-size: 1.8rem;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 25px 0;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.9);
  background-image: linear-gradient(135deg, rgba(254, 214, 227, 0.3), rgba(255, 238, 173, 0.3));
  border-radius: 20px;
  box-shadow: 
    0 6px 20px rgba(0, 0, 0, 0.15),
    inset 0 0 30px rgba(255, 255, 255, 0.5);
  border: 3px solid rgba(254, 214, 227, 0.4);
  animation: timerPulse 2s ease-in-out infinite;
}

@keyframes timerPulse {
  0%, 100% { 
    transform: scale(1);
    box-shadow: 
      0 6px 20px rgba(0, 0, 0, 0.15),
      inset 0 0 30px rgba(255, 255, 255, 0.5);
  }
  50% { 
    transform: scale(1.05);
    box-shadow: 
      0 8px 30px rgba(0, 0, 0, 0.2),
      inset 0 0 40px rgba(255, 255, 255, 0.7),
      0 0 40px rgba(254, 214, 227, 0.4);
  }
}

.badge-animate {
  font-size: 5rem;
  margin-bottom: 20px;
  animation: bounceIn 1s ease-out;
}

@keyframes bounceIn {
  0% { transform: scale(0); opacity: 0; }
  50% { transform: scale(1.2); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes popIn {
  0% {
    opacity: 0;
    transform: scale(0);
  }
  60% {
    opacity: 1;
    transform: scale(1.08);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>

