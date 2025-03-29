<template>
  <div class="quiz-form container">
    <h2>{{ isEditing ? 'Edit Quiz' : 'Create New Quiz' }}</h2>
    
    <div class="form-container">
      <form @submit.prevent="saveQuiz">
        <div class="form-group">
          <label for="name"> Name:</label>
          <input type="text" id="name" v-model="quiz.name" class="form-control" required />
        </div>
        
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea id="description" v-model="quiz.description" class="form-control" rows="3"></textarea>
        </div>
        
        <div class="form-group">
          <label for="duration">Duration:</label>
          <input type="number" id="duration" v-model="quiz.duration" class="form-control" min="1" required placeholder="Enter time in minutes"/>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">Save</button>
          <button type="button" @click="cancel" class="btn btn-secondary">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'QuizForm',
  props: {
    subject_id: {
      type: [String, Number],
      required: true
    },
    chapter_id: {
      type: [String, Number],
      required: true
    },
    id: {  // Fixed syntax
      type: [String, Number],
      required: false
    }
  },
  data() {
    return {
      quiz: {
        name: '',
        code: '',
        description: '',
        duration: null
      },
      isEditing: false
    };
  },
  created() {
    if (this.id) {
      this.isEditing = true;
      this.fetchQuiz();
    }
  },
  methods: {
    async fetchQuiz() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/admin/quiz/${this.id}`,
        {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      }
        );
        this.quiz = response.data;  // Fixed incorrect assignment
      } catch (error) {
        console.error('Error fetching quiz:', error);
      }
    },
    async saveQuiz() { // Fixed function name and added async
      const quizData = {
        name: this.quiz.name,
        description: this.quiz.description,
        duration: this.quiz.duration
      };
      let url;
      if (this.isEditing) {
        url = `${process.env.VUE_APP_API_URL}/admin/quiz/${this.id}`;
      } else {
        url = `${process.env.VUE_APP_API_URL}/admin/subject/${this.subject_id}/chapter/${this.chapter_id}/new`;
      }
      
      try {
        const response = await axios({
          method: this.isEditing ? 'put' : 'post',  
          url,
          data: quizData,
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      });
        console.log('Quiz saved:', response.data);
        this.$router.push('/admin');  // Navigate after successful save
      } catch (error) {
        console.error('Error saving quiz:', error);
      }
    },
    cancel() {
      this.$router.push('/admin');
    }
  }
};
</script>

<style scoped>
.quiz-form {
  padding: 30px;
  max-width: 600px;
  margin: 50px auto;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background: rgb(37 34 50);
  text-align: center;
}

.form-container {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: white;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #a855f7;
  border-radius: 5px;
  font-size: 16px;
  transition: 0.3s;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s ease;
}

.btn-primary {
  background: #4a90e2;
  color: white;
}

.btn-secondary {
  background: #ccc;
}

h2 {
  color: #4a90e2;
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.8rem;
}
</style>
