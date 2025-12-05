<template>
  <div class="mind-painting-container">
    <!-- 绘画模式选择界面 -->
    <div v-if="showModeSelection" class="mode-selection-container">
      <div class="page-header">
        <button class="back-button" @click="goBack">
          <span class="back-icon">←</span>
          返回主界面
        </button>
        <h1>心灵画语</h1>
      </div>

      <h2 class="mode-selection-title">选择绘画模式</h2>

      <div class="mode-options">
        <!-- 主题绘画模式 -->
        <div class="mode-card" @click="selectPaintingMode('themed')">
          <div class="mode-icon">🎨</div>
          <h3>主题绘画</h3>
          <p class="mode-description">提供与大学生活紧密相关的主题，帮助您聚焦表达特定情绪和想法。</p>
          <div class="mode-examples">
            <p>推荐主题示例：</p>
            <ul>
              <li>• 画下你最近的压力源</li>
              <li>• 描绘你心中的理想宿舍关系</li>
              <li>• 为你的未来涂上颜色</li>
              <li>• 画一幅代表你期末考试心情的画</li>
              <li>• 画出你最喜欢的学习角落</li>
              <li>• 用色彩表达你和朋友的关系</li>
            </ul>
          </div>
        </div>

        <!-- 自由绘画模式 -->
        <div class="mode-card" @click="selectPaintingMode('free')">
          <div class="mode-icon">🌈</div>
          <h3>自由绘画</h3>
          <p class="mode-description">完全自由创作，不受任何主题限制，让您的灵感自然流露，表达当下心境。</p>
          <div class="mode-examples">
            <p>适合场景：</p>
            <ul>
              <li>• 释放内心情绪</li>
              <li>• 自由发挥创造力</li>
              <li>• 冥想后的心灵表达</li>
              <li>• 随意涂鸦放松心情</li>
            </ul>
          </div>
        </div>

        <!-- 房树人测试模式 -->
        <div class="mode-card" @click="selectPaintingMode('htp')">
          <div class="mode-icon">🏠</div>
          <h3>房树人测试 (HTP)</h3>
          <p class="mode-description">将经典绘画心理测验数字化，通过绘制房屋、树木和人物，由AI进行标准化分析。</p>
          <div class="mode-examples">
            <p>测试说明：</p>
            <ul>
              <li>• 请在同一张画布上绘制房子、树和人</li>
              <li>• 按照您内心的想法自由绘制</li>
              <li>• AI将分析图像中的象征元素</li>
              <li>• 提供更专业的心理参考评估</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- 主题选择界面 -->
    <div v-else-if="showThemeSelection" class="theme-selection-container">
      <div class="page-header">
        <button class="back-button" @click="showThemeSelection = false; showModeSelection = true">
          <span class="back-icon">←</span>
          返回模式选择
        </button>
        <h1>心灵画语</h1>
      </div>

      <h2 class="theme-selection-title">选择绘画主题</h2>
      <p class="theme-selection-subtitle">请选择一个主题，帮助您聚焦表达特定的情绪和想法：</p>

      <div class="theme-options">
        <div
          v-for="theme in themeOptions"
          :key="theme.text"
          class="theme-card"
          @click="selectTheme(theme.text)"
        >
          <div class="theme-icon">{{ theme.emoji }}</div>
          <p class="theme-text">{{ theme.text }}</p>
        </div>
      </div>
    </div>

    <!-- 画布列表界面 -->
    <div v-else-if="showCanvasList" class="canvas-list-container">
      <div class="page-header">
        <button class="back-button" @click="showCanvasList = false; showModeSelection = true">
          <span class="back-icon">←</span>
          返回模式选择
        </button>
        <h1>心灵画语</h1>
      </div>

      <div class="canvas-list-header">
        <h2>我的画布</h2>
        <button class="new-canvas-button" @click="createNewCanvas">创建新画布</button>
      </div>

      <div class="canvas-grid" v-if="filteredCanvases.length > 0">
        <div v-for="canvas in filteredCanvases" :key="canvas.id" class="canvas-item">
          <div class="canvas-thumbnail" @click="loadCanvas(canvas.id)">
            <img :src="canvas.thumbnail" alt="画布缩略图" />
            <div class="canvas-name">{{ canvas.name }}</div>
          </div>
          <div class="canvas-actions">
            <button class="rename-button" @click.stop="showRenameDialog(canvas)">重命名</button>
            <button class="delete-button" @click.stop="deleteCanvas(canvas.id)">删除</button>
          </div>
        </div>
      </div>

      <div v-else class="no-canvases">
        <p>您还没有创建任何{{ currentPaintingMode === 'themed' ? '主题画' : currentPaintingMode === 'htp' ? '房树人测试' : '自由创作' }}</p>
        <button class="new-canvas-button" @click="createNewCanvas">创建第一个画布</button>
      </div>
    </div>

    <!-- 绘画界面 -->
    <div v-else class="painting-container">
      <div class="page-header">
        <button class="back-button" @click="showCanvasList = true; stopGuidanceSpeech()">
          <span class="back-icon">←</span>
          返回画布列表
        </button>
        <h1>心灵画语</h1>
        <div class="canvas-info">
          <span class="canvas-name-display">{{ currentCanvasName }}</span>
          <button class="rename-button-small" @click="showRenameDialog({id: currentCanvasId, name: currentCanvasName})">
            {{ isDefaultName ? '命名' : '重命名' }}
          </button>
        </div>
      </div>

      <p>通过绘画表达您的情绪，AI 将为您分析。</p>

      <div class="canvas-area">
        <!-- 画笔工具栏移到画布上方 -->
        <div class="tool-bar">
          <!-- 画笔类型选择 -->
          <div class="tool-section">
            <label>画笔类型:</label>
            <div class="brush-type-buttons">
              <button :class="['brush-button', { active: currentTool === 'brush' && brushType === 'normal' }]" @click="selectTool('brush', 'normal')">普通笔</button>
              <button :class="['brush-button', { active: currentTool === 'brush' && brushType === 'pen' }]" @click="selectTool('brush', 'pen')">钢笔</button>
              <button :class="['brush-button', { active: currentTool === 'brush' && brushType === 'watercolor' }]" @click="selectTool('brush', 'watercolor')">水彩笔</button>
              <button :class="['brush-button', { active: currentTool === 'brush' && brushType === 'pencil' }]" @click="selectTool('brush', 'pencil')">铅笔</button>
            </div>
          </div>

          <!-- 橡皮擦工具 -->
          <div class="tool-section">
            <label>橡皮擦:</label>
            <div class="eraser-buttons">
              <button :class="['eraser-button', { active: currentTool === 'eraser' }]" @click="selectTool('eraser')">橡皮擦</button>
              <select v-model="eraserType" class="eraser-type-select">
                <option value="pixel">擦除像素</option>
                <option value="stroke">擦除整笔</option>
              </select>
            </div>
          </div>

          <!-- 颜色和大小控制 -->
          <div class="tool-section">
            <label>颜色:</label>
            <input type="color" v-model="currentColor" />
          </div>

          <div class="tool-section">
            <label>粗细: {{ brushSize }}</label>
            <input type="range" min="1" max="30" v-model="brushSize" />
          </div>

          <!-- 操作按钮 -->
          <div class="tool-section">
            <button class="action-button" @click="undo" :disabled="history.length === 0">撤回</button>
            <button class="action-button" @click="clearCanvas">清空画布</button>
            <button class="action-button" @click="saveCanvas">保存画布</button>
            <button class="action-button" @click="analyzeDrawing">分析绘画</button>
          </div>
        </div>

        <!-- 画布放在工具栏下方 -->
        <canvas ref="drawingCanvas" @mousedown="startDrawing" @mousemove="draw" @mouseup="stopDrawing" @mouseleave="stopDrawing"></canvas>
      </div>
      
      <!-- 绘画提示区域 -->
      <div v-if="showPaintingPrompt && paintingPrompt" class="painting-prompt">
        {{ paintingPrompt }}
      </div>

      <!-- 操作按钮 - 移动到画布下方，分析报告上方 -->
      <!-- 按钮已移到艺术疗愈小故事之前 -->

      <div v-if="analysisResult" class="analysis-result">
        <h2>研心合一 - 心灵画语分析报告</h2>
        
        <!-- 概览部分 -->
        <div class="analysis-overview">
          <div class="stress-meter">
            <h3>压力水平评估</h3>
            <div class="stress-index-container">
              <div class="stress-index-value" :class="getStressLevelClass(analysisResult.stressLevel)">
                {{ Number(analysisResult.stressIndex).toFixed(1) }}/10.0
              </div>
              <div class="stress-level-label">{{ analysisResult.stressLevel }}</div>
            </div>
          </div>
          
          <div class="painting-info">
            <h3>绘画信息</h3>
            <p><strong>绘画模式:</strong> {{ currentPaintingMode === 'htp' ? '房树人测试' : currentPaintingMode === 'themed' ? '主题绘画' : '自由绘画' }}</p>
            <p><strong>绘画时长:</strong> {{ analysisResult.detailedAnalysis?.paintingTime?.toFixed(1) || 0 }}秒</p>
            <p><strong>提交时间:</strong> {{ getTimeCategoryText(analysisResult.detailedAnalysis?.timeAnalysis?.category) }}</p>
          </div>
        </div>
        
        <!-- 心理画像 -->
        <div class="personality-portrait">
          <h3>个性化心理画像</h3>
          <div class="portrait-content">
            <!-- 只显示内容描述，移除标题 -->
            <div v-if="analysisResult.moodDescription">
              <p>{{ analysisResult.moodDescription }}</p>
            </div>
          </div>
        </div>
        
        <!-- 情绪雷达图 -->
        <div class="mood-radar-section">
          <h3>情绪维度雷达图</h3>
          <div class="mood-radar-chart">
            <div class="radar-container">
              <canvas id="moodRadarChart"></canvas>
            </div>
          </div>
        </div>
        
        <!-- 多维度分析模块 - 优化展示 -->
        <div class="detailed-analysis">
          <h3>多维度分析详情</h3>
          
          <div class="analysis-grid">
            <!-- 色彩情感分析 -->
            <div class="analysis-card card-color">
              <div class="card-header">
                <div class="card-icon">🎨</div>
                <h4>色彩情感分析</h4>
              </div>
              <div class="analysis-content-improved" v-html="formatMarkdownAnalysis(analysisResult.aiAnalysis?.colorAnalysis || generateColorAnalysis(analysisResult.detailedAnalysis?.colorAnalysis))">
              </div>
            </div>
            
            <!-- 笔触动力学分析 -->
            <div class="analysis-card card-brush">
              <div class="card-header">
                <div class="card-icon">✏️</div>
                <h4>笔触动力学分析</h4>
              </div>
              <div class="analysis-content-improved" v-html="formatMarkdownAnalysis(analysisResult.aiAnalysis?.strokeAnalysis || generateBrushAnalysis(analysisResult.detailedAnalysis?.strokeAnalysis))">
              </div>
            </div>
            
            <!-- 构图与空间分析 -->
            <div class="analysis-card card-composition">
              <div class="card-header">
                <div class="card-icon">🖼️</div>
                <h4>构图与空间分析</h4>
              </div>
              <div class="analysis-content-improved" v-html="formatMarkdownAnalysis(analysisResult.aiAnalysis?.compositionAnalysis || generateCompositionAnalysis(analysisResult.detailedAnalysis?.compositionAnalysis))">
              </div>
            </div>
          </div>
          
          <!-- 针对性建议部分 -->
          <div v-if="analysisResult.aiAnalysis?.suggestions" class="suggestions-section">
            <h4>💡 针对性建议</h4>
            <div class="suggestions-content">
              {{ analysisResult.aiAnalysis.suggestions }}
            </div>
          </div>
        </div>
        
        <!-- 操作按钮移到艺术疗愈小故事之前 - 添加明显边框 -->
        <div v-if="analysisResult" class="analysis-actions highlighted-section">
          <button class="action-button" @click="generateIntervention" :disabled="isGeneratingMindMirror">
          生成心灵镜像
          <span v-if="isGeneratingMindMirror">⏳</span>
        </button>
          <button class="action-button" @click="generateAndPlayMindfulnessGuidance" :disabled="isGeneratingGuidance">
            {{ isPlayingGuidance ? '暂停语音引导' : '语音绘画引导' }}
            <span v-if="isPlayingGuidance">⏸️</span>
            <span v-else-if="isGeneratingGuidance">⏳</span>
          </button>
          <button class="action-button" @click="generateHealingStory" :disabled="isGeneratingStory">
            生成疗愈小故事
            <span v-if="isGeneratingStory">⏳</span>
          </button>
          <button class="action-button" @click="goBack">返回主页</button>
        </div>
        
        <!-- 心灵镜像对话框 -->
        <div v-if="showMindMirrorDialog" class="modal-overlay" @click="closeMindMirrorDialog">
          <div class="mind-mirror-modal" @click.stop>
            <div class="modal-header">
              <h3>🌟 心灵镜像</h3>
              <button class="close-button" @click="closeMindMirrorDialog">×</button>
            </div>
            
            <div class="modal-content">
              <div class="mind-mirror-container">
                <!-- 原始画作预览 -->
                <div class="painting-comparison">
                  <div class="painting-item">
                    <h4>原始画作</h4>
                    <div class="painting-preview">
                      <canvas v-if="drawingCanvas.value" ref="originalPaintingPreview" width="300" height="250"></canvas>
                    </div>
                  </div>
                  
                  <div class="arrow-icon">→</div>
                  
                  <!-- 积极版本 -->
                  <div class="painting-item">
                    <h4>积极版本</h4>
                    <div class="painting-preview">
                      <canvas v-if="drawingCanvas.value" ref="positivePaintingPreview" width="300" height="250"></canvas>
                    </div>
                  </div>
                </div>
                
                <!-- 引导语 -->
                <div class="guidance-text">
                  <div class="guidance-icon">💡</div>
                  <p>{{ mindMirrorResult?.guidance_text || '正在生成引导语...' }}</p>
                </div>
                
                <!-- 积极版本描述 -->
                <div class="positive-image-description">
                  {{ mindMirrorResult?.positive_image_description || '正在生成积极版本描述...' }}
                </div>
                
                <!-- 反思问题 -->
                <div class="reflection-section">
                  <h4>🔍 思考一下</h4>
                  <p>观察这两种版本的画面，你觉得情绪上有什么不同的感受？</p>
                  <p>在生活中，你可以如何引入这样的"积极视角"来看待挑战？</p>
                </div>
              </div>
            </div>
            
            <div class="modal-footer">
              <button class="action-button" @click="closeMindMirrorDialog">我明白了</button>
            </div>
          </div>
        </div>
        
        <!-- 疗愈小故事显示区域 -->
        <div v-if="healingStory" class="healing-story-section">
          <h3>📖 艺术疗愈小故事</h3>
          <div class="healing-story-content">
            {{ healingStory }}
          </div>
        </div>
      </div>
    </div>

    <!-- 重命名对话框 -->
    <div v-if="showRenameModal" class="modal-overlay" @click="closeRenameDialog">
      <div class="rename-modal" @click.stop>
        <h3>重命名画布</h3>
        <input type="text" v-model="newCanvasName" @keyup.enter="confirmRename" />
        <div class="modal-buttons">
          <button @click="closeRenameDialog">取消</button>
          <button @click="confirmRename">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import axios from 'axios'

export default {
  name: 'MindPaintingView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const drawingCanvas = ref(null)
    let ctx = null
    let isDrawing = false

    // 绘画工具相关状态
    const currentColor = ref('#000000')
    const brushSize = ref(5)
    const brushType = ref('normal') // 普通笔、钢笔、水彩笔、铅笔
    const currentTool = ref('brush') // brush 或 eraser
    const eraserType = ref('pixel') // pixel 或 stroke
    const analysisResult = ref(null)

    // 历史记录相关
    const history = ref([])
    const MAX_HISTORY = 50

    // 绘画模式相关
    const showModeSelection = ref(true) // 默认显示模式选择页面
    const showThemeSelection = ref(false) // 主题选择页面
    const currentPaintingMode = ref('') // 当前选择的绘画模式
    const themeOptions = ref([
      { text: '画下你最近的压力源', emoji: '⚡' },
      { text: '描绘你心中的理想宿舍关系', emoji: '🏠' },
      { text: '为你的未来涂上颜色', emoji: '🌈' },
      { text: '画一幅代表你期末考试心情的画', emoji: '📝' },
      { text: '画出你最喜欢的学习角落', emoji: '📚' },
      { text: '用色彩表达你和朋友的关系', emoji: '🤝' },
      { text: '描绘你面对挑战时的内心世界', emoji: '⛰️' },
      { text: '画出你想象中毕业后的生活', emoji: '🌟' }
    ])
    const selectedTheme = ref('') // 选择的主题

    // 画布管理相关
    const showCanvasList = ref(false) // 默认不显示画布列表
    const savedCanvases = ref([]) // 所有保存的画布
    const filteredCanvases = ref([]) // 当前模式下的画布
    const currentCanvasId = ref(null)
    const currentCanvasName = ref('')
    const isDefaultName = ref(false)
    const showPaintingPrompt = ref(true) // 是否显示绘画提示
    const paintingPrompt = ref('') // 绘画提示内容

    // 重命名对话框相关
    const showRenameModal = ref(false)
    const canvasToRename = ref(null)
    const newCanvasName = ref('')

    // 选择绘画模式
    const selectPaintingMode = (mode) => {
      currentPaintingMode.value = mode
      showModeSelection.value = false

      // 根据模式设置初始状态
      if (mode === 'themed') {
        // 主题模式下显示主题选择界面
        showThemeSelection.value = true
        selectedTheme.value = ''
      } else {
        // 其他模式直接显示画布列表
        showThemeSelection.value = false
        showCanvasList.value = true
        filterCanvasesByMode()
      }
    }

    // 选择绘画主题
    const selectTheme = (theme) => {
      selectedTheme.value = theme
      showThemeSelection.value = false
      showCanvasList.value = true
      filterCanvasesByMode()
    }

    // 根据当前模式过滤画布列表
    const filterCanvasesByMode = () => {
      if (currentPaintingMode.value === 'themed') {
        // 主题模式下，可以选择是否按特定主题过滤
        // 这里我们只按模式过滤
        filteredCanvases.value = savedCanvases.value.filter(c =>
            c.mode === 'themed'
        )
      } else {
        // 其他模式按模式类型过滤
        filteredCanvases.value = savedCanvases.value.filter(c =>
            c.mode === currentPaintingMode.value
        )
      }
    }

    onMounted(() => {
      // 加载保存的画布列表
      loadSavedCanvases()

      if (drawingCanvas.value) {
        ctx = drawingCanvas.value.getContext('2d')
        resizeCanvas()
        window.addEventListener('resize', resizeCanvas)
      }
    })

    onUnmounted(() => {
      window.removeEventListener('resize', resizeCanvas)
      // 页面离开时自动保存当前画布
      if (!showCanvasList.value && currentCanvasId.value) {
        autoSaveCanvas()
      }
      // 页面离开时停止语音播放
      stopGuidanceSpeech()
    })

    // 初始化画布上下文
    const initCanvasContext = () => {
      if (drawingCanvas.value) {
        // 总是重新获取ctx，确保它是有效的
        ctx = drawingCanvas.value.getContext('2d')
        // 设置默认线条样式
        ctx.lineCap = 'round'
        ctx.lineJoin = 'round'
        resizeCanvas()
      }
    }

    const resizeCanvas = () => {
      if (!drawingCanvas.value || !ctx) return

      const width = drawingCanvas.value.offsetWidth
      const height = 600 // 增大画布高度

      // 保存当前画布内容
      const imageData = ctx.getImageData(0, 0, drawingCanvas.value.width, drawingCanvas.value.height)

      // 调整画布大小
      drawingCanvas.value.width = width
      drawingCanvas.value.height = height

      // 恢复画布内容
      ctx.putImageData(imageData, 0, 0)

      // 设置默认线条样式
      ctx.lineCap = 'round'
      ctx.lineJoin = 'round'
    }

    // 选择工具
    const selectTool = (tool, type = null) => {
      currentTool.value = tool
      if (type) {
        brushType.value = type

        // 优化1：选择铅笔时，锁定颜色为铅笔的浅灰色
        if (type === 'pencil') {
          currentColor.value = '#AAAAAA' // 铅笔浅灰色
        }
      }

      // 根据工具类型更改鼠标样式
      if (drawingCanvas.value) {
        if (tool === 'eraser') {
          drawingCanvas.value.style.cursor = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='${brushSize.value + 10}' height='${brushSize.value + 10}' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='1' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='3' width='18' height='18' rx='2' ry='2'%3E%3C/rect%3E%3C/svg%3E") ${brushSize.value / 2 + 5} ${brushSize.value / 2 + 5}, crosshair`
        } else {
          // 根据不同画笔类型设置不同的鼠标光标颜色
          let cursorColor = '%23000000'
          if (brushType.value === 'pencil') {
            cursorColor = '%23AAAAAA' // 铅笔光标使用浅灰色
          }
          drawingCanvas.value.style.cursor = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='${brushSize.value + 2}' height='${brushSize.value + 2}' viewBox='0 0 24 24' fill='${cursorColor}' stroke='none'%3E%3Ccircle cx='12' cy='12' r='${brushSize.value / 2}'%3E%3C/circle%3E%3C/svg%3E") ${brushSize.value / 2 + 1} ${brushSize.value / 2 + 1}, crosshair`
        }
      }
    }

    // 保存当前画布状态到历史记录
    const saveState = () => {
      if (!ctx || !drawingCanvas.value) return

      try {
        const imageData = ctx.getImageData(0, 0, drawingCanvas.value.width, drawingCanvas.value.height)
        history.value.push(imageData)

        // 限制历史记录数量
        if (history.value.length > MAX_HISTORY) {
          history.value.shift() // 删除最旧的记录
        }
      } catch (error) {
        console.error('保存历史记录失败:', error)
      }
    }

    // 撤回操作
    const undo = () => {
      if (history.value.length === 0 || !ctx || !drawingCanvas.value) return

      const lastState = history.value.pop()
      try {
        ctx.putImageData(lastState, 0, 0)
      } catch (error) {
        console.error('恢复历史记录失败:', error)
      }
    }

    // 当前正在绘制的路径
    const currentPath = ref([])
    
    // 绘画时间相关
    const drawingStartTime = ref(null)
    const totalDrawingTime = ref(0)
    const lastDrawTime = ref(null)
    const pathCount = ref(0)
    const strokeStats = ref({
      totalLength: 0,
      averageLength: 0,
      jitterCount: 0,
      overlapCount: 0,
      discontinuityCount: 0
    })

    // 计算两点之间的距离
    const calculateDistance = (point1, point2) => {
      const dx = point2.x - point1.x
      const dy = point2.y - point1.y
      return Math.sqrt(dx * dx + dy * dy)
    }
    
    // 计算三点之间的角度变化（用于检测抖动）
    const calculateJitter = (point1, point2, point3) => {
      const dx1 = point2.x - point1.x
      const dy1 = point2.y - point1.y
      const dx2 = point3.x - point2.x
      const dy2 = point3.y - point2.y
      
      const angle1 = Math.atan2(dy1, dx1)
      const angle2 = Math.atan2(dy2, dx2)
      
      const angleDiff = Math.abs(angle1 - angle2)
      return angleDiff > Math.PI / 3 // 如果角度变化超过60度，认为是抖动
    }

    const startDrawing = (e) => {
      // 确保ctx存在，如果不存在则初始化
      if (!ctx) {
        initCanvasContext()
        // 如果仍然没有ctx，说明初始化失败，不继续执行
        if (!ctx) return
      }

      isDrawing = true

      // 记录绘画开始时间（如果是首次开始）
      if (!drawingStartTime.value) {
        drawingStartTime.value = Date.now()
      }
      lastDrawTime.value = Date.now()

      // 开始新笔画前保存当前状态
      saveState()

      // 初始化当前笔画的点集合
      currentPath.value = []

      // 确保ctx有效后再执行绘制
      if (ctx) {
        draw(e)
      }
    }

    const draw = (e) => {
      if (!isDrawing || !ctx || !drawingCanvas.value) return

      const rect = drawingCanvas.value.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top

      // 记录当前点
      currentPath.value.push({x, y, time: Date.now()})

      ctx.lineWidth = brushSize.value

      if (currentTool.value === 'eraser') {
        // 橡皮擦模式
        ctx.globalCompositeOperation = 'destination-out'
        ctx.strokeStyle = 'rgba(0,0,0,1)'

        // 设置橡皮擦的样式
        ctx.lineCap = 'round'
        ctx.lineJoin = 'round'
      } else {
        // 画笔模式，根据不同画笔类型设置不同样式
        ctx.globalCompositeOperation = 'source-over'
        ctx.strokeStyle = currentColor.value

        // 根据画笔类型设置不同的样式
        switch (brushType.value) {
          case 'normal':
            ctx.lineCap = 'round'
            ctx.lineJoin = 'round'
            ctx.globalAlpha = 1
            break
          case 'pen':
            // 优化钢笔笔触，使其更接近真实写字效果
            ctx.lineCap = 'round'
            ctx.lineJoin = 'round'
            ctx.globalAlpha = 0.9
            // 模拟钢笔的压感效果，根据速度调整线条粗细
            if (currentPath.value.length > 1) {
              const prevPoint = currentPath.value[currentPath.value.length - 2]
              const distance = Math.sqrt(
                  Math.pow(x - prevPoint.x, 2) + Math.pow(y - prevPoint.y, 2)
              )
              // 根据移动速度调整线条粗细，速度越快线条越细
              const dynamicWidth = Math.max(0.5, brushSize.value * (1 - Math.min(distance / 20, 0.7)))
              ctx.lineWidth = dynamicWidth
            }
            break
          case 'watercolor':
            // 降低水彩笔透明度，使其更加透明
            ctx.lineCap = 'round'
            ctx.lineJoin = 'round'
            ctx.globalAlpha = 0.2 // 进一步降低透明度
            ctx.shadowBlur = 8 // 增加模糊效果使颜色过渡更自然
            ctx.shadowColor = currentColor.value
            // 模拟水彩的扩散效果
            ctx.shadowOffsetX = 0
            ctx.shadowOffsetY = 0
            break
          case 'pencil':
            ctx.lineCap = 'round' // 改为round以避免方块效果
            ctx.lineJoin = 'round' // 改为round以避免方块效果
            ctx.globalAlpha = 0.8
            // 铅笔效果添加不规则性，模拟真实铅笔效果
            if (currentPath.value.length > 1) {
              // 添加一些随机的不规律性
              ctx.lineWidth = brushSize.value * (0.9 + Math.random() * 0.2)
            }
            break
        }
      }

      // 改进的绘画逻辑，解决快速绘制时出现圆点或方块的问题
      if (currentPath.value.length === 1) {
        ctx.beginPath()
        ctx.moveTo(x, y)
        // 对于第一个点，也绘制一个小圆点，避免快速点击时看不到
        ctx.arc(x, y, ctx.lineWidth / 2, 0, Math.PI * 2)
        ctx.fillStyle = ctx.strokeStyle
        ctx.fill()
      } else {
        const prevPoint = currentPath.value[currentPath.value.length - 2]
        const distance = Math.sqrt(
            Math.pow(x - prevPoint.x, 2) + Math.pow(y - prevPoint.y, 2)
        )

        // 如果两点之间距离过大，使用贝塞尔曲线平滑连接，避免跳点形成方块
        if (distance > ctx.lineWidth * 2) {
          const controlX = (prevPoint.x + x) / 2
          const controlY = (prevPoint.y + y) / 2
          ctx.beginPath()
          ctx.moveTo(prevPoint.x, prevPoint.y)
          ctx.quadraticCurveTo(controlX, controlY, x, y)
          ctx.stroke()
        } else {
          ctx.beginPath()
          ctx.moveTo(prevPoint.x, prevPoint.y)
          ctx.lineTo(x, y)
          ctx.stroke()
        }
      }

      // 重置水彩效果的阴影，避免影响后续绘制
      if (brushType.value === 'watercolor') {
        ctx.shadowBlur = 0
      }
    }

    const stopDrawing = () => {
      isDrawing = false
      if (ctx) {
        ctx.beginPath()
      }

      // 更新总绘画时间
      if (lastDrawTime.value) {
        totalDrawingTime.value += Date.now() - lastDrawTime.value
      }

      // 如果是擦除整笔模式，可以在这里处理
      if (currentTool.value === 'eraser' && eraserType.value === 'stroke' && currentPath.value.length > 0) {
        // 这里可以实现整笔画擦除的逻辑
        // 简单做法是重新绘制整个画布，跳过当前路径
        return
      }

      if (currentPath.value.length > 0) {
        // 分析当前路径的特征
        const pathLength = currentPath.value.length
        let totalSegmentLength = 0
        let jitterDetected = 0
        let discontinuityCount = 0
        
        for (let i = 1; i < pathLength; i++) {
          const distance = calculateDistance(currentPath.value[i-1], currentPath.value[i])
          totalSegmentLength += distance
          
          // 检测不连续性（过大的距离）
          if (distance > 20) {
            discontinuityCount++
          }
          
          // 检测抖动（角度变化大的点）
          if (i > 1 && calculateJitter(currentPath.value[i-2], currentPath.value[i-1], currentPath.value[i])) {
            jitterDetected++
          }
        }
        
        // 更新笔触统计
        strokeStats.value.totalLength += totalSegmentLength
        strokeStats.value.jitterCount += jitterDetected
        strokeStats.value.discontinuityCount += discontinuityCount
        strokeStats.value.averageLength = strokeStats.value.totalLength / (pathCount.value + 1)
        
        // 检测是否有涂改痕迹（通过速度变化判断）
        let hasOverlap = false
        if (pathLength > 5) {
          // 简化的重叠检测
          for (let i = 5; i < pathLength; i++) {
            for (let j = 0; j < i - 5; j++) {
              if (calculateDistance(currentPath.value[i], currentPath.value[j]) < 10) {
                hasOverlap = true
                strokeStats.value.overlapCount++
                break
              }
            }
            if (hasOverlap) break
          }
        }
        
        pathCount.value++
      }
    }

    const clearCanvas = () => {
      if (!ctx || !drawingCanvas.value) {
        initCanvasContext()
        if (!ctx) return
      }

      if (confirm('确定要清空画布吗？')) {
        // 清空前保存状态以便可以撤销
        saveState()
        ctx.clearRect(0, 0, drawingCanvas.value.width, drawingCanvas.value.height)
        analysisResult.value = null
      }
    }

    // 生成默认画布名称
    const generateDefaultCanvasName = () => {
      const now = new Date()
      const dateStr = `${now.getFullYear()}/${String(now.getMonth() + 1).padStart(2, '0')}/${String(now.getDate()).padStart(2, '0')}`

      // 计算今天的流水号
      const todayCanvases = savedCanvases.value.filter(c => c.name.startsWith(dateStr))
      const serialNumber = todayCanvases.length + 1

      return `${dateStr}-${serialNumber}`
    }

    // 创建新画布
    const createNewCanvas = () => {
      // 自动保存当前画布
      if (!showCanvasList.value && currentCanvasId.value && ctx && drawingCanvas.value) {
        autoSaveCanvas()
      }

      // 生成新的画布ID和名称
      currentCanvasId.value = Date.now().toString()
      let defaultName = generateDefaultCanvasName()

      // 根据当前模式定制画布名称
      if (currentPaintingMode.value === 'themed' && selectedTheme.value) {
        defaultName = `主题画 - ${selectedTheme.value.substring(0, 10)}...`
      } else if (currentPaintingMode.value === 'htp') {
        defaultName = `房树人测试 - ${new Date().toLocaleDateString()}`
      } else if (currentPaintingMode.value === 'free') {
        defaultName = `自由创作 - ${new Date().toLocaleTimeString()}`
      }

      currentCanvasName.value = defaultName
      isDefaultName.value = true

      // 显示绘画界面
      showCanvasList.value = false
      
      // 设置绘画提示
      showPaintingPrompt.value = true
      if (currentPaintingMode.value === 'themed' && selectedTheme.value) {
        paintingPrompt.value = `您已选择主题绘画，请您根据【${selectedTheme.value}】主题进行绘画：请自由地表达您对这个主题的感受和想法，不要担心绘画技巧，重要的是表达内心的真实情感。`
      } else if (currentPaintingMode.value === 'free') {
        paintingPrompt.value = `您已选择自由绘画，请随意发挥，放松心情：这里没有任何限制，您可以画任何想画的内容，让您的思绪自由流动，用色彩和线条表达此刻的心情。`
      } else if (currentPaintingMode.value === 'htp') {
        paintingPrompt.value = `您已选择房树人测试：请在同一张画布上绘制房子、树木和人物。这个经典的心理测验可以帮助我们了解您的内心世界。请按照您内心的想法自由绘制，不需要特别技巧。`
      }

      // 确保canvas和ctx已初始化后再清空画布
      setTimeout(() => {
        // 初始化画布上下文
        initCanvasContext()

        if (ctx && drawingCanvas.value) {
          ctx.clearRect(0, 0, drawingCanvas.value.width, drawingCanvas.value.height)
        }

        // 重置状态
        history.value = []
        analysisResult.value = null

        // 重置默认工具配置
        currentColor.value = '#000000' // 默认颜色：黑色
        brushSize.value = 5 // 默认粗细：5
        brushType.value = 'normal' // 默认画笔类型：普通笔
        currentTool.value = 'brush' // 默认工具：画笔
        selectTool('brush', 'normal')
      }, 200) // 增加延迟时间，确保DOM完全渲染
    }

    // 保存画布
    const saveCanvas = () => {
      if (!currentCanvasId.value) return

      // 获取画布数据URL
      const imageData = drawingCanvas.value.toDataURL('image/png')

      // 创建缩略图（这里简化处理，直接使用原图作为缩略图）
      const thumbnail = imageData

      // 查找是否已存在该画布
      const existingIndex = savedCanvases.value.findIndex(c => c.id === currentCanvasId.value)

      const canvasData = {
        id: currentCanvasId.value,
        name: currentCanvasName.value,
        data: imageData,
        thumbnail: thumbnail,
        lastModified: new Date().toISOString(),
        mode: currentPaintingMode.value, // 保存当前绘画模式
        theme: selectedTheme.value // 保存选择的主题（如果有）
      }

      if (existingIndex >= 0) {
        // 更新现有画布
        savedCanvases.value[existingIndex] = canvasData
      } else {
        // 添加新画布
        savedCanvases.value.push(canvasData)
        // 如果当前显示画布列表，更新过滤后的列表
        if (showCanvasList.value) {
          filterCanvasesByMode()
        }
      }

      // 保存到localStorage
      localStorage.setItem('mindPaintingCanvases', JSON.stringify(savedCanvases.value))

      alert('画布保存成功！')
    }

    // 自动保存画布
    const autoSaveCanvas = () => {
      if (!currentCanvasId.value || !drawingCanvas.value) return

      // 获取画布数据URL
      const imageData = drawingCanvas.value.toDataURL('image/png')

      // 创建缩略图
      const thumbnail = imageData

      // 查找是否已存在该画布
      const existingIndex = savedCanvases.value.findIndex(c => c.id === currentCanvasId.value)

      const canvasData = {
        id: currentCanvasId.value,
        name: currentCanvasName.value,
        data: imageData,
        thumbnail: thumbnail,
        lastModified: new Date().toISOString(),
        mode: currentPaintingMode.value, // 保存当前绘画模式
        theme: selectedTheme.value // 保存选择的主题（如果有）
      }

      if (existingIndex >= 0) {
        // 更新现有画布
        savedCanvases.value[existingIndex] = canvasData
      } else {
        // 添加新画布
        savedCanvases.value.push(canvasData)
        // 如果当前显示画布列表，更新过滤后的列表
        if (showCanvasList.value) {
          filterCanvasesByMode()
        }
      }

      // 保存到localStorage
      localStorage.setItem('mindPaintingCanvases', JSON.stringify(savedCanvases.value))
    }

    // 加载保存的画布列表
    const loadSavedCanvases = () => {
      const saved = localStorage.getItem('mindPaintingCanvases')
      if (saved) {
        try {
          const allCanvases = JSON.parse(saved)
          // 为旧版本画布添加mode字段（如果没有）
          savedCanvases.value = allCanvases.map(canvas => ({
            ...canvas,
            mode: canvas.mode || 'free' // 默认为自由模式
          }))

          // 如果当前显示画布列表，则应用过滤
          if (showCanvasList.value) {
            filterCanvasesByMode()
          }
        } catch (e) {
          console.error('加载保存的画布失败:', e)
          savedCanvases.value = []
          filteredCanvases.value = []
        }
      }
    }

    // 加载指定画布
    const loadCanvas = (canvasId) => {
      // 自动保存当前画布
      if (!showCanvasList.value && currentCanvasId.value && currentCanvasId.value !== canvasId) {
        autoSaveCanvas()
      }

      // 查找要加载的画布
      const canvasToLoad = savedCanvases.value.find(c => c.id === canvasId)
      if (!canvasToLoad) return

      // 设置当前画布信息
      currentCanvasId.value = canvasToLoad.id
      currentCanvasName.value = canvasToLoad.name
      isDefaultName.value = currentCanvasName.value.startsWith(`${new Date().getFullYear()}/`)

      // 显示绘画界面
      showCanvasList.value = false
      
      // 设置绘画提示
      showPaintingPrompt.value = true
      if (canvasToLoad.mode === 'themed' && canvasToLoad.theme) {
        paintingPrompt.value = `您已选择主题绘画，请您根据【${canvasToLoad.theme}】主题进行绘画：请自由地表达您对这个主题的感受和想法，不要担心绘画技巧，重要的是表达内心的真实情感。`
      } else if (canvasToLoad.mode === 'free') {
        paintingPrompt.value = `您已选择自由绘画，请随意发挥，放松心情：这里没有任何限制，您可以画任何想画的内容，让您的思绪自由流动，用色彩和线条表达此刻的心情。`
      } else if (canvasToLoad.mode === 'htp') {
        paintingPrompt.value = `您已选择房树人测试：请在同一张画布上绘制房子、树木和人物。这个经典的心理测验可以帮助我们了解您的内心世界。请按照您内心的想法自由绘制，不需要特别技巧。`
      }

      // 确保canvas和ctx已初始化后再加载画布数据
      setTimeout(() => {
        // 初始化画布上下文
        initCanvasContext()

        // 创建图像对象来加载画布数据
        const img = new Image()
        img.onload = () => {
          if (ctx && drawingCanvas.value) {
            // 清空画布
            ctx.clearRect(0, 0, drawingCanvas.value.width, drawingCanvas.value.height)
            // 绘制加载的图像
            ctx.drawImage(img, 0, 0, drawingCanvas.value.width, drawingCanvas.value.height)
          }
          // 重置历史记录
          history.value = []
          analysisResult.value = null
        }
        img.src = canvasToLoad.data
      }, 100)
    }

    // 删除画布
    const deleteCanvas = (canvasId) => {
      if (confirm('确定要删除这个画布吗？此操作不可恢复。')) {
        savedCanvases.value = savedCanvases.value.filter(c => c.id !== canvasId)
        // 保存到localStorage
        localStorage.setItem('mindPaintingCanvases', JSON.stringify(savedCanvases.value))
      }
    }

    // 显示重命名对话框
    const showRenameDialog = (canvas) => {
      canvasToRename.value = canvas
      newCanvasName.value = canvas.name
      showRenameModal.value = true
    }

    // 关闭重命名对话框
    const closeRenameDialog = () => {
      showRenameModal.value = false
      canvasToRename.value = null
      newCanvasName.value = ''
    }

    // 确认重命名
    const confirmRename = () => {
      if (!canvasToRename.value || !newCanvasName.value.trim()) {
        alert('请输入画布名称')
        return
      }

      // 更新画布名称
      const canvasIndex = savedCanvases.value.findIndex(c => c.id === canvasToRename.value.id)
      if (canvasIndex >= 0) {
        savedCanvases.value[canvasIndex].name = newCanvasName.value.trim()

        // 如果是当前正在编辑的画布，也更新当前名称
        if (currentCanvasId.value === canvasToRename.value.id) {
          currentCanvasName.value = newCanvasName.value.trim()
          isDefaultName.value = false
        }

        // 保存到localStorage
        localStorage.setItem('mindPaintingCanvases', JSON.stringify(savedCanvases.value))

        // 关闭对话框
        closeRenameDialog()
      }
    }



    // RGB转HSV颜色空间
    const rgbToHsv = (r, g, b) => {
      r /= 255, g /= 255, b /= 255;
      
      const max = Math.max(r, g, b);
      const min = Math.min(r, g, b);
      let h = 0, s, v = max;
      
      const d = max - min;
      s = max === 0 ? 0 : d / max;
      
      if (max !== min) {
        switch (max) {
          case r: h = (g - b) / d + (g < b ? 6 : 0); break;
          case g: h = (b - r) / d + 2; break;
          case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
      }
      
      return { h: h * 360, s: s, v: v };
    }
    
    // 分析色彩特征
    const analyzeColors = (imageData) => {
      const data = imageData.data;
      const pixelCount = data.length / 4;
      
      let warmColorCount = 0;
      let coolColorCount = 0;
      let highSaturationCount = 0;
      let lowValueCount = 0;
      
      // 色彩直方图
      const colorHistogram = {};
      
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];
        const a = data[i + 3];
        
        // 跳过透明像素
        if (a === 0) continue;
        
        const hsv = rgbToHsv(r, g, b);
        
        // 冷色调 vs 暖色调 (简化判断)
        if ((hsv.h >= 0 && hsv.h <= 60) || (hsv.h >= 300 && hsv.h <= 360)) {
          warmColorCount++;
        } else if (hsv.h >= 180 && hsv.h <= 240) {
          coolColorCount++;
        }
        
        // 饱和度分析
        if (hsv.s > 0.7) highSaturationCount++;
        
        // 明度分析
        if (hsv.v < 0.3) lowValueCount++;
        
        // 简化的颜色分类统计
        const colorKey = `${Math.floor(r/50)}_${Math.floor(g/50)}_${Math.floor(b/50)}`;
        colorHistogram[colorKey] = (colorHistogram[colorKey] || 0) + 1;
      }
      
      return {
        warmToCoolRatio: coolColorCount > 0 ? warmColorCount / coolColorCount : warmColorCount,
        highSaturationRatio: highSaturationCount / pixelCount,
        lowValueRatio: lowValueCount / pixelCount,
        colorDiversity: Object.keys(colorHistogram).length
      };
    }
    
    // 分析构图和空间特征
    const analyzeComposition = (imageData, canvas) => {
      const data = imageData.data;
      const width = canvas.width;
      const height = canvas.height;
      
      let pixelCount = 0;
      let xSum = 0;
      let ySum = 0;
      let topPixels = 0;
      let bottomPixels = 0;
      let leftPixels = 0;
      let rightPixels = 0;
      
      // 计算重心和空间分布
      for (let i = 0; i < data.length; i += 4) {
        const a = data[i + 3];
        if (a > 0) { // 非透明像素
          const pixelIndex = i / 4;
          const x = pixelIndex % width;
          const y = Math.floor(pixelIndex / width);
          
          xSum += x;
          ySum += y;
          pixelCount++;
          
          // 计算空间分布
          if (y < height * 0.3) topPixels++;
          if (y > height * 0.7) bottomPixels++;
          if (x < width * 0.3) leftPixels++;
          if (x > width * 0.7) rightPixels++;
        }
      }
      
      const centerX = pixelCount > 0 ? xSum / pixelCount : width / 2;
      const centerY = pixelCount > 0 ? ySum / pixelCount : height / 2;
      
      // 计算画面密度
      const totalPixels = width * height;
      const density = pixelCount / totalPixels;
      
      return {
        center: { x: centerX, y: centerY },
        verticalBalance: bottomPixels > 0 ? topPixels / bottomPixels : topPixels,
        horizontalBalance: rightPixels > 0 ? leftPixels / rightPixels : leftPixels,
        density: density,
        isTopHeavy: centerY < height * 0.4,
        isBottomHeavy: centerY > height * 0.6,
        isLeftHeavy: centerX < width * 0.4,
        isRightHeavy: centerX > width * 0.6
      };
    }
    
    // 分析提交时间
    const analyzeSubmissionTime = () => {
      const now = new Date();
      const hour = now.getHours();
      
      let timeCategory = 'normal';
      if (hour >= 22 || hour < 6) {
        timeCategory = 'late_night';
      } else if (hour >= 6 && hour < 9) {
        timeCategory = 'morning';
      } else if (hour >= 12 && hour < 14) {
        timeCategory = 'noon';
      } else if (hour >= 18 && hour < 22) {
        timeCategory = 'evening';
      }
      
      return {
        hour: hour,
        timeCategory: timeCategory,
        isLateNight: timeCategory === 'late_night',
        dayOfWeek: now.getDay()
      };
    }
    
    // 生成压力指数
    const calculateStressIndex = (colorAnalysis, strokeAnalysis, composition, timeAnalysis) => {
      let stressScore = 0;
      
      // 色彩因素 (低明度、低饱和度、冷色调可能代表压力)
      stressScore += colorAnalysis.lowValueRatio * 20;
      stressScore += colorAnalysis.highSaturationRatio * 10; // 过高的饱和度也可能代表情绪波动
      
      // 笔触因素 (抖动、不连续、涂改痕迹可能代表焦虑)
      stressScore += (strokeAnalysis.jitterCount / (pathCount.value || 1)) * 25;
      stressScore += (strokeAnalysis.discontinuityCount / (pathCount.value || 1)) * 15;
      stressScore += (strokeAnalysis.overlapCount / (pathCount.value || 1)) * 20;
      
      // 构图因素 (不平衡、过密可能代表压力)
      if (composition.isTopHeavy || composition.isBottomHeavy || 
          composition.isLeftHeavy || composition.isRightHeavy) {
        stressScore += 10;
      }
      if (composition.density > 0.8) stressScore += 15; // 过满
      if (composition.density < 0.1) stressScore += 5;  // 过空
      
      // 时间因素 (深夜作画可能代表压力)
      if (timeAnalysis.isLateNight) stressScore += 10;
      
      // 时间因素 (绘画时间过长或过短)
      const totalMinutes = totalDrawingTime.value / 1000 / 60;
      if (totalMinutes > 30) stressScore += 10; // 耗时过长可能代表犹豫
      if (totalMinutes < 1) stressScore += 5;   // 过快可能代表敷衍
      
      // 限制在0-100范围内
      stressScore = Math.min(100, Math.max(0, stressScore));
      
      // 转换为0-10的指数
      const stressIndex = (stressScore / 10).toFixed(1);
      
      let stressLevel = '轻度';
      if (stressScore > 60) stressLevel = '高度';
      else if (stressScore > 30) stressLevel = '中度';
      
      return { score: stressScore, index: stressIndex, level: stressLevel };
    }
    
    // 生成情绪雷达图数据
    const generateMoodRadar = (colorAnalysis, strokeAnalysis, composition) => {
      // 基于各种分析维度生成情绪数据
      const happy = 50 - (colorAnalysis.lowValueRatio * 40) + (colorAnalysis.highSaturationRatio * 30);
      const sad = 30 + (colorAnalysis.lowValueRatio * 50) - (colorAnalysis.warmToCoolRatio * 20);
      const anxious = 20 + (strokeAnalysis.jitterCount / (pathCount.value || 1) * 50) + 
                     (strokeAnalysis.discontinuityCount / (pathCount.value || 1) * 30);
      const calm = 40 - (strokeAnalysis.jitterCount / (pathCount.value || 1) * 30) - 
                   (composition.density * 20);
      const angry = 10 + (strokeAnalysis.overlapCount / (pathCount.value || 1) * 40) - 
                    (colorAnalysis.warmToCoolRatio * 10);
      const creative = 30 + (colorAnalysis.colorDiversity / 20) + (strokeAnalysis.averageLength / 100);
      
      // 归一化到0-100范围
      const normalize = (value) => Math.min(100, Math.max(0, Math.round(value)));
      
      return {
        happy: normalize(happy),
        sad: normalize(sad),
        anxious: normalize(anxious),
        calm: normalize(calm),
        angry: normalize(angry),
        creative: normalize(creative)
      };
    }
    
    // 生成个性化心理画像
    const generatePersonalityPortrait = (colorAnalysis, strokeAnalysis, composition, timeAnalysis, stressInfo) => {
      let portrait = [];
      
      // 基于色彩分析
      if (colorAnalysis.warmToCoolRatio > 1.5) {
        portrait.push('您的画作充满了温暖的色调，显示出您当前情感状态较为积极和热情。');
      } else if (colorAnalysis.warmToCoolRatio < 0.5) {
        portrait.push('您使用了较多的冷色调，这可能反映出您当前比较冷静或是有些内敛的情绪。');
      }
      
      if (colorAnalysis.highSaturationRatio > 0.3) {
        portrait.push('明亮饱和的色彩选择表明您可能充满活力和创造力。');
      } else if (colorAnalysis.lowValueRatio > 0.3) {
        portrait.push('画作中的深色元素较多，可能暗示您需要关注一下内心的情绪状态。');
      }
      
      // 基于笔触分析
      if (strokeAnalysis.jitterCount / (pathCount.value || 1) > 5) {
        portrait.push('画作中有些抖动的线条，这可能反映出您最近有些焦虑或不安。');
      } else if (strokeAnalysis.averageLength > 100) {
        portrait.push('流畅的长线条显示出您思路清晰，行动果断。');
      }
      
      if (strokeAnalysis.overlapCount > 3) {
        portrait.push('画面中出现了一些反复涂抹的痕迹，这可能表明您在做决定时有些犹豫或纠结。');
      }
      
      // 基于构图分析
      if (composition.isTopHeavy) {
        portrait.push('您的画作重心偏上，显示出您可能有丰富的想象力和理想主义倾向。');
      } else if (composition.isBottomHeavy) {
        portrait.push('画作的重心偏下，表明您可能是一个踏实、注重现实的人。');
      }
      
      if (composition.density > 0.8) {
        portrait.push('画面元素较为密集，可能反映出您当前的生活或思绪比较忙碌。');
      } else if (composition.density < 0.1) {
        portrait.push('画面留有较多空白，这可能代表您需要更多的空间或是有些疏离感。');
      }
      
      // 基于时间分析
      if (timeAnalysis.isLateNight) {
        portrait.push('深夜创作可能表明您的思绪较为活跃，或是有一些未解决的问题在脑海中萦绕。');
      }
      
      // 基于压力指数
      if (stressInfo.score > 60) {
        portrait.push('根据您的画作特征，您目前可能承受着较高的压力，建议适当放松和休息。');
      } else if (stressInfo.score < 20) {
        portrait.push('您的画作透露出轻松和平静的氛围，这是非常好的状态。');
      }
      
      // 如果没有足够的特征，提供一个通用描述
      if (portrait.length === 0) {
        portrait.push('您的画作展现了平衡和和谐的特质，这通常代表着稳定的心理状态。');
      }
      
      return portrait.join(' ');
    }
    
    const analyzeDrawing = async () => {
      console.log('🚀 analyzeDrawing函数被调用了！')
      
      // 隐藏绘画提示
      showPaintingPrompt.value = false
      
      try {
        console.log('🔍 检查drawingCanvas是否存在:', drawingCanvas.value ? '存在' : '不存在')
        
        if (!drawingCanvas.value) {
          console.error('❌ drawingCanvas不存在！');
          alert('画布初始化失败，请刷新页面重试！');
          return;
        }
        
        const canvas = drawingCanvas.value;
        console.log('✅ 成功获取画布引用')
        
        console.log('📊 尝试获取画布上下文...')
        const ctx = canvas.getContext('2d');
        if (!ctx) {
          console.error('❌ 无法获取画布上下文！');
          alert('无法初始化画布，请刷新页面重试！');
          return;
        }
        console.log('✅ 成功获取画布上下文')
        
        console.log('📸 尝试获取画布图像数据...')
        const imageDataObj = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageDataObj.data;
        console.log('✅ 成功获取画布图像数据，像素数量:', data.length / 4)
        
        let isEmpty = true;
        console.log('🔍 开始检查画布是否为空...')

        // 检查画布是否为空
        for (let i = 0; i < data.length; i += 4) {
          if (data[i] !== 255 || data[i + 1] !== 255 || data[i + 2] !== 255 || data[i + 3] !== 0) {
            isEmpty = false;
            break;
          }
        }

        console.log('📊 画布检查完成，是否为空:', isEmpty)
        if (isEmpty) {
          console.log('⚠️ 画布为空，提示用户先绘制内容')
          alert('画布为空，请先绘制内容再进行分析！');
          return;
        }
        console.log('✅ 画布不为空，可以进行分析')
        
        // 1. 进行本地分析
        console.log('📊 开始本地分析...')
        
        // 计算总绘画时间（秒）
        const totalPaintingTimeSeconds = totalDrawingTime.value / 1000;
        console.log('⏱️ 总绘画时间:', totalPaintingTimeSeconds.toFixed(2), '秒')
        
        // 色彩分析
        const colorAnalysis = analyzeColors(imageDataObj);
        console.log('🎨 色彩分析结果:', colorAnalysis)
        
        // 构图分析
        const compositionAnalysis = analyzeComposition(imageDataObj, canvas);
        console.log('🖼️ 构图分析结果:', compositionAnalysis)
        
        // 提交时间分析
        const timeAnalysis = analyzeSubmissionTime();
        console.log('🕐 提交时间分析结果:', timeAnalysis)
        
        // 计算压力指数
        const stressInfo = calculateStressIndex(colorAnalysis, strokeStats.value, compositionAnalysis, timeAnalysis);
        console.log('📊 压力分析结果:', stressInfo)
        
        // 生成情绪雷达图数据
        const moodRadarData = generateMoodRadar(colorAnalysis, strokeStats.value, compositionAnalysis);
        console.log('📈 情绪雷达图数据:', moodRadarData)
        
        // 生成心理画像
        const personalityPortrait = generatePersonalityPortrait(colorAnalysis, strokeStats.value, compositionAnalysis, timeAnalysis, stressInfo);
        console.log('👤 心理画像:', personalityPortrait)
        
        const imageData = canvas.toDataURL('image/png')
        console.log('📤 开始准备发送画作进行AI分析...')
        console.log('📊 数据准备完成，准备执行API调用...')

        // 使用auth store获取用户token
        const token = authStore.getToken;
        console.log('🔄 即将执行API调用到 /paintings/analyze，使用token:', token ? '已提供' : '未提供')

        // 显示等待动画
        const loadingDiv = document.createElement('div');
        loadingDiv.style.cssText = `
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-color: rgba(0, 0, 0, 0.5);
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          z-index: 9999;
          font-family: 'Microsoft YaHei', sans-serif;
        `;
        
        const spinner = document.createElement('div');
        spinner.style.cssText = `
          width: 50px;
          height: 50px;
          border: 5px solid #f3f3f3;
          border-top: 5px solid #3498db;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-bottom: 20px;
        `;
        
        const loadingText = document.createElement('div');
        loadingText.textContent = '正在生成您的心理侧写...';
        loadingText.style.cssText = `
          color: white;
          font-size: 18px;
          font-weight: bold;
        `;
        
        loadingDiv.appendChild(spinner);
        loadingDiv.appendChild(loadingText);
        document.body.appendChild(loadingDiv);
        
        // 添加动画样式
        const styleSheet = document.createElement('style');
        styleSheet.textContent = `
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `;
        document.head.appendChild(styleSheet);

        try {
          const response = await axios.post('/api/v1/paintings/analyze', {
            image_data_url: imageData,
            painting_mode: currentPaintingMode.value === 'htp' ? 'house_tree_person' : currentPaintingMode.value === 'themed' ? 'theme_painting' : 'free_drawing',
            theme: selectedTheme.value || '',
            painting_time_seconds: totalPaintingTimeSeconds,
            local_analysis: {
              color_analysis: colorAnalysis,
              stroke_analysis: strokeStats.value,
              composition_analysis: compositionAnalysis,
              time_analysis: timeAnalysis
            }
          }, {
            headers: {
              'Authorization': token ? `Bearer ${token}` : ''
            },
            timeout: 30000 // 设置30000ms超时，因为AI分析需要更多时间
          });

          console.log('✅ API调用完成，收到响应，状态码:', response.status)
          
          if (response.status === 200) {
            console.log('📝 响应正常，获取到分析结果...')
            const result = response.data;
            console.log('📊 成功获取AI分析结果:', result)
            
            // 构建各维度分析的Markdown格式描述
            const buildMarkdownAnalysis = (data) => {
              if (!data) return '';
              let markdown = [];
              for (const [key, value] of Object.entries(data)) {
                // 转换中文key为更友好的描述
                const keyMap = {
                  'emotion_tendency': '情绪倾向',
                  'cool_color_ratio': '冷色调占比',
                  'warm_color_ratio': '暖色调占比',
                  'color_diversity': '色彩多样性',
                  'stroke_characteristics': '线条特征',
                  'pressure_level': '力度水平',
                  'stroke_consistency': '连贯性',
                  'emotional_stability': '情绪稳定性',
                  '密度': '画面密度',
                  'space_utilization': '空间利用率',
                  '中心位置': '中心位置',
                  '元素排列方式': '元素排列方式'
                };
                const displayKey = keyMap[key] || key;
                markdown.push(`- **${displayKey}**: ${value}`);
              }
              return markdown.join('\n');
            };

            // 提取API返回的结构化数据
            const aiContentDescription = result.content_description || '暂无内容描述';
            const aiAnalysisResult = result.analysis_result || '';
            
            // 从API返回的结构化分析中提取各部分数据
            const aiColorAnalysis = buildMarkdownAnalysis(result.color_emotion_analysis?.data) || 
                                   (result.color_emotion_analysis?.description ? `- **分析结果**: ${result.color_emotion_analysis.description}` : '');
            const aiStrokeAnalysis = buildMarkdownAnalysis(result.brush_dynamics_analysis?.data) || 
                                   (result.brush_dynamics_analysis?.description ? `- **分析结果**: ${result.brush_dynamics_analysis.description}` : '');
            const aiCompositionAnalysis = buildMarkdownAnalysis(result.composition_analysis?.data) || 
                                        (result.composition_analysis?.description ? `- **分析结果**: ${result.composition_analysis.description}` : '');
            
            // 使用API返回的情绪雷达图数据
            const apiMoodRadarData = result.mood_radar_data || moodRadarData;
            
            // 合并多维度分析内容
            const multiDimensionAnalysis = [
              aiColorAnalysis && `**色彩情感分析**\n${aiColorAnalysis}`,
              aiStrokeAnalysis && `**笔触动力学分析**\n${aiStrokeAnalysis}`,
              aiCompositionAnalysis && `**构图与空间分析**\n${aiCompositionAnalysis}`
            ].filter(Boolean).join('\n\n');
            
            // 创建详细的心理画像 - 优先使用API的content_description
            const detailedPersonalityPortrait = aiContentDescription;
            
            // 合并本地分析和AI分析结果，优先使用API返回的真实数据
            analysisResult.value = {
              // 使用API返回的压力相关数据
              stressIndex: apiMoodRadarData?.压力水平 ? apiMoodRadarData.压力水平.toFixed(1) : parseFloat(stressInfo.index),
              stressLevel: apiMoodRadarData?.压力水平 ? 
                (apiMoodRadarData.压力水平 > 7 ? '高度' : apiMoodRadarData.压力水平 > 4 ? '中度' : '轻度') : stressInfo.level,
              
              // 使用API返回的情绪雷达数据
              moodRadar: apiMoodRadarData,
              
              // 使用AI返回的个性化心理画像
              moodDescription: aiContentDescription,
              explanation: aiAnalysisResult || detailedPersonalityPortrait,
              personalityPortrait: detailedPersonalityPortrait,
              
              aiAnalysis: {
                colorAnalysis: aiColorAnalysis,
                strokeAnalysis: aiStrokeAnalysis,
                compositionAnalysis: aiCompositionAnalysis,
                symbolAnalysis: '', // API暂未提供单独的符号分析
                suggestions: '', // 可以从content_description中提取建议
                multiDimensionAnalysis: multiDimensionAnalysis || 'AI分析暂不可用，以下是本地分析结果'
              },
              
              // 添加详细分析数据供前端使用
              detailedAnalysis: {
                colorAnalysis: colorAnalysis,
                strokeAnalysis: strokeStats.value,
                compositionAnalysis: compositionAnalysis,
                timeAnalysis: timeAnalysis,
                paintingTime: totalPaintingTimeSeconds
              }
            }
            
            console.log('🎨 完整分析结果已更新到UI')
            
            // 确保情绪雷达图在DOM更新后显示，使用API返回的数据
            setTimeout(() => {
              showMoodRadarChart(apiMoodRadarData);
            }, 100);
            
            // 移除等待动画
            document.body.removeChild(loadingDiv);
            document.head.removeChild(styleSheet);
            
            alert('绘画分析完成！已生成您的情绪报告和心理画像。');
          }
        } catch (apiError) {
          // 移除等待动画
          if (loadingDiv && document.body.contains(loadingDiv)) {
            document.body.removeChild(loadingDiv);
          }
          if (styleSheet && document.head.contains(styleSheet)) {
            document.head.removeChild(styleSheet);
          }
          console.warn('⚠️ API调用失败，将使用本地分析结果:', apiError.message)
          // 生成本地多维度分析描述
            const generateLocalMultiDimensionAnalysis = () => {
              let analysis = [];
              
              // 色彩分析描述
              analysis.push('**色彩情感分析**');
              if (colorAnalysis.warmToCoolRatio > 1.5) {
                analysis.push('- 暖色调占主导，显示积极情绪');
              } else if (colorAnalysis.warmToCoolRatio < 0.5) {
                analysis.push('- 冷色调为主，可能反映冷静或内敛情绪');
              } else {
                analysis.push('- 色彩平衡，情绪稳定');
              }
            
            // 笔触分析描述
            analysis.push('\n**笔触动力学分析**');
            if (strokeStats.value.jitterCount / (pathCount.value || 1) > 5) {
              analysis.push('- 线条有些抖动，可能有些焦虑');
            } else {
              analysis.push('- 线条流畅，情绪稳定');
            }
            analysis.push(`- 线条数量: ${strokeStats.value.pathCount || 0}条`);
            analysis.push(`- 平均长度: ${Math.round(strokeStats.value.averageLength || 0)}px`);
            
            // 构图分析描述
            analysis.push('\n**构图与空间分析**');
            if (compositionAnalysis.density > 0.8) {
              analysis.push('- 画面密集，思绪活跃');
            } else if (compositionAnalysis.density < 0.1) {
              analysis.push('- 画面留白多，需要更多表达');
            } else {
              analysis.push('- 构图平衡，思维清晰');
            }
            analysis.push(`- 重心位置: ${compositionAnalysis.centerOfGravity || '居中'}`);
            
            return analysis.join('\n');
          };
          
          // 创建更详细的本地心理画像
          const detailedLocalPortrait = `${personalityPortrait} 您的绘画展现了独特的个人风格，反映出您作为考研学生的内心世界。从色彩使用、笔触特征和构图方式可以看出您的思考模式和情绪状态。建议您在备考过程中保持这种表达和自我觉察的习惯，这对心理健康非常有益。`;
          
          // 如果API调用失败，只使用本地分析结果
          analysisResult.value = {
            stressIndex: parseFloat(stressInfo.index),
            stressLevel: stressInfo.level,
            moodRadar: moodRadarData,
            moodDescription: '基于本地分析的画作解读',
            explanation: detailedLocalPortrait,
            personalityPortrait: detailedLocalPortrait,
            aiAnalysis: {
              multiDimensionAnalysis: generateLocalMultiDimensionAnalysis()
            },
            detailedAnalysis: {
              colorAnalysis: colorAnalysis,
              strokeAnalysis: strokeStats.value,
              compositionAnalysis: compositionAnalysis,
              timeAnalysis: timeAnalysis,
              paintingTime: totalPaintingTimeSeconds
            }
          }
          
          // 移除等待动画
          if (loadingDiv && document.body.contains(loadingDiv)) {
            document.body.removeChild(loadingDiv);
          }
          if (styleSheet && document.head.contains(styleSheet)) {
            document.head.removeChild(styleSheet);
          }
          
          console.log('🎨 本地分析结果已更新到UI')
          
          // 显示情绪雷达图
          showMoodRadarChart(moodRadarData);
          
          alert('已使用本地分析引擎完成绘画分析！生成了您的情绪报告和心理画像。');
        }
      } catch (error) {
        console.error('分析过程中出错:', error);
        console.error('错误类型:', error.name);
        console.error('错误信息:', error.message);
        
        // 增强的错误诊断信息
        if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
          console.error('⚠️ 连接错误：无法连接到后端服务器。请检查：');
          console.error('1. 后端服务器是否正在运行');
          console.error('2. 后端端口8000是否正确');
          console.error('3. 网络连接是否正常');
          alert('连接错误：无法连接到后端服务器。请确保服务器正在运行并检查网络连接。');
        }
        
        // 显示真实错误信息
        analysisResult.value = {
          stressIndex: '0.0',
          stressLevel: '-',
          moodRadar: {},
          moodDescription: '分析失败',
          explanation: `分析错误：${error.message}`
        }

        alert(`分析失败：${error.message}`);
      }
    }
    
    // 显示情绪雷达图
    const showMoodRadarChart = (moodData) => {
      console.log('📊 准备显示情绪雷达图:', moodData)
      
      // 使用Canvas API绘制雷达图
      const canvas = document.getElementById('moodRadarChart');
      if (!canvas) return;
      
      // 设置canvas的实际像素尺寸，确保绘制比例正确
      const container = canvas.parentElement;
      const rect = container.getBoundingClientRect();
      const size = Math.min(rect.width, rect.height);
      canvas.width = size;
      canvas.height = size;
      
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      
      // 清空画布
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // 默认数据，如果没有提供数据
      const defaultData = {
        happy: 60,
        calm: 50,
        anxious: 30,
        sad: 20,
        angry: 10,
        creative: 70
      };
      
      const data = moodData || defaultData;
      
      // 检查是否是API返回的中文键名数据
      const isChineseKeyFormat = Object.keys(data).some(key => key.includes('度') || key.includes('水平') || key.includes('情绪'));
      
      let labels, values;
      
      if (isChineseKeyFormat) {
        // 处理API返回的中文键名数据
        labels = ['积极情绪', '专注度', '焦虑程度', '压力水平', '情绪稳定性', '创造力'];
        // 使用安全的属性访问，确保即使数据缺失也不会出错
        values = [
          data['积极情绪'] || 0,
          data['专注度'] || 0,
          data['焦虑程度'] || 0,
          data['压力水平'] || 0,
          data['情绪稳定性'] || 0,
          data['创造力'] || 0
        ];
      } else {
        // 处理原始英文键名数据
        labels = ['快乐', '平静', '焦虑', '悲伤', '愤怒', '创造力'];
        values = [data.happy || 0, data.calm || 0, data.anxious || 0, data.sad || 0, data.angry || 0, data.creative || 0];
      }
      
      // 保持数据原始范围，API返回的中文键名数据范围是0-10，无需乘以10
      // 这样可以确保雷达图比例正确
      
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      // 减小半径，确保标签不会被截断
      const radius = Math.min(centerX, centerY) * 0.7;
      const angleStep = (2 * Math.PI) / values.length;
      
      // 绘制网格
      ctx.strokeStyle = '#e0e0e0';
      ctx.lineWidth = 1;
      
      for (let level = 1; level <= 5; level++) {
        const levelRadius = (radius / 5) * level;
        ctx.beginPath();
        
        for (let i = 0; i < values.length; i++) {
          const angle = i * angleStep - Math.PI / 2;
          const x = centerX + levelRadius * Math.cos(angle);
          const y = centerY + levelRadius * Math.sin(angle);
          
          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        
        ctx.closePath();
        ctx.stroke();
      }
      
      // 绘制轴线
      ctx.strokeStyle = '#999';
      ctx.lineWidth = 1;
      
      for (let i = 0; i < values.length; i++) {
        const angle = i * angleStep - Math.PI / 2;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX + radius * Math.cos(angle), centerY + radius * Math.sin(angle));
        ctx.stroke();
      }
      
      // 绘制数据区域
      ctx.fillStyle = 'rgba(102, 126, 234, 0.2)';
      ctx.strokeStyle = '#667eea';
      ctx.lineWidth = 3;
      ctx.beginPath();
      
      for (let i = 0; i < values.length; i++) {
        const angle = i * angleStep - Math.PI / 2;
        // 调整计算方式，因为数据范围是0-10而不是0-100
        const valueRadius = (radius / 10) * values[i];
        const x = centerX + valueRadius * Math.cos(angle);
        const y = centerY + valueRadius * Math.sin(angle);
        
        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
      
      // 绘制数据点
      ctx.fillStyle = '#764ba2';
      for (let i = 0; i < values.length; i++) {
        const angle = i * angleStep - Math.PI / 2;
        // 调整计算方式，与数据区域保持一致
        const valueRadius = (radius / 10) * values[i];
        const x = centerX + valueRadius * Math.cos(angle);
        const y = centerY + valueRadius * Math.sin(angle);
        
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fill();
      }
      
      // 绘制标签 - 调整位置以适应增大的雷达图
      ctx.fillStyle = '#2c3e50';
      ctx.font = '16px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      for (let i = 0; i < values.length; i++) {
        const angle = i * angleStep - Math.PI / 2;
        // 标签位置调整为半径的1.1倍，确保在雷达图外围且不超出画布
        const labelRadius = radius * 1.1;
        const x = centerX + labelRadius * Math.cos(angle);
        const y = centerY + labelRadius * Math.sin(angle);
        
        ctx.fillText(labels[i], x, y);
      }
    }
    
    // 获取压力等级对应的样式类
    const getStressLevelClass = (level) => {
      switch (level) {
        case '低':
          return 'stress-level-low';
        case '中':
          return 'stress-level-medium';
        case '高':
          return 'stress-level-high';
        default:
          return '';
      }
    }
    
    // 获取提交时间分类文本
    const getTimeCategoryText = (category) => {
      const categoryMap = {
        morning: '早晨（6:00-12:00）',
        afternoon: '下午（12:00-18:00）',
        evening: '晚上（18:00-23:00）',
        night: '深夜（23:00-6:00）'
      };
      return categoryMap[category] || category;
    }
    
    // 格式化Markdown风格的分析内容为HTML
    const formatMarkdownAnalysis = (text) => {
      if (!text) return '';
      
      // 首先移除所有不必要的标点符号和横杠
      let formatted = text
        .replace(/[：:；;。、,，.]\s*$/gm, '')  // 移除行尾的标点符号
        .replace(/^\s*-\s*/gm, '')  // 移除行首的横杠和空格
        .replace(/^\s*•\s*/gm, '')  // 移除行首的点号和空格
        .replace(/^\s*\*\s*/gm, '')  // 移除行首的星号和空格
        .replace(/\*([^*]*)\*/g, '$1')  // 移除文本中间的单个星号
        .replace(/\*\*(.*?)\*\*\s*[:：]/g, '<h4>$1</h4>')  // 将**标题**: 转换为h4，去掉冒号
        .replace(/\*\*(.*?)\*\*/g, '<h4>$1</h4>');      // 将**标题**转换为h4
      
      // 处理键值对格式
      formatted = formatted.replace(/^([^:：]+)[：:](.*)$/gm, '<p><strong>$1</strong><span>$2</span></p>');
      
      return formatted;
    }
    
    // 生成色彩分析报告
    const generateColorAnalysis = (colorData) => {
      if (!colorData) return '色彩分析数据加载中...';
      
      const analysis = [];
      
      // 色彩情感倾向
      if (colorData.warmToCoolRatio > 1.5) {
        analysis.push('**情感倾向**: 温暖积极，充满活力');
      } else if (colorData.warmToCoolRatio < 0.5) {
        analysis.push('**情感倾向**: 冷静内敛，思维理性');
      } else {
        analysis.push('**情感倾向**: 平衡和谐，情绪稳定');
      }
      
      // 色彩多样性
      analysis.push(`**色彩多样性**: ${colorData.colorDiversity > 20 ? '丰富' : colorData.colorDiversity > 10 ? '适中' : '单一'}`);
      
      return analysis.join('\n');
    };
    
    // 生成笔触分析报告
    const generateBrushAnalysis = (brushData) => {
      if (!brushData) return '笔触分析数据加载中...';
      
      const analysis = [];
      
      // 线条流畅性
      if (brushData.averageLength > 100) {
        analysis.push('**线条特点**: 流畅自信，思维开阔');
      } else if (brushData.averageLength > 50) {
        analysis.push('**线条特点**: 稳健有序，计划性强');
      } else {
        analysis.push('**线条特点**: 细致谨慎，注重细节');
      }
      
      // 线条连续性
      if (brushData.continuity > 0.8) {
        analysis.push('**线条连续性**: 高，注意力集中');
      } else {
        analysis.push('**线条连续性**: 中低，思维活跃或易分散');
      }
      
      return analysis.join('\n');
    };
    
    // 生成构图分析报告
    const generateCompositionAnalysis = (compositionData) => {
      if (!compositionData) return '构图分析数据加载中...';
      
      const analysis = [];
      
      // 画面密度
      if (compositionData.density > 0.8) {
        analysis.push('**画面密度**: 高，信息丰富或压力较大');
      } else if (compositionData.density < 0.1) {
        analysis.push('**画面密度**: 低，思维开阔或情绪平静');
      } else {
        analysis.push('**画面密度**: 适中，平衡感良好');
      }
      
      // 空间利用
      analysis.push(`**空间利用率**: ${Math.round((compositionData.density || 0) * 100)}%`);
      
      // 重心位置
      analysis.push(`**重心位置**: ${compositionData.centerOfGravity || '居中'}`);
      
      return analysis.join('\n');
    };

    const goBack = () => {
      router.push('/dashboard')
    }

    const generateIntervention = async () => {
      if (!drawingCanvas.value) {
        console.log('无法生成心灵镜像：画布不存在')
        alert('画布初始化失败，请重新尝试！')
        return
      }
      
      isGeneratingMindMirror.value = true
      mindMirrorResult.value = null
      
      try {
        // 获取画布图像数据
        const canvas = drawingCanvas.value
        const imageData = canvas.toDataURL('image/png')
        console.log('📤 开始发送画作生成心灵镜像...')
        
        // 准备请求配置
        const requestConfig = {
          timeout: 30000 // 设置30000ms超时，因为AI生成需要更多时间
        }
        
        // 只有当token存在时才添加认证头
        const token = localStorage.getItem('token')
        if (token) {
          requestConfig.headers = {
            'Authorization': `Bearer ${token}`
          }
        }
        
        // 调用后端API生成心灵镜像
        const response = await axios.post('/api/v1/paintings/generate-mind-mirror', {
          image_data_url: imageData
        }, requestConfig)
        
        if (response.data.success) {
          mindMirrorResult.value = {
            positive_image_description: response.data.positive_image_description,
            guidance_text: response.data.guidance_text,
            is_real_mirror: response.data.is_real_mirror
          }
          console.log('心灵镜像生成成功:', mindMirrorResult.value)
        } else {
          console.error('生成心灵镜像失败:', response.data.message)
          // 使用默认响应
          mindMirrorResult.value = {
            positive_image_description: response.data.positive_image_description || '这是一幅充满阳光和希望的画面，色彩明亮温暖，构图和谐平衡。',
            guidance_text: response.data.guidance_text || '看，如果给这里加一缕阳光，是不是感觉充满了希望？',
            is_real_mirror: false
          }
        }
        
        // 复制原始画布到预览画布
        setTimeout(() => {
          // 确保画布引用存在
          if (!originalPaintingPreview.value || !drawingCanvas.value) {
            console.error('画布引用不存在，无法渲染预览')
            return
          }
          
          try {
            // 获取画布上下文
            const previewCtx = originalPaintingPreview.value.getContext('2d')
            const originalCanvas = drawingCanvas.value
            
            // 清空预览画布
            previewCtx.clearRect(0, 0, 300, 250)
            
            // 计算缩放比例以适应预览区域
            const scaleX = 300 / originalCanvas.width
            const scaleY = 250 / originalCanvas.height
            const scale = Math.min(scaleX, scaleY)
            
            // 计算居中位置
            const offsetX = (300 - originalCanvas.width * scale) / 2
            const offsetY = (250 - originalCanvas.height * scale) / 2
            
            // 绘制缩放后的画布内容
            previewCtx.drawImage(
              originalCanvas,
              0, 0, originalCanvas.width, originalCanvas.height,
              offsetX, offsetY, originalCanvas.width * scale, originalCanvas.height * scale
            )
            
            // 渲染积极版本预览（使用相同的画布数据）
            if (positivePaintingPreview.value) {
              const positiveCtx = positivePaintingPreview.value.getContext('2d')
              
              // 清空预览画布
              positiveCtx.clearRect(0, 0, 300, 250)
              
              // 绘制缩放后的画布内容
              positiveCtx.drawImage(
                originalCanvas,
                0, 0, originalCanvas.width, originalCanvas.height,
                offsetX, offsetY, originalCanvas.width * scale, originalCanvas.height * scale
              )
              
              // 为积极版本添加一些视觉效果，使其看起来更积极
              positiveCtx.globalCompositeOperation = 'multiply'
              positiveCtx.fillStyle = 'rgba(255, 240, 200, 0.3)'
              positiveCtx.fillRect(0, 0, 300, 250)
              positiveCtx.globalCompositeOperation = 'source-over'
            }
          } catch (error) {
            console.error('渲染画布预览时出错:', error)
          }
        }, 300) // 增加延迟确保DOM完全更新
        
        // 显示心灵镜像结果对话框
        showMindMirrorDialog.value = true
      } catch (error) {
        console.error('生成心灵镜像异常:', error)
        // 错误时使用默认值
        mindMirrorResult.value = {
          positive_image_description: '这是一幅充满阳光和希望的画面，色彩明亮温暖，构图和谐平衡。',
          guidance_text: '看，如果给这里加一缕阳光，是不是感觉充满了希望？',
          is_real_mirror: false
        }
        
        // 复制原始画布到预览画布
        setTimeout(() => {
          // 确保画布引用存在
          if (!originalPaintingPreview.value || !drawingCanvas.value) {
            console.error('画布引用不存在，无法渲染预览')
            return
          }
          
          try {
            // 获取画布上下文
            const previewCtx = originalPaintingPreview.value.getContext('2d')
            const originalCanvas = drawingCanvas.value
            
            // 清空预览画布
            previewCtx.clearRect(0, 0, 300, 250)
            
            // 计算缩放比例以适应预览区域
            const scaleX = 300 / originalCanvas.width
            const scaleY = 250 / originalCanvas.height
            const scale = Math.min(scaleX, scaleY)
            
            // 计算居中位置
            const offsetX = (300 - originalCanvas.width * scale) / 2
            const offsetY = (250 - originalCanvas.height * scale) / 2
            
            // 绘制缩放后的画布内容
            previewCtx.drawImage(
              originalCanvas,
              0, 0, originalCanvas.width, originalCanvas.height,
              offsetX, offsetY, originalCanvas.width * scale, originalCanvas.height * scale
            )
            
            // 渲染积极版本预览（使用相同的画布数据）
            if (positivePaintingPreview.value) {
              const positiveCtx = positivePaintingPreview.value.getContext('2d')
              
              // 清空预览画布
              positiveCtx.clearRect(0, 0, 300, 250)
              
              // 绘制缩放后的画布内容
              positiveCtx.drawImage(
                originalCanvas,
                0, 0, originalCanvas.width, originalCanvas.height,
                offsetX, offsetY, originalCanvas.width * scale, originalCanvas.height * scale
              )
              
              // 为积极版本添加一些视觉效果，使其看起来更积极
              positiveCtx.globalCompositeOperation = 'multiply'
              positiveCtx.fillStyle = 'rgba(255, 240, 200, 0.3)'
              positiveCtx.fillRect(0, 0, 300, 250)
              positiveCtx.globalCompositeOperation = 'source-over'
            }
          } catch (error) {
            console.error('渲染画布预览时出错:', error)
          }
        }, 300) // 增加延迟确保DOM完全更新
        
        showMindMirrorDialog.value = true
      } finally {
        isGeneratingMindMirror.value = false
      }
    }
    
    // 语音引导相关状态
    const isGeneratingGuidance = ref(false)
    const currentGuidance = ref(null)
    const isPlayingGuidance = ref(false)
    const isGeneratingStory = ref(false)
    const healingStory = ref(null)
    // 心灵镜像相关状态
    const isGeneratingMindMirror = ref(false)
    const mindMirrorResult = ref(null)
    const originalPaintingPreview = ref(null)
    const positivePaintingPreview = ref(null)
    
    // 生成并播放正念绘画引导
    const generateAndPlayMindfulnessGuidance = async () => {
      if (isPlayingGuidance.value) {
        // 如果正在播放，停止播放
        stopGuidanceSpeech()
        return
      }
      
      try {
        isGeneratingGuidance.value = true
        
        // 如果已有引导文本，直接播放
        if (currentGuidance.value) {
          playGuidanceSpeech()
          isGeneratingGuidance.value = false
          return
        }
        
        // 启用API调用，使用后端AI生成功能
        const useApiCall = true;
        
        // 直接使用本地分析结果调用API（如果有）
        // 简化流程：不管画布是否已保存，都尝试使用现有分析数据
        if (useApiCall && analysisResult.value) {
          try {
            // 直接发送本地分析结果到后端生成引导，无需依赖画作ID
            console.log('Generating guidance using local analysis data');
            const response = await axios.post(`/api/v1/paintings/generate-guidance-direct`, {
              painting_analysis: analysisResult.value
            }, {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
              },
              timeout: 6000
            })
            
            if (response.data && response.data.success) {
              currentGuidance.value = response.data.guidance.guidance_text
              
              // 清空画布，准备新的创作
              clearCanvas()
              
              // 播放引导语音
              playGuidanceSpeech()
              
              alert('AI个性化引导已生成，请跟随引导进行创作')
              isGeneratingGuidance.value = false
              return
            }
          } catch (apiError) {
            console.warn('直接API调用失败，尝试备用方案:', apiError.message);
            // 继续执行，尝试其他方案
          }
        }
        
        // 备用方案：检查是否有已保存的画布
        // 检测是否为时间戳格式的临时ID（纯数字且长度为13位或10位）
        const isTimestampId = currentCanvasId.value && /^\d{10,13}$/.test(currentCanvasId.value);
        const isSavedCanvas = currentCanvasId.value && 
          !isTimestampId && 
          savedCanvases.value.some(c => c.id === currentCanvasId.value) &&
          !isDefaultName.value;
        
        console.log('Canvas ID validation:', {
          id: currentCanvasId.value,
          isSavedCanvas,
          isTimestampId,
          hasLocalAnalysis: !!analysisResult.value,
          isDefaultName: isDefaultName.value
        });
        
        if (isSavedCanvas && useApiCall) {
          try {
            // 调用后端API生成引导文本，设置6000ms超时，并添加认证头
            console.log('Generating guidance for painting ID:', currentCanvasId.value);
            const response = await axios.post(`/api/v1/paintings/generate-guidance/${currentCanvasId.value}`, {}, {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
              },
              timeout: 6000
            })
            
            if (response.data && response.data.success) {
              currentGuidance.value = response.data.guidance.guidance_text
              
              // 清空画布，准备新的创作
              clearCanvas()
              
              // 播放引导语音
              playGuidanceSpeech()
              
              alert('语音引导已生成，请跟随引导进行创作')
              isGeneratingGuidance.value = false
              return
            }
          } catch (apiError) {
            console.warn('API调用失败，使用默认引导文本:', apiError.message);
            // 继续执行，使用默认引导文本
          }
        }
        
        // 使用默认引导文本
        console.log('Using default guidance as painting ID is not saved in database');
        currentGuidance.value = '现在，请你轻轻放下手中的笔，先做三次深呼吸 —— 吸气时感受新鲜空气充满胸腔，呼气时慢慢释放所有紧绷的情绪，让肩膀自然下沉，眉心也跟着舒展。等你感觉心跳变得平稳，再缓缓睁开眼睛，把目光轻轻落在面前的画布上。\n' +
            '你看，这张空白的画布就像一片等待被温柔唤醒的小世界，而你的画笔，就是能为它注入生命力的魔法棒。接下来，我想邀请你先闭上眼睛，在脑海里勾勒一幅画面：清晨的阳光穿过层层叠叠的树叶，洒下细碎的金斑，落在一片开满小雏菊的草地上。风轻轻吹过，雏菊的花瓣会轻轻摇晃，像在和你打招呼；远处还有一条弯弯的小溪，溪水清澈得能看见水底圆润的鹅卵石，阳光照在水面上，会折射出星星点点的光，像撒了一把碎钻。\n' +
            '现在，慢慢睁开眼睛，拿起你的画笔吧。不用急着画完整的场景，我们从最让你心动的部分开始 —— 如果你喜欢那片阳光，就先蘸取一点温暖的黄色，轻轻在画布上点出几缕光线，想象每一笔都是阳光在画布上跳跃；如果你更偏爱小溪，就用淡淡的蓝色画出弯曲的线条，线条不用笔直，像溪水自然流淌的样子就好，再用白色点缀几滴溅起的水花，让溪水看起来灵动又鲜活。\n' +
            '画着画着，你可以试着给草地添上颜色 —— 不一定是均匀的绿色，或许靠近阳光的地方，草色会偏浅黄，像被阳光吻过；而躲在树荫下的草，颜色会深一点，带着湿润的生机。接着，我们来画小雏菊：先在草地上点出小小的白色圆圈当花瓣，再用黄色点上花心，每一朵雏菊都可以有自己的姿态，有的完全绽放，有的还是小小的花苞，就像生活里那些不同阶段的美好，都值得被认真描绘。\n' +
            '如果你的画笔不小心画错了线条也没关系，就把它当成是这片小世界里意外的惊喜 —— 比如多余的一笔，或许能变成随风飘动的蒲公英；颜色涂出边界的地方，就当是阳光漫过了草地的边缘。你看，连 "不完美" 都能变成独特的风景，就像你自己，每一个真实的瞬间都值得被接纳、被喜爱。\n' +
            '现在，让你的画笔继续在画布上游走吧。可以给小溪边加几块灰色的鹅卵石，石头上还能有淡淡的纹路；也可以在天空的位置添上几朵蓬松的白云，用浅蓝和白色轻轻晕染，让天空看起来又高又开阔。画的时候不用在意细节是否精致，重点是感受画笔在指尖移动的感觉，感受每一种颜色带给你的心情 —— 黄色的温暖、蓝色的平静、绿色的生机，这些都是你内心深处积极力量的写照。\n' +
            '等你觉得画面差不多完整了，就停下笔，退后一步看看自己的作品。你会发现，你不仅画出了一片清晨的草地，更画出了此刻内心的平静与希望。这片小小的画布，就像一个属于你的能量空间，每当你感到疲惫或迷茫时，都可以回到这里，用画笔重新唤醒这些积极的画面，让它们成为你继续向前的力量。\n'
        // 清空画布
        clearCanvas()
        
        // 播放引导语音
        playGuidanceSpeech()
        
        alert('使用默认语音引导，请跟随引导进行创作')
      } catch (error) {
        console.error('生成引导失败:', error)
        
        // 使用默认引导文本作为备用
        currentGuidance.value = '现在，请你轻轻放下手中的笔，先做三次深呼吸 —— 吸气时感受新鲜空气充满胸腔，呼气时慢慢释放所有紧绷的情绪，让肩膀自然下沉，眉心也跟着舒展。等你感觉心跳变得平稳，再缓缓睁开眼睛，把目光轻轻落在面前的画布上。\n' +
            '你看，这张空白的画布就像一片等待被温柔唤醒的小世界，而你的画笔，就是能为它注入生命力的魔法棒。接下来，我想邀请你先闭上眼睛，在脑海里勾勒一幅画面：清晨的阳光穿过层层叠叠的树叶，洒下细碎的金斑，落在一片开满小雏菊的草地上。风轻轻吹过，雏菊的花瓣会轻轻摇晃，像在和你打招呼；远处还有一条弯弯的小溪，溪水清澈得能看见水底圆润的鹅卵石，阳光照在水面上，会折射出星星点点的光，像撒了一把碎钻。\n' +
            '现在，慢慢睁开眼睛，拿起你的画笔吧。不用急着画完整的场景，我们从最让你心动的部分开始 —— 如果你喜欢那片阳光，就先蘸取一点温暖的黄色，轻轻在画布上点出几缕光线，想象每一笔都是阳光在画布上跳跃；如果你更偏爱小溪，就用淡淡的蓝色画出弯曲的线条，线条不用笔直，像溪水自然流淌的样子就好，再用白色点缀几滴溅起的水花，让溪水看起来灵动又鲜活。\n' +
            '画着画着，你可以试着给草地添上颜色 —— 不一定是均匀的绿色，或许靠近阳光的地方，草色会偏浅黄，像被阳光吻过；而躲在树荫下的草，颜色会深一点，带着湿润的生机。接着，我们来画小雏菊：先在草地上点出小小的白色圆圈当花瓣，再用黄色点上花心，每一朵雏菊都可以有自己的姿态，有的完全绽放，有的还是小小的花苞，就像生活里那些不同阶段的美好，都值得被认真描绘。\n' +
            '如果你的画笔不小心画错了线条也没关系，就把它当成是这片小世界里意外的惊喜 —— 比如多余的一笔，或许能变成随风飘动的蒲公英；颜色涂出边界的地方，就当是阳光漫过了草地的边缘。你看，连 “不完美” 都能变成独特的风景，就像你自己，每一个真实的瞬间都值得被接纳、被喜爱。\n' +
            '现在，让你的画笔继续在画布上游走吧。可以给小溪边加几块灰色的鹅卵石，石头上还能有淡淡的纹路；也可以在天空的位置添上几朵蓬松的白云，用浅蓝和白色轻轻晕染，让天空看起来又高又开阔。画的时候不用在意细节是否精致，重点是感受画笔在指尖移动的感觉，感受每一种颜色带给你的心情 —— 黄色的温暖、蓝色的平静、绿色的生机，这些都是你内心深处积极力量的写照。\n' +
            '等你觉得画面差不多完整了，就停下笔，退后一步看看自己的作品。你会发现，你不仅画出了一片清晨的草地，更画出了此刻内心的平静与希望。这片小小的画布，就像一个属于你的能量空间，每当你感到疲惫或迷茫时，都可以回到这里，用画笔重新唤醒这些积极的画面，让它们成为你继续向前的力量。\n'
        // 清空画布
        clearCanvas()
        
        // 播放引导语音
        playGuidanceSpeech()
        
        alert('使用默认引导进行绘画练习')
      } finally {
        isGeneratingGuidance.value = false
      }
    }
    
    // 播放引导语音 - 使用更自然的真人声音效果
    const playGuidanceSpeech = () => {
      if (!currentGuidance.value) return
      
      // 停止之前可能在播放的语音
      stopGuidanceSpeech()
      
      // 创建语音合成实例，增强文本处理使语音更自然
      let text = currentGuidance.value
      
      // 1. 增强标点符号停顿 - 模拟真人说话节奏
      // 长句末尾停顿更长
      text = text.replace(/([。！？])/g, '$1<break time="400ms">')
      // 分句停顿适中
      text = text.replace(/([；：])/g, '$1<break time="300ms">')
      // 短停顿
      text = text.replace(/([，、])/g, '$1<break time="150ms">')
      
      // 2. 处理段落 - 添加更长的自然停顿
      text = text.replace(/\n\n/g, '<break time="800ms">')
      text = text.replace(/\n/g, '<break time="600ms">')
      
      // 3. 添加情感标记词（某些浏览器支持）
      text = text.replace(/感受|体会|想象/g, '<emphasis level="moderate">$&</emphasis>')
      text = text.replace(/平静|放松|舒适/g, '<emphasis level="strong">$&</emphasis>')
      
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'zh-CN' // 设置为中文
      
      // 4. 优化语音参数使其更接近真人声音
      utterance.rate = 0.85 // 稍微放慢语速，更显自然
      utterance.pitch = 0.95 // 微调音调，避免机械感
      utterance.volume = 0.98 // 接近满音量，更清晰
      
      // 5. 改进声音选择逻辑 - 增加更多声音选项
      const voices = window.speechSynthesis.getVoices()
      console.log('可用语音:', voices.map(v => v.name + ' (' + v.lang + ')'))
      
      // 扩展女性声音关键词，增加更多可能的中文声音名称
      const femaleVoicePatterns = [
        'Female', 'female', '女', '女声', 
        'Huihui', 'Yunxi', 'Xiaoxiao', 'Yaoyao', 
        'Luna', 'Zira', '微软', 'Microsoft',
        'Lingua', 'Melina', 'Mei-Jia', 'Ting-Ting',
        'Zhiyu', 'Yating', 'Suyun', 'Aiwei'
      ]
      
      // 改进的声音筛选逻辑
      let preferredVoice = voices.find(voice => {
        const isCN = voice.lang === 'zh-CN' || voice.lang.startsWith('zh-') || 
                    voice.lang === 'cmn-CN' || voice.name.includes('Chinese')
        const hasFemaleKeywords = femaleVoicePatterns.some(pattern => 
          voice.name.includes(pattern)
        )
        // 优先选择高质量语音引擎
        const isHighQuality = voice.name.includes('Premium') || 
                             voice.name.includes('Neural') ||
                             voice.name.includes('Enhanced')
        
        return isCN && (hasFemaleKeywords || isHighQuality)
      })
      
      // 如果没有找到理想的中文女性声音，尝试其他中文声音
      if (!preferredVoice) {
        preferredVoice = voices.find(voice => 
          voice.lang === 'zh-CN' || voice.lang.startsWith('zh-') ||
          voice.lang === 'cmn-CN'
        )
      }
      
      // 如果还是没有找到中文声音，尝试其他自然度较高的声音
      if (!preferredVoice && voices.length > 0) {
        // 寻找听起来更自然的声音
        const naturalVoices = voices.filter(v => 
          v.name.includes('Neural') || v.name.includes('Premium') ||
          v.name.includes('Enhanced') || v.name.includes('Female')
        )
        
        if (naturalVoices.length > 0) {
          preferredVoice = naturalVoices[0]
        } else {
          // 选择第一个可用声音作为后备
          preferredVoice = voices[0]
        }
        console.warn('未找到理想的中文声音，使用替代声音:', preferredVoice.name)
      }
      
      // 如果有找到合适的声音，设置它并根据不同声音调整参数
      if (preferredVoice) {
        utterance.voice = preferredVoice
        console.log('选择的语音:', preferredVoice.name)
        
        // 为不同声音引擎优化参数
        if (preferredVoice.name.includes('Huihui')) {
          utterance.pitch = 1.08
          utterance.rate = 0.82
        } else if (preferredVoice.name.includes('Yunxi') || preferredVoice.name.includes('Xiaoxiao')) {
          utterance.pitch = 1.02
          utterance.rate = 0.88
        } else if (preferredVoice.name.includes('Zira') || preferredVoice.name.includes('Microsoft')) {
          utterance.pitch = 1.05
          utterance.rate = 0.8
        } else if (preferredVoice.name.includes('Neural')) {
          // 神经网络声音引擎特殊优化
          utterance.pitch = 1.0
          utterance.rate = 0.85
        } else if (preferredVoice.name.includes('Female') && !preferredVoice.name.includes('Chinese')) {
          // 非中文女声，降低语速以提高可理解性
          utterance.pitch = 1.1
          utterance.rate = 0.75
        }
      }
      
      // 监听语音结束事件
      utterance.onend = () => {
        isPlayingGuidance.value = false
        console.log('语音播放结束')
      }
      
      utterance.onerror = (event) => {
        console.error('语音合成错误:', event)
        isPlayingGuidance.value = false
        // 更友好的错误提示
        alert('已退出语音绘画引导')
      }
      
      utterance.onstart = () => {
        console.log('语音开始播放')
      }
      
      // 6. 增强的语音播放控制
      // 添加韵律调整（prosody）参数，提升自然度
      utterance.prosody = {
        rate: utterance.rate,
        pitch: utterance.pitch
      }
      
      // 添加语音情感设置（如果浏览器支持）
      if (typeof utterance.emotion !== 'undefined') {
        utterance.emotion = 'calm' // 平静的情绪，适合正念引导
      }
      
      // 确保获取了所有可用声音后再播放
      if (voices.length === 0) {
        console.log('声音列表为空，等待加载...')
        // 如果声音列表为空，等待onvoiceschanged事件
        const handleVoicesChanged = () => {
          console.log('声音加载完成，重新播放')
          playGuidanceSpeech() // 重新调用以应用声音设置
          window.speechSynthesis.onvoiceschanged = null
        }
        window.speechSynthesis.onvoiceschanged = handleVoicesChanged
        // 主动触发一次声音加载
        window.speechSynthesis.getVoices()
      } else {
        // 增加语音缓冲时间，确保播放流畅
        setTimeout(() => {
          // 开始播放
          console.log('开始播放语音')
          window.speechSynthesis.speak(utterance)
          isPlayingGuidance.value = true
        }, 100) // 100ms缓冲时间，避免播放卡顿
      }
    }
    
    // 停止引导语音
    const stopGuidanceSpeech = () => {
      window.speechSynthesis.cancel()
      isPlayingGuidance.value = false
    }

    // 心灵镜像对话框相关
    const showMindMirrorDialog = ref(false)
    
    const closeMindMirrorDialog = () => {
      showMindMirrorDialog.value = false
    }
    
    // 生成疗愈小故事
    const generateHealingStory = async () => {
      if (!analysisResult.value) {
        console.log('无法生成疗愈故事：没有分析结果')
        return
      }
      
      isGeneratingStory.value = true
      healingStory.value = null
      
      try {
        console.log('尝试直接使用分析数据生成疗愈故事...')
        
        // 调用新的API端点，直接传递分析结果
        const response = await axios.post('/api/v1/paintings/generate-story-direct', {
          analysis_result: analysisResult.value
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          timeout: 30000 // 设置30000ms超时，因为AI生成需要更多时间
        })
        
        healingStory.value = response.data.story
        console.log('疗愈故事生成成功')
      } catch (error) {
        console.error('生成疗愈故事失败:', error)
        // 失败时使用默认故事
        healingStory.value = '在一片绿意盎然的森林中，你发现了一面神奇的镜子。当你望向镜中，看到的不仅是自己，还有无数可能。每一片落叶都代表一个过去的烦恼，每一道阳光都预示着新的希望。深呼吸，感受大自然的治愈力量，你会发现，内心的平静一直都在那里，等待你去发现。'
      } finally {
        isGeneratingStory.value = false
      }
    }

    return {
      goBack,
      drawingCanvas,
      currentColor,
      brushSize,
      brushType,
      currentTool,
      isGeneratingStory,
      healingStory,
      generateHealingStory,
      isGeneratingMindMirror,
        mindMirrorResult,
        generateIntervention,
        showMindMirrorDialog,
        closeMindMirrorDialog,
        originalPaintingPreview,
        positivePaintingPreview,
      eraserType,
      analysisResult,
      history,
      showCanvasList,
      showModeSelection,
      showThemeSelection,
      currentPaintingMode,
      themeOptions,
      selectedTheme,
      savedCanvases,
      filteredCanvases,
      currentCanvasId,
      currentCanvasName,
      isDefaultName,
      showRenameModal,
      newCanvasName,
      startDrawing,
      draw,
      stopDrawing,
      clearCanvas,
      selectTool,
      undo,
      saveCanvas,
      createNewCanvas,
      loadCanvas,
      deleteCanvas,
      showRenameDialog,
      closeRenameDialog,
      confirmRename,
      analyzeDrawing,
      generateAndPlayMindfulnessGuidance,
      isGeneratingGuidance,
      currentGuidance,
      isPlayingGuidance,
      stopGuidanceSpeech,
      selectPaintingMode,
      selectTheme,
      showMoodRadarChart,
      getStressLevelClass,
      getTimeCategoryText,
      formatMarkdownAnalysis,
      generateColorAnalysis,
      generateBrushAnalysis,
        generateCompositionAnalysis,
        showPaintingPrompt,
        paintingPrompt
    }
  }
}
</script>

<style scoped>
/* 绘画提示区域样式 */
.painting-prompt {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 16px;
  padding: 20px 24px;
  margin-bottom: 18px;
  text-align: center;
  font-size: 16px;
  line-height: 1.7;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
  border: 1px solid #e2e8f0;
  border-left: 5px solid #6366f1;
  color: #475569;
  font-weight: 500;
  animation: promptSlideIn 0.6s ease-out;
  transition: all 0.3s ease;
}

.painting-prompt:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

@keyframes promptSlideIn {
  from {
    opacity: 0;
    transform: translateY(10px) translateX(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0) translateX(0);
  }
}

/* 情绪状态描述区域 */
.mood-description-section {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.mood-description-content {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
}

/* 多维度分析网格布局 */
.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

/* 分析卡片样式 - 优化设计 */
.analysis-card {
  background: #ffffff;
  border-radius: 14px;
  padding: 18px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid #f0f0f0;
}

.analysis-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* 卡片头部样式 */
.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0f0f0;
}

.card-icon {
  font-size: 24px;
  margin-right: 12px;
}

.card-header h4 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #374151;
}

/* 卡片类型特定样式 */
.card-color {
  border-top: 4px solid #ec4899;
}

.card-brush {
  border-top: 4px solid #3b82f6;
}

.card-composition {
  border-top: 4px solid #10b981;
}

.card-color .card-header h4 {
  color: #be185d;
}

.card-brush .card-header h4 {
  color: #1d4ed8;
}

.card-composition .card-header h4 {
  color: #059669;
}

/* 分析内容样式 */
.analysis-content {
  font-size: 17px;
  line-height: 1.7;
}

.analysis-content h4 {
  color: #4b5563;
  font-size: 18px;
  margin-top: 14px;
  margin-bottom: 10px;
  font-weight: 600;
}

.analysis-content strong {
  color: #111827;
  font-size: 17px;
}

.analysis-content ul {
  padding-left: 20px;
  margin-bottom: 14px;
}

.analysis-content li {
  margin-bottom: 8px;
  line-height: 1.7;
  color: #6b7280;
  font-size: 17px;
}

/* 改进的分析内容样式 */
.analysis-content-improved {
  font-size: 18px;
  line-height: 1.8;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.analysis-content-improved h4 {
  color: #2c3e50;
  font-size: 22px;
  margin: 0 0 15px 0;
  font-weight: 700;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 8px;
}

.analysis-content-improved p {
  margin: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.analysis-content-improved p strong {
  color: #111827;
  font-size: 19px;
  font-weight: 700;
  flex: 1;
  margin-right: 15px;
}

.analysis-content-improved p span {
  color: #2c3e50;
  font-size: 19px;
  font-weight: 600;
  text-align: right;
}

.analysis-content br {
  display: block;
  margin: 12px 0;
  content: '';
}

/* 多维度分析卡片样式 */
.multi-dimension-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border-left: 4px solid #6366f1;
}

.multi-dimension-card .analysis-content h4 {
  color: #4f46e5;
  font-size: 18px;
  margin-top: 20px;
  margin-bottom: 12px;
  font-weight: 600;
}

.multi-dimension-card .analysis-content ul {
  padding-left: 20px;
  margin-bottom: 16px;
}

.multi-dimension-card .analysis-content li {
  margin-bottom: 8px;
  line-height: 1.5;
  color: #4b5563;
}

.multi-dimension-card .analysis-content br {
  display: block;
  margin: 8px 0;
  content: '';
}

/* 针对性建议部分 */
.suggestions-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.suggestions-section h4 {
  color: #10b981;
  font-size: 18px;
  margin-bottom: 12px;
  font-weight: 600;
}

.suggestions-content {
  font-size: 16px;
  line-height: 1.6;
  color: #4b5563;
  background-color: #f0fdf4;
  padding: 16px;
  border-radius: 8px;
  border-left: 3px solid #10b981;
}
.mind-painting-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  min-height: 100vh;
  border-radius: 8px;
}

/* 分析结果样式 */
.analysis-result {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 30px;
  margin-top: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.analysis-result h2 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
  font-size: 28px;
  font-weight: 700;
}

.analysis-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.stress-meter {
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
  border-radius: 12px;
  padding: 25px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(255, 154, 158, 0.2);
}

.stress-meter h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 20px;
}

.stress-index-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stress-index-value {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.stress-level-low {
  color: #27ae60;
}

.stress-level-medium {
  color: #f39c12;
}

.stress-level-high {
  color: #e74c3c;
}

.stress-level-label {
  font-size: 18px;
  color: #555;
  font-weight: 600;
}

.painting-info {
  background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 15px rgba(161, 196, 253, 0.2);
}

.painting-info h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 20px;
}

.painting-info p {
  color: #34495e;
  margin-bottom: 10px;
  font-size: 16px;
  line-height: 1.6;
}

.painting-info p strong {
  color: #2c3e50;
}

.mood-radar-section {
  margin-bottom: 20px;
  text-align: center;
}

.mood-radar-section h3 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 24px;
}

.mood-radar-chart {
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.radar-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  aspect-ratio: 1/1;
  margin: 0;
}

.radar-container canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.personality-portrait {
  margin-bottom: 40px;
  background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(212, 252, 121, 0.2);
}

.personality-portrait h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 24px;
  text-align: center;
}

.portrait-content {
  color: #2c3e50;
  font-size: 18px;
  line-height: 1.8;
  font-weight: 500;
  text-align: justify;
}

.detailed-analysis h3 {
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 24px;
  text-align: center;
}

.analysis-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 25px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border-left: 5px solid #3498db;
}

.analysis-card h4 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 20px;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.analysis-item {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.analysis-item .label {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 8px;
}

.analysis-item .value {
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
}

.analysis-actions {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 40px auto;
  flex-wrap: wrap;
  max-width: 1200px;
  padding: 35px;
}

/* 高亮区域样式 */
.highlighted-section {
  border-top: 5px solid #667eea;
  border-bottom: 5px solid #667eea;
  background-color: rgba(102, 126, 234, 0.1);
  border-radius: 15px;
}

/* 统一样式的操作按钮 */
.action-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 28px 56px;
  border-radius: 45px;
  font-size: 24px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
  display: inline-flex;
  align-items: center;
  gap: 16px;
  min-width: 220px;
  justify-content: center;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  line-height: 1.4;
}

.action-button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.action-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.primary-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.primary-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.success-button {
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(82, 196, 26, 0.3);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.success-button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(82, 196, 26, 0.4);
}

.success-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.secondary-button {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
}

.secondary-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(240, 147, 251, 0.4);
}

/* 模式选择页面样式 */
.mode-selection-container {
  text-align: center;
}

.mode-selection-title {
  color: #2c3e50;
  margin-bottom: 40px;
  font-size: 28px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.mode-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.mode-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 2px solid transparent;
}

.mode-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.mode-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.mode-card h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 24px;
}

.mode-description {
  color: #555;
  margin-bottom: 20px;
  line-height: 1.6;
  font-size: 16px;
}

.mode-examples {
  text-align: left;
  background: rgba(0, 123, 255, 0.05);
  padding: 15px;
  border-radius: 10px;
  margin-top: 20px;
}

.mode-examples p {
  color: #007bff;
  font-weight: 600;
  margin-bottom: 10px;
  font-size: 14px;
}

.mode-examples ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.mode-examples li {
  color: #666;
  margin-bottom: 5px;
  font-size: 14px;
  line-height: 1.5;
}

/* 主题选择页面样式 */
.theme-selection-container {
  text-align: center;
}

.theme-selection-title {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 28px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.theme-selection-subtitle {
  color: #555;
  margin-bottom: 40px;
  font-size: 18px;
}

.theme-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.theme-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(245, 247, 250, 0.95));
  border-radius: 20px;
  padding: 30px 25px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(15px);
  border: 2px solid transparent;
  text-align: center;
  min-height: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.theme-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
  transition: left 0.5s ease;
}

.theme-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 15px 30px rgba(0, 123, 255, 0.25);
  border-color: #007bff;
  background: linear-gradient(135deg, rgba(255, 255, 255, 1), rgba(240, 245, 255, 1));
}

.theme-card:hover::before {
  left: 100%;
}

.theme-icon {
  font-size: 42px;
  margin-bottom: 18px;
  transition: transform 0.3s ease;
  z-index: 1;
}

.theme-card:hover .theme-icon {
  transform: scale(1.2) rotate(5deg);
}

.theme-text {
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
  line-height: 1.6;
  margin: 0;
  z-index: 1;
  transition: color 0.3s ease;
}

.theme-card:hover .theme-text {
  color: #007bff;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .theme-options {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
  }
  
  .theme-card {
    min-height: 140px;
    padding: 20px;
  }
  
  .theme-icon {
    font-size: 36px;
    margin-bottom: 12px;
  }
  
  .theme-text {
    font-size: 14px;
  }
}

.theme-card:hover .theme-icon {
  opacity: 1;
  transform: scale(1.1);
  transition: all 0.3s ease;
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 20px;
  flex-wrap: wrap;
}

.page-header h1 {
  flex: 1;
  min-width: 200px;
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

/* 画布区域样式 */
.canvas-area {
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

canvas {
  background-color: white;
  border-top: 1px solid #ccc; /* 修改为上边框 */
  cursor: crosshair;
  width: 100%;
  max-width: 1200px; /* 进一步增大最大宽度 */
  height: 600px; /* 设置固定高度 */
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);
}

/* 工具栏样式 */
.tool-bar {
  padding: 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 1200px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.tool-section {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.tool-section label {
  font-weight: 600;
  color: #2c3e50;
  white-space: nowrap;
}

/* 画笔类型按钮 */
.brush-type-buttons, .eraser-buttons {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.brush-button, .eraser-button {
  background-color: #fff;
  border: 2px solid #ddd;
  border-radius: 5px;
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.brush-button:hover, .eraser-button:hover {
  background-color: #f0f0f0;
  border-color: #007bff;
}

.brush-button.active, .eraser-button.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

/* 颜色选择器 */
input[type="color"] {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

/* 滑块样式 */
input[type="range"] {
  width: 120px;
  height: 6px;
  background: #ddd;
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  background: #007bff;
  border-radius: 50%;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: #007bff;
  border-radius: 50%;
  cursor: pointer;
  border: none;
}

/* 操作按钮 */
.action-button {
  background-color: #007bff;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-button:hover:not(:disabled) {
  background-color: #0056b3;
}

.action-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 分析结果样式 */
.analysis-result {
  background-color: #e8f5e9;
  padding: 20px;
  border-radius: 10px;
  margin-top: 30px;
  text-align: left;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.analysis-result h2 {
  color: #4CAF50;
  margin-bottom: 15px;
}

.analysis-result p {
  margin-bottom: 10px;
  color: #333;
}

/* 画布列表样式 */
.canvas-list-container {
  width: 100%;
}

.canvas-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 15px;
}

.canvas-list-header h2 {
  color: #2c3e50;
  margin: 0;
}

.new-canvas-button {
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  border: none;
  border-radius: 25px;
  padding: 12px 25px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(76, 175, 80, 0.3);
}

.new-canvas-button:hover {
  background: linear-gradient(135deg, #45a049, #3d8b40);
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(76, 175, 80, 0.4);
}

.canvas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.canvas-item {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.canvas-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
}

.canvas-thumbnail {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  cursor: pointer;
  background-color: #f5f5f5;
}

.canvas-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.canvas-thumbnail:hover img {
  transform: scale(1.05);
}

.canvas-name {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 10px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  color: white;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.canvas-actions {
  display: flex;
  justify-content: space-around;
  padding: 15px;
  gap: 10px;
}

.rename-button, .delete-button {
  flex: 1;
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.rename-button {
  background-color: #2196F3;
  color: white;
}

.rename-button:hover {
  background-color: #1976D2;
}

.delete-button {
  background-color: #f44336;
  color: white;
}

.delete-button:hover {
  background-color: #d32f2f;
}

.no-canvases {
  text-align: center;
  padding: 60px 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.no-canvases p {
  font-size: 18px;
  color: #666;
  margin-bottom: 30px;
}

/* 画布信息显示 */
.canvas-info {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 255, 255, 0.8);
  padding: 8px 15px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.canvas-name-display {
  font-weight: 600;
  color: #2c3e50;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rename-button-small {
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 15px;
  padding: 5px 12px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.rename-button-small:hover {
  background-color: #1976D2;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
  overflow: hidden; /* 防止滚动 */
}

.rename-modal {
  background: white;
  border-radius: 12px;
  padding: 30px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.rename-modal h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #2c3e50;
}

.rename-modal input[type="text"] {
  width: 100%;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  margin-bottom: 20px;
  transition: border-color 0.2s ease;
}

.rename-modal input[type="text"]:focus {
  outline: none;
  border-color: #007bff;
}

.modal-buttons {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
}

.modal-buttons button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.modal-buttons button:first-child {
  background-color: #f0f0f0;
  color: #333;
}

.modal-buttons button:first-child:hover {
  background-color: #e0e0e0;
}

.modal-buttons button:last-child {
  background-color: #007bff;
  color: white;
}

.modal-buttons button:last-child:hover {
    background-color: #0056b3;
  }
  
  /* 多维度分析网格布局 */
  .analysis-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 24px;
    margin-bottom: 24px;
  }
  
  .analysis-card {
    background-color: #ffffff;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #f0f0f0;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .analysis-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  }
  
  .card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid #f3f4f6;
  }
  
  .card-icon {
    font-size: 24px;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f8fafc;
    border-radius: 8px;
  }
  
  .analysis-card h4 {
    margin: 0;
    color: #1e293b;
    font-size: 1.2rem;
    font-weight: 600;
  }
  
  /* 为不同类型的卡片设置不同的主题色 */
  .analysis-card.card-color .card-header {
    border-color: #ff6b6b;
  }
  
  .analysis-card.card-brush .card-header {
    border-color: #4ecdc4;
  }
  
  .analysis-card.card-composition .card-header {
    border-color: #45b7d1;
  }
  
  .analysis-content {
    color: #555;
    line-height: 1.6;
  }

  /* 响应式设计 */
@media (max-width: 768px) {
  .tool-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .tool-section {
    justify-content: center;
  }

  .canvas-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .canvas-info {
    width: 100%;
    justify-content: space-between;
  }
}
/* 疗愈小故事相关样式 */
  .info-button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    margin: 0 10px;
    transition: background-color 0.3s;
  }
  
  .info-button:hover:not(:disabled) {
    background-color: #2980b9;
  }
  
  .info-button:disabled {
    background-color: #95a5a6;
    cursor: not-allowed;
  }
  
  .healing-story-section {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  }
  
  .healing-story-section h3 {
    color: #343a40;
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 20px;
  }
  
  .healing-story-content {
    color: #495057;
    line-height: 1.6;
    font-size: 16px;
    background-color: white;
    padding: 15px;
    border-radius: 5px;
    border-left: 4px solid #3498db;
  }
  
  /* 心灵镜像对话框样式 */
  .mind-mirror-modal {
    background: white;
    border-radius: 15px;
    width: 90%;
    max-width: 1000px;
    max-height: 85vh;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    animation: modalSlideIn 0.3s ease-out;
    display: flex;
    flex-direction: column;
  }
  
  /* 积极版本描述样式 */
  .positive-image-description {
    background-color: #e3f2fd;
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
    border-left: 4px solid #2196f3;
    line-height: 1.6;
    font-size: 16px;
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 30px;
    border-bottom: 1px solid #e5e7eb;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 15px 15px 0 0;
  }
  
  .modal-header h3 {
    margin: 0;
    font-size: 24px;
    font-weight: 700;
  }
  
  .close-button {
    background: none;
    border: none;
    color: white;
    font-size: 28px;
    cursor: pointer;
    padding: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background-color 0.3s;
  }
  
  .close-button:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }
  
  .modal-content {
    padding: 30px;
    overflow-y: auto;
    max-height: calc(85vh - 150px); /* 确保内容区域不会挤压页脚 */
  }
  
  .modal-footer {
    padding: 20px 30px;
    border-top: 1px solid #e5e7eb;
    display: flex;
    justify-content: center;
  }
  
  .mind-mirror-container {
    display: flex;
    flex-direction: column;
    gap: 30px;
  }
  
  .painting-comparison {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    flex-wrap: wrap;
  }
  
  .painting-item {
    flex: 1;
    min-width: 250px;
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .painting-item h4 {
    text-align: center;
    color: #2c3e50;
    font-size: 18px;
    margin: 0;
  }
  
  .painting-preview {
    width: 100%;
    height: 250px;
    background-color: #f8f9fa;
    border: 2px dashed #ced4da;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }
  
  .painting-preview canvas {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
  
  .arrow-icon {
    font-size: 36px;
    color: #667eea;
    margin: 0 20px;
    animation: pulse 2s infinite;
  }
  
  .positive-version {
    width: 100%;
    height: 250px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border: 2px solid #667eea;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    position: relative;
    overflow: hidden;
  }
  
  .sunshine-animation {
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 48px;
    animation: rotate 10s linear infinite;
  }
  
  .positive-description {
    font-size: 18px;
    color: #2c3e50;
    text-align: center;
    line-height: 1.6;
    font-weight: 500;
    z-index: 1;
    padding: 15px;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
  }
  
  .guidance-text {
    background-color: #fff3cd;
    border: 2px solid #ffeaa7;
    border-radius: 12px;
    padding: 25px;
    display: flex;
    align-items: flex-start;
    gap: 20px;
  }
  
  .guidance-icon {
    font-size: 32px;
    flex-shrink: 0;
    margin-top: 5px;
  }
  
  .guidance-text p {
    font-size: 20px;
    color: #856404;
    line-height: 1.8;
    font-weight: 600;
    margin: 0;
  }
  
  .reflection-section {
    background-color: #e8f5e8;
    border: 2px solid #c3e6cb;
    border-radius: 12px;
    padding: 25px;
  }
  
  .reflection-section h4 {
    color: #155724;
    font-size: 20px;
    margin-top: 0;
    margin-bottom: 20px;
  }
  
  .reflection-section p {
    font-size: 18px;
    color: #155724;
    line-height: 1.8;
    margin: 12px 0;
  }
  
  @keyframes modalSlideIn {
    from {
      opacity: 0;
      transform: translateY(-50px) scale(0.9);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }
  
  @keyframes pulse {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.2);
    }
  }
  
  @keyframes rotate {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  
  /* 响应式设计 */
  @media (max-width: 768px) {
    .painting-comparison {
      flex-direction: column;
    }
    
    .arrow-icon {
      transform: rotate(90deg);
      margin: 20px 0;
    }
    
    .guidance-text {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
    
    .mind-mirror-modal {
      width: 95%;
      margin: 10px;
      max-width: none;
    }
  }
  </style>

