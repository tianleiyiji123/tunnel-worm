<template>
  <div class="space-y-3">
    <label class="block text-sm font-medium text-[#6B705C]">上传文件</label>
    <el-upload
      ref="uploadRef"
      v-model:file-list="fileList"
      action=""
      :auto-upload="false"
      :multiple="true"
      :limit="10"
      :on-exceed="handleExceed"
      :on-change="handleChange"
      :on-remove="handleChange"
      drag
    >
      <div class="flex flex-col items-center py-4">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#52B788]/20 to-[#2D6A4F]/20 flex items-center justify-center mb-3">
          <UploadCloud :size="28" class="text-[#2D6A4F]" />
        </div>
        <p class="text-sm font-medium text-[#1B1B1B]">将文件拖拽到此处，或点击选择</p>
        <p class="text-xs text-[#6B705C]/60 mt-1.5">单文件不超过 50MB，最多 10 个文件</p>
      </div>
    </el-upload>

    <!-- File list -->
    <div v-if="fileList.length > 0" class="space-y-2">
      <div
        v-for="(file, index) in fileList"
        :key="file.uid"
        class="flex items-center gap-3 p-3 bg-[#FEFAE0]/50 rounded-xl border border-[#DDA15E]/20"
      >
        <div class="w-10 h-10 rounded-lg bg-[#2D6A4F]/10 flex items-center justify-center flex-shrink-0">
          <FileText :size="20" class="text-[#2D6A4F]" />
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-[#1B1B1B] truncate">{{ file.name }}</p>
          <p class="text-xs text-[#6B705C]/60">{{ formatSize(file.size || 0) }}</p>
        </div>
        <button
          @click="removeFile(index)"
          class="p-1.5 rounded-lg hover:bg-[#E76F51]/10 text-[#6B705C] hover:text-[#E76F51] transition-colors cursor-pointer"
        >
          <X :size="16" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { UploadCloud, FileText, X } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'
import type { UploadInstance, UploadUserFile } from 'element-plus'

const uploadRef = ref<UploadInstance>()
const fileList = ref<UploadUserFile[]>([])

const emit = defineEmits<{
  'update:modelValue': [files: File[]]
}>()

function formatSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

function handleExceed() {
  ElMessage.warning('最多上传 10 个文件')
}

function handleChange() {
  const rawFiles: File[] = []
  fileList.value.forEach(f => {
    if (f.raw) rawFiles.push(f.raw as File)
  })
  emit('update:modelValue', rawFiles)
}

function removeFile(index: number) {
  fileList.value.splice(index, 1)
  handleChange()
}

function getRawFiles(): File[] {
  const rawFiles: File[] = []
  fileList.value.forEach(f => {
    if (f.raw) rawFiles.push(f.raw as File)
  })
  return rawFiles
}

defineExpose({ getRawFiles })
</script>
