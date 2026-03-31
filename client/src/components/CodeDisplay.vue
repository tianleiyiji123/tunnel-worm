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
            <svg width="36" height="36" viewBox="22 62 137 82" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="codeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#f97316"/>
                  <stop offset="100%" style="stop-color:#ef4444"/>
                </linearGradient>
              </defs>
              <path d="M40 120 Q70 80 100 100 Q130 120 160 80" fill="none" stroke="#f9731626" stroke-width="20" stroke-linecap="round"/>
              <path d="M40 120 Q70 80 100 100 Q130 120 160 80" fill="none" stroke="url(#codeGrad)" stroke-width="4" stroke-linecap="round"/>
              <circle cx="44" cy="118" r="14" fill="url(#codeGrad)"/>
              <circle cx="38" cy="115" r="5" fill="white"/>
              <circle cx="39.5" cy="114" r="2.5" fill="#fefefe"/>
              <circle cx="40" cy="113" r="1.4" fill="#1a1a1a"/>
              <path d="M36 120 Q44 127 52 120" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
              <circle cx="58" cy="106" r="10" fill="url(#codeGrad)" opacity="0.7"/>
              <circle cx="74" cy="96" r="11" fill="url(#codeGrad)" opacity="0.75"/>
              <circle cx="92" cy="100" r="12" fill="url(#codeGrad)" opacity="0.8"/>
              <circle cx="110" cy="108" r="11" fill="url(#codeGrad)" opacity="0.75"/>
              <circle cx="126" cy="100" r="10" fill="url(#codeGrad)" opacity="0.7"/>
              <circle cx="140" cy="88" r="9" fill="url(#codeGrad)" opacity="0.6"/>
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
