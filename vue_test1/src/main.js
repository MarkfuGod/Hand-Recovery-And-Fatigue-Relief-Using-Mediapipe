// main.ts
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import './fonts/index.css' //全局使用


const app = createApp(App)

app.use(ElementPlus)
app.mount('#app')