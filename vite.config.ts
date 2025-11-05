/// <reference types="vite/client" />
import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import vueJsx from "@vitejs/plugin-vue-jsx"
import vueDevTools from 'vite-plugin-vue-devtools'
import AutoImport from "unplugin-auto-import/vite"
import Components from "unplugin-vue-components/vite"
import { ElementPlusResolver } from "unplugin-vue-components/resolvers"
import { defineConfig, loadEnv } from "vite"
import { spawn } from 'child_process'

// Configuring Vite: https://cn.vite.dev/config
export default defineConfig(({ mode }) => {
  const { VITE_PUBLIC_PATH } = loadEnv(mode, process.cwd(), "") as unknown as ImportMetaEnv
  return {
    base: VITE_PUBLIC_PATH,
    // 入口文件
    plugins: [
      vue(),
      // 支持 JSX、TSX 语法
      vueJsx(),
      // 自动按需导入 API
      AutoImport({
        imports: ['vue', 'vue-router', 'pinia'],
        dts: 'types/auto/auto-imports.d.ts',
        resolvers: [ElementPlusResolver()],
      }),
      // 自动按需导入组件
      Components({
        dts: 'types/auto/components.d.ts',
        resolvers: [ElementPlusResolver()],
      }),
      vueDevTools(),
      // 插件：启动exe
      {
        name: 'launch-exe',
        configureServer(server) {
          server.httpServer?.once('listening', () => {
            // 启动 exe 文件
            const exePath = 'html-view/main.exe' // 修改为你的 exe 路径
            const child = spawn(exePath, [], {
              detached: true,
              stdio: 'ignore'
            })
            child.unref()
            console.log('✅ 已启动本地应用程序')
          })
        }
      }
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    // 开发环境服务器配置
    server: {
      // 是否监听所有地址
      host: true,
      // 端口号
      port: 3333,
      // 端口被占用时，是否直接退出
      strictPort: false,
      // 是否自动打开浏览器
      open: true,
      // 反向代理
      proxy: {
        "/api": {
          target: "http://127.0.0.1:8089",
          // 是否为 WebSocket
          ws: false,
          // 是否允许跨域
          changeOrigin: true,
          pathRewrite:{
            '^/api':''
          }
        }
      },
      // 是否允许跨域
      cors: true,
    },
  }
})
