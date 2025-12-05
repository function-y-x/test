<template>
  <div class="test-container">
    <h1>鼓励语和微行动测试</h1>
    
    <!-- 测试按钮 -->
    <div class="test-buttons">
      <button @click="showTestEncourage">测试鼓励语弹窗</button>
      <button @click="showTestMicroAction">测试微行动弹窗</button>
    </div>

    <!-- 鼓励语弹窗 -->
    <div v-if="showEncourage" class="encourage-popup">
      <div class="encourage-card">
        <div class="encourage-badge">🏅</div>
        <h2 class="encourage-title">{{ encourageText }}</h2>
        <button class="encourage-btn" @click="startMicroAction">接受微行动挑战</button>
        <button class="encourage-btn" @click="closeEncourage">关闭</button>
      </div>
    </div>

    <!-- 微行动挑战弹窗 -->
    <div v-if="showMicroAction" class="micro-action-popup">
      <div class="micro-action-card">
        <div class="micro-action-icon">💡</div>
        <h2 class="micro-action-title">微行动挑战</h2>
        <p class="micro-action-desc">{{ microAction }}</p>
        <div v-if="!microActionStarted">
          <button class="micro-action-btn" @click="beginMicroAction">开始挑战</button>
          <button class="micro-action-btn" @click="closeMicroAction">关闭</button>
        </div>
        <div v-else-if="!microActionCompleted">
          <div class="micro-action-timer">剩余时间：{{ microActionTime }} 秒</div>
          <button class="micro-action-btn" @click="completeMicroAction">完成微行动</button>
        </div>
        <div v-else>
          <div class="badge-animate">🏆</div>
          <h3>恭喜获得徽章！</h3>
          <p>你已成功打破负面循环，欢迎回到学习！</p>
          <button class="micro-action-btn" @click="closeMicroAction">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'TestEmotionalFeatures',
  setup() {
    // 状态
    const showEncourage = ref(false)
    const encourageText = ref('')
    const showMicroAction = ref(false)
    const microAction = ref('')
    const microActionStarted = ref(false)
    const microActionCompleted = ref(false)
    const microActionTime = ref(180)
    let microActionTimer = null

    // 数据
    const encourageList = [
      '你已经很棒了，继续前进！',
      '每一次努力都值得被肯定！',
      '你正在变得更强大！',
      '你的坚持终将带来美好结果！',
      '相信自己，你可以做到！',
      '今天的你已经比昨天更进步！'
    ]

    const microActionList = [
      '整理一下书桌，营造清爽学习环境',
      '喝一杯水，补充能量',
      '做3分钟简单伸展操，舒缓身体',
      '写下一个小目标并立即行动',
      '收拾一下房间的一角',
      '站起来走动一分钟，活动筋骨'
    ]

    // 方法
    const showTestEncourage = () => {
      encourageText.value = encourageList[Math.floor(Math.random() * encourageList.length)]
      showEncourage.value = true
    }

    const closeEncourage = () => {
      showEncourage.value = false
    }

    const showTestMicroAction = () => {
      microAction.value = microActionList[Math.floor(Math.random() * microActionList.length)]
      showMicroAction.value = true
      microActionStarted.value = false
      microActionCompleted.value = false
      microActionTime.value = 10 // 测试用10秒
    }

    const startMicroAction = () => {
      showEncourage.value = false
      showTestMicroAction()
    }

    const beginMicroAction = () => {
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
      if (microActionTimer) clearInterval(microActionTimer)
      microActionStarted.value = false
      microActionCompleted.value = true
    }

    const closeMicroAction = () => {
      if (microActionTimer) clearInterval(microActionTimer)
      showMicroAction.value = false
      microActionStarted.value = false
      microActionCompleted.value = false
    }

    return {
      showEncourage,
      encourageText,
      showMicroAction,
      microAction,
      microActionStarted,
      microActionCompleted,
      microActionTime,
      showTestEncourage,
      closeEncourage,
      showTestMicroAction,
      startMicroAction,
      beginMicroAction,
      completeMicroAction,
      closeMicroAction
    }
  }
}
</script>

<style scoped>
.test-container {
  padding: 20px;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  min-height: 100vh;
}

.test-buttons {
  margin: 20px 0;
}

.test-buttons button {
  background: #667eea;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 10px;
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
  padding: 40px;
  text-align: center;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  transform: scale(0);
  animation: popIn 0.5s ease-out forwards;
}

@keyframes popIn {
  0% { transform: scale(0); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
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
  margin: 5px;
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
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  transform: scale(0);
  animation: popIn 0.5s ease-out forwards;
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
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
  margin: 20px 0;
  padding: 15px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
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
</style>