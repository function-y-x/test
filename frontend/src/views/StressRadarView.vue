<template>
  <div class="stress-radar-container">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span>
        返回主界面
      </button>
      <h1>压力雷达</h1>
    </div>
    
    <!-- 睡眠时长记录和考研倒计时区域 -->
    <div class="info-cards-container">
      <!-- 睡眠时长记录卡片 -->
      <div class="sleep-record-card">
        <div class="card-icon">😴</div>
        <div v-if="!todaySleepRecorded" class="sleep-input-container">
          <label for="sleepHours">记录昨日睡眠时长（小时）：</label>
          <input 
            type="number" 
            id="sleepHours" 
            v-model="sleepHours" 
            min="0" 
            max="24" 
            step="0.5"
            placeholder="请输入睡眠时长"
          />
          <button @click="submitSleepHours" class="submit-sleep-btn">提交</button>
        </div>
        <div v-else class="sleep-display">
          <div class="sleep-text">昨日睡眠时长</div>
          <div class="sleep-value">{{ todaySleepHours }} 小时</div>
        </div>
      </div>

      <!-- 考研倒计时卡片 -->
      <div class="countdown-card">
        <div class="card-icon">📚</div>
        <div class="countdown-content">
          <div class="countdown-title">考研倒计时</div>
          
          <!-- 日期编辑区域 -->
          <div class="exam-date-editor">
            <input 
              type="date" 
              v-model="editableExamDate" 
              @change="updateExamDate"
              class="exam-date-input"
              :min="today"
            />
            <button 
              v-if="isExamDateChanged" 
              @click="saveExamDate"
              class="save-date-btn"
              :disabled="isSaving"
            >
              {{ isSaving ? '保存中...' : '保存' }}
            </button>
          </div>
          
          <div class="countdown-days">
            <span class="days-number">{{ daysUntilExam }}</span>
            <span class="days-text">天</span>
          </div>
          <div class="countdown-message">{{ motivationalMessage }}</div>
        </div>
      </div>
    </div>
    
    <p>这里将展示您的考试倒计时、模考趋势、睡眠与任务完成度叠图，并提供一键"处方"生成器。</p>
    
    <!-- 图表区域 -->
    <div class="chart-container">
      <canvas id="stressRadarChart"></canvas>
    </div>

    <!-- 日历区域 -->
    <div class="calendar-section">
      <h2 class="section-title">📅 学习日历</h2>
      <p class="section-description">点击日期可以添加标注，记录您的学习DDL和进度</p>
      <InteractiveCalendar />
    </div>
    
    <!-- 一键生成处方按钮 -->
    <button 
      class="prescription-button" 
      @click="generatePrescription"
      :disabled="isGenerating"
    >
      {{ isGenerating ? '正在生成中...' : '一键生成压力处方' }}
    </button>

    <!-- 压力处方显示区域 -->
    <div v-if="showPrescription" class="prescription-result">
      <div class="prescription-header">
        <h3>📋 压力处方分析</h3>
        <button @click="closePrescription" class="close-btn">×</button>
      </div>
      
      <!-- 压力来源分析 -->
      <div v-if="prescriptionData.analysis" class="stress-analysis">
        <h4>压力来源分析</h4>
        <div class="source-item" v-for="source in prescriptionData.analysis.main_sources" :key="source.source">
          <div class="source-name">{{ source.name }}</div>
          <div class="source-bar-container">
            <div 
              class="source-bar" 
              :style="{ 
                width: `${source.score}%`,
                backgroundColor: getSourceColor(source.score)
              }"
            ></div>
            <span class="source-score">{{ source.score.toFixed(0) }}分</span>
          </div>
        </div>
        <div class="total-score">
          总体压力指数: <strong>{{ prescriptionData.analysis.total_score.toFixed(1) }}/100</strong>
        </div>
      </div>
      
      <!-- AI 生成的处方内容 -->
      <div class="prescription-content">
        <h4>🔮 AI 处方建议</h4>
        <div 
          class="prescription-text" 
          v-html="renderedPrescription"
        ></div>
        <span v-if="isGenerating" class="typing-cursor">|</span>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import Chart from 'chart.js/auto'
import axios from 'axios'
import { marked } from 'marked'
import InteractiveCalendar from '@/components/InteractiveCalendar.vue'

export default {
  name: 'StressRadarView',
  components: {
    InteractiveCalendar
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const chartInstance = ref(null)
    const sleepHours = ref(null)
    const todaySleepRecorded = ref(false)
    const todaySleepHours = ref(0)
    
    // 考研倒计时相关数据 - 从用户信息中获取
    const user = computed(() => authStore.getUser)
    
    // 可编辑的考研日期
    const editableExamDate = ref('')
    const originalExamDate = ref('')
    const isSaving = ref(false)
    
    // 今天的日期（用于日期选择器的最小值）
    const today = computed(() => {
      return new Date().toISOString().split('T')[0]
    })
    
    // 初始化考研日期
    const initExamDate = () => {
      if (user.value?.exam_date) {
        // 从 ISO 字符串中直接提取日期部分，避免时区转换
        editableExamDate.value = user.value.exam_date.split('T')[0]
      } else {
        editableExamDate.value = '2025-12-27'
      }
      originalExamDate.value = editableExamDate.value
    }
    
    // 检查日期是否被修改
    const isExamDateChanged = computed(() => {
      return editableExamDate.value !== originalExamDate.value
    })
    
    // 当前使用的考研日期
    const examDate = computed(() => editableExamDate.value)
    
    // 计算距离考研还有多少天
    const daysUntilExam = computed(() => {
      const today = new Date()
      const exam = new Date(examDate.value)
      const diffTime = exam - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      return diffDays > 0 ? diffDays : 0
    })
    
    // 根据剩余天数生成激励语
    const motivationalMessage = computed(() => {
      const days = daysUntilExam.value
      if (days > 300) {
        return '时间充裕，稳扎稳打！💪'
      } else if (days > 180) {
        return '冲刺阶段，全力以赴！🔥'
      } else if (days > 100) {
        return '百日冲刺，再接再厉！⚡'
      } else if (days > 30) {
        return '最后一搏，你能行！🎯'
      } else if (days > 0) {
        return '决战在即，加油！🚀'
      } else {
        return '考试已结束，期待好成绩！🎉'
      }
    })

    const goBack = () => {
      router.push('/dashboard')
    }

    // 更新考研日期（当用户修改日期时）
    const updateExamDate = () => {
      // 日期选择器值变化时自动触发
      console.log('考研日期已修改为:', editableExamDate.value)
    }

    // 保存考研日期到后端
    const saveExamDate = async () => {
      if (!editableExamDate.value) {
        alert('请选择考研日期')
        return
      }

      isSaving.value = true
      try {
        const token = authStore.getToken
        if (!token) {
          alert('请先登录')
          return
        }

        // 将日期转换为 UTC 时间的午夜零点，避免时区问题
        const dateToSave = new Date(editableExamDate.value + 'T00:00:00Z').toISOString()

        const response = await axios.put('/auth/me', {
          exam_date: dateToSave
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        // 使用后端返回的最新用户信息更新本地存储
        if (response.data) {
          localStorage.setItem('user', JSON.stringify(response.data))
          authStore.user = response.data
        }

        originalExamDate.value = editableExamDate.value
        alert('考研日期保存成功！')
      } catch (error) {
        console.error('保存考研日期失败:', error)
        alert(error.response?.data?.detail || '保存失败，请稍后重试')
      } finally {
        isSaving.value = false
      }
    }

    // 检查今天是否已记录睡眠时长
    const checkTodaySleepRecord = async () => {
      try {
        const token = authStore.getToken
        if (!token) return

        const response = await axios.get('/sleeps/today', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.data) {
          todaySleepRecorded.value = true
          todaySleepHours.value = response.data.sleep_hours
        }
      } catch (error) {
        // 404表示今天还没有记录，这是正常情况
        if (error.response?.status !== 404) {
          console.error('检查睡眠记录失败:', error)
        }
      }
    }

    // 提交睡眠时长
    const submitSleepHours = async () => {
      if (!sleepHours.value || sleepHours.value < 0 || sleepHours.value > 24) {
        alert('请输入有效的睡眠时长（0-24小时）')
        return
      }

      try {
        const token = authStore.getToken
        if (!token) {
          alert('请先登录')
          return
        }

        await axios.post('/sleeps/', {
          sleep_hours: parseFloat(sleepHours.value)
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        todaySleepRecorded.value = true
        todaySleepHours.value = sleepHours.value
        alert('睡眠时长记录成功！')
        
        // 重新加载图表数据
        fetchWeeklyData()
      } catch (error) {
        console.error('提交睡眠时长失败:', error)
        alert(error.response?.data?.detail || '提交失败，请稍后重试')
      }
    }

    // 获取近一周的情绪数据和睡眠数据
    const fetchWeeklyData = async () => {
      const token = authStore.getToken
      if (!token) {
        console.log('未找到认证token，使用默认数据')
        createDefaultChart()
        return
      }

      try {
        // 同时获取情绪数据和睡眠数据
        const [moodResponse, sleepResponse] = await Promise.all([
          axios.get('/moods/weekly-scores', {
            headers: { 'Authorization': `Bearer ${token}` }
          }),
          axios.get('/sleeps/weekly-data', {
            headers: { 'Authorization': `Bearer ${token}` }
          })
        ])

        console.log('周情绪数据:', moodResponse.data)
        console.log('周睡眠数据:', sleepResponse.data)

        if (moodResponse.data?.success && sleepResponse.data?.success) {
          const moodData = moodResponse.data.data
          const sleepData = sleepResponse.data.data
          
          // 提取日期标签（格式：MM-DD）
          const labels = moodData.map(day => {
            const date = new Date(day.date)
            const month = String(date.getMonth() + 1).padStart(2, '0')
            const dayNum = String(date.getDate()).padStart(2, '0')
            return `${month}-${dayNum}`
          })
          
          // 提取压力得分和睡眠时长
          const stressScores = moodData.map(day => day.score)
          const sleepHours = sleepData.map(day => day.sleep_hours)
          
          // 创建图表
          createChart(labels, stressScores, sleepHours, moodData, sleepData)
        } else {
          createDefaultChart()
        }
      } catch (error) {
        console.error('获取周数据失败:', error)
        createDefaultChart()
      }
    }

    // 创建图表
    const createChart = (labels, stressScores, sleepHours, moodData, sleepData) => {
      const ctx = document.getElementById('stressRadarChart')
      
      // 如果已有图表实例，先销毁
      if (chartInstance.value) {
        chartInstance.value.destroy()
      }

      chartInstance.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: '压力指数',
              data: stressScores,
              borderColor: 'rgb(255, 99, 132)',
              backgroundColor: 'rgba(255, 99, 132, 0.1)',
              tension: 0.4,
              fill: true,
              pointRadius: 6,
              pointHoverRadius: 8,
              pointBackgroundColor: 'rgb(255, 99, 132)',
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              yAxisID: 'y'
            },
            {
              label: '睡眠时长（小时）',
              data: sleepHours,
              borderColor: 'rgb(75, 192, 192)',
              backgroundColor: 'rgba(75, 192, 192, 0.1)',
              tension: 0.4,
              fill: true,
              pointRadius: 6,
              pointHoverRadius: 8,
              pointBackgroundColor: 'rgb(75, 192, 192)',
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              yAxisID: 'y1'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false
          },
          plugins: {
            title: {
              display: true,
              text: '近一周压力与睡眠趋势',
              font: {
                size: 18,
                weight: 'bold'
              },
              padding: 20
            },
            legend: {
              display: true,
              position: 'top'
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const datasetLabel = context.dataset.label
                  const value = context.parsed.y
                  if (datasetLabel === '压力指数') {
                    return `压力指数: ${value}`
                  } else {
                    return `睡眠时长: ${value}小时`
                  }
                },
                footer: function(tooltipItems) {
                  // 只显示一次通用信息
                  const index = tooltipItems[0].dataIndex
                  const dayData = moodData[index]
                  const sleepInfo = sleepData[index]
                  return [
                    `完整日期: ${dayData.date}`,
                    `星期: ${dayData.weekday}`,
                    `压力记录数: ${dayData.count}次`,
                    sleepInfo.has_data ? '有睡眠记录' : '默认睡眠时长'
                  ].join('\n')
                }
              }
            }
          },
          scales: {
            y: {
              type: 'linear',
              display: true,
              position: 'left',
              beginAtZero: true,
              max: 10,
              title: {
                display: true,
                text: '压力等级 (1-10)',
                font: {
                  size: 14
                }
              },
              ticks: {
                stepSize: 1
              }
            },
            y1: {
              type: 'linear',
              display: true,
              position: 'right',
              beginAtZero: true,
              max: 12,
              title: {
                display: true,
                text: '睡眠时长（小时）',
                font: {
                  size: 14
                }
              },
              grid: {
                drawOnChartArea: false
              }
            },
            x: {
              title: {
                display: true,
                text: '日期 (月-日)',
                font: {
                  size: 14
                }
              }
            }
          }
        }
      })
    }

    // 创建默认图表（没有数据时）
    const createDefaultChart = () => {
      const ctx = document.getElementById('stressRadarChart')
      
      if (chartInstance.value) {
        chartInstance.value.destroy()
      }

      // 生成近7天的日期标签
      const labels = []
      for (let i = 6; i >= 0; i--) {
        const date = new Date()
        date.setDate(date.getDate() - i)
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const day = String(date.getDate()).padStart(2, '0')
        labels.push(`${month}-${day}`)
      }

      chartInstance.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: '压力指数（暂无数据）',
              data: [5, 5, 5, 5, 5, 5, 5],
              borderColor: 'rgba(255, 99, 132, 0.5)',
              backgroundColor: 'rgba(255, 99, 132, 0.1)',
              tension: 0.4,
              fill: true,
              borderDash: [5, 5],
              yAxisID: 'y'
            },
            {
              label: '睡眠时长（默认）',
              data: [7, 7, 7, 7, 7, 7, 7],
              borderColor: 'rgba(75, 192, 192, 0.5)',
              backgroundColor: 'rgba(75, 192, 192, 0.1)',
              tension: 0.4,
              fill: true,
              borderDash: [5, 5],
              yAxisID: 'y1'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: '近一周压力与睡眠趋势（暂无数据）',
              font: {
                size: 18
              }
            },
            legend: {
              display: true,
              position: 'top'
            }
          },
          scales: {
            y: {
              type: 'linear',
              display: true,
              position: 'left',
              beginAtZero: true,
              max: 10,
              title: {
                display: true,
                text: '压力等级 (1-10)'
              }
            },
            y1: {
              type: 'linear',
              display: true,
              position: 'right',
              beginAtZero: true,
              max: 12,
              title: {
                display: true,
                text: '睡眠时长（小时）'
              },
              grid: {
                drawOnChartArea: false
              }
            },
            x: {
              title: {
                display: true,
                text: '日期 (月-日)'
              }
            }
          }
        }
      })
    }

    // 配置 marked 选项
    marked.setOptions({
      breaks: true,        // 支持换行
      gfm: true,          // GitHub 风格 Markdown
      headerIds: false,   // 不生成 header id
      mangle: false       // 不混淆邮箱
    })

    // 压力处方相关
    const isGenerating = ref(false)
    const showPrescription = ref(false)
    const prescriptionData = ref({
      analysis: null,
      prescription: ''
    })

    // 实时渲染 Markdown
    const renderedPrescription = computed(() => {
      if (!prescriptionData.value.prescription) {
        return '<p style="color: #999;">AI 正在分析中...</p>'
      }
      try {
        return marked.parse(prescriptionData.value.prescription)
      } catch (e) {
        return prescriptionData.value.prescription
      }
    })

    // 生成压力处方
    const generatePrescription = async () => {
      try {
        const token = authStore.getToken
        if (!token) {
          alert('请先登录')
          return
        }

        isGenerating.value = true
        showPrescription.value = true
        prescriptionData.value = {
          analysis: null,
          prescription: ''
        }

        // 使用 fetch 进行流式接收（支持自定义 headers）
        const apiUrl = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000/api/v1'
        const response = await fetch(`${apiUrl}/stress-prescription/generate`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()

        // eslint-disable-next-line no-constant-condition
        while (true) {
          const { done, value } = await reader.read()
          
          if (done) {
            isGenerating.value = false
            break
          }

          // 解码数据
          const chunk = decoder.decode(value, { stream: true })
          const lines = chunk.split('\n')

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const dataStr = line.substring(6).trim()
              
              if (dataStr === '[DONE]') {
                isGenerating.value = false
                break
              }

              try {
                const data = JSON.parse(dataStr)
                
                if (data.type === 'analysis') {
                  // 接收压力分析数据
                  prescriptionData.value.analysis = data.data
                } else if (data.type === 'prescription') {
                  // 流式接收处方文本
                  prescriptionData.value.prescription += data.content
                }
              } catch (e) {
                // 忽略解析错误
              }
            }
          }
        }

      } catch (error) {
        console.error('生成压力处方失败:', error)
        
        // 显示详细错误信息
        let errorMsg = '生成失败，请重试'
        if (error.message) {
          errorMsg += `\n错误信息: ${error.message}`
        }
        
        alert(errorMsg)
        isGenerating.value = false
        showPrescription.value = false
      }
    }

    // 关闭处方显示
    const closePrescription = () => {
      showPrescription.value = false
    }

    // 根据分数获取颜色
    const getSourceColor = (score) => {
      if (score < 20) return '#81c784'
      if (score < 40) return '#fdd835'
      if (score < 60) return '#ffb74d'
      if (score < 80) return '#ff8a65'
      return '#ef5350'
    }

    onMounted(() => {
      initExamDate()
      checkTodaySleepRecord()
      fetchWeeklyData()
    })

    return {
      goBack,
      sleepHours,
      todaySleepRecorded,
      todaySleepHours,
      submitSleepHours,
      editableExamDate,
      examDate,
      daysUntilExam,
      motivationalMessage,
      today,
      isExamDateChanged,
      isSaving,
      updateExamDate,
      saveExamDate,
      isGenerating,
      showPrescription,
      prescriptionData,
      renderedPrescription,
      generatePrescription,
      closePrescription,
      getSourceColor
    }
  }
}
</script>

<style scoped>
.stress-radar-container {
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

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

p {
  color: #555;
  margin-bottom: 30px;
}

.chart-container {
  width: 100%;
  height: 400px;
  margin-bottom: 30px;
}

.prescription-button {
  background-color: #007bff;
  color: white;
  padding: 15px 35px;
  font-size: 1.2em;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 50px;
  margin-bottom: 40px;
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}

.prescription-button:hover:not(:disabled) {
  background-color: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4);
}

.prescription-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  opacity: 0.6;
}

/* 压力处方显示区域 */
.prescription-result {
  background: white;
  border-radius: 16px;
  padding: 30px;
  margin-top: 30px;
  margin-bottom: 40px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.prescription-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
}

.prescription-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5em;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2em;
  color: #999;
  cursor: pointer;
  line-height: 1;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #333;
}

/* 压力来源分析 */
.stress-analysis {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 25px;
}

.stress-analysis h4 {
  margin: 0 0 15px 0;
  color: #495057;
  font-size: 1.1em;
}

.source-item {
  margin-bottom: 15px;
}

.source-name {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 8px;
  font-size: 1em;
}

.source-bar-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.source-bar {
  height: 25px;
  border-radius: 12px;
  transition: width 0.5s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.source-score {
  font-weight: bold;
  color: #666;
  min-width: 50px;
}

.total-score {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #dee2e6;
  font-size: 1.1em;
  color: #495057;
}

.total-score strong {
  color: #007bff;
  font-size: 1.2em;
}

/* AI 处方内容 */
.prescription-content {
  background: #f0f8ff;
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid #007bff;
}

.prescription-content h4 {
  margin: 0 0 15px 0;
  color: #007bff;
  font-size: 1.1em;
}

.prescription-text {
  line-height: 1.8;
  color: #2c3e50;
  font-size: 1em;
  word-wrap: break-word;
}

/* Markdown 渲染样式 */
.prescription-text :deep(h1),
.prescription-text :deep(h2),
.prescription-text :deep(h3),
.prescription-text :deep(h4) {
  color: #007bff;
  margin-top: 1em;
  margin-bottom: 0.5em;
  font-weight: bold;
}

.prescription-text :deep(h1) { font-size: 1.5em; }
.prescription-text :deep(h2) { font-size: 1.3em; }
.prescription-text :deep(h3) { font-size: 1.1em; }
.prescription-text :deep(h4) { font-size: 1em; }

.prescription-text :deep(p) {
  margin: 0.8em 0;
  line-height: 1.8;
}

.prescription-text :deep(strong) {
  color: #007bff;
  font-weight: bold;
}

.prescription-text :deep(em) {
  font-style: italic;
  color: #666;
}

.prescription-text :deep(ul),
.prescription-text :deep(ol) {
  margin: 1em 0;
  padding-left: 2em;
}

.prescription-text :deep(li) {
  margin: 0.5em 0;
  line-height: 1.6;
}

.prescription-text :deep(code) {
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
  color: #d63384;
}

.prescription-text :deep(blockquote) {
  border-left: 4px solid #007bff;
  padding-left: 1em;
  margin: 1em 0;
  color: #666;
  font-style: italic;
}

.prescription-text :deep(hr) {
  border: none;
  border-top: 2px solid #e0e0e0;
  margin: 1.5em 0;
}

.typing-cursor {
  display: inline-block;
  width: 2px;
  height: 1.2em;
  background-color: #007bff;
  animation: blink 1s step-end infinite;
  margin-left: 2px;
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0;
  }
}

.calendar-section {
  margin-top: 40px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.15);
}

.section-title {
  color: #2c3e50;
  margin: 0 0 10px 0;
  font-size: 1.8em;
  font-weight: 700;
  text-align: center;
}

.section-description {
  color: #666;
  text-align: center;
  margin-bottom: 30px;
  font-size: 1em;
}

/* 信息卡片容器 */
.info-cards-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .info-cards-container {
    grid-template-columns: 1fr;
  }
}

/* 睡眠记录卡片 */
.sleep-record-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.sleep-record-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.sleep-record-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #28a745, #20c997);
}

/* 考研倒计时卡片 */
.countdown-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.countdown-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.countdown-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #ff6b6b, #feca57);
}

.card-icon {
  font-size: 2.5em;
  text-align: center;
  margin-bottom: 15px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.sleep-input-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.sleep-input-container label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1em;
  text-align: center;
}

.sleep-input-container input {
  padding: 10px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1em;
  width: 150px;
  transition: border-color 0.3s ease;
  text-align: center;
}

.sleep-input-container input:focus {
  outline: none;
  border-color: #28a745;
}

.submit-sleep-btn {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  padding: 10px 25px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1em;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.submit-sleep-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
}

.sleep-display {
  text-align: center;
}

.sleep-text {
  font-size: 1em;
  color: #666;
  margin-bottom: 10px;
}

.sleep-value {
  font-size: 2.5em;
  font-weight: 700;
  background: linear-gradient(135deg, #28a745, #20c997);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 考研倒计时内容 */
.countdown-content {
  text-align: center;
}

.countdown-title {
  font-size: 1.2em;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 15px;
}

/* 日期编辑器 */
.exam-date-editor {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.exam-date-input {
  padding: 10px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1em;
  color: #2c3e50;
  transition: all 0.3s ease;
  cursor: pointer;
  background: white;
  font-weight: 500;
}

.exam-date-input:hover {
  border-color: #ff6b6b;
}

.exam-date-input:focus {
  outline: none;
  border-color: #ff6b6b;
  box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
}

.save-date-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #ff6b6b, #feca57);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.9em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.save-date-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
}

.save-date-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.countdown-days {
  margin: 20px 0;
}

.days-number {
  font-size: 3.5em;
  font-weight: 800;
  background: linear-gradient(135deg, #ff6b6b, #feca57);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  display: inline-block;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.days-text {
  font-size: 1.5em;
  font-weight: 600;
  color: #ff6b6b;
  margin-left: 5px;
}

.countdown-message {
  font-size: 1em;
  color: #666;
  font-weight: 500;
  margin-top: 15px;
  padding: 10px 20px;
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(254, 202, 87, 0.1));
  border-radius: 8px;
  display: inline-block;
}
</style>

