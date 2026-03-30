<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-white/70 backdrop-blur-lg border-b border-[#2D6A4F]/10 shadow-sm">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-2.5 group">
        <div class="w-9 h-9 bg-[#fefefe] rounded-xl flex items-center justify-center shadow-md shadow-black/5 group-hover:shadow-lg transition-all duration-300 group-hover:scale-105 border border-black/5">
          <svg width="24" height="24" viewBox="22 62 137 82" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="hGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#f97316"/>
                <stop offset="100%" style="stop-color:#ef4444"/>
              </linearGradient>
            </defs>
            <path d="M40 120 Q70 80 100 100 Q130 120 160 80" fill="none" stroke="#f9731626" stroke-width="20" stroke-linecap="round"/>
            <path d="M40 120 Q70 80 100 100 Q130 120 160 80" fill="none" stroke="url(#hGrad)" stroke-width="4" stroke-linecap="round"/>
            <circle cx="44" cy="118" r="14" fill="url(#hGrad)"/>
            <circle cx="38" cy="115" r="5" fill="white"/>
            <circle cx="39.5" cy="114" r="2.5" fill="#fefefe"/>
            <circle cx="40" cy="113" r="1.4" fill="#1a1a1a"/>
            <path d="M36 120 Q44 127 52 120" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
            <circle cx="58" cy="106" r="10" fill="url(#hGrad)" opacity="0.7"/>
            <circle cx="74" cy="96" r="11" fill="url(#hGrad)" opacity="0.75"/>
            <circle cx="92" cy="100" r="12" fill="url(#hGrad)" opacity="0.8"/>
            <circle cx="110" cy="108" r="11" fill="url(#hGrad)" opacity="0.75"/>
            <circle cx="126" cy="100" r="10" fill="url(#hGrad)" opacity="0.7"/>
            <circle cx="140" cy="88" r="9" fill="url(#hGrad)" opacity="0.6"/>
          </svg>
        </div>
        <span class="text-xl font-bold text-[#1B1B1B] tracking-tight">隧隧虫</span>
      </router-link>

      <!-- Nav -->
      <nav class="flex items-center gap-2">
        <router-link
          to="/"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
          :class="$route.path === '/' ? 'bg-[#2D6A4F]/10 text-[#2D6A4F]' : 'text-[#6B705C] hover:text-[#2D6A4F] hover:bg-[#2D6A4F]/5'"
        >
          <span class="flex items-center gap-1.5">
            <Upload size="16" />
            发送资源
          </span>
        </router-link>
        <router-link
          to="/retrieve"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
          :class="$route.path === '/retrieve' ? 'bg-[#2D6A4F]/10 text-[#2D6A4F]' : 'text-[#6B705C] hover:text-[#2D6A4F] hover:bg-[#2D6A4F]/5'"
        >
          <span class="flex items-center gap-1.5">
            <Download size="16" />
            提取资源
          </span>
        </router-link>

        <!-- Divider -->
        <div class="w-px h-5 bg-[#2D6A4F]/10 mx-1"></div>

        <!-- User section -->
        <template v-if="isLoggedIn">
          <el-dropdown trigger="click" @command="handleCommand">
            <button class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-[#2D6A4F] bg-[#2D6A4F]/5 hover:bg-[#2D6A4F]/10 transition-all cursor-pointer">
              <UserRound size="16" />
              <span>{{ username }}</span>
              <ChevronDown size="14" class="opacity-50" />
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="records">
                  <span class="flex items-center gap-2">
                    <History size="14" />
                    我的记录
                  </span>
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <span class="flex items-center gap-2 text-red-500">
                    <LogOut size="14" />
                    退出登录
                  </span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <button
            @click="$emit('openLogin')"
            class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium text-[#6B705C] hover:text-[#2D6A4F] hover:bg-[#2D6A4F]/5 transition-all cursor-pointer"
          >
            <LogIn size="16" />
            登录
          </button>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Upload, Download, LogIn, LogOut, UserRound, ChevronDown, History } from 'lucide-vue-next'
import { useAuth } from '../composables/useAuth'

const emit = defineEmits<{
  openLogin: []
}>()

const router = useRouter()
const { isLoggedIn, username, logout } = useAuth()

function handleCommand(command: string) {
  if (command === 'records') {
    router.push('/records')
  } else if (command === 'logout') {
    logout()
    router.push('/')
  }
}
</script>
