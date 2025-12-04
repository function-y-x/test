<template>
  <div class="mind-painting-container">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span>
        返回主界面
      </button>
      <h1>心灵画语</h1>
    </div>
    <p>通过绘画表达您的情绪，AI 将为您分析。</p>

    <div class="canvas-area">
      <canvas ref="drawingCanvas" @mousedown="startDrawing" @mousemove="draw" @mouseup="stopDrawing" @mouseleave="stopDrawing"></canvas>
      <div class="controls">
        <input type="color" v-model="currentColor" />
        <input type="range" min="1" max="20" v-model="brushSize" />
        <span>画笔大小: {{ brushSize }}</span>
        <button @click="clearCanvas">清空画布</button>
        <button @click="analyzeDrawing">分析绘画</button>
      </div>
    </div>

    <div v-if="analysisResult" class="analysis-result">
      <h2>绘画分析结果</h2>
      <p><strong>压力指数:</strong> {{ analysisResult.stressIndex }}</p>
      <p><strong>情绪雷达:</strong> {{ analysisResult.moodRadar }}</p>
      <p><strong>解释:</strong> {{ analysisResult.explanation }}</p>
      <button @click="generateIntervention">生成心灵镜像/正念绘画脚本</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'MindPaintingView',
  setup() {
    const router = useRouter()
    const drawingCanvas = ref(null)
    let ctx = null
    let isDrawing = false
    const currentColor = ref('#000000')
    const brushSize = ref(5)
    const analysisResult = ref(null)

    onMounted(() => {
      ctx = drawingCanvas.value.getContext('2d')
      resizeCanvas()
      window.addEventListener('resize', resizeCanvas)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', resizeCanvas)
    })

    const resizeCanvas = () => {
      drawingCanvas.value.width = drawingCanvas.value.offsetWidth
      drawingCanvas.value.height = 400 // Fixed height for simplicity
      ctx.lineCap = 'round'
      ctx.lineJoin = 'round'
    }

    const startDrawing = (e) => {
      isDrawing = true
      draw(e)
    }

    const draw = (e) => {
      if (!isDrawing) return
      const rect = drawingCanvas.value.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top

      ctx.lineWidth = brushSize.value
      ctx.strokeStyle = currentColor.value
      ctx.lineTo(x, y)
      ctx.stroke()
      ctx.beginPath()
      ctx.moveTo(x, y)
    }

    const stopDrawing = () => {
      isDrawing = false
      ctx.beginPath()
    }

    const clearCanvas = () => {
      ctx.clearRect(0, 0, drawingCanvas.value.width, drawingCanvas.value.height)
      analysisResult.value = null
    }

    const analyzeDrawing = async () => {
      const imageData = drawingCanvas.value.toDataURL('image/png')
      // In a real application, send imageData to backend for AI analysis
      console.log('Analyzing drawing...', imageData.substring(0, 100) + '...')

      // Simulate AI analysis result
      analysisResult.value = {
        stressIndex: (Math.random() * 0.5 + 0.3).toFixed(2), // 0.3 to 0.8
        moodRadar: '色彩偏冷，笔触略显急促，可能存在一定压力。',
        explanation: '画面中蓝色和灰色调较多，线条不够流畅，反映出您近期可能感到一些焦虑和紧张。'
      }
      alert('绘画分析完成！')
    }

    const goBack = () => {
      router.push('/dashboard')
    }

    const generateIntervention = () => {
      alert('生成心灵镜像或正念绘画脚本... (此功能待后端实现)')
      // In a real application, send analysisResult to backend to generate intervention
    }

    return {
      goBack,
      drawingCanvas,
      currentColor,
      brushSize,
      analysisResult,
      startDrawing,
      draw,
      stopDrawing,
      clearCanvas,
      analyzeDrawing,
      generateIntervention
    }
  }
}
</script>

<style scoped>
.mind-painting-container {
  padding: 20px;
  max-width: 900px;
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

.canvas-area {
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

canvas {
  background-color: white;
  border-bottom: 1px solid #ccc;
  cursor: crosshair;
  width: 100%;
  max-width: 800px; /* Limit canvas width */
}

.controls {
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.controls input[type="color"] {
  width: 40px;
  height: 40px;
  border: none;
  padding: 0;
}

.controls input[type="range"] {
  width: 120px;
}

.controls button {
  background-color: #007bff;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.controls button:hover {
  background-color: #0056b3;
}

.analysis-result {
  background-color: #e8f5e9;
  padding: 20px;
  border-radius: 10px;
  margin-top: 30px;
  text-align: left;
}

.analysis-result h2 {
  color: #4CAF50;
  margin-bottom: 15px;
}

.analysis-result p {
  margin-bottom: 10px;
  color: #333;
}
</style>

