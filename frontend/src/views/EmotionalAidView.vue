<template>
  <div class="emotional-aid-container">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span>
        返回主界面
      </button>
      <h1>情绪急救</h1>
    </div>
    <p>当您感到压力或情绪低落时，这里提供快速的微干预。</p>

    <div class="aid-options">
      <div class="aid-card" @click="startBreathingExercise">
        <h3>90秒呼吸指导</h3>
        <p>通过深呼吸平静心情。</p>
      </div>
      <div class="aid-card" @click="returnToStudy">
        <h3>返回学习</h3>
        <p>快速回到专注状态。</p>
      </div>
      <div class="aid-card" @click="showMicroReview">
        <h3>微复盘</h3>
        <p>分析情绪来源，找到解决方案。</p>
      </div>
    </div>

    <div v-if="showBreathing" class="breathing-exercise">
      <h2>深呼吸练习</h2>
      <p>吸气... 保持... 呼气...</p>
      <div class="breathing-circle"></div>
      <button @click="stopBreathing">停止</button>
    </div>

    <div v-if="showMicroReviewForm" class="micro-review-form">
      <h2>微复盘</h2>
      <p>是什么导致了您的情绪低落？</p>
      <textarea v-model="cause1" placeholder="原因一"></textarea>
      <textarea v-model="cause2" placeholder="原因二"></textarea>
      <button @click="submitMicroReview">提交复盘</button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'EmotionalAidView',
  setup() {
    const router = useRouter()
    const showBreathing = ref(false)
    const showMicroReviewForm = ref(false)
    const cause1 = ref('')
    const cause2 = ref('')

    const goBack = () => {
      router.push('/dashboard')
    }

    const startBreathingExercise = () => {
      showBreathing.value = true
      showMicroReviewForm.value = false
      // Simulate breathing animation or guide
      alert('开始90秒呼吸指导...')
    }

    const stopBreathing = () => {
      showBreathing.value = false
      alert('呼吸练习结束。')
    }

    const returnToStudy = () => {
      alert('好的，让我们重新投入学习！')
      // Optionally navigate back to Home or FlowTraining
    }

    const showMicroReview = () => {
      showMicroReviewForm.value = true
      showBreathing.value = false
    }

    const submitMicroReview = () => {
      console.log('Micro Review Submitted:', { cause1: cause1.value, cause2: cause2.value })
      alert('复盘已提交。')
      showMicroReviewForm.value = false
      cause1.value = ''
      cause2.value = ''
      // Send data to backend
    }

    return {
      goBack,
      showBreathing,
      showMicroReviewForm,
      cause1,
      cause2,
      startBreathingExercise,
      stopBreathing,
      returnToStudy,
      showMicroReview,
      submitMicroReview
    }
  }
}
</script>

<style scoped>
.emotional-aid-container {
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

.aid-options {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  margin-bottom: 40px;
}

.aid-card {
  background: rgba(255, 255, 255, 0.85);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  padding: 20px;
  margin: 10px;
  width: 250px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.aid-card:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.aid-card h3 {
  color: #007bff;
  margin-bottom: 10px;
}

.aid-card p {
  color: #555;
  font-size: 0.9em;
}

.breathing-exercise {
  background-color: #e8f5e9;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  margin-top: 20px;
}

.breathing-exercise h2 {
  color: #4CAF50;
  margin-bottom: 15px;
}

.breathing-circle {
  width: 100px;
  height: 100px;
  background-color: #81c784;
  border-radius: 50%;
  margin: 20px auto;
  animation: breathe 5s infinite alternate;
}

@keyframes breathe {
  0% { transform: scale(0.8); opacity: 0.6; }
  100% { transform: scale(1.2); opacity: 1; }
}

.micro-review-form {
  background-color: #ffe0b2;
  padding: 30px;
  border-radius: 10px;
  margin-top: 20px;
}

.micro-review-form h2 {
  color: #fb8c00;
  margin-bottom: 15px;
}

.micro-review-form textarea {
  width: calc(100% - 22px);
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ffb74d;
  border-radius: 5px;
  min-height: 80px;
}

button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}

button:hover {
  background-color: #0056b3;
}
</style>

