// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/main/Main'),
    children: [
      {
        path: '',
        name: 'Home',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
      },
    ],
  },
  {
    path: '/login',
    component: ()=>import('@/views/Login.vue'),
  },
  {
    path:'/register',
    name: 'register',
    component: ()=>import('@/views/Register.vue')
  },
  {
    path:'/bank',
    name:'bank',
    component: ()=>import('@/layouts/main/Main'),
    children: [
      {
        path: '/bank',
        name: 'Bank',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/views/Bank.vue'),
      },
    ],

  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
