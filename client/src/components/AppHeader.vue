<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-white/70 backdrop-blur-lg border-b border-[#2D6A4F]/10 shadow-sm">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-2.5 group">
        <div class="w-9 h-9 bg-gradient-to-br from-[#2D6A4F] to-[#52B788] rounded-xl flex items-center justify-center shadow-md shadow-[#2D6A4F]/20 group-hover:shadow-lg group-hover:shadow-[#2D6A4F]/30 transition-all duration-300 group-hover:scale-105">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" class="text-white">
            <path d="M12 4C9 4 6 6 6 10c0 3 2 5 4 7 1-1 2-1 2-1s1 0 2 1c2-2 4-4 4-7 0-4-3-6-6-6z" fill="currentColor" opacity="0.3"/>
            <path d="M12 2c-2 0-4 1-5 3l-1 2c-1 2-1 4 0 6l3 5c1 2 3 3 5 3s4-1 5-3l3-5c1-2 1-4 0-6l-1-2c-1-2-3-3-5-3h-4z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/>
            <circle cx="10" cy="9" r="1.2" fill="currentColor"/>
            <circle cx="14" cy="9" r="1.2" fill="currentColor"/>
            <path d="M10 12c0 0 1 1.5 2 1.5s2-1.5 2-1.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" fill="none"/>
          </svg>
        </div>
        <span class="text-xl font-bold text-[#2D6A4F] tracking-tight">隧隧虫</span>
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
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { Upload, Download } from 'lucide-vue-next'
</script>
