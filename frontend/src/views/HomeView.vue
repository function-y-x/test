<template>
  <div class="home-container">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span>
        返回主界面
      </button>
      <h1>首页概览</h1>
    </div>
    
    <!-- 概览卡片组 -->
    <div class="overview-cards">
      <div class="card">
        <h3>今日进度</h3>
        <div class="progress-circle">
          <span class="progress-text">{{ completedTasks }}/{{ totalTasks }}</span>
        </div>
      </div>
      <div class="card">
        <h3>学习时长</h3>
        <div class="study-time">
          <span class="time-text">2.5h</span>
          <small>今日累计</small>
        </div>
      </div>
      <div class="card">
        <h3>压力指数</h3>
        <div class="stress-level" :class="stressLevelClass">
          <span class="stress-text">{{ stressScore }}/10</span>
          <small>{{ stressLevelText }}</small>
        </div>
      </div>
    </div>

    <!-- 今日任务 -->
    <div class="section">
      <h2>今日任务</h2>
      <div class="task-list">
        <div v-for="task in dailyTasks" :key="task.id" class="task-item">
          <input type="checkbox" v-model="task.completed" @change="updateProgress" />
          <span :class="{ 'completed': task.completed }">{{ task.name }}</span>
        </div>
      </div>
      <button @click="startFlow" class="flow-button">一键进入心流</button>
    </div>

    <!-- 每日心情打卡 -->
    <div class="section mood-section">
      <h2>每日心情打卡</h2>
      <div class="mood-check-form">
        <div class="mood-input-group">
          <label>压力评分: {{ stressScore }}</label>
          <input type="range" min="1" max="10" v-model="stressScore" @input="updateStressLevel" />
        </div>
        <div class="mood-input-group">
          <input type="text" v-model="moodKeyword" placeholder="情绪关键词 (如：焦虑, 动力十足)" />
        </div>
        <div class="mood-input-group">
          <input type="text" v-model="sourceTag" placeholder="来源标签 (如：英语, 数学, 专业)" />
        </div>
        <button @click="submitDailyMood" class="submit-mood-button">提交打卡</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'HomeView',
  setup() {
    const router = useRouter()
    
    const goBack = () => {
      router.push('/dashboard')
    }
    
    const dailyTasks = ref([
      { id: 1, name: '完成英语阅读理解', completed: false },
      { id: 2, name: '数学真题一套', completed: false },
      { id: 3, name: '专业课知识点复习', completed: false }
    ])

    const stressScore = ref(5)
    const moodKeyword = ref('')
    const sourceTag = ref('')

    const completedTasks = computed(() => {
      return dailyTasks.value.filter(task => task.completed).length
    })

    const totalTasks = computed(() => {
      return dailyTasks.value.length
    })

    const stressLevelClass = computed(() => {
      if (stressScore.value <= 3) return 'low'
      if (stressScore.value <= 6) return 'medium'
      return 'high'
    })

    const stressLevelText = computed(() => {
      if (stressScore.value <= 3) return '低压力'
      if (stressScore.value <= 6) return '中等压力'
      return '高压力'
    })

    const updateProgress = () => {
      // 任务完成状态改变时的逻辑
    }

    const updateStressLevel = () => {
      // 压力评分改变时的逻辑
    }

    const startFlow = () => {
      router.push('/flow-training')
    }

    const submitDailyMood = () => {
      console.log('Daily Mood Submitted:', {
        stressScore: stressScore.value,
        moodKeyword: moodKeyword.value,
        sourceTag: sourceTag.value
      })
      alert('心情打卡成功！')
      // Here you would send this data to the backend
    }

    return {
      goBack,
      dailyTasks,
      stressScore,
      moodKeyword,
      sourceTag,
      completedTasks,
      totalTasks,
      stressLevelClass,
      stressLevelText,
      updateProgress,
      updateStressLevel,
      startFlow,
      submitDailyMood
    }
  }
}
</script>

<style scoped>
.home-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  min-height: 100vh;
  border-radius: 8px;
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  gap: 20px;
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

.page-header h1 {
  color: #2c3e50;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 2em;
  font-weight: 300;
}

/* 概览卡片组 */
.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 24px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.card h3 {
  color: #2c3e50;
  margin: 0 0 16px 0;
  font-size: 1.1em;
  font-weight: 600;
}

.progress-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4CAF50, #45a049);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.progress-text {
  color: white;
  font-weight: bold;
  font-size: 1.1em;
}

.study-time, .stress-level {
  text-align: center;
}

.time-text, .stress-text {
  display: block;
  font-size: 1.8em;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 4px;
}

.stress-level.low .stress-text { color: #4CAF50; }
.stress-level.medium .stress-text { color: #FF9800; }
.stress-level.high .stress-text { color: #f44336; }

.stress-level small {
  color: #666;
  font-size: 0.9em;
}

/* 区块样式 */
.section {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.section h2 {
  color: #2c3e50;
  margin: 0 0 20px 0;
  font-size: 1.4em;
  font-weight: 600;
}

/* 任务列表 */
.task-list {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.task-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 1.1em;
  padding: 8px 0;
}

.task-item:last-child {
  margin-bottom: 0;
}

.task-item input[type="checkbox"] {
  margin-right: 12px;
  transform: scale(1.3);
  accent-color: #4CAF50;
}

.task-item span.completed {
  text-decoration: line-through;
  color: #999;
}

.flow-button {
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  padding: 12px 24px;
  font-size: 1.1em;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.flow-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

/* 心情打卡区域 */
.mood-section {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(15px);
  border: 2px solid rgba(255, 255, 255, 0.4);
}

.mood-check-form {
  display: grid;
  gap: 16px;
}

.mood-input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.mood-input-group label {
  color: #2c3e50;
  font-weight: 600;
  font-size: 1em;
}

.mood-input-group input[type="range"] {
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: #ddd;
  accent-color: #2196F3;
}

.mood-input-group input[type="text"] {
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1em;
  transition: border-color 0.3s ease;
}

.mood-input-group input[type="text"]:focus {
  outline: none;
  border-color: #2196F3;
}

.submit-mood-button {
  background: linear-gradient(135deg, #2196F3, #1976D2);
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: 600;
  transition: all 0.3s ease;
  justify-self: start;
}

.submit-mood-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .overview-cards {
    grid-template-columns: 1fr;
  }
  
  .section {
    padding: 16px;
    margin-bottom: 16px;
  }
}
</style>

