import { createApp } from 'vue'
import App from './App.vue'
import ViewUiPlus from 'view-ui-plus'
import 'view-ui-plus/dist/styles/viewuiplus.css'
import axios from "axios";
import *as VueRouter from 'vue-router'
import routes from './router.js'

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes: routes,
})

const app = createApp(App)
app.config.globalProperties.$axios = axios



app.use(ViewUiPlus).use(router).mount('#app')
