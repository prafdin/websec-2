import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView'
import PanelView from '../views/PanelView'
import SettingsView from '../views/SettingsView'

const routes = [
  {
    path: '/login',
    component: LoginView
  },
  {
    path: '/panel',
    name: 'panel',
    component: PanelView
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView
  },
  {
    path: '/',
    redirect: '/panel'
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to) => {
  const publicPages = ['/login']
  const authRequired = !publicPages.includes(to.path)
  const logged = document.cookie.replace(/(?:(?:^|.*;\s*)login-token\s*=\s*([^;]*).*$)|^.*$/, '$1')

  if (authRequired && !logged) {
    return '/login'
  }
})

export default router
