<template>
  <div class="space-y-5 animate-tunnel-emerge">
    <!-- Text content -->
    <div v-if="data.text_content" class="space-y-2">
      <div class="flex items-center justify-between">
        <label class="text-sm font-medium text-[#6B705C]">文本内容</label>
        <button
          @click="copyText"
          class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-[#2D6A4F] bg-[#2D6A4F]/10 rounded-lg hover:bg-[#2D6A4F]/20 transition-colors cursor-pointer"
        >
          <Check v-if="textCopied" size="14" />
          <Copy v-else size="14" />
          {{ textCopied ? '已复制' : '复制' }}
        </button>
      </div>
      <div class="p-4 bg-[#FEFAE0]/50 rounded-xl border border-[#DDA15E]/20 max-h-60 overflow-y-auto">
        <pre class="text-sm text-[#1B1B1B] whitespace-pre-wrap break-all font-sans leading-relaxed">{{ data.text_content }}</pre>
      </div>
    </div>

    <!-- File list -->
    <div v-if="data.files && data.files.length > 0" class="space-y-2">
      <label class="text-sm font-medium text-[#6B705C]">
        文件 ({{ data.files.length }} 个)
      </label>
      <div class="space-y-2">
        <div
          v-for="(file, index) in data.files"
          :key="index"
          class="flex items-center gap-3 p-3.5 bg-white/60 rounded-xl border border-[#2D6A4F]/10 hover:border-[#2D6A4F]/30 transition-all duration-200 group"
        >
          <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-[#52B788]/20 to-[#2D6A4F]/20 flex items-center justify-center flex-shrink-0">
            <FileText size="20" class="text-[#2D6A4F]" />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-[#1B1B1B] truncate">{{ file.name }}</p>
            <p class="text-xs text-[#6B705C]/60">{{ formatSize(file.size) }}</p>
          </div>
          <a
            :href="file.download_url"
            download
            class="flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-white bg-[#2D6A4F] rounded-lg hover:bg-[#40916C] transition-colors sm:opacity-0 sm:group-hover:opacity-100 shrink-0"
          >
            <Download size="14" />
            下载
          </a>
        </div>
      </div>
    </div>

    <!-- Meta info -->
    <div class="flex items-center justify-between pt-2 border-t border-[#2D6A4F]/10">
      <span class="text-xs text-[#6B705C]/50">
        已被提取 {{ data.download_count }} 次
      </span>
      <span class="text-xs text-[#6B705C]/50">
        过期时间: {{ formatExpiry(data.expires_at) }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Copy, Check, FileText, Download } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

interface TransferData {
  code: string
  type: string
  text_content: string | null
  files: Array<{ name: string; size: number; content_type: string; download_url: string }> | null
  created_at: string
  expires_at: string
  download_count: number
}

const props = defineProps<{ data: TransferData }>()

const textCopied = ref(false)

function formatSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

function formatExpiry(dateStr: string): string {
  return new Date(dateStr).toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

async function copyText() {
  if (!props.data.text_content) return
  try {
    await navigator.clipboard.writeText(props.data.text_content)
    textCopied.value = true
    ElMessage.success('文本已复制')
    setTimeout(() => { textCopied.value = false }, 2000)
  } catch {
    ElMessage.error('复制失败')
  }
}
</script>
