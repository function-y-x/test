<template>
  <div class="stress-radar-container">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span>
        返回主界面
      </button>
      <h1>压力雷达</h1>
    </div>
    <p>这里将展示您的考试倒计时、模考趋势、睡眠与任务完成度叠图，并提供一键"处方"生成器。</p>
    <div class="chart-container">
      <canvas id="stressRadarChart"></canvas>
    </div>
    <button class="prescription-button">一键生成处方</button>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Chart from 'chart.js/auto'

export default {
  name: 'StressRadarView',
  setup() {
    const router = useRouter()

    const goBack = () => {
      router.push('/dashboard')
    }
    onMounted(() => {
      const ctx = document.getElementById('stressRadarChart');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
          datasets: [{
            label: '焦虑指数',
            data: [0.5, 0.6, 0.7, 0.65, 0.75, 0.8, 0.7],
            borderColor: 'rgb(255, 99, 132)',
            tension: 0.1
          }]
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
    });

    return {
      goBack
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
  padding: 12px 25px;
  font-size: 1.1em;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.prescription-button:hover {
  background-color: #0056b3;
}
</style>

