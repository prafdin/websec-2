import { createApp } from 'vue'
import App from './App'
import router from './router/router'
import './assets/index.css'

createApp(App).use(router).mount('#app')
