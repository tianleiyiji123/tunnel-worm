<template>
  <header
    class="fixed top-0 left-0 right-0 z-50 bg-white/70 backdrop-blur-lg border-b border-[#2D6A4F]/10 shadow-sm"
  >
    <div
      class="max-w-5xl mx-auto px-4 sm:px-6 h-14 sm:h-16 flex items-center justify-between"
    >
      <!-- Logo -->
      <router-link
        to="/"
        class="flex items-center gap-2.5 group"
        @click="closeMobileMenu"
      >
        <div
          class="w-9 h-9 bg-[#fefefe] rounded-xl flex items-center justify-center shadow-md shadow-black/5 group-hover:shadow-lg transition-all duration-300 group-hover:scale-105 border border-black/5 overflow-hidden"
        >
          <img
            :src="logoImg"
            alt="隧隧虫"
            class="w-full h-full object-contain"
          />
        </div>
        <span class="text-xl font-bold text-[#1B1B1B] tracking-tight"
          >隧隧虫</span
        >
      </router-link>

      <!-- Desktop Nav -->
      <nav class="hidden sm:flex items-center gap-2">
        <router-link
          to="/"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
          :class="
            $route.path === '/'
              ? 'bg-[#2D6A4F]/10 text-[#2D6A4F]'
              : 'text-[#6B705C] hover:text-[#2D6A4F] hover:bg-[#2D6A4F]/5'
          "
        >
          <span class="flex items-center gap-1.5">
            <Upload size="16" />
            发送资源
          </span>
        </router-link>
        <router-link
          to="/retrieve"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
          :class="
            $route.path === '/retrieve'
              ? 'bg-[#2D6A4F]/10 text-[#2D6A4F]'
              : 'text-[#6B705C] hover:text-[#2D6A4F] hover:bg-[#2D6A4F]/5'
          "
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
            <button
              class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-[#2D6A4F] bg-[#2D6A4F]/5 hover:bg-[#2D6A4F]/10 transition-all cursor-pointer"
            >
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
      <div
        v-if="mobileMenuOpen"
        class="sm:hidden bg-white/95 backdrop-blur-lg border-t border-[#2D6A4F]/10"
      >
        <nav class="max-w-5xl mx-auto px-4 py-3 space-y-1">
          <router-link
            to="/"
            class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all"
            :class="
              $route.path === '/'
                ? 'bg-[#2D6A4F]/10 text-[#2D6A4F]'
                : 'text-[#6B705C] hover:bg-[#2D6A4F]/5'
            "
            @click="closeMobileMenu"
          >
            <Upload size="18" />
            发送资源
          </router-link>
          <router-link
            to="/retrieve"
            class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all"
            :class="
              $route.path === '/retrieve'
                ? 'bg-[#2D6A4F]/10 text-[#2D6A4F]'
                : 'text-[#6B705C] hover:bg-[#2D6A4F]/5'
            "
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
              @click="
                handleCommand('records');
                closeMobileMenu();
              "
            >
              <UserRound size="18" />
              {{ username }}
            </button>
            <button
              class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-red-500 hover:bg-red-50 transition-all w-full cursor-pointer"
              @click="
                handleCommand('logout');
                closeMobileMenu();
              "
            >
              <LogOut size="18" />
              退出登录
            </button>
          </template>
          <template v-else>
            <button
              class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-[#6B705C] hover:bg-[#2D6A4F]/5 transition-all w-full cursor-pointer"
              @click="
                $emit('openLogin');
                closeMobileMenu();
              "
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
import { ref, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import {
  Upload,
  Download,
  LogIn,
  LogOut,
  UserRound,
  ChevronDown,
  History,
  Menu,
  X,
} from "lucide-vue-next";
import { useAuth } from "../composables/useAuth";
import logoImg from "../assets/images/logo.png";

const emit = defineEmits<{
  openLogin: [];
}>();

const router = useRouter();
const route = useRoute();
const { isLoggedIn, username, logout } = useAuth();
const mobileMenuOpen = ref(false);

// Close mobile menu on route change
watch(
  () => route.path,
  () => {
    mobileMenuOpen.value = false;
  }
);

function closeMobileMenu() {
  mobileMenuOpen.value = false;
}

function handleCommand(command: string) {
  if (command === "records") {
    router.push("/records");
  } else if (command === "logout") {
    logout();
    router.push("/");
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
