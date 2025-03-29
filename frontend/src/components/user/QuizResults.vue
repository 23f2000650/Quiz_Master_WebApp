<template>
  <div class="quiz-results container">
    <NavUser />
    <h1>Quiz Results</h1>

    <div v-if="results.length" class="results-list">
      <div v-for="result in results" :key="result.result_id" class="result-summary card">
        <div class="result-header">
          <h2>Quiz ID: {{ result.quiz_name }}</h2>
          <!-- <div class="result-status" :class="result.passed ? 'passed' : 'failed'">
            {{ result.passed ? 'PASSED' : 'FAILED' }}
          </div> -->
        </div>

        <div class="result-stats">
          <div class="stat-item">
            <div class="stat-label">Score</div>
            <div class="stat-value">{{ result.percentage }}%</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Total Questions</div>
            <div class="stat-value">{{ result.total_marks }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Completed At</div>
            <div class="stat-value">{{ formatDate(result.completed_at) }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Correct</div>
            <div class="stat-value">{{ result.marks_scored }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Incorrect</div>
            <div class="stat-value">{{ result.total_marks - result.marks_scored }}</div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="no-results">No results found.</div>

    <div class="actions">
      <button @click="goToDashboard" class="btn">Back to Dashboard</button>
    </div>
  </div>
</template>

<script>
import NavUser from "./NavUser.vue";
import axios from "axios";

export default {
  name: "QuizResults",
  components: { NavUser },
  data() {
    return {
      results: [],
    };
  },
  async created() {
    try {
      const user_id = localStorage.getItem("user_id");

      const response = await axios.get(`${process.env.VUE_APP_API_URL}/user/${user_id}/quiz/results`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      this.results = response.data.map((result) => ({
        ...result,
        percentage: ((result.marks_scored / result.total_marks) * 100).toFixed(2),
        passed: result.marks_scored / result.total_marks >= 0.5, // Example pass condition
      }));
    } catch (error) {
      console.error("Error fetching results:", error);
    }
  },
  methods: {
    goToDashboard() {
      this.$router.push("/dashboard");
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    },
  },
};
</script>

<style scoped>
.quiz-results {
  padding: 20px;
}

.card {
  background-color: #1e1b2c;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.result-status {
  padding: 8px 15px;
  border-radius: 4px;
  font-weight: bold;
}

.passed {
  background-color: #e6f7e6;
  color: #4caf50;
}

.failed {
  background-color: #ffebee;
  color: #f44336;
}

.result-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
}

.stat-item {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  flex: 1;
  min-width: 120px;
  text-align: center;
}

.stat-label {
  font-size: 0.9em;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 1.2em;
  font-weight: bold;
  color: #333;
}

.actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 20px;
}

h1, h2, h3 {
  color: #ffffff;
}

.no-results {
  text-align: center;
  font-size: 1.2em;
  color: #ccc;
  margin-top: 20px;
}
</style>
