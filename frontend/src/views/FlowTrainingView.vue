<template>
  <div class="flow-training-container">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span>
        返回主界面
      </button>
      <h1>心流训练</h1>
    </div>
    <p>通过番茄钟计时器、应用白名单和微任务，帮助您进入专注的心流状态。</p>

    <div class="pomodoro-timer">
      <div class="timer-display">{{ formattedTime }}</div>
      <div class="timer-controls">
        <button @click="startTimer" :disabled="isRunning">开始</button>
        <button @click="pauseTimer" :disabled="!isRunning">暂停</button>
        <button @click="resetTimer">重置</button>
      </div>
    </div>

    <div class="app-whitelist">
      <h2>应用白名单</h2>
      <ul>
        <li v-for="app in whitelistApps" :key="app">{{ app }}</li>
      </ul>
      <input type="text" v-model="newApp" placeholder="添加允许学习的应用/网站" />
      <button @click="addAppToWhitelist">添加</button>
    </div>

    <div class="micro-task-gate">
      <h2>两分钟闸门</h2>
      <p>每次开始专注前，完成一个微任务。</p>
      <textarea v-model="microTask" placeholder="例如：划出本章重点、抄写一个定义"></textarea>
      <button @click="completeMicroTask">完成微任务</button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'FlowTrainingView',
  setup() {
    const router = useRouter()
    const timer = ref(25 * 60) // 25 minutes in seconds
    const isRunning = ref(false)
    let interval = null

    const goBack = () => {
      router.push('/dashboard')
    }

    const whitelistApps = ref(['VS Code', 'Google Docs', 'JianShu.com'])
    const newApp = ref('')
    const microTask = ref('')

    const formattedTime = computed(() => {
      const minutes = Math.floor(timer.value / 60)
        .toString()
        .padStart(2, '0')
      const seconds = (timer.value % 60).toString().padStart(2, '0')
      return `${minutes}:${seconds}`
    })

    const startTimer = () => {
      if (!isRunning.value) {
        isRunning.value = true
        interval = setInterval(() => {
          if (timer.value > 0) {
            timer.value--
          } else {
            clearInterval(interval)
            isRunning.value = false
            alert('番茄钟结束！休息一下。')
            // Trigger session review/micro-reward
          }
        }, 1000)
      }
    }

    const pauseTimer = () => {
      clearInterval(interval)
      isRunning.value = false
    }

    const resetTimer = () => {
      clearInterval(interval)
      isRunning.value = false
      timer.value = 25 * 60
    }

    const addAppToWhitelist = () => {
      if (newApp.value && !whitelistApps.value.includes(newApp.value)) {
        whitelistApps.value.push(newApp.value)
        newApp.value = ''
      }
    }

    const completeMicroTask = () => {
      if (microTask.value) {
        alert(`微任务完成: ${microTask.value}！现在可以开始专注了。`)
        microTask.value = ''
        // Log micro-task completion to backend
      } else {
        alert('请先输入一个微任务。')
      }
    }

    onUnmounted(() => {
      clearInterval(interval)
    })

    return {
      goBack,
      timer,
      isRunning,
      formattedTime,
      whitelistApps,
      newApp,
      microTask,
      startTimer,
      pauseTimer,
      resetTimer,
      addAppToWhitelist,
      completeMicroTask
    }
  }
}
</script>

<style scoped>
.flow-training-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  min-height: 100vh;
  border-radius: 8px;
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
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

h1 {
  color: #2c3e50;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

p {
  color: #555;
  margin-bottom: 30px;
}

.pomodoro-timer {
  background-color: #e8f5e9; /* Light green */
  padding: 30px;
  border-radius: 10px;
  margin-bottom: 30px;
  text-align: center;
}

.timer-display {
  font-size: 4em;
  font-weight: bold;
  color: #4CAF50;
  margin-bottom: 20px;
}

.timer-controls button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 0 10px;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

.timer-controls button:hover:not(:disabled) {
  background-color: #45a049;
}

.timer-controls button:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}

.app-whitelist,
.micro-task-gate {
  background-color: #e3f2fd; /* Light blue */
  padding: 25px;
  border-radius: 10px;
  margin-bottom: 25px;
}

.app-whitelist h2,
.micro-task-gate h2 {
  color: #1976d2;
  margin-bottom: 15px;
}

.app-whitelist ul {
  list-style: inside;
  padding: 0;
  margin-bottom: 15px;
}

.app-whitelist li {
  margin-bottom: 5px;
  color: #333;
}

.app-whitelist input,
.micro-task-gate textarea {
  width: calc(100% - 22px);
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #bbdefb;
  border-radius: 5px;
}

.app-whitelist button,
.micro-task-gate button {
  background-color: #2196f3;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.app-whitelist button:hover,
.micro-task-gate button:hover {
  background-color: #1976d2;
}
</style>

