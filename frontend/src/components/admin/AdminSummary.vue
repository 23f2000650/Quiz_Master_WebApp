<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from "chart.js";
import { Bar } from "vue-chartjs";
import NavAdmin from './NavAdmin.vue'; // Import the NavAdmin component

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const dashboardData = ref(null);
const subjectChartData = ref(null);
const chapterChartData = ref(null);

const fetchDashboardData = async () => {
  try {
    const response = await axios.get(`${process.env.VUE_APP_API_URL}/admin/summary`,
    {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      }
    );
    dashboardData.value = response.data;

    subjectChartData.value = {
      labels: response.data.subject_performance.map((s) => s.subject),
      datasets: [
        {
          label: "Attempts",
          data: response.data.subject_performance.map((s) => s.attempts),
          backgroundColor: "#4CAF50",
        },
        {
          label: "Average Score",
          data: response.data.subject_performance.map((s) => s.avg_score),
          backgroundColor: "#FF9800",
        },
      ],
    };

    chapterChartData.value = {
      labels: response.data.chapter_performance.map((c) => c.chapter),
      datasets: [
        {
          label: "Attempts",
          data: response.data.chapter_performance.map((c) => c.attempts),
          backgroundColor: "#2196F3",
        },
        {
          label: "Average Score",
          data: response.data.chapter_performance.map((c) => c.avg_score),
          backgroundColor: "#FFC107",
        },
      ],
    };
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
  }
};

onMounted(fetchDashboardData);
</script>

<template>
  <div class="dashboard-container">
    <!-- Navigation Bar -->
    <NavAdmin />

    <h1 class="title">Admin Dashboard</h1>

    <div class="grid-container">
      <div class="card" v-if="dashboardData">
        <h2>Total Users</h2>
        <p>{{ dashboardData.total_users - 1 }}</p>
      </div>
      <div class="card" v-if="dashboardData">
        <h2>Total Subjects</h2>
        <p>{{ dashboardData.total_subjects }}</p>
      </div>
      <div class="card" v-if="dashboardData">
        <h2>Total Chapters</h2>
        <p>{{ dashboardData.total_chapters }}</p>
      </div>
      <div class="card" v-if="dashboardData">
        <h2>Total Quizzes</h2>
        <p>{{ dashboardData.total_quizzes }}</p>
      </div>
    </div>

    <div class="chart-grid">
      <div class="chart-container" v-if="subjectChartData">
        <h2>Subject-wise Performance</h2>
        <Bar :data="subjectChartData" />
      </div>
      <div class="chart-container" v-if="chapterChartData">
        <h2>Chapter-wise Performance</h2>
        <Bar :data="chapterChartData" />
      </div>
    </div>

    <div class="table-container" v-if="dashboardData">
      <h2>Recent Quiz Results</h2>
      <table>
        <thead>
          <tr>
            <th>User</th>
            <th>Quiz</th>
            <th>Score</th>
            <th>Completed At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in dashboardData.recent_results" :key="result.quiz">
            <td>{{ result.user }}</td>
            <td>{{ result.quiz }}</td>
            <td>{{ result.score }}</td>
            <td>{{ result.completed_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1200px;
  margin: auto;
}

.title {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.card {
  background: #221f30;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 4px 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
}

.card:hover {
  transform: scale(1.05);
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.chart-container {
  background: #221f30;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 4px 4px 15px rgba(0, 0, 0, 0.1);
}

.table-container {
  background: #221f30;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 4px 4px 15px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  border-bottom: 1px solid #ddd;
  text-align: left;
}

th {
  background: #black;
}
</style>
