import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('@/views/home/HomeView.vue'),
        meta: { title: '首页' },
      },
      {
        path: 'itinerary/generate',
        name: 'itinerary-generate',
        component: () => import('@/views/itinerary/GenerateView.vue'),
        meta: { title: 'AI 行程生成', requiresAuth: true },
      },
      {
        path: 'itinerary/:id',
        name: 'itinerary-detail',
        component: () => import('@/views/itinerary/DetailView.vue'),
        meta: { title: '行程详情', requiresAuth: true },
      },
      {
        path: 'search',
        name: 'search',
        component: () => import('@/views/search/SearchView.vue'),
        meta: { title: '搜索' },
      },
      {
        path: 'payment/:orderId?',
        name: 'payment',
        component: () => import('@/views/itinerary/PaymentView.vue'),
        meta: { title: '预订支付', requiresAuth: true },
      },
      {
        path: 'user',
        name: 'user',
        component: () => import('@/views/user/UserView.vue'),
        meta: { title: '用户中心', requiresAuth: true },
        children: [
          {
            path: '',
            name: 'user-dashboard',
            component: () => import('@/components/user/UserDashboard.vue'),
            meta: { title: '用户概览' },
          },
          {
            path: 'itineraries',
            name: 'user-itineraries',
            component: () => import('@/views/user/ItinerariesView.vue'),
            meta: { title: '我的行程' },
          },
          {
            path: 'orders',
            name: 'user-orders',
            component: () => import('@/views/user/OrdersView.vue'),
            meta: { title: '我的订单' },
          },
          {
            path: 'settings',
            name: 'user-settings',
            component: () => import('@/views/user/SettingsView.vue'),
            meta: { title: '偏好设置' },
          },
          {
            path: 'favorites',
            name: 'user-favorites',
            component: () => import('@/views/user/FavoritesView.vue'),
            meta: { title: '我的收藏' },
          },
          {
            path: 'member',
            name: 'member-center',
            component: () => import('@/views/user/MemberCenter.vue'),
            meta: { title: '会员中心' },
          },
        ],
      },
    ],
  },
  {
    path: '/editor/:id',
    component: () => import('@/layouts/EditorLayout.vue'),
    children: [
      {
        path: '',
        name: 'itinerary-editor',
        component: () => import('@/views/itinerary/EditorView.vue'),
        meta: { title: '行程编辑器', requiresAuth: true },
      },
    ],
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { title: '登录' },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/auth/RegisterView.vue'),
    meta: { title: '注册' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Route guard
router.beforeEach((to, _from, next) => {
  // Set page title
  document.title = to.meta.title ? `${to.meta.title} - 智游` : '智游 - AI 智能行程规划'

  // Check auth — read token directly from localStorage to avoid Pinia init order issues
  const token = localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !token) {
    // Save target path for post-login redirect
    next({
      path: '/login',
      query: { redirect: to.fullPath },
    })
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    // Already logged in, redirect to home or saved redirect
    const redirect = to.query.redirect as string
    next(redirect || '/')
  } else {
    next()
  }
})

export default router
