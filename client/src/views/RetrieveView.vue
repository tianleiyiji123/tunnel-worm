<template>
  <div class="max-w-2xl mx-auto px-4 sm:px-6 py-12 sm:py-20">
    <!-- Hero -->
    <div class="text-center mb-10 animate-tunnel-emerge">
      <div class="w-20 h-20 mx-auto mb-5 bg-[#fefefe] rounded-3xl flex items-center justify-center animate-worm-wiggle shadow-md shadow-black/5 border border-black/5">
        <svg width="56" height="56" viewBox="60 130 330 200" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="retGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#f97316"/>
              <stop offset="100%" style="stop-color:#ef4444"/>
            </linearGradient>
          </defs>
          <path d="M100 300 Q130 270 160 285 Q190 300 220 270 Q250 240 280 260 Q310 280 340 250 Q370 220 400 240 Q420 255 420 255" fill="none" stroke="#f9731618" stroke-width="36" stroke-linecap="round"/>
          <ellipse cx="100" cy="300" rx="24" ry="22" fill="url(#retGrad)" opacity="0.5"/>
          <ellipse cx="152" cy="278" rx="26" ry="24" fill="url(#retGrad)" opacity="0.55"/>
          <ellipse cx="208" cy="268" rx="28" ry="26" fill="url(#retGrad)" opacity="0.6"/>
          <ellipse cx="266" cy="262" rx="30" ry="28" fill="url(#retGrad)" opacity="0.65"/>
          <ellipse cx="326" cy="250" rx="32" ry="30" fill="url(#retGrad)" opacity="0.7"/>
          <ellipse cx="386" cy="238" rx="34" ry="32" fill="url(#retGrad)" opacity="0.8"/>
          <ellipse cx="420" cy="238" rx="48" ry="46" fill="url(#retGrad)"/>
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
      <h1 class="text-3xl sm:text-4xl font-bold text-[#1B1B1B] mb-2">
        提取你的资源
      </h1>
      <p class="text-[#6B705C] text-base sm:text-lg">
        输入发送方提供的密码
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
import { Unlock, AlertCircle, CheckCircle } from 'lucide-vue-next'
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
    ElMessage.error(detail)
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
