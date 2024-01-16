import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main/Main'
import Donates from '@/components/Main/Donates'
import Givers from '@/components/Givers/Givers'
import Messages from '@/components/Messages'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Intro from '@/components/Intro'

Vue.use(Router)

export default new Router({
  routes: [
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
  ]
})
