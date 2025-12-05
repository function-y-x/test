<template>
  <div class="stress-score-calendar">
    <!-- 紧张分数图例 -->
    <div class="stress-legend">
      <h4>紧张指数图例</h4>
      <div class="legend-items">
        <div class="legend-item">
          <span class="color-box" style="background-color: #e0e0e0"></span>
          <span>无压力 (0)</span>
        </div>
        <div class="legend-item">
          <span class="color-box" style="background-color: #4caf50"></span>
          <span>低压力 (1-30)</span>
        </div>
        <div class="legend-item">
          <span class="color-box" style="background-color: #ffeb3b"></span>
          <span>中等 (31-60)</span>
        </div>
        <div class="legend-item">
          <span class="color-box" style="background-color: #ff9800"></span>
          <span>高压力 (61-80)</span>
        </div>
        <div class="legend-item">
          <span class="color-box" style="background-color: #f44336"></span>
          <span>极高 (81-100)</span>
        </div>
      </div>
    </div>

    <!-- 日历视图 -->
    <div class="calendar-view">
      <div class="calendar-header">
        <button @click="previousMonth" class="nav-button">&lt;</button>
        <h3>{{ currentYear }}年{{ currentMonth }}月</h3>
        <button @click="nextMonth" class="nav-button">&gt;</button>
      </div>

      <div class="calendar-grid">
        <!-- 星期标题 -->
        <div class="weekday-header" v-for="day in weekdays" :key="day">
          {{ day }}
        </div>

        <!-- 日期单元格 -->
        <div
          v-for="day in calendarDays"
          :key="day.key"
          class="calendar-day"
          :class="{
            'other-month': !day.isCurrentMonth,
            'today': day.isToday,
            'has-stress': day.stressScore > 0
          }"
          :style="{ borderColor: getStressColor(day.stressScore) }"
          @click="handleDayClick(day)"
        >
          <div class="date-number">{{ day.date }}</div>
          <div
            v-if="day.stressScore > 0"
            class="stress-indicator"
            :style="{ backgroundColor: getStressColor(day.stressScore) }"
            :title="`紧张指数: ${day.stressScore} - ${getStressDescription(day.stressScore)}`"
          >
            {{ day.stressScore }}
          </div>
        </div>
      </div>
    </div>

    <!-- 日期详情弹窗 -->
    <div v-if="selectedDay" class="day-detail-modal" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ selectedDay.fullDate }}</h3>
          <button @click="closeModal" class="close-button">×</button>
        </div>
        <div class="modal-body">
          <div class="stress-info">
            <div class="stress-score-large" :style="{ color: getStressColor(selectedDay.stressScore) }">
              {{ selectedDay.stressScore }}
            </div>
            <div class="stress-label">紧张指数</div>
            <div class="stress-desc">{{ getStressDescription(selectedDay.stressScore) }}</div>
            <div class="stress-suggestion">{{ getStressSuggestion(selectedDay.stressScore) }}</div>
          </div>

          <div v-if="selectedDay.note" class="note-info">
            <h4>任务详情</h4>
            <p class="note-text">{{ selectedDay.note.note_text }}</p>
            
            <div v-if="selectedDay.note.ddl_date" class="ddl-info">
              <div class="info-row">
                <span class="label">截止日期:</span>
                <span class="value">{{ selectedDay.note.ddl_date }}</span>
              </div>
              <div class="info-row">
                <span class="label">当前进度:</span>
                <div class="progress-container">
                  <div class="progress-bar">
                    <div 
                      class="progress-fill" 
                      :style="{ width: `${selectedDay.note.progress}%` }"
                    ></div>
                  </div>
                  <span class="progress-text">{{ selectedDay.note.progress }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  getStressColor,
  getStressDescription,
  getStressSuggestion,
  getMonthStressScores,
  recalculateAllStressScores
} from '@/utils/stressScoreHelper';

export default {
  name: 'StressScoreCalendar',
  data() {
    return {
      currentYear: new Date().getFullYear(),
      currentMonth: new Date().getMonth() + 1,
      weekdays: ['日', '一', '二', '三', '四', '五', '六'],
      stressScores: {},
      notes: {},
      selectedDay: null
    };
  },
  computed: {
    calendarDays() {
      const days = [];
      const firstDay = new Date(this.currentYear, this.currentMonth - 1, 1);
      const lastDay = new Date(this.currentYear, this.currentMonth, 0);
      const prevMonthLastDay = new Date(this.currentYear, this.currentMonth - 1, 0);
      
      // 上个月的日期（填充）
      const firstDayOfWeek = firstDay.getDay();
      for (let i = firstDayOfWeek - 1; i >= 0; i--) {
        const date = prevMonthLastDay.getDate() - i;
        days.push({
          date,
          isCurrentMonth: false,
          stressScore: 0,
          key: `prev-${date}`
        });
      }
      
      // 当前月的日期
      for (let date = 1; date <= lastDay.getDate(); date++) {
        const dateStr = `${this.currentYear}-${this.currentMonth.toString().padStart(2, '0')}-${date.toString().padStart(2, '0')}`;
        const isToday = this.isToday(this.currentYear, this.currentMonth, date);
        
        days.push({
          date,
          fullDate: dateStr,
          isCurrentMonth: true,
          isToday,
          stressScore: this.stressScores[dateStr] || 0,
          note: this.notes[dateStr] || null,
          key: `current-${date}`
        });
      }
      
      // 下个月的日期（填充到6行）
      const remainingDays = 42 - days.length;
      for (let date = 1; date <= remainingDays; date++) {
        days.push({
          date,
          isCurrentMonth: false,
          stressScore: 0,
          key: `next-${date}`
        });
      }
      
      return days;
    }
  },
  methods: {
    getStressColor,
    getStressDescription,
    getStressSuggestion,
    
    isToday(year, month, date) {
      const today = new Date();
      return (
        today.getFullYear() === year &&
        today.getMonth() + 1 === month &&
        today.getDate() === date
      );
    },
    
    async loadStressScores() {
      try {
        const token = this.$store.state.auth?.token;
        if (!token) return;
        
        this.stressScores = await getMonthStressScores(token, this.currentYear, this.currentMonth);
      } catch (error) {
        console.error('加载紧张分数失败:', error);
      }
    },
    
    async loadNotes() {
      try {
        const token = this.$store.state.auth?.token;
        if (!token) return;
        
        const response = await fetch('/api/calendar-notes/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.ok) {
          const notes = await response.json();
          this.notes = {};
          notes.forEach(note => {
            this.notes[note.note_date] = note;
          });
        }
      } catch (error) {
        console.error('加载备注失败:', error);
      }
    },
    
    previousMonth() {
      if (this.currentMonth === 1) {
        this.currentMonth = 12;
        this.currentYear--;
      } else {
        this.currentMonth--;
      }
      this.loadStressScores();
    },
    
    nextMonth() {
      if (this.currentMonth === 12) {
        this.currentMonth = 1;
        this.currentYear++;
      } else {
        this.currentMonth++;
      }
      this.loadStressScores();
    },
    
    handleDayClick(day) {
      if (day.isCurrentMonth) {
        this.selectedDay = day;
      }
    },
    
    closeModal() {
      this.selectedDay = null;
    },
    
    async recalculateScores() {
      try {
        const token = this.$store.state.auth?.token;
        if (!token) return;
        
        await recalculateAllStressScores(token);
        await this.loadStressScores();
      } catch (error) {
        console.error('重新计算紧张分数失败:', error);
      }
    }
  },
  async mounted() {
    await this.loadStressScores();
    await this.loadNotes();
    
    // 每天首次打开时重新计算分数
    const lastCalculate = localStorage.getItem('lastStressCalculate');
    const today = new Date().toDateString();
    
    if (lastCalculate !== today) {
      await this.recalculateScores();
      localStorage.setItem('lastStressCalculate', today);
    }
  }
};
</script>

<style scoped>
.stress-score-calendar {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 图例样式 */
.stress-legend {
  margin-bottom: 20px;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 8px;
}

.stress-legend h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #666;
}

.legend-items {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.color-box {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

/* 日历样式 */
.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.nav-button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.nav-button:hover {
  background: #f0f0f0;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10px;
}

.weekday-header {
  padding: 10px;
  text-align: center;
  font-weight: bold;
  color: #666;
  font-size: 14px;
}

.calendar-day {
  aspect-ratio: 1;
  border: 2px solid transparent;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.calendar-day:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.calendar-day.other-month {
  opacity: 0.3;
  cursor: default;
}

.calendar-day.today {
  background: #e3f2fd;
}

.date-number {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 4px;
}

.stress-indicator {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 弹窗样式 */
.day-detail-modal {
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
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
}

.close-button {
  font-size: 28px;
  border: none;
  background: none;
  cursor: pointer;
  color: #999;
  line-height: 1;
  padding: 0;
  width: 30px;
  height: 30px;
}

.close-button:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.stress-info {
  text-align: center;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 20px;
}

.stress-score-large {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stress-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.stress-desc {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 12px;
}

.stress-suggestion {
  font-size: 14px;
  color: #666;
  font-style: italic;
}

.note-info h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
}

.note-text {
  margin-bottom: 15px;
  line-height: 1.6;
}

.ddl-info {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.info-row .label {
  font-weight: bold;
  margin-right: 10px;
  min-width: 80px;
}

.progress-container {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-bar {
  flex: 1;
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #8bc34a);
  transition: width 0.3s;
}

.progress-text {
  font-weight: bold;
  min-width: 40px;
}

@media (max-width: 768px) {
  .calendar-grid {
    gap: 5px;
  }
  
  .calendar-day {
    padding: 4px;
  }
  
  .date-number {
    font-size: 14px;
  }
  
  .stress-indicator {
    width: 24px;
    height: 24px;
    font-size: 10px;
  }
}
</style>

