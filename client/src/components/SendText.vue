<template>
  <div class="space-y-3">
    <label class="block text-sm font-medium text-[#6B705C]">文本内容</label>
    <textarea
      v-model="textContent"
      class="brand-textarea"
      placeholder="在这里粘贴或输入要传输的文本内容..."
      @input="$emit('update:modelValue', textContent)"
    ></textarea>
    <div class="flex justify-between items-center text-xs text-[#6B705C]/60">
      <span>支持任意文本内容，接收方可以直接复制</span>
      <span>{{ textContent.length }} 字</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const textContent = ref('')
defineEmits(['update:modelValue'])

function getText(): string {
  return textContent.value.trim()
}

function clear() {
  textContent.value = ''
}

defineExpose({ getText, clear })
</script>
