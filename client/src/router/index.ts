import { createRouter, createWebHistory } from 'vue-router'
import { getSetupStatus } from '../api'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/setup',
      name: 'setup',
      component: () => import('../views/SetupView.vue'),
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
    {
      path: '/s/:code',
      name: 'share-link',
      redirect: (to) => `/retrieve?code=${to.params.code}`,
    },
    {
      path: '/records',
      name: 'records',
      component: () => import('../views/RecordsView.vue'),
    },
  ],
})

// Navigation guard: redirect based on init status
let _initialized: boolean | null = null

router.beforeEach(async (to, _from, next) => {
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

  // Already initialized → block /setup access, redirect to home
  if (_initialized && to.name === 'setup') {
    next({ name: 'send' })
    return
  }

  // Not initialized → redirect to /setup for any other route
  if (!_initialized && to.name !== 'setup') {
    next({ name: 'setup' })
    return
  }

  next()
})

export function markInitialized() {
  _initialized = true
}

export default router
