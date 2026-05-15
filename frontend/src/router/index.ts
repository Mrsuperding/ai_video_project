import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/pages/home/Index.vue')
      },
      {
        path: 'user/profile',
        name: 'Profile',
        component: () => import('@/pages/user/Profile.vue')
      },
      {
        path: 'user/membership',
        name: 'Membership',
        component: () => import('@/pages/user/Membership.vue')
      },
      {
        path: 'user/wallet',
        name: 'Wallet',
        component: () => import('@/pages/user/Wallet.vue')
      },
      {
        path: 'digital-human',
        name: 'DigitalHumanList',
        component: () => import('@/pages/digital-human/List.vue')
      },
      {
        path: 'digital-human/create',
        name: 'DigitalHumanCreate',
        component: () => import('@/pages/digital-human/Create.vue')
      },
      {
        path: 'digital-human/:id',
        name: 'DigitalHumanDetail',
        component: () => import('@/pages/digital-human/Detail.vue')
      },
      {
        path: 'script',
        name: 'ScriptList',
        component: () => import('@/pages/script/List.vue')
      },
      {
        path: 'script/create',
        name: 'ScriptCreate',
        component: () => import('@/pages/script/Create.vue')
      },
      {
        path: 'script/:id/edit',
        name: 'ScriptEdit',
        component: () => import('@/pages/script/Edit.vue')
      },
      {
        path: 'asset',
        name: 'Asset',
        component: () => import('@/pages/asset/MyAssets.vue')
      },
      {
        path: 'video',
        name: 'VideoList',
        component: () => import('@/pages/video/List.vue')
      },
      {
        path: 'video/create',
        name: 'VideoCreate',
        component: () => import('@/pages/video/Create.vue')
      },
      {
        path: 'video/:id',
        name: 'VideoDetail',
        component: () => import('@/pages/video/Detail.vue')
      },
      {
        path: 'video/:id/output',
        name: 'VideoOutput',
        component: () => import('@/pages/video/Output.vue')
      }
    ]
  },
  {
    path: '/auth',
    component: () => import('@/layouts/EmptyLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/pages/auth/Login.vue')
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('@/pages/auth/Register.vue')
      },
      {
        path: 'forgot-password',
        name: 'ForgotPassword',
        component: () => import('@/pages/auth/ForgotPassword.vue')
      }
    ]
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/pages/admin/Dashboard.vue')
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/pages/admin/Users.vue')
      },
      {
        path: 'reviews',
        name: 'AdminReviews',
        component: () => import('@/pages/admin/Reviews.vue')
      },
      {
        path: 'statistics',
        name: 'AdminStatistics',
        component: () => import('@/pages/admin/Statistics.vue')
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('@/pages/admin/Settings.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (!token && !to.path.startsWith('/auth')) {
    next('/auth/login')
  } else {
    next()
  }
})

export default router