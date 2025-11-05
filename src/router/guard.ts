import NProgress from 'nprogress'
import type { Router } from 'vue-router'
import { useTitle } from '@/useState/useTitle'
import { getToken } from '@/utils/caches/cookie.ts'
import { isWhiteList } from '@/router/whitelist.ts'

NProgress.configure({ showSpinner: false })
const { setTitle } = useTitle()
const LOGIN_PATH = '/login'
export function registerNavigationGuard(router: Router) {
  // 全局前置守卫
  router.beforeEach(async (to, _from) => {
    NProgress.start()
    // 如果没有登录
    if (!getToken()) {
      if (isWhiteList(to)) {
        // 如果是白名单，则直接跳转
        return true
      }
      // 其他没有访问权限的页面将被重定向到登录页面
      return LOGIN_PATH
    }
    if (to.path === LOGIN_PATH) return '/'
    return true
    // try {
    //   // 设置 replace: true, 因此导航将不会留下历史记录
    //   return { ...to, replace: true }
    // } catch (error) {
    //   ElMessage.error((error as Error).message || '路由守卫发生错误')
    //   return LOGIN_PATH
    // }
  })

  // 全局后置钩子
  router.afterEach((to) => {
    setTitle(to.meta.title)
    NProgress.done()
  })
}
