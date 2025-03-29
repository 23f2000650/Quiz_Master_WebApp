<template>
  <div class="admin-dashboard">
    <NavAdmin />
    </div>
  <div class="question-form container">
    <h2>Create New Question</h2>
    <div class="form-container">
      <form @submit.prevent="saveQuestion">
        <div class="form-group">
          <label for="text">Question Text:</label>
          <textarea id="text" v-model="question.text" class="form-control" rows="3" required></textarea>
        </div>
        
        <div class="form-group">
          <label>Options:</label>
          <div v-for="(option, index) in question.options" :key="index" class="option-item">
            <input type="text" v-model="question.options[index]" class="form-control" :placeholder="`Option ${index + 1}`" required />
          </div>
        </div>
        
        <div class="form-group">
          <label for="correctOption">Correct Option:</label>
          <input type="number" id="correctOption" v-model.number="question.correctOption" class="form-control" min="1" max="4" required />
        </div>
        
        <div class="form-actions">
          <button type="submit" class="btn">Save Question</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavAdmin from './NavAdmin.vue';

export default {
  name: 'QuestionForm',
  components: {
    NavAdmin
  },
  props: {
    subject_id: {
      type: String,
      required: true
    },
    chapter_id: {
      type: String,
      required: true
    },
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      question: {
        text: '',
        options: ['', '', '', ''],
        correctOption: null,
        subjectId: this.subject_id,
        chapterId: this.chapter_id,
        quizId: this.id
      }
    };
  },
  methods: {
    async saveQuestion() {
    console.log('Saving question:', this.question);
    const apiUrl = process.env.VUE_APP_API_URL + '/admin/questions/new';

    try {
      const response = await axios.post(apiUrl, this.question,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        }
      });
      
      console.log('Server response:', response.data);

      if (response.status !== 200 && response.status !== 201) { 
        throw new Error(`Failed to save question, status: ${response.status}`);
      }

      this.resetForm();
      this.$emit('question-saved');
      console.log('Question saved successfully');
    } catch (error) {
      console.error('Error saving question:', error.response ? error.response.data : error.message);
    }
  },
    resetForm() {
      this.question = {
        text: '',
        options: ['', '', '', ''],
        correctOption: null,
        subjectId: this.subjectId,
        chapterId: this.chapterId,
        quizId: this.quizId
      };
    }
  }
};
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.question-form {
  padding: 25px;
  max-width: 600px;
  /* margin: 30px auto; */
  background: #302c45;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-container {
  display: flex;
  flex-direction: column;
}

h2 {
  color: #fff;
  text-align: center;
  margin-bottom: 25px;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

label {
  color: #fff;
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  font-size: 0.95rem;
}

.form-control {
  width: 100%;
  padding: 12px;
  background: #423c5d;
  border: 1px solid #504a6d;
  border-radius: 4px;
  color: #fff;
  font-size: 0.9rem;
}

.form-control:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}

.option-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 25px;
  cursor: pointer;
  border-radius: 5px;
  font-weight: bold;
  transition: background 0.3s, transform 0.2s;
  min-width: 120px;
}

.btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

.btn:active {
  transform: translateY(0);
}
</style>