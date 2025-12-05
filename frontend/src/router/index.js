import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import OnboardingView from '../views/OnboardingView.vue'
import DashboardView from '../views/DashboardView.vue'
import StressRadarView from '../views/StressRadarView.vue'
import FlowTrainingView from '../views/FlowTrainingView.vue'
import EmotionalAidView from '../views/EmotionalAidView.vue'
import MindPaintingView from '../views/MindPaintingView.vue'
import MessengerView from '../views/MessengerView.vue'
import ErrorReviewView from '../views/ErrorReviewView.vue'
import WeeklyReportView from '../views/WeeklyReportView.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/onboarding',
    name: 'Onboarding',
    component: OnboardingView
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/stress-radar',
    name: 'StressRadar',
    component: StressRadarView,
    meta: { requiresAuth: true }
  },
  {
    path: '/flow-training',
    name: 'FlowTraining',
    component: FlowTrainingView,
    meta: { requiresAuth: true }
  },
  {
    path: '/emotional-aid',
    name: 'EmotionalAid',
    component: EmotionalAidView,
    meta: { requiresAuth: true }
  },
  {
    path: '/mind-painting',
    name: 'MindPainting',
    component: MindPaintingView,
    meta: { requiresAuth: true }
  },
  {
    path: '/messenger',
    name: 'Messenger',
    component: MessengerView,
    meta: { requiresAuth: true }
  },
  {
    path: '/error-review',
    name: 'ErrorReview',
    component: ErrorReviewView,
    meta: { requiresAuth: true }
  },
  {
    path: '/weekly-report',
    name: 'WeeklyReport',
    component: WeeklyReportView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  // 临时跳过认证检查，用于开发测试
  // 注释掉下面的认证逻辑，直接允许所有路由访问
  /*
  const authStore = useAuthStore()
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authStore.isLoggedIn) {
      // 用户未登录，重定向到登录页
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
  */
  // 开发模式：直接允许所有路由访问
  next()
})

export default router

