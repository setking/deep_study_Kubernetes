import { createRouter } from 'vue-router'
import { routerConfig } from '@/router/config.ts'
import type { RouteRecordRaw } from "vue-router"
import { registerNavigationGuard } from '@/router/guard.ts'

const Layouts = () => import('@/layouts/default.vue')


export const constantRoutes:RouteRecordRaw[] = [
  {
    path:'/redirect',
    component: Layouts,
    meta: {
      title: '重定向',
      noCache: true
    },
    children: [
      {
        path: ":path(.*)",
        component: () => import('@/views/redirect/index.vue')
      }
    ]
  },
  {
    path: "/403",
    component: () => import("@/views/error/403.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/404",
    component: () => import("@/views/error/404.vue"),
    meta: {
      hidden: true
    },
    alias: "/:pathMatch(.*)*"
  },
  {
    path: "/login",
    component: () => import("@/views/login/index.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path:'/',
    component: Layouts,
    children: [
      {
        path: "home",
        component: () => import('@/views/home/index.vue'),
        name:"Home",
        meta: {
          title: "首页",
          noCache: true
        }
      }
    ]
  }
]

export const router = createRouter({
  history: routerConfig.history,
  routes: constantRoutes,
})
// 注册路由导航守卫
registerNavigationGuard(router)