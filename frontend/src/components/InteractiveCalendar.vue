<template>
  <div class="calendar-container">
    <div class="calendar-header">
      <button class="nav-button" @click="previousMonth">
        <span>◀</span>
      </button>
      <h2 class="month-year">{{ currentMonthYear }}</h2>
      <button class="nav-button" @click="nextMonth">
        <span>▶</span>
      </button>
    </div>

    <div class="calendar-grid">
      <div class="weekday" v-for="day in weekDays" :key="day">{{ day }}</div>
      
      <div 
        v-for="(date, index) in calendarDays" 
        :key="index"
        class="calendar-day"
        :class="{ 
          'empty': !date, 
          'today': isToday(date),
          'other-month': date && !isCurrentMonth(date),
          'has-stress': date && getStressScore(date) > 0
        }"
        :style="{ 
          backgroundColor: date && getStressScore(date) > 0 ? getStressColor(getStressScore(date)) : (date ? '#ffffff' : 'transparent')
        }"
        @click="date && selectDate(date)"
      >
        <span 
          class="date-number" 
          v-if="date"
          :style="{ color: getStressScore(date) > 0 ? '#ffffff' : '#2c3e50' }"
        >
          {{ date.getDate() }}
        </span>
        <span 
          class="date-note" 
          v-if="date && dateNotes[formatDate(date)]"
          :style="{ color: getStressScore(date) > 0 ? '#ffffff' : '#666' }"
        >
          {{ dateNotes[formatDate(date)] }}
        </span>
        <!-- 紧张分数指示器 -->
        <div 
          v-if="date && getStressScore(date) > 0" 
          class="stress-indicator"
          :title="`紧张指数: ${getStressScore(date)} - ${getStressDescription(getStressScore(date))}`"
        >
          {{ getStressScore(date) }}
        </div>
      </div>
    </div>

    <!-- 日期标注弹窗 -->
    <div v-if="showNoteModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>标注日期: {{ formatDateDisplay(selectedDate) }}</h3>
          <button class="close-button" @click="closeModal">×</button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label>当日DDL:</label>
            <textarea 
              v-model="currentNote" 
              placeholder="输入计划..."
              rows="4"
            ></textarea>
          </div>

          <div class="form-group">
            <label>DDL进度: {{ currentProgress }}%</label>
            <div class="progress-slider-container">
              <input 
                type="range" 
                v-model="currentProgress" 
                min="0" 
                max="100" 
                step="5"
                class="progress-slider"
                @input="updateProgressDisplay"
              />
              <div class="progress-bar-bg">
                <div 
                  class="progress-bar-fill" 
                  :style="{ width: currentProgress + '%' }"
                ></div>
              </div>
              <div class="progress-labels">
                <span>0%</span>
                <span>25%</span>
                <span>50%</span>
                <span>75%</span>
                <span>100%</span>
              </div>
            </div>
          </div>

          <!-- 显示紧张分数 -->
          <div v-if="currentStressScore !== null" class="form-group stress-score-display">
            <label>紧张指数:</label>
            <div class="stress-score-container">
              <div 
                class="stress-score-badge"
                :style="{ 
                  backgroundColor: getStressColor(currentStressScore),
                  color: currentStressScore > 0 ? 'white' : '#666'
                }"
              >
                {{ currentStressScore }}
              </div>
              <span class="stress-description">{{ getStressDescription(currentStressScore) }}</span>
            </div>
            <p class="stress-suggestion">{{ getStressSuggestion(currentStressScore) }}</p>
          </div>

          <div class="modal-actions">
            <button class="btn btn-clear" @click="clearDateData">清除</button>
            <button class="btn btn-save" @click="saveDateData">保存</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/store/auth'
import { 
  getStressColor, 
  getStressDescription, 
  getStressSuggestion 
} from '@/utils/stressScoreHelper'

export default {
  name: 'InteractiveCalendar',
  setup() {
    const authStore = useAuthStore()
    const currentDate = ref(new Date())
    const selectedDate = ref(null)
    const showNoteModal = ref(false)
    const currentNote = ref('')
    const currentProgress = ref(0)  // DDL进度
    const currentDdlDate = ref('')  // DDL截止日期
    const currentStressScore = ref(null)  // 紧张分数
    
    // 存储日期的备注、进度、DDL日期和紧张分数
    const dateNotes = ref({})
    const dateProgress = ref({})  // 存储每个日期的DDL进度
    const dateDdlDates = ref({})  // 存储每个日期的DDL截止日期
    const dateStressScores = ref({})  // 存储每个日期的紧张分数

    const weekDays = ['日', '一', '二', '三', '四', '五', '六']

    const currentMonthYear = computed(() => {
      const year = currentDate.value.getFullYear()
      const month = currentDate.value.getMonth() + 1
      return `${year}年 ${month}月`
    })

    const calendarDays = computed(() => {
      const year = currentDate.value.getFullYear()
      const month = currentDate.value.getMonth()
      
      // 获取当月第一天
      const firstDay = new Date(year, month, 1)
      const firstDayWeek = firstDay.getDay()
      
      // 获取当月最后一天
      const lastDay = new Date(year, month + 1, 0)
      const lastDate = lastDay.getDate()
      
      // 获取上个月的最后几天
      const prevMonthLastDay = new Date(year, month, 0)
      const prevMonthLastDate = prevMonthLastDay.getDate()
      
      const days = []
      
      // 填充上个月的日期
      for (let i = firstDayWeek - 1; i >= 0; i--) {
        days.push(new Date(year, month - 1, prevMonthLastDate - i))
      }
      
      // 填充当月日期
      for (let i = 1; i <= lastDate; i++) {
        days.push(new Date(year, month, i))
      }
      
      // 填充下个月的日期，使总数达到42（6行×7列）
      const remainingDays = 42 - days.length
      for (let i = 1; i <= remainingDays; i++) {
        days.push(new Date(year, month + 1, i))
      }
      
      return days
    })

    const formatDate = (date) => {
      if (!date) return ''
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    }

    const formatDateDisplay = (date) => {
      if (!date) return ''
      const year = date.getFullYear()
      const month = date.getMonth() + 1
      const day = date.getDate()
      return `${year}年${month}月${day}日`
    }

    const isToday = (date) => {
      if (!date) return false
      const today = new Date()
      return formatDate(date) === formatDate(today)
    }

    const isCurrentMonth = (date) => {
      if (!date) return false
      return date.getMonth() === currentDate.value.getMonth() &&
             date.getFullYear() === currentDate.value.getFullYear()
    }

    const selectDate = (date) => {
      selectedDate.value = date
      const key = formatDate(date)
      currentNote.value = dateNotes.value[key] || ''
      currentProgress.value = dateProgress.value[key] || 0
      // DDL日期就是标注的日期本身
      currentDdlDate.value = key
      currentStressScore.value = dateStressScores.value[key] || 0
      showNoteModal.value = true
    }

    const getStressScore = (date) => {
      const key = formatDate(date)
      return dateStressScores.value[key] || 0
    }

    const updateProgressDisplay = () => {
      // 进度条滑动时的回调，确保响应式更新
    }

    const saveDateData = async () => {
      if (selectedDate.value) {
        try {
          const token = authStore.getToken
          if (!token) {
            console.error('未登录，无法保存日历数据')
            alert('请先登录')
            return
          }

          const key = formatDate(selectedDate.value)
          
          // 调用后端 API 保存数据
          // DDL日期就是标注的日期本身
          const response = await axios.post('/calendar-notes', {
            note_date: key,
            note_text: currentNote.value.trim() || null,
            color: '#ffffff',  // 固定为白色，不再由用户选择
            progress: currentProgress.value,
            ddl_date: key  // DDL日期 = 标注日期
          }, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          })

          if (response.data) {
            // 更新本地数据
            if (currentNote.value.trim()) {
              dateNotes.value[key] = currentNote.value.trim()
            }
            dateProgress.value[key] = currentProgress.value
            dateDdlDates.value[key] = key  // DDL日期就是标注日期
            dateStressScores.value[key] = response.data.stress_score || 0  // 保存后端返回的紧张分数
            console.log('日历备注保存成功，紧张分数:', response.data.stress_score)
          }
        } catch (error) {
          console.error('保存日历备注失败:', error)
          alert('保存失败，请重试')
        }
      }
      closeModal()
    }

    const clearDateData = async () => {
      if (selectedDate.value) {
        try {
          const token = authStore.getToken
          if (!token) {
            console.error('未登录，无法删除日历数据')
            alert('请先登录')
            return
          }

          const key = formatDate(selectedDate.value)
          
          // 调用后端 API 删除数据
          await axios.delete(`/calendar-notes/date/${key}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          })

          // 更新本地数据
          delete dateNotes.value[key]
          delete dateProgress.value[key]
          delete dateDdlDates.value[key]
          delete dateStressScores.value[key]
          console.log('日历备注删除成功')
        } catch (error) {
          // 404 表示该日期没有备注，也算删除成功
          if (error.response && error.response.status === 404) {
            const key = formatDate(selectedDate.value)
            delete dateNotes.value[key]
            delete dateProgress.value[key]
            delete dateDdlDates.value[key]
            delete dateStressScores.value[key]
          } else {
            console.error('删除日历备注失败:', error)
            alert('删除失败，请重试')
          }
        }
      }
      closeModal()
    }

    const closeModal = () => {
      showNoteModal.value = false
      selectedDate.value = null
      currentNote.value = ''
      currentProgress.value = 0
      currentDdlDate.value = ''
      currentStressScore.value = 0
    }

    const previousMonth = () => {
      currentDate.value = new Date(
        currentDate.value.getFullYear(),
        currentDate.value.getMonth() - 1,
        1
      )
    }

    const nextMonth = () => {
      currentDate.value = new Date(
        currentDate.value.getFullYear(),
        currentDate.value.getMonth() + 1,
        1
      )
    }

    // 从后端加载数据
    const loadCalendarNotes = async () => {
      try {
        const token = authStore.getToken
        if (!token) {
          console.log('未登录，跳过加载日历数据')
          return
        }

        const response = await axios.get('/calendar-notes', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.data && Array.isArray(response.data)) {
          // 将数组格式的数据转换为对象格式
          response.data.forEach(note => {
            const key = note.note_date
            if (note.note_text) {
              dateNotes.value[key] = note.note_text
            }
            dateProgress.value[key] = note.progress || 0
            dateDdlDates.value[key] = note.ddl_date || null
            dateStressScores.value[key] = note.stress_score || 0
          })
          console.log('日历数据加载成功，共', response.data.length, '条记录')
        }
      } catch (error) {
        console.error('加载日历数据失败:', error)
      }
    }

    onMounted(() => {
      loadCalendarNotes()
    })

    return {
      currentDate,
      selectedDate,
      showNoteModal,
      currentNote,
      currentProgress,
      currentDdlDate,
      currentStressScore,
      weekDays,
      currentMonthYear,
      calendarDays,
      dateNotes,
      dateProgress,
      dateDdlDates,
      dateStressScores,
      formatDate,
      formatDateDisplay,
      isToday,
      isCurrentMonth,
      getStressScore,
      getStressColor,
      getStressDescription,
      getStressSuggestion,
      selectDate,
      updateProgressDisplay,
      saveDateData,
      clearDateData,
      closeModal,
      previousMonth,
      nextMonth
    }
  }
}
</script>

<style scoped>
.calendar-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 0 auto;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
}

.month-year {
  font-size: 1.5em;
  color: #2c3e50;
  margin: 0;
  font-weight: 600;
}

.nav-button {
  background: #007bff;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  font-size: 1.2em;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.nav-button:hover {
  background: #0056b3;
  transform: scale(1.1);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.weekday {
  text-align: center;
  font-weight: bold;
  color: #555;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
  font-size: 0.9em;
}

.calendar-day {
  aspect-ratio: 1;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 80px;
  max-height: 100px;
  position: relative;
  overflow: hidden;
}

.calendar-day:not(.empty):hover {
  border-color: #007bff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
}

.calendar-day.empty {
  cursor: default;
  border: none;
}

.calendar-day.today {
  border-color: #ff6b6b !important;
  border-width: 3px !important;
  font-weight: bold;
  box-shadow: 0 0 12px rgba(255, 107, 107, 0.5);
  position: relative;
}

.calendar-day.today::before {
  content: '今';
  position: absolute;
  top: 2px;
  left: 2px;
  background: #ff6b6b;
  color: white;
  font-size: 10px;
  padding: 2px 4px;
  border-radius: 3px;
  font-weight: bold;
  z-index: 10;
}

.calendar-day.other-month {
  opacity: 0.4;
}

.date-number {
  font-size: 1.1em;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.date-note {
  font-size: 0.7em;
  color: #666;
  text-align: center;
  overflow: hidden;
  width: 100%;
  padding: 0 4px;
  line-height: 1.3;
  max-height: 3.9em;
  word-break: break-word;
  word-wrap: break-word;
}

/* 紧张分数指示器 */
.stress-indicator {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: bold;
  color: rgba(0, 0, 0, 0.8);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(255, 255, 255, 0.5);
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.calendar-day.has-stress {
  border-width: 3px;
}

/* 弹窗样式 */
.modal-overlay {
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
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 16px 16px 0 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.3em;
}

.close-button {
  background: none;
  border: none;
  font-size: 2em;
  color: white;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.3s ease;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #2c3e50;
  font-size: 1em;
}

.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1em;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

/* DDL日期输入框样式 */
.date-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1em;
  font-family: inherit;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.date-input:focus {
  outline: none;
  border-color: #667eea;
}

/* 紧张分数显示区域 */
.stress-score-display {
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  padding: 16px;
  border-radius: 12px;
  border: 2px solid #e0e0e0;
}

.stress-score-container {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.stress-score-badge {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  animation: scoreAppear 0.5s ease-out;
}

@keyframes scoreAppear {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.stress-description {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.stress-suggestion {
  margin: 0;
  padding: 12px;
  background: white;
  border-radius: 8px;
  font-size: 14px;
  color: #666;
  font-style: italic;
  line-height: 1.5;
}

/* 进度条样式 */
.progress-slider-container {
  margin-top: 10px;
}

.progress-slider {
  width: 100%;
  height: 8px;
  border-radius: 5px;
  background: #e0e0e0;
  outline: none;
  opacity: 0.9;
  transition: opacity 0.2s;
  margin-bottom: 15px;
  cursor: pointer;
}

.progress-slider:hover {
  opacity: 1;
}

.progress-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.progress-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.6);
}

.progress-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.progress-slider::-moz-range-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.6);
}

.progress-bar-bg {
  width: 100%;
  height: 24px;
  background: #f0f0f0;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  margin-bottom: 12px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  transition: width 0.3s ease;
  position: relative;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.progress-bar-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0) 100%);
  border-radius: 12px;
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.75em;
  color: #999;
  margin-top: 5px;
}

.progress-labels span {
  flex: 1;
  text-align: center;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1em;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-clear {
  background: #f5f5f5;
  color: #666;
}

.btn-clear:hover {
  background: #e0e0e0;
}

.btn-save {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-save:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .calendar-container {
    padding: 15px;
  }

  .calendar-day {
    min-height: 60px;
    max-height: 80px;
    padding: 5px;
  }

  .date-number {
    font-size: 0.9em;
  }

  .date-note {
    font-size: 0.6em;
    line-height: 1.2;
    max-height: 3.6em;
  }

  .modal-content {
    width: 95%;
  }
}
</style>

