<template>
  <div class="user-dashboard container">
    <div class="dashboard-header">
      <NavUser />
      <div class="header-actions">
        <button @click="downloadCSV" class="btn btn-download">
          <i class="download-icon">↓</i> Download Quiz Details
        </button>
      </div>
    </div>
    <h1>User Dashboard</h1>

    <div class="row">
      <!-- Upcoming Quizzes -->
      <div class="col-md-8">
        <div class="card">
          <h3>Upcoming Quizzes</h3>
          <div class="quiz-list" v-if="upcomingQuizzes.length">
            <div v-for="quiz in upcomingQuizzes" :key="quiz.id" class="quiz-item">
              <div class="quiz-detail">
                <h4>{{ quiz.title }}</h4>
                <p>{{ quiz.description }}</p>
                <p>Due date: {{ quiz.dueDate }}</p>
                <p>Duration: {{ quiz.duration }} mins</p>
              </div>
              <div class="quiz-actions">
                <button @click="startQuiz(quiz.id)" class="btn">Start Quiz</button>
              </div>
            </div>
          </div>
          <p v-else>No upcoming quizzes available.</p>
        </div>
      </div>

      <!-- Statistics -->
      <div class="col-md-4">
        <div class="card">
          <h3>Statistics</h3>
          <div class="stats-list">
            <div class="stat-item">
              <span class="stat-label">Total Quizzes:</span>
              <span class="stat-value">{{ stats.totalQuizzes }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Completed:</span>
              <span class="stat-value">{{ stats.completed }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Best Performance:</span>
              <span class="stat-value">{{ stats.bestPerformance }}/{{ stats.totalMarks }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Results -->
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <h3>Recent Results</h3>
          <div class="results-table">
            <table class="table">
              <thead>
                <tr>
                  <th>Quiz</th>
                  <th>Date</th>
                  <th>Score</th>
                  <th>Total Marks</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="result in recentResults" :key="result.id">
                  <td>{{ result.quizTitle }}</td>
                  <td>{{ result.date }}</td>
                  <td>{{ result.score }}</td>
                  <td>{{ result.totalMarks }}</td>
                </tr>
              </tbody>
            </table>
            <p v-if="recentResults.length === 0">No recent results available.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavUser from './NavUser.vue';

export default {
  name: 'UserDashboard',
  components: { NavUser },
  data() {
    return {
      upcomingQuizzes: [],
      stats: {
        totalQuizzes: 0,
        completed: 0,
        averageScore: 0,
        bestPerformance: 'N/A'
      },
      recentResults: []
    };
  },
  methods: {
    async fetchDashboardData() {
      const API_URL = process.env.VUE_APP_API_URL;
      const user_id = localStorage.getItem("user_id");
      try {
        const [quizzes, stats, results] = await Promise.all([
          axios.get(`${API_URL}/user/quizzes/upcoming`),
          axios.get(`${API_URL}/user/${user_id}/stats`),
          axios.get(`${API_URL}/user/${user_id}/results/recent`)
        ]);

        this.upcomingQuizzes = quizzes.data;
        this.stats = stats.data;
        this.recentResults = results.data;
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    },
    async downloadCSV() {
      const API_URL = process.env.VUE_APP_API_URL;
      const user_id = localStorage.getItem("user_id");
      try {
        const response = await axios({
          url: `${API_URL}/user/${user_id}/download_csv`,
          method: 'GET',
          responseType: 'blob' // Important for file download
        });

        // Create a link element to trigger the download
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        
        // Generate filename with current date
        const date = new Date().toISOString().split('T')[0];
        link.setAttribute('download', `quiz_details_${date}.csv`);
        
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        console.error('Error downloading CSV:', error);
        // Optionally show an error message to the user
        alert('Failed to download CSV. Please try again.');
      }
    },
    startQuiz(id) {
      this.$router.push(`/quiz/${id}/start`);
    },
    viewResult(id) {
      this.$router.push(`/results/${id}`);
    }
  },
  mounted() {
    this.fetchDashboardData();
  }
};
</script>


  
  <style scoped>
  .user-dashboard {
    padding: 20px;
  }
  
  

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  align-items: center;
}

.btn-download {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-download:hover {
  background-color: #45a049;
}

.download-icon {
  font-weight: bold;
  font-size: 1.2em;
}


  .row {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 20px;
  }
  
  .col-md-4 {
    width: 33.333%;
    padding: 0 10px;
  }
  
  .col-md-6 {
    width: 50%;
    padding: 0 10px;
  }
  
  .col-md-8 {
    width: 66.666%;
    padding: 0 10px;
  }
  
  .col-md-12 {
    width: 100%;
    padding: 0 10px;
  }
  
  .card {
    background-color: #1e1b2c;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
  }
  
  .quiz-item {
    border-bottom: 1px solid #eee;
    padding: 10px 0;
    display: flex;
    justify-content: space-between;
  }
  
  .quiz-actions {
    display: flex;
    align-items: center;
  }
  
  .stats-list {
    margin-top: 10px;
  }
  
  .stat-item {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #eee;
  }
  
  .table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .table th, .table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #eee;
  }
  
  .status {
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 0.9em;
  }
  
  .passed {
    background-color: #e6f7e6;
    color: #4CAF50;
  }
  
  .failed {
    background-color: #ffebee;
    color: #F44336;
  }
  
  .chart-container {
    height: 300px;
  }
  
  .btn-sm {
    padding: 4px 8px;
    font-size: 0.9em;
  }
  
  h1, h3 {
    color: #ffffff; 
    margin-bottom: 15px;
  }

  h1{
    display : flex;
  }
  </style>