import { createRouter, createWebHistory } from 'vue-router'
import Main from './components/Main/Main.vue'
import Donates from '@/components/Main/Donates.vue'
import Givers from '@/components/Givers/Givers.vue'
import Messages from '@/components/Messages.vue'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import Intro from '@/components/Intro.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Main
  },
  {
    path: '/donates/:takerId',
    name: 'donates',
    component: Donates,
    props: true
  },
  {
    path: '/givers',
    name: 'givers',
    component: Givers
  },
  {
    path: '/messages',
    name: 'messages',
    component: Messages
  },
  {
    path: '/intro',
    name: 'intro',
    component: Intro
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'  // Redirect unknown routes to home
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Add navigation guard to debug routing
router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.path)
  next()
})

export default router
