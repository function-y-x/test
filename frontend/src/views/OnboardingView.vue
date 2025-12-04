<template>
  <div class="onboarding-container">
    <h1>欢迎来到研心合一！</h1>
    <p>让我们快速设置您的学习计划。</p>

    <div v-if="step === 1" class="onboarding-step">
      <h2>第一步：设置考试日期</h2>
      <input type="date" v-model="examDate" />
      <button @click="nextStep">下一步</button>
    </div>

    <div v-if="step === 2" class="onboarding-step">
      <h2>第二步：选择重点科目</h2>
      <div class="subject-selection">
        <label><input type="checkbox" value="英语" v-model="selectedSubjects" /> 英语</label>
        <label><input type="checkbox" value="数学" v-model="selectedSubjects" /> 数学</label>
        <label><input type="checkbox" value="专业课" v-model="selectedSubjects" /> 专业课</label>
        <label><input type="checkbox" value="政治" v-model="selectedSubjects" /> 政治</label>
      </div>
      <button @click="nextStep">下一步</button>
    </div>

    <div v-if="step === 3" class="onboarding-step">
      <h2>第三步：选择 AI 伴侣风格</h2>
      <select v-model="aiCompanionStyle">
        <option disabled value="">请选择</option>
        <option>导师型</option>
        <option>研友型</option>
        <option>暖心型</option>
      </select>
      <button @click="finishOnboarding">完成</button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import axios from 'axios'

export default {
  name: 'OnboardingView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const step = ref(1)
    const examDate = ref('')
    const selectedSubjects = ref([])
    const aiCompanionStyle = ref('')

    const nextStep = () => {
      step.value++
    }

    const finishOnboarding = async () => {
      // 发送引导数据到后端
      try {
        const token = localStorage.getItem('token')
        if (token) {
          // 更新用户信息
          // 将日期转换为 UTC 时间的午夜零点，避免时区问题
          let examDateISO = null
          if (examDate.value) {
            examDateISO = new Date(examDate.value + 'T00:00:00Z').toISOString()
          }
          
          const response = await axios.put('/auth/me', {
            exam_date: examDateISO,
            selected_subjects: selectedSubjects.value,
            ai_companion_style: aiCompanionStyle.value
          }, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          })
          
          console.log('用户信息更新成功:', response.data)
          
          // 使用后端返回的最新用户信息更新本地存储
          if (response.data) {
            localStorage.setItem('user', JSON.stringify(response.data))
            // 同时更新store中的用户信息
            authStore.user = response.data
          }
        }
      } catch (error) {
        console.error('更新用户信息失败:', error)
        // 即使失败也继续，不影响用户体验
      }
      
      // 保存引导完成状态
      localStorage.setItem('onboardingCompleted', 'true')
      
      // 如果用户已经登录，跳转到dashboard，否则跳转到home
      const isLoggedIn = localStorage.getItem('token')
      if (isLoggedIn) {
        router.push('/dashboard')
      } else {
        router.push('/home')
      }
    }

    return {
      step,
      examDate,
      selectedSubjects,
      aiCompanionStyle,
      nextStep,
      finishOnboarding
    }
  }
}
</script>

<style scoped>
.onboarding-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #e0f7fa 0%, #bbdefb 100%);
  color: #333;
  font-family: 'Arial', sans-serif;
  padding: 20px;
}

h1 {
  color: #007bff;
  margin-bottom: 15px;
}

p {
  font-size: 1.1em;
  margin-bottom: 30px;
}

.onboarding-step {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.onboarding-step h2 {
  color: #555;
  margin-bottom: 20px;
}

.onboarding-step input[type="date"],
.onboarding-step select {
  width: calc(100% - 22px);
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.subject-selection label {
  display: block;
  margin-bottom: 10px;
  font-size: 1.1em;
}

.onboarding-step button {
  background-color: #28a745;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 1em;
}

.onboarding-step button:hover {
  background-color: #218838;
}
</style>

