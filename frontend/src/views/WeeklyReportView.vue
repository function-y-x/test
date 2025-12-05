<template>
  <div class="weekly-report-container">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span>
        返回主界面
      </button>
      <h1>我的周报</h1>
    </div>
    <p>回顾您一周的学习与情绪数据，获取个性化建议。</p>

    <div class="report-section">
      <h2>情绪趋势</h2>
      <div class="chart-container">
        <canvas id="moodTrendChart"></canvas>
      </div>
    </div>

    <div class="report-section">
      <h2>学习效率与情绪散点图</h2>
      <div class="chart-container">
        <canvas id="efficiencyMoodScatterChart"></canvas>
      </div>
    </div>

    <div class="report-section">
      <h2>本周洞察与建议</h2>
      <div class="insights">
        <p><strong>变化检测:</strong> 本周新增早起 ×3、晚睡 -2h、学习英语频次 ↑。</p>
        <p><strong>弱因果提示:</strong> 晚于 23:30 睡觉的日子，次日学习效率降低，且情绪波动加剧。</p>
      </div>
      <div class="suggestions">
        <h3>个性化策略（预测焦虑 -8%）</h3>
        <ul>
          <li>加 1 次午后 20min 小睡</li>
          <li>英语调到上午第一节</li>
          <li>晚间只做“可赢题”，并且坚持早睡</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Chart from 'chart.js/auto'

export default {
  name: 'WeeklyReportView',
  setup() {
    const router = useRouter()

    const goBack = () => {
      router.push('/dashboard')
    }
    onMounted(() => {
      // Mood Trend Chart
      const moodTrendCtx = document.getElementById('moodTrendChart');
      new Chart(moodTrendCtx, {
        type: 'line',
        data: {
          labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
          datasets: [
            {
              label: '焦虑指数',
              data: [0.5, 0.6, 0.7, 0.65, 0.75, 0.8, 0.7],
              borderColor: 'rgb(255, 99, 132)',
              tension: 0.1,
              yAxisID: 'y'
            },
            {
              label: '自信指数',
              data: [0.7, 0.65, 0.6, 0.7, 0.6, 0.55, 0.65],
              borderColor: 'rgb(54, 162, 235)',
              tension: 0.1,
              yAxisID: 'y'
            },
            {
              label: '专注指数',
              data: [0.6, 0.7, 0.65, 0.75, 0.7, 0.6, 0.7],
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1,
              yAxisID: 'y'
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 1
            }
          }
        }
      });

      // Efficiency vs Mood Scatter Chart
      const scatterCtx = document.getElementById('efficiencyMoodScatterChart');
      new Chart(scatterCtx, {
        type: 'scatter',
        data: {
          datasets: [
            {
              label: '学习效率 vs 情绪',
              data: [
                { x: 0.8, y: 0.7, r: 5 }, // x: 学习效率 (TPR), y: 情绪 (自信指数)
                { x: 0.6, y: 0.5, r: 7 },
                { x: 0.9, y: 0.8, r: 6 },
                { x: 0.7, y: 0.6, r: 5 },
                { x: 0.5, y: 0.4, r: 8 },
                { x: 0.85, y: 0.75, r: 6 },
              ],
              backgroundColor: 'rgba(255, 99, 132, 0.6)',
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            x: {
              type: 'linear',
              position: 'bottom',
              title: {
                display: true,
                text: '学习效率 (TPR)'
              },
              min: 0,
              max: 1
            },
            y: {
              type: 'linear',
              position: 'left',
              title: {
                display: true,
                text: '情绪 (自信指数)'
              },
              min: 0,
              max: 1
            },
          },
        },
      });
    });

    return {
      goBack
    }
  }
}
</script>

<style scoped>
.weekly-report-container {
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

.report-section {
  background-color: #f9f9f9;
  padding: 25px;
  border-radius: 10px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.report-section h2 {
  color: #007bff;
  margin-bottom: 20px;
}

.chart-container {
  width: 100%;
  height: 350px;
  margin-bottom: 20px;
}

.insights p {
  background-color: #e0f7fa;
  border-left: 4px solid #00bcd4;
  padding: 10px;
  margin-bottom: 10px;
  color: #333;
}

.suggestions h3 {
  color: #4CAF50;
  margin-top: 30px;
  margin-bottom: 15px;
}

.suggestions ul {
  list-style: none;
  padding: 0;
}

.suggestions li {
  background-color: #e8f5e9;
  border: 1px solid #a5d6a7;
  padding: 10px 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  color: #333;
}
</style>

