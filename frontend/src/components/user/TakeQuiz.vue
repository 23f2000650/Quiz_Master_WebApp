<template>
  <NavUser />
  <div class="quiz-container">
    <h2>{{ quizInfo.title }}</h2>
    <p v-if="quizInfo.description">{{ quizInfo.description }}</p>
    <div v-if="!quizCompleted">
      <div v-if="currentQuestion">
        <h3>Question {{ currentIndex + 1 }} of {{ questions.length }}</h3>
        <p>{{ currentQuestion.question_text }}</p>
        <ul>
          <li 
            v-for="(option, index) in currentQuestion.options" 
            :key="index" 
            :class="{ selected: userAnswers[currentIndex] === option.value }"
            @click="selectOption(option.value)">
            {{ option.label }}. {{ option.value }}
          </li>
        </ul>
        <button @click="nextQuestion" :disabled="!userAnswers[currentIndex]">
          {{ isLastQuestion ? 'Submit' : 'Next' }}
        </button>
        <p v-if="timeRemaining">Time left: {{ timeRemaining }}s</p>
      </div>
    </div>
    <div v-else>
      <h3>Quiz Completed!</h3>
      <p>Your Score: {{ score }} / {{ questions.length }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavUser from './NavUser.vue';
export default {
  props: {
    qid: {
      type: String,
      required: true
    }
  },
  components: {
    NavUser
  },
  data() {
    return {
      quizInfo: {},
      questions: [],
      currentIndex: 0,
      userAnswers: [],
      timeRemaining: 0,
      quizCompleted: false,
      timer: null
    };
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentIndex] || null;
    },
    isLastQuestion() {
      return this.currentIndex === this.questions.length - 1;
    },
    score() {
      return this.userAnswers.filter((answer, index) => 
        answer === this.questions[index].correct_option
      ).length;
    }
  },
  methods: {
    async fetchQuizData() {
      if (!this.qid) return; // Ensure qid exists before fetching
      try {
        console.log('Fetching quiz data for qid:', this.qid);
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/user/quiz/${this.qid}`,
        {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
        );
        console.log('Quiz data:', response.data);

        const rawQuestions = response.data;

        // Transform API response to match expected format
        this.questions = rawQuestions.map((item, index) => ({
          question_text: `Q${index + 1}: ${item.question}`, // Generic question text
          options: [
            { label: 'A', value: item.option_a },
            { label: 'B', value: item.option_b },
            { label: 'C', value: item.option_c },
            { label: 'D', value: item.option_d }
          ],
          correct_option: item[`option_${this.getCorrectOptionKey(item.answer)}`] // Get correct option dynamically
        }));

        this.timeRemaining = response.data[0].time*60; // Set default timer
        console.log(this.timeRemaining)
        this.startTimer();
      } catch (error) {
        console.error('Error fetching quiz data:', error);
      }
    },
    getCorrectOptionKey(answer) {
      const answerMap = { "1": "a", "2": "b", "3": "c", "4": "d" };
      return answerMap[answer] || "a"; // Default to "a" if invalid answer
    },
    startTimer() {
      if (this.timeRemaining > 0) {
        this.timer = setInterval(() => {
          if (this.timeRemaining > 0) {
            this.timeRemaining--;
          } else {
            clearInterval(this.timer);
            this.submitQuiz();
          }
        }, 1000);
      }
    },
    selectOption(option) {
      this.userAnswers[this.currentIndex] = option; // ✅ Directly assign value
      this.userAnswers = [...this.userAnswers]; // ✅ Ensure reactivity by creating a new array
    },
    nextQuestion() {
      if (this.isLastQuestion) {
        this.submitQuiz();
      } else {
        this.currentIndex++;
      }
    },
    submitQuiz() {
  this.quizCompleted = true;
  clearInterval(this.timer);

  const payload = {
    qid: this.qid,
    user_id: localStorage.getItem("user_id"),
    score: this.score,
    total_marks: this.questions.length,
    //time_taken: (this.questions[0].time * 60) - this.timeRemaining,
    date_of_completion: new Date().toISOString() // Get current date in ISO format
  };

  axios.post(`${process.env.VUE_APP_API_URL}/user/quiz/submit`, payload,
  {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
  )
    .then(response => {
      console.log('Quiz submitted successfully:', response.data);
    })
    .catch(error => {
      console.error('Error submitting quiz:', error);
    });
}

  },
  watch: {
    qid: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchQuizData();
        }
      }
    }
  }
};
</script>

<style scoped>
.quiz-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border-radius: 8px;
  background: #25233a;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}
li.selected {
  background: #a0d468;
  color: white;
}
button {
  margin-top: 10px;
  padding: 8px 16px;
  border: none;
  background: #4a90e2;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}
button:disabled {
  background: #7c6bc0;
  cursor: not-allowed;
}
</style>
