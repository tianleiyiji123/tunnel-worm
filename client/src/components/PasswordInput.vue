<template>
  <div class="space-y-3">
    <label class="block text-sm font-medium text-[#6B705C]">提取密码</label>
    <div class="flex items-center justify-center gap-2 sm:gap-3">
      <div class="flex items-center gap-2">
        <input
          v-for="i in 4"
          :key="i"
          :ref="el => { if (el) inputRefs[i-1] = el as HTMLInputElement }"
          type="text"
          maxlength="1"
          autocomplete="off"
          class="w-14 h-14 sm:w-16 sm:h-16 text-center text-2xl sm:text-3xl font-bold text-[#2D6A4F] bg-white/80 border-2 border-[#2D6A4F]/20 rounded-xl focus:outline-none focus:border-[#2D6A4F] focus:ring-4 focus:ring-[#2D6A4F]/10 transition-all duration-200 uppercase"
          :value="digits[i-1]"
          @input="onInput(i-1, $event)"
          @keydown.backspace="onBackspace(i-1, $event)"
          @paste="onPaste"
          @focus="($event.target as HTMLInputElement).select()"
        />
      </div>
    </div>
    <p class="text-xs text-[#6B705C]/50 text-center">输入发送方提供的 4 位密码</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['update:modelValue'])

const digits = ref<string[]>(['', '', '', ''])
const inputRefs = ref<HTMLInputElement[]>([])

// Allow uppercase letters and digits only
const allowedChars = /^[A-Z0-9]$/

function onInput(index: number, event: Event) {
  const input = event.target as HTMLInputElement
  const value = input.value.toUpperCase().replace(/[^A-Z0-9]/g, '')
  digits.value[index] = value.slice(-1)
  emit('update:modelValue', digits.value.join(''))

  if (value && index < 3) {
    inputRefs.value[index + 1]?.focus()
  }
}

function onBackspace(index: number, event: KeyboardEvent) {
  if (!digits.value[index] && index > 0) {
    digits.value[index - 1] = ''
    inputRefs.value[index - 1]?.focus()
    emit('update:modelValue', digits.value.join(''))
  }
}

function onPaste(event: ClipboardEvent) {
  event.preventDefault()
  const paste = (event.clipboardData?.getData('text') || '').toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 4)
  for (let i = 0; i < paste.length; i++) {
    digits.value[i] = paste[i]
  }
  emit('update:modelValue', digits.value.join(''))
  const nextEmpty = digits.value.findIndex(d => !d)
  if (nextEmpty >= 0) {
    inputRefs.value[nextEmpty]?.focus()
  }
}

// Expose method to clear
function clear() {
  digits.value = ['', '', '', '']
  inputRefs.value[0]?.focus()
}

defineExpose({ clear })
</script>
