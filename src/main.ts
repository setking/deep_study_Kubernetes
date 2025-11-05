import './assets/main.css'

import { createApp } from 'vue'
import { pinia } from "@/pinia"
import { router } from "@/router"
import App from '@/App.vue'

const app = createApp(App)

// 安装 pinia 和 router
app.use(pinia).use(router)

// router 准备就绪后挂载应用
router.isReady().then(() => {
  app.mount("#app")
})

