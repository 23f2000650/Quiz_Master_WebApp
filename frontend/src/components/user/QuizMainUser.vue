<template>
  <div class="quiz-management container">
    <NavUser />
    <h1>Quiz Management</h1>

    <input v-model="searchQuery" type="text" placeholder="Search quizzes..." class="search-bar" />

    <table class="quiz-table" v-if="filteredQuizzes.length">
      <thead>
        <tr>
          <th>Subject</th>
          <th>Chapter</th>
          <th>Quiz Name</th>
          <th>Duration</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
          <td>{{ quiz.subjectTitle }}</td>
          <td>{{ quiz.chapterTitle }}</td>
          <td>{{ quiz.title }}</td>
          <td>{{ quiz.duration }} mins</td>
          <td>{{ quiz.description }}</td>
          <td class="quiz-actions">
            <button @click="startTest(quiz.id)" class="btn">Start Test</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="loading">Loading quizzes...</p>
    <p v-else-if="!filteredQuizzes.length">No quizzes available.</p>
  </div>
</template>

<script>
import NavUser from './NavUser.vue';
import axios from 'axios';

export default {
  name: 'QuizMainUser',
  components: { NavUser },
  data() {
    return {
      searchQuery: '',
      subjects: [], // Store raw API data
      loading: false
    };
  },
  computed: {
    // Extract quizzes from subjects dynamically
    quizzes() {
      return this.subjects.flatMap(subject =>
        subject.chapters.flatMap(chapter =>
          chapter.quizzes.map(quiz => ({
            id: quiz.id,
            title: quiz.title,
            duration: quiz.duration,
            description: quiz.description,
            subjectTitle: subject.title, // Store subject title
            chapterTitle: chapter.title // Store chapter title
          }))
        )
      );
    },
    // Apply search filtering
    filteredQuizzes() {
      const searchLower = this.searchQuery.toLowerCase();
      return this.quizzes.filter(quiz =>
        quiz.title.toLowerCase().includes(searchLower) ||
        quiz.description.toLowerCase().includes(searchLower) ||
        quiz.subjectTitle.toLowerCase().includes(searchLower) ||
        quiz.chapterTitle.toLowerCase().includes(searchLower)
      );
    }
  },
  methods: {
    async fetchQuizzes() {
      this.loading = true;
      const url = `${process.env.VUE_APP_API_URL}/user/quizzes`;

      const token = localStorage.getItem("token");
      console.log("Using token:", token);  // Debugging

      if (!token) {
        console.error("No token found! Make sure the user is logged in.");
        this.loading = false;
        return;
      }

      try {
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        console.log("Response data:", response.data);
        this.subjects = response.data;

      } catch (error) {
        console.error("Error fetching quizzes:", error.response ? error.response.data : error.message);
      } finally {
        this.loading = false;
      }
    },
    startTest(qid) {
      this.$router.push(`/quiz/${qid}/start`);
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
}

.search-bar {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #4a90e2;
  border-radius: 4px;
  background: #1e1c2a;
  color: white;
}

.quiz-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  background: #25233a;
  color: white;
  border-radius: 8px;
  overflow: hidden;
}

.quiz-table th, .quiz-table td {
  border: 1px solid #4a90e2;
  padding: 12px;
  text-align: center;
}

.quiz-table th {
  background-color: #4a90e2;
  color: white;
}

.quiz-table tbody tr:hover {
  background-color: #33304d;
}

.quiz-actions {
  text-align: center;
}

.btn {
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 15px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn:hover {
  background-color: #357ac9;
}
</style>
