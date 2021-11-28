import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../pages/Home.vue')
  },
  {
    path: '/registration',
    name: 'Registration',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    component: () => import('../pages/Registration.vue')
  },
  {
    path: '/visit',
    name: 'Visit',
    component: () => import('../pages/Visit.vue')
  },
  {
    path: '/my_user',
    name: 'User',
    component: () => import('../pages/MyUser.vue')
  },
  {
    path: '/dev',
    name: 'Dev',
    component: () => import('../pages/Dev.vue')
  },
  {
    path: '/blank',
    name: 'Blank',
    component: () => import('../pages/Blank.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
