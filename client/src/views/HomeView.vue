<template>
  <div class="max-w-2xl mx-auto px-4 sm:px-6 py-12 sm:py-20">
    <!-- Hero Section -->
    <div class="text-center mb-10 animate-tunnel-emerge">
      <div class="w-20 h-20 mx-auto mb-5 bg-[#fefefe] rounded-3xl flex items-center justify-center animate-worm-wiggle shadow-md shadow-black/5 border border-black/5">
        <svg width="56" height="56" viewBox="60 130 330 200" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#f97316"/>
              <stop offset="100%" style="stop-color:#ef4444"/>
            </linearGradient>
          </defs>
          <path d="M100 300 Q130 270 160 285 Q190 300 220 270 Q250 240 280 260 Q310 280 340 250 Q370 220 400 240 Q420 255 420 255" fill="none" stroke="#f9731618" stroke-width="36" stroke-linecap="round"/>
          <ellipse cx="100" cy="300" rx="24" ry="22" fill="url(#heroGrad)" opacity="0.5"/>
          <ellipse cx="152" cy="278" rx="26" ry="24" fill="url(#heroGrad)" opacity="0.55"/>
          <ellipse cx="208" cy="268" rx="28" ry="26" fill="url(#heroGrad)" opacity="0.6"/>
          <ellipse cx="266" cy="262" rx="30" ry="28" fill="url(#heroGrad)" opacity="0.65"/>
          <ellipse cx="326" cy="250" rx="32" ry="30" fill="url(#heroGrad)" opacity="0.7"/>
          <ellipse cx="386" cy="238" rx="34" ry="32" fill="url(#heroGrad)" opacity="0.8"/>
          <ellipse cx="420" cy="238" rx="48" ry="46" fill="url(#heroGrad)"/>
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
        跨设备，传什么都可以
      </h1>
      <p class="text-[#6B705C] text-base sm:text-lg">
        上传文本或文件，生成密码，另一台设备输入密码即可提取
      </p>
    </div>

    <!-- Main Card -->
    <div class="brand-card p-6 sm:p-8 animate-tunnel-emerge" style="animation-delay: 0.15s">
      <!-- Tabs -->
      <div class="flex gap-1 p-1 bg-[#F5F0E8] rounded-xl mb-6">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="flex-1 py-2.5 px-4 rounded-lg text-sm font-medium transition-all duration-200 cursor-pointer"
          :class="activeTab === tab.id
            ? 'bg-white text-[#2D6A4F] shadow-sm'
            : 'text-[#6B705C] hover:text-[#2D6A4F]'"
        >
          <span class="flex items-center justify-center gap-1.5">
            <component :is="tab.icon" :size="16" />
            {{ tab.label }}
          </span>
        </button>
      </div>

      <!-- Text Tab -->
      <div v-show="activeTab === 'text'">
        <SendText ref="sendTextRef" />
      </div>

      <!-- File Tab -->
      <div v-show="activeTab === 'file'">
        <SendFile ref="sendFileRef" />
      </div>

      <!-- Mixed Tab -->
      <div v-show="activeTab === 'mixed'" class="space-y-6">
        <SendText ref="mixedTextRef" />
        <div class="flex items-center gap-3">
          <div class="flex-1 h-px bg-[#2D6A4F]/10"></div>
          <span class="text-xs text-[#6B705C]/50 font-medium">还可以附带文件</span>
          <div class="flex-1 h-px bg-[#2D6A4F]/10"></div>
        </div>
        <SendFile ref="sendFileRef2" />
      </div>

      <!-- Submit Button -->
      <div class="mt-8">
        <button
          @click="handleSubmit"
          :disabled="loading"
          class="brand-btn-primary w-full flex items-center justify-center gap-2 py-4 text-base"
          :class="loading ? 'opacity-70 cursor-not-allowed' : ''"
        >
          <div v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
          <Worm v-else :size="20" />
          {{ loading ? '正在传输...' : '生成密码' }}
        </button>
      </div>
    </div>

    <!-- Footer hint -->
    <p class="text-center text-xs text-[#6B705C]/40 mt-6">
      资源保留 24 小时后自动删除 · 数据仅存于服务器，不经过第三方
    </p>

    <!-- Code Display Modal -->
    <CodeDisplay
      :visible="showCodeModal"
      :code="generatedCode"
      :expiresAt="expiresAt"
      @close="showCodeModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Type, FileUp, Layers } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'
import { createTransfer } from '../api'
import SendText from '../components/SendText.vue'
import SendFile from '../components/SendFile.vue'
import CodeDisplay from '../components/CodeDisplay.vue'

const Worm = {
  template: `<svg width="20" height="20" viewBox="60 130 330 200" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="btnWormGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#fff;stop-opacity:0.9"/><stop offset="100%" style="stop-color:#fff;stop-opacity:0.7"/></linearGradient></defs><path d="M100 300 Q130 270 160 285 Q190 300 220 270 Q250 240 280 260 Q310 280 340 250 Q370 220 400 240 Q420 255 420 255" fill="none" stroke="white" stroke-width="36" stroke-linecap="round" opacity="0.2"/><ellipse cx="100" cy="300" rx="24" ry="22" fill="url(#btnWormGrad)" opacity="0.5"/><ellipse cx="152" cy="278" rx="26" ry="24" fill="url(#btnWormGrad)" opacity="0.55"/><ellipse cx="208" cy="268" rx="28" ry="26" fill="url(#btnWormGrad)" opacity="0.6"/><ellipse cx="266" cy="262" rx="30" ry="28" fill="url(#btnWormGrad)" opacity="0.65"/><ellipse cx="326" cy="250" rx="32" ry="30" fill="url(#btnWormGrad)" opacity="0.7"/><ellipse cx="386" cy="238" rx="34" ry="32" fill="url(#btnWormGrad)" opacity="0.8"/><ellipse cx="420" cy="238" rx="48" ry="46" fill="url(#btnWormGrad)"/></svg>`
}

const tabs = [
  { id: 'text', label: '文本', icon: Type },
  { id: 'file', label: '文件', icon: FileUp },
  { id: 'mixed', label: '文本 + 文件', icon: Layers },
]

const activeTab = ref('text')
const loading = ref(false)
const showCodeModal = ref(false)
const generatedCode = ref('')
const expiresAt = ref('')
const sendTextRef = ref<InstanceType<typeof SendText> | null>(null)
const mixedTextRef = ref<InstanceType<typeof SendText> | null>(null)
const sendFileRef = ref<InstanceType<typeof SendFile> | null>(null)
const sendFileRef2 = ref<InstanceType<typeof SendFile> | null>(null)

function getFilesFromRef(fileRef: InstanceType<typeof SendFile> | null): File[] {
  if (!fileRef) return []
  return fileRef.getRawFiles()
}

async function handleSubmit() {
  loading.value = true
  try {
    const formData = new FormData()
    formData.append('type', activeTab.value)

    if (activeTab.value === 'text' || activeTab.value === 'mixed') {
      const text = activeTab.value === 'text'
        ? sendTextRef.value?.getText()
        : mixedTextRef.value?.getText()
      if (!text && activeTab.value === 'text') {
        ElMessage.warning('请输入文本内容')
        loading.value = false
        return
      }
      if (text) formData.append('text_content', text)
    }

    if (activeTab.value === 'file' || activeTab.value === 'mixed') {
      const files = activeTab.value === 'mixed'
        ? getFilesFromRef(sendFileRef2.value)
        : getFilesFromRef(sendFileRef.value)

      if (!files?.length && activeTab.value === 'file') {
        ElMessage.warning('请至少上传一个文件')
        loading.value = false
        return
      }
      if (files?.length) {
        files.forEach((f: File) => formData.append('files', f))
      }
    }

    const result = await createTransfer(formData)
    generatedCode.value = result.code
    expiresAt.value = result.expires_at
    showCodeModal.value = true
  } catch (err: any) {
    const detail = err.response?.data?.detail || '传输失败，请重试'
    ElMessage.error(detail)
  } finally {
    loading.value = false
  }
}
</script>
