import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/LoginComponent.vue'
import Register from '../components/RegisterComponent.vue'
import AdminDashboard from '../components/admin/AdminDashboard.vue'
import QuizForm from '../components/admin/QuizForm.vue'
import QuestionForm from '../components/admin/QuestionForm.vue'
import ChapterForm from '../components/admin/ChapterForm.vue'
import UserDashboard from '../components/user/UserDashboard.vue'
import QuizResults from '../components/user/QuizResults.vue'
import HomePage from '../views/HomePage.vue'
import SubjectForm from '../components/admin/SubjectForm.vue'
import QuizMain from '../components/admin/QuizMain.vue'
import AdminSummary from '../components/admin/AdminSummary.vue'
import UserSummary from '../components/user/UserSummary.vue'
import QuizMainUser from '../components/user/QuizMainUser.vue'
import QuizQuestion from '../components/admin/QuizQuestion.vue'
import TakeQuiz from '../components/user/TakeQuiz.vue'
import AdminUsers from '@/components/admin/AdminUsers.vue'


const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: Login },
  { path: '/register', component: Register },

  { path: '/admin', component: AdminDashboard },
  { path: '/admin/quiz', component: QuizMain },
  { path: '/admin/summary', component: AdminSummary },
  { path: '/admin/users', component: AdminUsers },
  //dashboard pathss  
  { path: '/admin/subject/new', component: SubjectForm},
  { path: '/admin/subject/:id/edit', component: SubjectForm, props: true},
  //chapter paths
  { path: '/admin/subject/:subject_id/chapter/new', component: ChapterForm, props: true },
  { path: '/admin/subject/:subject_id/chapter/:id/edit', component: ChapterForm, props: true },
  //quiz paths
  { path: '/admin/:subject_id/chapter/:chapter_id/quiz/new', component: QuizForm, props: true },
  { path: '/admin/:subject_id/chapter/:chapter_id/quiz/:id/edit', component: QuizForm, props: true },
  //to view questions
  { path: '/admin/quiz/:id/questions', component: QuizQuestion, props: true},
  { path: '/admin/quiz/:id/questions/:ques_id/edit', component: QuizQuestion, props: true},
  //to add questions
  { path: '/admin/subject/:subject_id/chapter/:chapter_id/quiz/:id/new', component: QuestionForm, props: true },
  { path: '/admin/chapter/:chapter_id/quiz/:id/new', component: QuestionForm, props: true },


  //user paths
  { path: '/dashboard', component: UserDashboard },
  { path: '/user/scores', component: QuizResults },
  { path : '/user/summary', component: UserSummary },
  { path: '/user/quiz', component: QuizMainUser },
  { path: '/quiz/:qid/start', component: TakeQuiz, props: true },

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router;
