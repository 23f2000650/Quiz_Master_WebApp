<template>
  <div class="admin-dashboard container">
    <NavAdmin />
    <h1>Welcome, Admin!</h1>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else class="grid-container">
      <div v-for="subject in subjects" :key="subject.subject_id" class="subject-card">
        <h3>Subject: {{ subject.title }}</h3>
        <div class="subject-actions">
          <button @click="editSubject(subject.subject_id)" class="btn">Edit</button>
          <button @click="deleteSubject(subject.subject_id)" class="btn btn-danger">Delete</button>
        </div>
        <div class="grid-container">
          <div v-for="chapter in subject.chapters" :key="chapter.chapter_id" class="chapter-card">
            <h4>Chapter: {{ chapter.title }}</h4>
            <div class="chapter-actions">
              <button @click="editChapter(subject.subject_id, chapter.chapter_id)" class="btn">Edit</button>
              <button @click="deleteChapter(subject.subject_id, chapter.chapter_id)" class="btn btn-danger">Delete Chapter</button>
            </div>
            <div class="grid-container">
              <div v-for="quiz in chapter.quizzes" :key="quiz.id" class="quiz-item">
                <h5>Quiz: {{ quiz.title }}</h5>
                <p>Desc: {{ quiz.description }}</p>
                <p>Duration: {{ quiz.duration }} Minutes</p>
                <div class="quiz-actions">
                  <button @click="addQues(subject.subject_id, chapter.chapter_id, quiz.id)" class="btn">Add Question</button>
                  <button @click="editQuiz(subject.subject_id, chapter.chapter_id, quiz.id)" class="btn">Edit</button>
                  <button @click="deleteQuiz(subject.subject_id, chapter.chapter_id, quiz.id)" class="btn btn-danger">Delete Quiz</button>
                </div>
              </div>
            </div>
            <button @click="createQuiz(subject.subject_id, chapter.chapter_id)" class="btn">+ Create New Quiz</button>
          </div>
        </div>
        <button @click="createChapter(subject.subject_id)" class="btn">+ Create New Chapter</button>
      </div>
    </div>
    <button @click="createSubject" class="btn">+ Create New Subject</button>
  </div>
</template>

<script>
import axios from 'axios';
import NavAdmin from './NavAdmin.vue';

export default {
  name: 'AdminDashboard',
  components: { NavAdmin },
  data() {
    return {
      subjects: [],
      loading: true,
      error: null
    };
  },
  async mounted() {
    await this.fetchSubjects();
  },
  methods: {
    async fetchSubjects() {
      try {
        const url = `${process.env.VUE_APP_API_URL}/admin/allquiz`;
        const response = await axios.get(url,
        {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      }
        );
        this.subjects = response.data;
      } catch (err) {
        this.error = 'Failed to load subjects. Please try again later.';
      } finally {
        this.loading = false;
      }
    },
    createSubject() {
      this.$router.push('/admin/subject/new');
    },
    createChapter(subject_id) {
      this.$router.push(`/admin/subject/${subject_id}/chapter/new`);
    },
    createQuiz(subject_id, chapter_id) {
      this.$router.push(`/admin/${subject_id}/chapter/${chapter_id}/quiz/new`);
    },
    editSubject(subject_id) {
      this.$router.push(`/admin/subject/${subject_id}/edit`);
    },
    async deleteSubject(subject_id) {
      if (!confirm('Are you sure you want to delete this subject?')) return;
      try {
        await axios.delete(`${process.env.VUE_APP_API_URL}/admin/subject/${subject_id}`,
        {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      }
        );
        this.fetchSubjects();
      } catch (err) {
        alert('Failed to delete subject.');
      }
    },
    editChapter(subject_id, chapter_id) {
      this.$router.push(`/admin/subject/${subject_id}/chapter/${chapter_id}/edit`);
    },
    async deleteChapter(subject_id, chapter_id) {
      if (!confirm('Are you sure you want to delete this chapter?')) return;
      try {
        await axios.delete(`${process.env.VUE_APP_API_URL}/admin/subject/${subject_id}/chapter/${chapter_id}`,
        {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      }
        );
        this.fetchSubjects();
      } catch (err) {
        alert('Failed to delete chapter.');
      }
    },
    editQuiz(subject_id, chapter_id, id) {
      this.$router.push(`/admin/${subject_id}/chapter/${chapter_id}/quiz/${id}/edit`);
    },
    addQues(subject_id, chapter_id,id) {
      this.$router.push(`/admin/subject/${subject_id}/chapter/${chapter_id}/quiz/${id}/new`);
    },
    async deleteQuiz(subject_id, chapter_id, id) {
      if (!confirm('Are you sure you want to delete this quiz?')) return;
      try {
        await axios.delete(`${process.env.VUE_APP_API_URL}/admin/subject/${subject_id}/chapter/${chapter_id}/quiz/${id}`,{
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      });
        this.fetchSubjects();
      } catch (err) {
        alert('Failed to delete quiz.');
      }
    }
  }
};
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
}

/* Main grid for subjects */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
  width: 100%;
}

/* Subject card - each will be its own column */
.subject-card {
  background-color: #14121e;
  border-radius: 8px;
  padding: 20px;
  border: 2px solid #4a90e2;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

/* Override grid for chapters to be full width inside subject */
.subject-card > .grid-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 15px;
}

/* Chapter card */
.chapter-card {
  background-color: #1e1b2c;
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #4a90e2;
  margin-bottom: 15px;
  width: 100%;
  box-sizing: border-box;
}

/* Quiz grid inside chapters */
.chapter-card > .grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  width: 100%;
}

/* Quiz item */
.quiz-item {
  background-color: #25233a;
  border-radius: 6px;
  padding: 12px;
  text-align: left;
  width: 100%;
  box-sizing: border-box;
  overflow-wrap: break-word;
  height: 100%;
}

.btn {
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  cursor: pointer;
  margin: 5px;
}

.btn-danger {
  background-color: #f44336;
}

.quiz-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.error-message {
  color: red;
  font-weight: bold;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .grid-container,
  .chapter-card > .grid-container {
    grid-template-columns: 1fr;
  }
}
</style>
