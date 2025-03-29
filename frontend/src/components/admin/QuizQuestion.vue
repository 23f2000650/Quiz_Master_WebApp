<template>
  <div class="quiz-questions container">
    <NavAdmin />
    <h1>Questions for {{ quizName }}</h1>
    
    <div class="action-buttons">
      <button @click="showAddForm = true" class="btn-add">Add New Question</button>
    </div>
    
    <div v-if="showAddForm" class="add-question-form">
      <h2>Add New Question</h2>
      <form @submit.prevent="addQuestion">
        <div class="form-grid">
          <div class="form-group">
            <label>Question</label>
            <textarea v-model="newQuestion.text" required></textarea>
          </div>
          
          <div class="form-group">
            <label>Option A</label>
            <input type="text" v-model="newQuestion.option_a" required>
          </div>
          
          <div class="form-group">
            <label>Option B</label>
            <input type="text" v-model="newQuestion.option_b" required>
          </div>
          
          <div class="form-group">
            <label>Option C</label>
            <input type="text" v-model="newQuestion.option_c" required>
          </div>
          
          <div class="form-group">
            <label>Option D</label>
            <input type="text" v-model="newQuestion.option_d" required>
          </div>
          
          <div class="form-group">
            <label>Correct Answer</label>
            <select v-model="newQuestion.answer" required>
              <option value="1">A</option>
              <option value="2">B</option>
              <option value="3">C</option>
              <option value="4">D</option>
            </select>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="btn-submit">Save Question</button>
          <button type="button" @click="showAddForm = false" class="btn-cancel">Cancel</button>
        </div>
      </form>
    </div>
    
    <div v-if="questions.length" class="questions-grid">
      <div v-for="(question, index) in questions" :key="question.id" class="question-item">
        <div v-if="!question.isEditing">
          <h3>{{ question.question }}</h3>
          <p><strong>Options:</strong></p>
          <ul>
            <li>A. {{ question.option_a }}</li>
            <li>B. {{ question.option_b }}</li>
            <li>C. {{ question.option_c }}</li>
            <li>D. {{ question.option_d }}</li>
          </ul>
          <p><strong>Answer:</strong> {{ getOptionLetter(question.answer) }}</p>
          <div class="question-actions">
            <button @click="startEditing(index)" class="btn-edit">Edit</button>
            <button @click="deleteQuestion(question.id)" class="btn-delete">Delete</button>
          </div>
        </div>
        
        <div v-else class="edit-question-form">
          <div class="form-grid">
            <div class="form-group">
              <label>Question</label>
              <textarea v-model="question.editedQuestion" required></textarea>
            </div>
            
            <div class="form-group">
              <label>Option A</label>
              <input type="text" v-model="question.editedOptionA" required>
            </div>
            
            <div class="form-group">
              <label>Option B</label>
              <input type="text" v-model="question.editedOptionB" required>
            </div>
            
            <div class="form-group">
              <label>Option C</label>
              <input type="text" v-model="question.editedOptionC" required>
            </div>
            
            <div class="form-group">
              <label>Option D</label>
              <input type="text" v-model="question.editedOptionD" required>
            </div>
            
            <div class="form-group">
              <label>Correct Answer</label>
              <select v-model="question.editedAnswer" required>
                <option value="1">A</option>
                <option value="2">B</option>
                <option value="3">C</option>
                <option value="4">D</option>
              </select>
            </div>
          </div>
          
          <div class="form-actions">
            <button @click="saveEdit(index)" class="btn-submit">Save Changes</button>
            <button @click="cancelEdit(index)" class="btn-cancel">Cancel</button>
          </div>
        </div>
      </div>
    </div>
    <p v-else>No questions found.</p>
  </div>
</template>

<script>
import { ref } from 'vue';
import NavAdmin from './NavAdmin.vue';
import axios from 'axios';

export default {
  name: 'QuizQuestions',
  components: { NavAdmin },
  props: {
    id: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const quizName = ref('');
    const questions = ref([]);
    const showAddForm = ref(false);
    const newQuestion = ref({
      text: '',
      option_a: '',
      option_b: '',
      option_c: '',
      option_d: '',
      answer: '1'
    });

    const getOptionLetter = (answer) => {
      const optionMap = {
        '1': 'A',
        '2': 'B',
        '3': 'C',
        '4': 'D'
      };
      return optionMap[answer] || answer;
    };

    const startEditing = (index) => {
      questions.value[index].isEditing = true;
      questions.value[index].editedQuestion = questions.value[index].question;
      questions.value[index].editedOptionA = questions.value[index].option_a;
      questions.value[index].editedOptionB = questions.value[index].option_b;
      questions.value[index].editedOptionC = questions.value[index].option_c;
      questions.value[index].editedOptionD = questions.value[index].option_d;
      questions.value[index].editedAnswer = questions.value[index].answer;
    };

    const cancelEdit = (index) => {
      delete questions.value[index].isEditing;
      delete questions.value[index].editedQuestion;
      delete questions.value[index].editedOptionA;
      delete questions.value[index].editedOptionB;
      delete questions.value[index].editedOptionC;
      delete questions.value[index].editedOptionD;
      delete questions.value[index].editedAnswer;
    };

    const saveEdit = async (index) => {
      try {
        const question = questions.value[index];
        const payload = {
          text: question.editedQuestion,
          quizId: props.id,
          options: [
            question.editedOptionA, 
            question.editedOptionB, 
            question.editedOptionC, 
            question.editedOptionD
          ],
          correctOption: question.editedAnswer,
        };

        // Send update request
        await axios.put(`${process.env.VUE_APP_API_URL}/admin/questions/${question.id}`, payload, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          }
        });

        // Refresh questions list
        await fetchQuestions();
      } catch (error) {
        console.error('Error updating question:', error);
      }
    };

    const fetchQuestions = async () => {
      try {
        console.log('Quiz ID:', props.id); // Debugging
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/admin/quiz/${props.id}/questions`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          }
        }
        );
        questions.value = response.data;
        quizName.value = response.data.length ? response.data[0].quiz_name : '';
      } catch (error) {
        console.error('Error fetching questions:', error);
      }
    };

    const addQuestion = async () => {
      try {
        const payload = {
          text: newQuestion.value.text,
          quizId: props.id,
          options: [
            newQuestion.value.option_a, 
            newQuestion.value.option_b, 
            newQuestion.value.option_c, 
            newQuestion.value.option_d
          ],
          correctOption: newQuestion.value.answer,
        };
        
        await axios.post(`${process.env.VUE_APP_API_URL}/admin/questions/new`, payload,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          }
        }
        );
        
        // Reset form
        newQuestion.value = {
          text: '',
          option_a: '',
          option_b: '',
          option_c: '',
          option_d: '',
          answer: '1'
        };
        
        showAddForm.value = false;
        
        // Refresh questions list
        await fetchQuestions();
      } catch (error) {
        console.error('Error adding question:', error);
      }
    };

    const deleteQuestion = async (questionId) => {
      if (confirm('Are you sure you want to delete this question?')) {
        try {
          await axios.delete(`${process.env.VUE_APP_API_URL}/admin/questions/${questionId}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            }
          }
          );
          // Refresh questions list
          await fetchQuestions();
        } catch (error) {
          console.error('Error deleting question:', error);
        }
      }
    };

    // Fetch questions on component mount
    fetchQuestions();

    return {
      quizName,
      questions,
      showAddForm,
      newQuestion,
      getOptionLetter,
      startEditing,
      cancelEdit,
      saveEdit,
      addQuestion,
      deleteQuestion
    };
  }
};
</script>

<style scoped>


.question-actions {
    display: flex;
    gap: 10px;
    margin-top: 15px;
  }
  
  .btn-edit {
    background: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-edit:hover {
    background: #45a049;
  }
  
  .edit-question-form {
    background: #2d2b42;
    border: 2px solid #4a90e2;
    border-radius: 8px;
    padding: 20px;
  }


  .quiz-questions {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .action-buttons {
    margin-bottom: 20px;
  }
  
  .btn-add {
    background: #4a90e2;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }
  
  .btn-add:hover {
    background: #3a80d2;
  }
  
  .questions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
  }
  
  .question-item {
    background: #25233a;
    border: 2px solid #4a90e2;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  
  h1 {
    color: #4a90e2;
    margin-bottom: 30px;
    font-size: 28px;
  }
  
  h2 {
    color: #4a90e2;
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  h3 {
    color: white;
    margin-top: 0;
    font-size: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    padding-bottom: 10px;
  }
  
  p {
    color: white;
    margin: 15px 0 5px;
  }
  
  ul {
    list-style-type: none;
    padding-left: 0;
  }
  
  li {
    margin-bottom: 10px;
  }
  
  .question-item ul li {
    color: #e2e2e2;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 4px;
    margin-bottom: 8px;
  }
  
  strong {
    color: #4a90e2;
  }
  
  .btn-delete {
    background: #e25353;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: auto;
    align-self: flex-start;
  }
  
  .btn-delete:hover {
    background: #d23939;
  }
  
  .add-question-form {
    background: #2d2b42;
    border: 2px solid #4a90e2;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 30px;
  }
  
  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
  }
  
  .form-group:first-child {
    grid-column: 1 / -1;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    color: white;
    margin-bottom: 5px;
  }
  
  .form-group input,
  .form-group textarea,
  .form-group select {
    width: 100%;
    padding: 10px;
    border-radius: 4px;
    border: 1px solid #4a4a6a;
    background: #1e1c2e;
    color: white;
  }
  
  .form-group textarea {
    min-height: 100px;
    resize: vertical;
  }
  
  .form-actions {
    display: flex;
    gap: 10px;
    margin-top: 20px;
  }
  
  .btn-submit {
    background: #4a90e2;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-cancel {
    background: #6c6c8a;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-submit:hover {
    background: #3a80d2;
  }
  
  .btn-cancel:hover {
    background: #5c5c7a;
  }
  </style>