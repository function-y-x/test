<template>
  <div class="error-review-container">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span>
        返回主界面
      </button>
      <h1>错题复盘表</h1>
    </div>
    <p>记录您的错题，AI 将帮助您分析错因并提供复习提醒。</p>

    <div class="error-input-section">
      <h2>添加新错题</h2>
      <textarea v-model="errorDescription" placeholder="输入错题内容或拍照上传..."></textarea>
      <input type="file" @change="handleImageUpload" accept="image/*" />
      <button @click="addError">添加错题</button>
    </div>

    <div class="error-list-section">
      <h2>我的错题</h2>
      <div v-for="error in errors" :key="error.id" class="error-item">
        <p>{{ error.description }}</p>
        <img v-if="error.image" :src="error.image" alt="错题图片" class="error-image" />
        <div class="ai-analysis" v-if="error.analysis">
          <strong>AI 分析:</strong> {{ error.analysis.reason }} ({{ error.analysis.type }})
        </div>
        <button @click="analyzeError(error.id)" :disabled="error.analysis">AI 分析</button>
        <button @click="deleteError(error.id)">删除</button>
      </div>
      <p v-if="errors.length === 0">暂无错题。</p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'ErrorReviewView',
  setup() {
    const router = useRouter()
    const errorDescription = ref('')
    const errorImage = ref(null)
    const errors = ref([])

    const goBack = () => {
      router.push('/dashboard')
    }

    const handleImageUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          errorImage.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }

    const addError = () => {
      if (errorDescription.value || errorImage.value) {
        errors.value.push({
          id: Date.now(),
          description: errorDescription.value,
          image: errorImage.value,
          analysis: null // AI analysis will be added here
        })
        errorDescription.value = ''
        errorImage.value = null
        alert('错题已添加！')
        // Send to backend
      } else {
        alert('请输入错题内容或上传图片。')
      }
    }

    const analyzeError = async (id) => {
      const error = errors.value.find(e => e.id === id)
      if (error) {
        // Simulate AI analysis (replace with actual API call to backend)
        await new Promise(resolve => setTimeout(resolve, 1500))
        const analysisTypes = ['概念不清', '技巧不足', '审题错误', '心态问题']
        const randomType = analysisTypes[Math.floor(Math.random() * analysisTypes.length)]
        error.analysis = {
          type: randomType,
          reason: `AI 认为这道错题的根本原因是：${randomType}。建议您针对性复习相关知识点。`
        }
        alert('AI 分析完成！')
        // Send analysis result to backend
      }
    }

    const deleteError = (id) => {
      errors.value = errors.value.filter(e => e.id !== id)
      alert('错题已删除。')
      // Send delete request to backend
    }

    return {
      goBack,
      errorDescription,
      errorImage,
      errors,
      handleImageUpload,
      addError,
      analyzeError,
      deleteError
    }
  }
}
</script>

<style scoped>
.error-review-container {
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

.error-input-section,
.error-list-section {
  background-color: #e3f2fd;
  padding: 25px;
  border-radius: 10px;
  margin-bottom: 25px;
}

.error-input-section h2,
.error-list-section h2 {
  color: #1976d2;
  margin-bottom: 15px;
}

.error-input-section textarea {
  width: calc(100% - 22px);
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #bbdefb;
  border-radius: 5px;
  min-height: 80px;
}

.error-input-section input[type="file"] {
  margin-bottom: 15px;
}

.error-input-section button {
  background-color: #2196f3;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.error-input-section button:hover {
  background-color: #1976d2;
}

.error-item {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.error-item p {
  margin: 0;
  color: #333;
}

.error-image {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
}

.ai-analysis {
  background-color: #e8f5e9;
  border-left: 4px solid #4CAF50;
  border-radius: 4px;
  font-size: 0.9em;
}

.error-item button {
  background-color: #4CAF50;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-right: 10px;
}

.error-item button:hover {
  background-color: #45a049;
}

.error-item button:last-child {
  background-color: #e74c3c;
}

.error-item button:last-child:hover {
  background-color: #c0392b;
}
</style>

