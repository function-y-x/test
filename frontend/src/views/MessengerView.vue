<template>
  <div class="messenger-container">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span>
        返回主界面
      </button>
      <h1>心语信使</h1>
    </div>
    <p>与 AI 研友进行多模态对话，获得情感支持和学习建议。</p>

    <div class="chat-area">
      <div v-for="message in messages" :key="message.id" :class="['chat-bubble', message.sender]">
        <p>{{ message.text }}</p>
        <img v-if="message.image" :src="message.image" alt="attachment" class="chat-image" />
        <audio v-if="message.audio" :src="message.audio" controls class="chat-audio"></audio>
      </div>
    </div>

    <div class="input-area">
      <textarea v-model="inputText" placeholder="输入你的消息..." @keyup.enter="sendMessage"></textarea>
      <input type="file" @change="handleImageUpload" accept="image/*" style="display: none;" ref="imageInput" />
      <button @click="imageInput.click()">上传图片</button>
      <button @click="startVoiceInput" v-if="!isRecording">语音输入</button>
      <button @click="stopVoiceInput" v-if="isRecording">停止录音</button>
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'MessengerView',
  setup() {
    const router = useRouter()
    const messages = ref([
      { id: 1, sender: 'ai', text: '你好，我是你的研心合一AI伴侣，有什么可以帮助你的吗？' }
    ])

    const goBack = () => {
      router.push('/dashboard')
    }
    const inputText = ref('')
    const imageInput = ref(null)
    const isRecording = ref(false)
    let mediaRecorder = null
    let audioChunks = []

    const sendMessage = async () => {
      if (inputText.value.trim() === '') return

      messages.value.push({ id: messages.value.length + 1, sender: 'user', text: inputText.value })
      const userMessage = inputText.value
      inputText.value = ''

      // Simulate AI response
      const aiResponse = await simulateAIResponse(userMessage)
      messages.value.push({ id: messages.value.length + 1, sender: 'ai', text: aiResponse })
    }

    const handleImageUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          messages.value.push({ id: messages.value.length + 1, sender: 'user', image: e.target.result })
          // Send image to backend for AI analysis
          simulateAIResponse('用户上传了图片').then(aiResponse => {
            messages.value.push({ id: messages.value.length + 1, sender: 'ai', text: aiResponse })
          })
        }
        reader.readAsDataURL(file)
      }
    }

    const startVoiceInput = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        mediaRecorder = new MediaRecorder(stream)
        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data)
        }
        mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
          const audioUrl = URL.createObjectURL(audioBlob)
          messages.value.push({ id: messages.value.length + 1, sender: 'user', audio: audioUrl })
          audioChunks = []

          // Send audioBlob to backend for speech-to-text and AI analysis
          simulateAIResponse('用户发送了语音消息').then(aiResponse => {
            messages.value.push({ id: messages.value.length + 1, sender: 'ai', text: aiResponse })
          })
        }
        mediaRecorder.start()
        isRecording.value = true
      } catch (error) {
        console.error('Error accessing microphone:', error)
        alert('无法访问麦克风，请检查权限设置。')
      }
    }

    const stopVoiceInput = () => {
      if (mediaRecorder && isRecording.value) {
        mediaRecorder.stop()
        isRecording.value = false
      }
    }

    const simulateAIResponse = async (userMessage) => {
      // This would be an actual API call to your FastAPI backend
      // For now, a simple simulated response
      await new Promise(resolve => setTimeout(resolve, 1000))
      if (userMessage.includes('压力')) {
        return '感觉有压力是正常的，我们来做个深呼吸练习吧。'
      } else if (userMessage.includes('错题')) {
        return '错题是进步的阶梯！请把错题拍照发给我，我们一起分析。'
      } else if (userMessage.includes('图片')) {
        return '我看到了您分享的图片，有什么想和我聊聊的吗？'
      } else if (userMessage.includes('语音')) {
        return '我听到了您的语音消息，请问有什么具体问题吗？'
      }
      return '我理解您的感受，请告诉我更多细节，我将尽力帮助您。'
    }

    return {
      goBack,
      messages,
      inputText,
      imageInput,
      isRecording,
      sendMessage,
      handleImageUpload,
      startVoiceInput,
      stopVoiceInput
    }
  }
}
</script>

<style scoped>
.messenger-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 40px);
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

.chat-area {
  flex-grow: 1;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  background-color: #f9f9f9;
}

.chat-bubble {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 15px;
  margin-bottom: 10px;
  line-height: 1.5;
}

.chat-bubble.user {
  background-color: #007bff;
  color: white;
  margin-left: auto;
  border-bottom-right-radius: 2px;
}

.chat-bubble.ai {
  background-color: #e2e2e2;
  color: #333;
  margin-right: auto;
  border-bottom-left-radius: 2px;
}

.chat-image {
  max-width: 100%;
  border-radius: 8px;
  margin-top: 10px;
}

.chat-audio {
  width: 100%;
  margin-top: 10px;
}

.input-area {
  display: flex;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.input-area textarea {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: vertical;
  min-height: 40px;
  max-height: 100px;
}

.input-area button {
  background-color: #28a745;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.input-area button:hover {
  background-color: #218838;
}
</style>

