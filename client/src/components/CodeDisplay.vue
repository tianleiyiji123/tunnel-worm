<template>
  <teleport to="body">
    <transition name="modal">
      <div v-if="visible" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="$emit('close')"></div>

        <!-- Modal -->
        <div class="relative brand-card p-8 max-w-md w-full text-center animate-tunnel-emerge">
          <!-- Worm icon -->
          <div class="w-16 h-16 mx-auto mb-4 bg-[#fefefe] rounded-2xl flex items-center justify-center animate-worm-wiggle shadow-md border border-black/5">
            <svg width="36" height="36" viewBox="60 130 330 200" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="codeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#f97316"/>
                  <stop offset="100%" style="stop-color:#ef4444"/>
                </linearGradient>
              </defs>
              <path d="M100 300 Q130 270 160 285 Q190 300 220 270 Q250 240 280 260 Q310 280 340 250 Q370 220 400 240 Q420 255 420 255" fill="none" stroke="#f9731618" stroke-width="36" stroke-linecap="round"/>
              <ellipse cx="100" cy="300" rx="24" ry="22" fill="url(#codeGrad)" opacity="0.5"/>
              <ellipse cx="152" cy="278" rx="26" ry="24" fill="url(#codeGrad)" opacity="0.55"/>
              <ellipse cx="208" cy="268" rx="28" ry="26" fill="url(#codeGrad)" opacity="0.6"/>
              <ellipse cx="266" cy="262" rx="30" ry="28" fill="url(#codeGrad)" opacity="0.65"/>
              <ellipse cx="326" cy="250" rx="32" ry="30" fill="url(#codeGrad)" opacity="0.7"/>
              <ellipse cx="386" cy="238" rx="34" ry="32" fill="url(#codeGrad)" opacity="0.8"/>
              <ellipse cx="420" cy="238" rx="48" ry="46" fill="url(#codeGrad)"/>
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

          <h3 class="text-lg font-bold text-[#2D6A4F] mb-1">资源已送达！</h3>
          <p class="text-sm text-[#6B705C] mb-6">将以下密码发送给接收方即可提取</p>

          <!-- Code display -->
          <div class="relative mb-6">
            <div class="flex items-center justify-center gap-2 sm:gap-3 bg-gradient-to-br from-[#FEFAE0] to-[#F5F0E8] border-2 border-[#DDA15E]/30 rounded-2xl py-4 sm:py-5 px-4 sm:px-6">
              <span
                v-for="(char, i) in displayCode"
                :key="i"
                class="text-4xl sm:text-5xl font-bold text-[#2D6A4F] w-12 h-13 sm:w-14 sm:h-14 flex items-center justify-center bg-white/80 rounded-xl shadow-sm border border-[#2D6A4F]/10 animate-tunnel-emerge"
                :style="{ animationDelay: `${i * 0.1}s` }"
              >{{ char }}</span>
            </div>
          </div>

          <!-- Copy button -->
          <button
            @click="copyCode"
            class="brand-btn-primary w-full flex items-center justify-center gap-2 mb-4"
          >
            <Check v-if="copied" size="18" />
            <Copy v-else size="18" />
            {{ copied ? '已复制到剪贴板' : '复制密码' }}
          </button>

          <!-- Expiry notice -->
          <p class="text-xs text-[#6B705C]/60 mb-4">
            密码将在 <span class="font-medium text-[#E76F51]">{{ expireText }}</span> 后过期
          </p>

          <!-- Done button -->
          <button
            @click="$emit('close')"
            class="text-sm text-[#6B705C] hover:text-[#2D6A4F] transition-colors cursor-pointer"
          >
            完成
          </button>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Copy, Check } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  visible: boolean
  code: string
  expiresAt: string
}>()

defineEmits(['close'])

const copied = ref(false)
const displayCode = computed(() => props.code.split(''))
const expireText = computed(() => {
  const expiry = new Date(props.expiresAt)
  const now = new Date()
  const diff = expiry.getTime() - now.getTime()
  const hours = Math.floor(diff / (1000 * 60 * 60))
  if (hours >= 1) return `${hours} 小时`
  const minutes = Math.floor(diff / (1000 * 60))
  return `${minutes} 分钟`
})

async function copyCode() {
  try {
    await navigator.clipboard.writeText(props.code)
    copied.value = true
    ElMessage.success('密码已复制')
    setTimeout(() => { copied.value = false }, 2000)
  } catch {
    // Fallback
    const ta = document.createElement('textarea')
    ta.value = props.code
    document.body.appendChild(ta)
    ta.select()
    document.execCommand('copy')
    document.body.removeChild(ta)
    copied.value = true
    ElMessage.success('密码已复制')
    setTimeout(() => { copied.value = false }, 2000)
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
