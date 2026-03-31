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
        <svg width="38" height="38" viewBox="60 130 330 200" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="dlgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#f97316"/>
              <stop offset="100%" style="stop-color:#ef4444"/>
            </linearGradient>
          </defs>
          <path d="M100 300 Q130 270 160 285 Q190 300 220 270 Q250 240 280 260 Q310 280 340 250 Q370 220 400 240 Q420 255 420 255" fill="none" stroke="#f9731618" stroke-width="36" stroke-linecap="round"/>
          <ellipse cx="100" cy="300" rx="24" ry="22" fill="url(#dlgGrad)" opacity="0.5"/>
          <ellipse cx="152" cy="278" rx="26" ry="24" fill="url(#dlgGrad)" opacity="0.55"/>
          <ellipse cx="208" cy="268" rx="28" ry="26" fill="url(#dlgGrad)" opacity="0.6"/>
          <ellipse cx="266" cy="262" rx="30" ry="28" fill="url(#dlgGrad)" opacity="0.65"/>
          <ellipse cx="326" cy="250" rx="32" ry="30" fill="url(#dlgGrad)" opacity="0.7"/>
          <ellipse cx="386" cy="238" rx="34" ry="32" fill="url(#dlgGrad)" opacity="0.8"/>
          <ellipse cx="420" cy="238" rx="48" ry="46" fill="url(#dlgGrad)"/>
          <ellipse cx="432" cy="228" rx="11" ry="12" fill="white"/>
          <ellipse cx="454" cy="226" rx="10" ry="11" fill="white"/>
          <circle cx="435" cy="227" r="6" fill="#1a1a1a"/>
          <circle cx="457" cy="225" r="5.5" fill="#1a1a1a"/>
          <circle cx="437" cy="225" r="2.2" fill="white"/>
          <circle cx="459" cy="223" r="2" fill="white"/>
          <path d="M432 248 Q443 256 454 246" fill="none" stroke="white" stroke-width="3" stroke-linecap="round"/>
          <circle cx="425" cy="240" r="7" fill="#ff6b6b" opacity="0.25"/>
          <circle cx="461" cy="238" r="6.5" fill="#ff6b6b" opacity="0.25"/>
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
  width: calc(100vw - 2rem) !important;
  max-width: 400px;
  margin: 0 auto;
}

.login-dialog :deep(.el-dialog__header) {
  display: none;
}

.login-dialog :deep(.el-dialog__body) {
  padding: 1.5rem 1.25rem;
}

@media (min-width: 400px) {
  .login-dialog :deep(.el-dialog__body) {
    padding: 2rem 1.75rem 1.5rem;
  }
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
