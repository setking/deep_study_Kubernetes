<script setup lang="ts">
import {getFilesApi} from "@/common/api/files"
import { CacheKey } from "@/constants/cache-key"
import Cookies from "js-cookie"
const htmlFiles = ref<any>([])
const currentFile = ref(htmlFiles.value[0])

const formatFiles = (files: any[]) => {
  return files.map((file: any) => {
    file.path = `/resource/${file.path}`
    return file
  })
}

onMounted(() => {
  const currentPage = Cookies.get(CacheKey.CURRENT_PAGE)
  if (currentPage) {

    console.log("读取 cookies：", currentPage)
    currentFile.value = JSON.parse(currentPage)
    console.log("当前页：", currentFile.value)
  }
  getFilesApi().then((data) => {
    htmlFiles.value = formatFiles(data)
  }).catch(() => {
    htmlFiles.value = []
  })

})
const setCurrentFile = (file: any) => {
  currentFile.value = file
  Cookies.set(CacheKey.CURRENT_PAGE, JSON.stringify(file))
}
</script>

<template>
  <div class="container">
    <div class="sidebar">
      <h3>文件列表</h3>
      <ul>
        <li
          v-for="file in htmlFiles"
          :key="file.path"
          @click="setCurrentFile(file)"
          :class="{ active: currentFile?.path === file.path }"
        >
          {{ file.name }}
        </li>
      </ul>

    </div>
    <div class="content">
      <iframe
        :title="currentFile?.name"
        :src="currentFile?.path"
        sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
      ></iframe>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.sidebar {
  width: 20vw;
  padding: 20px;
  height: 90vh;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  overflow-y: auto;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 10px;
  margin: 5px 0;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.3s;
}

.sidebar li:hover {
  background: #e0e0e0;
}

.sidebar li.active {
  background: #1976d2;
  color: white;
}

.content {
  width: 70vw;
  height: 90vh;
  overflow: hidden;
}

iframe {
  width: 100%;
  height: 100%;
  border: 1px solid #ddd;
  border-left: none;
  border-radius: 0 4px 4px 0;
}
</style>