<template>
  <div class="quiz-management container">
    <NavAdmin />
    <h1>Quiz Management</h1>

    <input v-model="searchQuery" type="text" placeholder="Search quizzes..." class="search-bar" />

    <div class="grid-container" v-if="quizzes.length">
      <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="quiz-card">
        <h3>{{ quiz.name }}</h3>
        <p>{{ quiz.description }}</p>
        <p>Duration: {{ quiz.time_duration }} hours</p>
        
        <div class="quiz-actions">
          <button @click="addQuestion(quiz.chapter_id,quiz.id)" class="btn">+ Add Question</button>
          <button @click="viewQuestions(quiz.id)" class="btn btn-view">View Questions</button>
          <button @click="deleteQuiz(quiz.id)" class="btn btn-danger">Delete Quiz</button>
        </div>
      </div>
    </div>
    
    <p v-else>Loading quizzes...</p>
  </div>
</template>

<script>
import NavAdmin from './NavAdmin.vue';
import axios from 'axios';

export default {
  name: 'QuizManagement',
  components: { NavAdmin },
  data() {
    return {
      searchQuery: '',
      quizzes: []
    };
  },
  computed: {
    filteredQuizzes() {
  return this.quizzes.filter(quiz =>
    quiz.name && quiz.name.toLowerCase().includes(this.searchQuery.toLowerCase())
  );
}

  },
  methods: {
    async fetchQuizzes() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/admin/quizzes`,
        {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      }
        );
        console.log('Fetched Data:', response.data); // Debugging
        this.quizzes = response.data;
      } catch (error) {
        console.error('Error fetching quizzes:', error);
      }
    },
    addQuestion( chapter_id,id) {
      this.$router.push(`/admin/chapter/${chapter_id}/quiz/${id}/new`);
    },

    viewQuestions(id) {
      this.$router.push(`/admin/quiz/${id}/questions`);
    },
    async deleteQuiz(quizId) {
      try {
        await axios.delete(`${process.env.VUE_APP_API_URL}/admin/quizzes/${quizId}`,
        {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      }
        );
        this.quizzes = this.quizzes.filter(quiz => quiz.id !== quizId);
      } catch (error) {
        console.error('Error deleting quiz:', error);
      }
    }
  },
  mounted() {
    this.fetchQuizzes();
  }
};
</script>

<style scoped>
.quiz-management {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-bar {
  width: 100%;
  padding: 12px;
  margin-bottom: 20px;
  border: 1px solid #4a90e2;
  border-radius: 6px;
  font-size: 16px;
  background-color: #2d2b42;
  color: white;
  transition: all 0.3s ease;
}

.search-bar:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.5);
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

.quiz-card {
  background-color: #25233a;
  border-radius: 10px;
  padding: 20px;
  border: 2px solid #4a90e2;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.quiz-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.quiz-card h3 {
  color: white;
  margin-bottom: 10px;
  font-size: 18px;
}

.quiz-card p {
  color: #cccccc;
  margin-bottom: 12px;
  flex-grow: 1;
}

.quiz-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: auto;
}

.btn {
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 15px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s ease;
}

.btn:hover {
  background-color: #3a80d2;
}

.btn-view {
  background-color: #5c6bc0;
}

.btn-view:hover {
  background-color: #4c5bb0;
}

.btn-danger {
  background-color: #f44336;
}

.btn-danger:hover {
  background-color: #e53935;
}

@media (min-width: 768px) {
  .quiz-actions {
    flex-direction: row;
    justify-content: center;
  }
}

@media (max-width: 767px) {
  .grid-container {
    grid-template-columns: 1fr;
  }
  
  .quiz-card {
    max-width: 100%;
  }
}
</style>