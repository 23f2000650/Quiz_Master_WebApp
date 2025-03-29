<template>
  <div class="nav">
    <NavUser />
  </div>
  <div class="dashboard-container">
    <div v-if="loading" class="loading-message">
      <p>Loading dashboard data...</p>
    </div>
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>
    
    <div v-else>
      <h1 class="dashboard-title">Performance Dashboard</h1>
      
      <!-- Summary Stats -->
      <div class="stats-container">
        <div class="stat-card">
          <h3>Average Score</h3>
          <p class="stat-value">{{ data.avg_score.toFixed(1) }}</p>
        </div>
        <div class="stat-card">
          <h3>Total Attempts</h3>
          <p class="stat-value">{{ data.total_attempts }}</p>
        </div>
        <div class="stat-card">
          <h3>Recent Score</h3>
          <p v-if="data.recent_performance && data.recent_performance.length">
            {{ data.recent_performance[0].score }} / {{ data.recent_performance[0].total }}
          </p>
          <p class="no-attempts" v-else>No recent attempts</p>
        </div>
      </div>

      <div class="charts-container">
        <!-- Subject Performance Chart -->
        <div class="chart-card">
          <h2>Subject Performance</h2>
          <canvas ref="subjectChart"></canvas>
        </div>
        
        <!-- Chapter Performance Chart -->
        <div class="chart-card">
          <h2>Chapter Performance</h2>
          <canvas ref="chapterChart"></canvas>
        </div>
        
        <!-- Recent Performance Timeline -->
        <div class="chart-card full-width">
          <h2>Recent Performance Timeline</h2>
          <canvas ref="recentChart"></canvas>
        </div>
        
        <!-- Recent Quizzes Table -->
        <div class="table-container full-width">
          <h2>Recent Quiz Attempts</h2>
          <div class="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Quiz Name</th>
                  <th>Score</th>
                  <th>Performance</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(quiz, index) in data.recent_performance" :key="index">
                  <td>{{ formatDate(quiz.completed_at) }}</td>
                  <td>{{ quiz.quiz_name }}</td>
                  <td>{{ quiz.score }} / {{ quiz.total }}</td>
                  <td>
                    <div class="progress-bar">
                      <div class="progress" :style="`width: ${(quiz.score / quiz.total * 100)}%`"></div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import Chart from 'chart.js/auto';
import axios from 'axios';
import NavUser from './NavUser.vue';

export default {
  name: 'UserSummary',
  components: { NavUser },
  props: {
    apiUrl: {
      type: String,
      default: `${process.env.VUE_APP_API_URL}/user/summary/${localStorage.getItem('user_id')}` // Default API endpoint
    }
  },
  setup(props) {
     const route = useRoute();
    const subjectChart = ref(null);
    const chapterChart = ref(null);
    const recentChart = ref(null);
    const data = ref({});
    const loading = ref(true);
    const error = ref(null);
    const charts = ref([]);
    
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    // Clear previous charts to avoid memory leaks
    const clearCharts = () => {
      charts.value.forEach(chart => chart.destroy());
      charts.value = [];
    };
    
    // Function to initialize all charts
    const initCharts = () => {
      clearCharts();
      
      // Subject Performance Chart
      if (data.value.subject_performance) {
        const subjectData = {
          labels: Object.keys(data.value.subject_performance),
          datasets: [{
            label: 'Average Score',
            data: Object.values(data.value.subject_performance).map(item => item.avg_score),
            backgroundColor: [
              'rgba(54, 162, 235, 0.6)',
              'rgba(75, 192, 192, 0.6)',
              'rgba(153, 102, 255, 0.6)',
              'rgba(255, 159, 64, 0.6)'
            ],
            borderColor: [
              'rgba(54, 162, 235, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
          }]
        };
        
        const subjectChartInstance = new Chart(subjectChart.value, {
          type: 'bar',
          data: subjectData,
          options: {
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Average Score'
                }
              }
            },
            plugins: {
              legend: {
                display: false
              }
            }
          }
        });
        
        charts.value.push(subjectChartInstance);
      }
      
      // Chapter Performance Chart
      if (data.value.chapter_performance) {
        const chapterData = {
          labels: Object.keys(data.value.chapter_performance),
          datasets: [{
            label: 'Average Score',
            data: Object.values(data.value.chapter_performance).map(item => item.avg_score),
            backgroundColor: [
              'rgba(255, 99, 132, 0.6)',
              'rgba(255, 159, 64, 0.6)',
              'rgba(255, 205, 86, 0.6)',
              'rgba(75, 192, 192, 0.6)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(255, 159, 64, 1)',
              'rgba(255, 205, 86, 1)',
              'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
          }]
        };
        
        const chapterChartInstance = new Chart(chapterChart.value, {
          type: 'bar',
          data: chapterData,
          options: {
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Average Score'
                }
              }
            },
            plugins: {
              legend: {
                display: false
              }
            }
          }
        });
        
        charts.value.push(chapterChartInstance);
      }
      
      // Recent Performance Chart
      if (data.value.recent_performance && data.value.recent_performance.length) {
        const sortedPerformance = [...data.value.recent_performance].sort((a, b) => 
          new Date(a.completed_at) - new Date(b.completed_at)
        );
        
        const recentData = {
          labels: sortedPerformance.map(item => formatDate(item.completed_at)),
          datasets: [{
            label: 'Score Percentage',
            data: sortedPerformance.map(item => (item.score / item.total) * 100),
            fill: false,
            borderColor: 'rgba(75, 192, 192, 1)',
            tension: 0.1,
            pointBackgroundColor: 'rgba(75, 192, 192, 1)',
            pointRadius: 5
          }]
        };
        
        const recentChartInstance = new Chart(recentChart.value, {
          type: 'line',
          data: recentData,
          options: {
            scales: {
              y: {
                beginAtZero: true,
                max: 100,
                title: {
                  display: true,
                  text: 'Score Percentage (%)'
                }
              }
            }
          }
        });
        
        charts.value.push(recentChartInstance);
      }
    };
    

    // Fetch data from API
    const fetchData = async () => {
      loading.value = true;
      error.value = null;
      try {
        
        const response = await axios.get(props.apiUrl,
        {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      }
        );
        data.value = response.data;
        loading.value = false;
        
        // Initialize charts after data is loaded
        setTimeout(() => {
          initCharts();
        }, 100);
      } catch (err) {
        console.error('Error fetching performance data:', err);
        error.value = 'Failed to load dashboard data. Please try again later.';
        loading.value = false;
      }
    };
    
    // Refresh data periodically if needed
    //const refreshData = (interval = 5 * 60 * 1000) => { // Default: 5 minutes
    //   return setInterval(() => {
    //     fetchData();
    //   }, interval);
    // };
    
    onMounted(fetchData); 

    watch(() => route.fullPath, fetchData);
    
    return {
      subjectChart,
      chapterChart,
      recentChart,
      data,
      loading,
      error,
      formatDate,
      fetchData
    };
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 24px;
  max-width: 900px;
  margin: auto;
  background-color: #4f4c61;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.loading-message, .error-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 18px;
  font-weight: 500;
}

.error-message p {
  color: red;
}

.dashboard-title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 24px;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: #272532;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card h3 {
  font-size: 16px;
  color: #6b7280;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
}

.no-attempts {
  font-size: 18px;
  font-style: italic;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}

.chart-card {
  background: #272532;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-card h2 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
}

.full-width {
  grid-column: span 2;
}

.table-container {
  background: #272532;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

th {
  font-size: 12px;
  text-transform: uppercase;
  font-weight: 600;
  color: #6b7280;
}

.progress-bar {
  width: 100%;
  background-color: #e5e7eb;
  border-radius: 8px;
  height: 8px;
}

.progress {
  height: 8px;
  background-color: #2563eb;
  border-radius: 8px;
}

</style>