<template>
  <el-dialog
    :model-value="visible"
    @update:model-value="$emit('update:visible', $event)"
    width="400px"
    :close-on-click-modal="false"
    class="login-dialog"
    align-center
    destroy-on-close
  >
    <!-- Header -->
    <div class="text-center mb-6">
      <div class="w-14 h-14 mx-auto mb-3 bg-[#fefefe] rounded-2xl flex items-center justify-center shadow-md border border-black/5">
        <svg width="38" height="38" viewBox="22 62 137 82" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="dlgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#f97316"/>
              <stop offset="100%" style="stop-color:#ef4444"/>
            </linearGradient>
          </defs>
          <path d="M40 120 Q70 80 100 100 Q130 120 160 80" fill="none" stroke="#f9731626" stroke-width="20" stroke-linecap="round"/>
          <path d="M40 120 Q70 80 100 100 Q130 120 160 80" fill="none" stroke="url(#dlgGrad)" stroke-width="4" stroke-linecap="round"/>
          <circle cx="44" cy="118" r="14" fill="url(#dlgGrad)"/>
          <circle cx="38" cy="115" r="5" fill="white"/>
          <circle cx="39.5" cy="114" r="2.5" fill="#fefefe"/>
          <circle cx="40" cy="113" r="1.4" fill="#1a1a1a"/>
          <path d="M36 120 Q44 127 52 120" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
          <circle cx="58" cy="106" r="10" fill="url(#dlgGrad)" opacity="0.7"/>
          <circle cx="74" cy="96" r="11" fill="url(#dlgGrad)" opacity="0.75"/>
          <circle cx="92" cy="100" r="12" fill="url(#dlgGrad)" opacity="0.8"/>
          <circle cx="110" cy="108" r="11" fill="url(#dlgGrad)" opacity="0.75"/>
          <circle cx="126" cy="100" r="10" fill="url(#dlgGrad)" opacity="0.7"/>
          <circle cx="140" cy="88" r="9" fill="url(#dlgGrad)" opacity="0.6"/>
        </svg>
      </div>
      <h2 class="text-lg font-bold text-[#1B1B1B]">欢迎来到隧隧虫</h2>
      <p class="text-sm text-[#6B705C]/60 mt-1">登录后文本永久保存，可查看操作记录</p>
    </div>

    <!-- Tabs -->
    <el-tabs v-model="activeTab" class="login-tabs">
      <!-- Login -->
      <el-tab-pane label="登录" name="login">
        <el-form @submit.prevent="handleLogin" class="space-y-4 mt-2">
          <el-form-item>
            <el-input
              v-model="loginForm.username"
              placeholder="用户名"
              size="large"
              prefix-icon="User"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="密码"
              size="large"
              prefix-icon="Lock"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>
          <button
            type="submit"
            :disabled="!loginForm.username || !loginForm.password || loading"
            class="brand-btn-primary w-full py-3 text-sm"
            :class="(!loginForm.username || !loginForm.password || loading) ? 'opacity-50 cursor-not-allowed' : ''"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </el-form>
      </el-tab-pane>

      <!-- Register -->
      <el-tab-pane label="注册" name="register">
        <el-form @submit.prevent="handleRegister" class="space-y-4 mt-2">
          <el-form-item>
            <el-input
              v-model="regForm.username"
              placeholder="用户名（2-50个字符）"
              size="large"
              prefix-icon="User"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-input
              v-model="regForm.password"
              type="password"
              placeholder="密码（至少4位）"
              size="large"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          <el-form-item>
            <el-input
              v-model="regForm.confirmPassword"
              type="password"
              placeholder="确认密码"
              size="large"
              prefix-icon="Lock"
              show-password
              @keyup.enter="handleRegister"
            />
          </el-form-item>
          <button
            type="submit"
            :disabled="!regForm.username || !regForm.password || regForm.password !== regForm.confirmPassword || loading"
            class="brand-btn-primary w-full py-3 text-sm"
            :class="(!regForm.username || !regForm.password || regForm.password !== regForm.confirmPassword || loading) ? 'opacity-50 cursor-not-allowed' : ''"
          >
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuth } from '../composables/useAuth'

const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits<{
  'update:visible': [val: boolean]
  'success': []
}>()

const { login, register, loading } = useAuth()
const activeTab = ref('login')

const loginForm = reactive({
  username: '',
  password: '',
})

const regForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
})

watch(() => props.visible, (val) => {
  if (val) {
    // Reset forms when dialog opens
    loginForm.username = ''
    loginForm.password = ''
    regForm.username = ''
    regForm.password = ''
    regForm.confirmPassword = ''
    activeTab.value = 'login'
  }
})

async function handleLogin() {
  if (!loginForm.username || !loginForm.password) return
  try {
    await login(loginForm.username, loginForm.password)
    ElMessage.success('登录成功')
    emit('update:visible', false)
    emit('success')
  } catch (err: any) {
    const detail = err.response?.data?.detail || '登录失败'
    ElMessage.error(detail)
  }
}

async function handleRegister() {
  if (!regForm.username || !regForm.password) return
  if (regForm.password !== regForm.confirmPassword) {
    ElMessage.warning('两次密码输入不一致')
    return
  }
  try {
    await register(regForm.username, regForm.password)
    ElMessage.success('注册成功')
    emit('update:visible', false)
    emit('success')
  } catch (err: any) {
    const detail = err.response?.data?.detail || '注册失败'
    ElMessage.error(detail)
  }
}
</script>

<style scoped>
.login-dialog :deep(.el-dialog) {
  border-radius: 1.25rem;
  overflow: hidden;
}

.login-dialog :deep(.el-dialog__header) {
  display: none;
}

.login-dialog :deep(.el-dialog__body) {
  padding: 2rem 1.75rem 1.5rem;
}

.login-tabs :deep(.el-tabs__header) {
  margin-bottom: 0;
}

.login-tabs :deep(.el-tabs__nav-wrap::after) {
  height: 1px;
  background-color: #2D6A4F15;
}

.login-tabs :deep(.el-tabs__item) {
  font-size: 0.9rem;
  font-weight: 500;
  color: #6B705C;
}

.login-tabs :deep(.el-tabs__item.is-active) {
  color: #1B1B1B;
  font-weight: 600;
}

.login-tabs :deep(.el-tabs__active-bar) {
  background-color: #f97316;
}

.login-tabs :deep(.el-input__wrapper) {
  border-radius: 0.75rem;
  box-shadow: 0 0 0 1px #2D6A4F20 inset;
  padding: 4px 12px;
}

.login-tabs :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #2D6A4F40 inset;
}

.login-tabs :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #2D6A4F inset, 0 0 0 3px #2D6A4F15;
}

.login-tabs :deep(.el-form-item) {
  margin-bottom: 1rem;
}
</style>
