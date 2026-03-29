import { createRouter, createWebHistory } from 'vue-router'
import { getSetupStatus } from '../api'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/setup',
      name: 'setup',
      component: () => import('../views/SetupView.vue'),
      meta: { skipInitCheck: true },
    },
    {
      path: '/',
      name: 'send',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/retrieve',
      name: 'retrieve',
      component: () => import('../views/RetrieveView.vue'),
    },
  ],
})

// Navigation guard: redirect to /setup if not initialized
let _initialized: boolean | null = null

router.beforeEach(async (to, _from, next) => {
  // Skip check for setup page itself
  if (to.meta.skipInitCheck) {
    next()
    return
  }

  // Cache the init status for this session
  if (_initialized === null) {
    try {
      const res = await getSetupStatus()
      _initialized = res.initialized
    } catch {
      // If API fails, assume initialized (dev mode with .env)
      _initialized = true
    }
  }

  if (!_initialized) {
    next({ name: 'setup' })
  } else {
    next()
  }
})

export default router
