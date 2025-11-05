<script setup lang="ts">
import { setToken } from '@/utils/caches/cookie.ts'
const route = useRoute()
const router = useRouter()
const start = () => {
  console.log('开始学习',route.params.path)
  setToken('isLearning')
  router.push("/")
}
</script>

<template>
  <div class="content">
    <div class="title">深入剖析Kubernetes</div>
    <div class="start">
      <el-button @click.prevent="start"> 开始学习 </el-button>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.content{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  flex-direction: column;
  .title {
    font-size: 30px;
    margin-bottom: 20px;
  }
  .start {
    margin-top: 20px;
    font-size: 18px;
  }
}
</style>