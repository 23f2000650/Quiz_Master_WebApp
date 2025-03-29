import { createApp } from 'vue'
import App from './App.vue'
import router from './router/routes.js';

const app = createApp(App) // Use App.vue as the root component
app.use(router)
app.mount('#app')
