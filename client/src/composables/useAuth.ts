import { ref, computed } from 'vue'
import { getMe, login as apiLogin, register as apiRegister, type UserInfo } from '../api'

const user = ref<UserInfo | null>(null)
const loading = ref(false)

// Restore user from localStorage on module init
const storedUser = localStorage.getItem('user')
if (storedUser) {
  try {
    user.value = JSON.parse(storedUser)
  } catch {
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }
}

export function useAuth() {
  const isLoggedIn = computed(() => !!user.value)
  const username = computed(() => user.value?.username || '')

  async function checkAuth() {
    const token = localStorage.getItem('token')
    if (!token) {
      user.value = null
      return
    }
    try {
      const res = await getMe()
      if (res.user) {
        user.value = res.user
        localStorage.setItem('user', JSON.stringify(res.user))
      } else {
        logout()
      }
    } catch {
      logout()
    }
  }

  async function login(usernameVal: string, password: string) {
    loading.value = true
    try {
      const res = await apiLogin(usernameVal, password)
      user.value = { id: res.id, username: res.username }
      localStorage.setItem('token', res.token)
      localStorage.setItem('user', JSON.stringify(user.value))
      return res
    } finally {
      loading.value = false
    }
  }

  async function register(usernameVal: string, password: string) {
    loading.value = true
    try {
      const res = await apiRegister(usernameVal, password)
      user.value = { id: res.id, username: res.username }
      localStorage.setItem('token', res.token)
      localStorage.setItem('user', JSON.stringify(user.value))
      return res
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    user,
    loading,
    isLoggedIn,
    username,
    checkAuth,
    login,
    register,
    logout,
  }
}
