<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 py-12 sm:py-20">
    <!-- Hero -->
    <div class="text-center mb-10 animate-tunnel-emerge">
      <div class="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-[#2D6A4F]/20 to-[#52B788]/20 rounded-2xl flex items-center justify-center">
        <History size="30" class="text-[#2D6A4F]" />
      </div>
      <h1 class="text-3xl sm:text-4xl font-bold text-[#1B1B1B] mb-2">我的记录</h1>
      <p v-if="isLoggedIn" class="text-[#6B705C] text-base">
        共 {{ sendCount }} 次发送，{{ retrieveCount }} 次提取
      </p>
    </div>

    <!-- Not logged in state -->
    <div v-if="!isLoggedIn" class="brand-card p-8 text-center animate-tunnel-emerge">
      <div class="w-16 h-16 mx-auto mb-4 bg-[#2D6A4F]/10 rounded-2xl flex items-center justify-center">
        <LogIn size="28" class="text-[#2D6A4F]" />
      </div>
      <h3 class="text-lg font-bold text-[#1B1B1B] mb-2">请先登录</h3>
      <p class="text-sm text-[#6B705C] mb-6">登录后可以查看发送和提取记录</p>
      <button @click="showLoginDialog = true" class="brand-btn-primary px-6 py-2.5">
        立即登录
      </button>
    </div>
    <template v-else>
      <!-- Tabs -->
      <div class="brand-card p-4 sm:p-6 animate-tunnel-emerge" style="animation-delay: 0.1s">
        <div class="flex gap-1 p-1 bg-[#F5F0E8] rounded-xl mb-4">
          <button
            @click="switchTab('send')"
            class="flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-200 cursor-pointer"
            :class="activeAction === 'send' ? 'bg-white text-[#2D6A4F] shadow-sm' : 'text-[#6B705C] hover:text-[#2D6A4F]'"
          >
            <span class="flex items-center justify-center gap-1.5">
              <Upload size="14" />
              发送记录
            </span>
          </button>
          <button
            @click="switchTab('retrieve')"
            class="flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-200 cursor-pointer"
            :class="activeAction === 'retrieve' ? 'bg-white text-[#2D6A4F] shadow-sm' : 'text-[#6B705C] hover:text-[#2D6A4F]'"
          >
            <span class="flex items-center justify-center gap-1.5">
              <Download size="14" />
              提取记录
            </span>
          </button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="py-12 text-center">
          <div class="w-8 h-8 border-2 border-[#2D6A4F]/20 border-t-[#2D6A4F] rounded-full animate-spin mx-auto"></div>
          <p class="text-sm text-[#6B705C]/60 mt-3">加载中...</p>
        </div>

        <!-- Empty state -->
        <div v-else-if="records.length === 0" class="py-12 text-center">
          <Inbox size="40" class="text-[#6B705C]/30 mx-auto mb-3" />
          <p class="text-sm text-[#6B705C]/60">暂无{{ activeAction === 'send' ? '发送' : '提取' }}记录</p>
        </div>

        <!-- Records list -->
        <div v-else class="space-y-3">
          <div
            v-for="item in records"
            :key="item.id"
            class="flex items-center gap-3 p-3 rounded-xl bg-[#F5F0E8]/50 hover:bg-[#F5F0E8] transition-colors group"
          >
            <!-- Action icon -->
            <div
              class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
              :class="item.action === 'send' ? 'bg-[#2D6A4F]/10' : 'bg-[#E76F51]/10'"
            >
              <component
                :is="item.action === 'send' ? Upload : Download"
                :size="18"
                :class="item.action === 'send' ? 'text-[#2D6A4F]' : 'text-[#E76F51]'"
              />
            </div>

            <!-- Info -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="text-sm font-medium text-[#1B1B1B]">
                  {{ item.action === 'send' ? '发送' : '提取' }}
                </span>
                <span class="text-xs text-[#6B705C]/50 font-mono bg-[#6B705C]/10 px-1.5 py-0.5 rounded">
                  {{ item.transfer_code }}
                </span>
                <!-- Permanent badge -->
                <span
                  v-if="item.permanent"
                  class="text-xs bg-[#52B788]/15 text-[#2D6A4F] px-1.5 py-0.5 rounded font-medium"
                >
                  永久
                </span>
                <!-- Type badge -->
                <span
                  v-if="item.transfer_type"
                  class="text-xs text-[#6B705C]/50"
                >
                  {{ typeLabel(item.transfer_type) }}
                </span>
              </div>
              <p class="text-xs text-[#6B705C]/60 mt-1 truncate">
                <template v-if="item.text_preview">
                  {{ item.text_preview }}
                </template>
                <template v-else-if="item.file_count > 0">
                  {{ item.file_count }} 个文件
                </template>
                <template v-else>
                  -
                </template>
              </p>
            </div>

            <!-- Time -->
            <div class="text-right shrink-0">
              <p class="text-xs text-[#6B705C]/50">{{ formatTime(item.created_at) }}</p>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="total > pageSize" class="mt-4 pt-4 border-t border-[#2D6A4F]/10 flex justify-center">
          <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="total"
            layout="prev, pager, next"
            small
            @current-change="fetchRecords"
          />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, inject, type Ref } from 'vue'
import { History, Upload, Download, LogIn, Inbox } from 'lucide-vue-next'
import { getRecords, type RecordItem } from '../api'
import { useAuth } from '../composables/useAuth'

const { isLoggedIn } = useAuth()
const showLoginDialog = inject<Ref<boolean>>('showLoginDialog')!
const activeAction = ref<'send' | 'retrieve'>('send')
const records = ref<RecordItem[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = 20
const total = ref(0)
const sendCount = ref(0)
const retrieveCount = ref(0)

function typeLabel(type: string) {
  const map: Record<string, string> = {
    text: '文本',
    file: '文件',
    mixed: '文本+文件',
  }
  return map[type] || type
}

function formatTime(dateStr: string) {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)} 小时前`
  if (diff < 172800000) return '昨天'

  return `${date.getMonth() + 1}/${date.getDate()} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

async function fetchRecords() {
  if (!isLoggedIn.value) return
  loading.value = true
  try {
    const res = await getRecords(activeAction.value, currentPage.value, pageSize)
    records.value = res.items
    total.value = res.total
  } catch {
    // silently fail
  } finally {
    loading.value = false
  }
}

async function fetchCounts() {
  if (!isLoggedIn.value) return
  try {
    const [sendRes, retrieveRes] = await Promise.all([
      getRecords('send', 1, 1),
      getRecords('retrieve', 1, 1),
    ])
    sendCount.value = sendRes.total
    retrieveCount.value = retrieveRes.total
  } catch {
    // silently fail
  }
}

function switchTab(action: 'send' | 'retrieve') {
  activeAction.value = action
  currentPage.value = 1
  fetchRecords()
}

function onLoginSuccess() {
  showLoginDialog.value = false
  fetchRecords()
  fetchCounts()
}

onMounted(() => {
  if (isLoggedIn.value) {
    fetchRecords()
    fetchCounts()
  }
})
</script>
