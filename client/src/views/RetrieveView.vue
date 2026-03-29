<template>
  <div class="max-w-2xl mx-auto px-4 sm:px-6 py-12 sm:py-20">
    <!-- Hero -->
    <div class="text-center mb-10 animate-tunnel-emerge">
      <div class="w-20 h-20 mx-auto mb-5 bg-gradient-to-br from-[#E76F51]/20 to-[#DDA15E]/20 rounded-3xl flex items-center justify-center">
        <Download size="36" class="text-[#E76F51]" />
      </div>
      <h1 class="text-3xl sm:text-4xl font-bold text-[#1B1B1B] mb-2">
        提取你的资源
      </h1>
      <p class="text-[#6B705C] text-base sm:text-lg">
        输入发送方提供的 4 位数字密码
      </p>
    </div>

    <!-- Input Card -->
    <div v-if="!transferData" class="brand-card p-6 sm:p-8 animate-tunnel-emerge" style="animation-delay: 0.15s">
      <PasswordInput ref="passwordInputRef" v-model="code" />

      <div class="mt-8">
        <button
          @click="handleRetrieve"
          :disabled="!code || code.length !== 4 || loading"
          class="brand-btn-secondary w-full flex items-center justify-center gap-2 py-4 text-base"
          :class="!code || code.length !== 4 || loading ? 'opacity-50 cursor-not-allowed' : ''"
        >
          <div v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
          <Unlock v-else size="20" />
          {{ loading ? '正在提取...' : '提取资源' }}
        </button>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="errorMsg" class="brand-card p-8 text-center animate-tunnel-emerge">
      <div class="w-16 h-16 mx-auto mb-4 bg-[#E76F51]/10 rounded-2xl flex items-center justify-center">
        <AlertCircle size="32" class="text-[#E76F51]" />
      </div>
      <h3 class="text-lg font-bold text-[#1B1B1B] mb-2">提取失败</h3>
      <p class="text-sm text-[#6B705C] mb-6">{{ errorMsg }}</p>
      <button @click="resetState" class="brand-btn-primary px-6 py-2.5">
        重新输入密码
      </button>
    </div>

    <!-- Success State -->
    <div v-else-if="transferData" class="brand-card p-6 sm:p-8">
      <!-- Success header -->
      <div class="flex items-center gap-3 mb-6 pb-4 border-b border-[#2D6A4F]/10">
        <div class="w-10 h-10 rounded-xl bg-[#52B788]/20 flex items-center justify-center">
          <CheckCircle size="22" class="text-[#2D6A4F]" />
        </div>
        <div>
          <h3 class="text-base font-bold text-[#2D6A4F]">资源提取成功</h3>
          <p class="text-xs text-[#6B705C]/60">密码 {{ transferData.code }}</p>
        </div>
      </div>

      <ResourcePreview :data="transferData" />

      <!-- New retrieval -->
      <div class="mt-6 pt-4 border-t border-[#2D6A4F]/10">
        <button @click="resetState" class="text-sm text-[#6B705C] hover:text-[#2D6A4F] transition-colors cursor-pointer">
          提取其他资源 →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Download, Unlock, AlertCircle, CheckCircle } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'
import { retrieveTransfer } from '../api'
import PasswordInput from '../components/PasswordInput.vue'
import ResourcePreview from '../components/ResourcePreview.vue'

interface TransferData {
  code: string
  type: string
  text_content: string | null
  files: Array<{ name: string; size: number; content_type: string; download_url: string }> | null
  created_at: string
  expires_at: string
  download_count: number
}

const code = ref('')
const loading = ref(false)
const errorMsg = ref('')
const transferData = ref<TransferData | null>(null)
const passwordInputRef = ref<InstanceType<typeof PasswordInput> | null>(null)

async function handleRetrieve() {
  if (code.value.length !== 4) return

  loading.value = true
  errorMsg.value = ''
  transferData.value = null

  try {
    const result = await retrieveTransfer(code.value)
    transferData.value = result
  } catch (err: any) {
    const detail = err.response?.data?.detail || '提取失败，请重试'
    errorMsg.value = detail
  } finally {
    loading.value = false
  }
}

function resetState() {
  code.value = ''
  errorMsg.value = ''
  transferData.value = null
  passwordInputRef.value?.clear()
}
</script>
