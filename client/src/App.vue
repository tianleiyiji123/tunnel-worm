<template>
  <div class="relative z-10 min-h-screen flex flex-col">
    <AppHeader @open-login="showLoginDialog = true" />
    <main class="flex-1 pt-16">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Login Dialog (global, not inside fixed header) -->
    <LoginDialog
      v-model:visible="showLoginDialog"
      @success="showLoginDialog = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, provide } from 'vue'
import AppHeader from './components/AppHeader.vue'
import LoginDialog from './components/LoginDialog.vue'

const showLoginDialog = ref(false)
provide('showLoginDialog', showLoginDialog)
</script>

<style>
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
</style>
