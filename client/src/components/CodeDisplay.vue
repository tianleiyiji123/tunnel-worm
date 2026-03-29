<template>
  <teleport to="body">
    <transition name="modal">
      <div v-if="visible" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="$emit('close')"></div>

        <!-- Modal -->
        <div class="relative brand-card p-8 max-w-md w-full text-center animate-tunnel-emerge">
          <!-- Worm icon -->
          <div class="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-[#52B788]/20 to-[#2D6A4F]/20 rounded-2xl flex items-center justify-center animate-worm-wiggle">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
              <path d="M12 4C9 4 6 6 6 10c0 3 2 5 4 7 1-1 2-1 2-1s1 0 2 1c2-2 4-4 4-7 0-4-3-6-6-6z" fill="#2D6A4F" opacity="0.3"/>
              <path d="M12 2c-2 0-4 1-5 3l-1 2c-1 2-1 4 0 6l3 5c1 2 3 3 5 3s4-1 5-3l3-5c1-2 1-4 0-6l-1-2c-1-2-3-3-5-3h-4z" stroke="#2D6A4F" stroke-width="1.5" stroke-linecap="round" fill="none"/>
              <circle cx="10" cy="9" r="1.2" fill="#2D6A4F"/>
              <circle cx="14" cy="9" r="1.2" fill="#2D6A4F"/>
              <path d="M10 12c0 0 1 1.5 2 1.5s2-1.5 2-1.5" stroke="#2D6A4F" stroke-width="1.2" stroke-linecap="round" fill="none"/>
            </svg>
          </div>

          <h3 class="text-lg font-bold text-[#2D6A4F] mb-1">资源已送达！</h3>
          <p class="text-sm text-[#6B705C] mb-6">将以下密码发送给接收方即可提取</p>

          <!-- Code display -->
          <div class="relative mb-6">
            <div class="flex items-center justify-center gap-3 bg-gradient-to-br from-[#FEFAE0] to-[#F5F0E8] border-2 border-[#DDA15E]/30 rounded-2xl py-5 px-6">
              <span
                v-for="(char, i) in displayCode"
                :key="i"
                class="text-5xl font-bold text-[#2D6A4F] w-12 h-14 flex items-center justify-center bg-white/80 rounded-xl shadow-sm border border-[#2D6A4F]/10 animate-tunnel-emerge"
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
