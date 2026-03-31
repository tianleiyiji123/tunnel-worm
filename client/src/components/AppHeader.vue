<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-white/70 backdrop-blur-lg border-b border-[#2D6A4F]/10 shadow-sm">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 h-14 sm:h-16 flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-2.5 group" @click="closeMobileMenu">
        <div class="w-9 h-9 bg-[#fefefe] rounded-xl flex items-center justify-center shadow-md shadow-black/5 group-hover:shadow-lg transition-all duration-300 group-hover:scale-105 border border-black/5">
          <svg width="28" height="28" viewBox="60 130 330 200" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="hGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#f97316"/>
                <stop offset="100%" style="stop-color:#ef4444"/>
              </linearGradient>
            </defs>
            <path d="M100 300 Q130 270 160 285 Q190 300 220 270 Q250 240 280 260 Q310 280 340 250 Q370 220 400 240 Q420 255 420 255" fill="none" stroke="#f9731618" stroke-width="36" stroke-linecap="round"/>
            <ellipse cx="100" cy="300" rx="24" ry="22" fill="url(#hGrad)" opacity="0.5"/>
            <ellipse cx="152" cy="278" rx="26" ry="24" fill="url(#hGrad)" opacity="0.55"/>
            <ellipse cx="208" cy="268" rx="28" ry="26" fill="url(#hGrad)" opacity="0.6"/>
            <ellipse cx="266" cy="262" rx="30" ry="28" fill="url(#hGrad)" opacity="0.65"/>
            <ellipse cx="326" cy="250" rx="32" ry="30" fill="url(#hGrad)" opacity="0.7"/>
            <ellipse cx="386" cy="238" rx="34" ry="32" fill="url(#hGrad)" opacity="0.8"/>
            <ellipse cx="420" cy="238" rx="48" ry="46" fill="url(#hGrad)"/>
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
        <span class="text-xl font-bold text-[#1B1B1B] tracking-tight">隧隧虫</span>
      </router-link>

      <!-- Desktop Nav -->
      <nav class="hidden sm:flex items-center gap-2">
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

      <!-- Mobile Menu Button -->
      <button
        class="sm:hidden p-2 -mr-2 rounded-lg text-[#6B705C] hover:text-[#2D6A4F] hover:bg-[#2D6A4F]/5 transition-all cursor-pointer"
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        <Menu v-if="!mobileMenuOpen" size="22" />
        <X v-else size="22" />
      </button>
    </div>

    <!-- Mobile Menu Panel -->
    <transition name="mobile-menu">
      <div v-if="mobileMenuOpen" class="sm:hidden bg-white/95 backdrop-blur-lg border-t border-[#2D6A4F]/10">
        <nav class="max-w-5xl mx-auto px-4 py-3 space-y-1">
          <router-link
            to="/"
            class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all"
            :class="$route.path === '/' ? 'bg-[#2D6A4F]/10 text-[#2D6A4F]' : 'text-[#6B705C] hover:bg-[#2D6A4F]/5'"
            @click="closeMobileMenu"
          >
            <Upload size="18" />
            发送资源
          </router-link>
          <router-link
            to="/retrieve"
            class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all"
            :class="$route.path === '/retrieve' ? 'bg-[#2D6A4F]/10 text-[#2D6A4F]' : 'text-[#6B705C] hover:bg-[#2D6A4F]/5'"
            @click="closeMobileMenu"
          >
            <Download size="18" />
            提取资源
          </router-link>

          <div class="h-px bg-[#2D6A4F]/10 my-2"></div>

          <!-- User section -->
          <template v-if="isLoggedIn">
            <button
              class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-[#6B705C] hover:bg-[#2D6A4F]/5 transition-all w-full cursor-pointer"
              @click="handleCommand('records'); closeMobileMenu()"
            >
              <UserRound size="18" />
              {{ username }}
            </button>
            <button
              class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-red-500 hover:bg-red-50 transition-all w-full cursor-pointer"
              @click="handleCommand('logout'); closeMobileMenu()"
            >
              <LogOut size="18" />
              退出登录
            </button>
          </template>
          <template v-else>
            <button
              class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-[#6B705C] hover:bg-[#2D6A4F]/5 transition-all w-full cursor-pointer"
              @click="$emit('openLogin'); closeMobileMenu()"
            >
              <LogIn size="18" />
              登录
            </button>
          </template>
        </nav>
      </div>
    </transition>
  </header>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Upload, Download, LogIn, LogOut, UserRound, ChevronDown, History, Menu, X } from 'lucide-vue-next'
import { useAuth } from '../composables/useAuth'

const emit = defineEmits<{
  openLogin: []
}>()

const router = useRouter()
const route = useRoute()
const { isLoggedIn, username, logout } = useAuth()
const mobileMenuOpen = ref(false)

// Close mobile menu on route change
watch(() => route.path, () => {
  mobileMenuOpen.value = false
})

function closeMobileMenu() {
  mobileMenuOpen.value = false
}

function handleCommand(command: string) {
  if (command === 'records') {
    router.push('/records')
  } else if (command === 'logout') {
    logout()
    router.push('/')
  }
}
</script>

<style scoped>
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
