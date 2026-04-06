<template>
  <teleport to="body">
    <transition name="modal">
      <div
        v-if="visible"
        class="fixed inset-0 z-[100] flex items-center justify-center p-4"
      >
        <!-- Backdrop -->
        <div
          class="absolute inset-0 bg-black/40 backdrop-blur-sm"
          @click="$emit('close')"
        ></div>

        <!-- Modal -->
        <div
          class="relative brand-card p-8 max-w-md w-full text-center animate-tunnel-emerge"
        >
          <!-- Worm icon -->
          <div
            class="w-16 h-16 mx-auto mb-4 bg-[#fefefe] rounded-2xl flex items-center justify-center animate-worm-wiggle shadow-md border border-black/5 overflow-hidden"
          >
            <img
              src="../assets/images/logo.png"
              alt="隧隧虫"
              class="w-full h-full object-contain"
            />
          </div>

          <h3 class="text-lg font-bold text-[#2D6A4F] mb-1">资源已送达！</h3>
          <p class="text-sm text-[#6B705C] mb-6">
            将以下密码发送给接收方即可提取
          </p>

          <!-- Code display -->
          <div class="relative mb-6">
            <div
              class="flex items-center justify-center gap-2 sm:gap-3 bg-gradient-to-br from-[#FEFAE0] to-[#F5F0E8] border-2 border-[#DDA15E]/30 rounded-2xl py-4 sm:py-5 px-4 sm:px-6"
            >
              <span
                v-for="(char, i) in displayCode"
                :key="i"
                class="text-4xl sm:text-5xl font-bold text-[#2D6A4F] w-12 h-13 sm:w-14 sm:h-14 flex items-center justify-center bg-white/80 rounded-xl shadow-sm border border-[#2D6A4F]/10 animate-tunnel-emerge"
                :style="{ animationDelay: `${i * 0.1}s` }"
                >{{ char }}</span
              >
            </div>
          </div>

          <!-- QR Code -->
          <div class="mb-5">
            <div
              class="inline-flex flex-col items-center p-4 bg-white rounded-2xl border border-[#2D6A4F]/10"
            >
              <canvas
                ref="qrCanvas"
                class="w-[160px] h-[160px] sm:w-[180px] sm:h-[180px]"
              ></canvas>
              <p class="text-xs text-[#6B705C]/60 mt-2">扫码即可在另一台设备提取</p>
            </div>
          </div>

          <!-- Share link -->
          <div class="mb-5">
            <div
              class="flex items-center gap-3 p-3 bg-[#FEFAE0]/40 rounded-xl border border-[#DDA15E]/15"
            >
              <div class="flex-1 min-w-0 text-left">
                <p class="text-xs text-[#6B705C]/50 mb-0.5">分享链接</p>
                <p
                  class="text-sm text-[#2D6A4F] font-medium truncate"
                >
                  {{ shareUrl }}
                </p>
              </div>
              <button
                @click="copyShareLink"
                class="flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-white bg-[#2D6A4F] rounded-lg hover:bg-[#40916C] transition-colors cursor-pointer shrink-0"
              >
                <Check v-if="linkCopied" size="14" />
                <Link v-else size="14" />
                {{ linkCopied ? "已复制" : "复制" }}
              </button>
            </div>
          </div>

          <!-- Copy code button -->
          <button
            @click="copyCode"
            class="brand-btn-primary w-full flex items-center justify-center gap-2 mb-4"
          >
            <Check v-if="copied" size="18" />
            <Copy v-else size="18" />
            {{ copied ? "已复制到剪贴板" : "复制密码" }}
          </button>

          <!-- Expiry notice -->
          <p class="text-xs text-[#6B705C]/60 mb-4">
            密码将在
            <span class="font-medium text-[#E76F51]">{{ expireText }}</span>
            后过期
          </p>

          <!-- Done button -->
          <button
            @click="$emit('close')"
            class="text-sm text-[#6B705C] hover:text-[#2D6A4F] transition-colors cursor-pointer"
          >
            完成
          </button>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from "vue";
import { Copy, Check, Link } from "lucide-vue-next";
import { ElMessage } from "element-plus";
import QRCode from "qrcode";

const props = defineProps<{
  visible: boolean;
  code: string;
  expiresAt: string;
}>();

defineEmits(["close"]);

const copied = ref(false);
const linkCopied = ref(false);
const qrCanvas = ref<HTMLCanvasElement | null>(null);
const displayCode = computed(() => props.code.split(""));
const shareUrl = computed(() => {
  return `${window.location.origin}/s/${props.code}`;
});
const expireText = computed(() => {
  const expiry = new Date(props.expiresAt);
  const now = new Date();
  const diff = expiry.getTime() - now.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  if (hours >= 1) return `${hours} 小时`;
  const minutes = Math.floor(diff / (1000 * 60));
  return `${minutes} 分钟`;
});

// Generate QR code when modal opens
watch(
  () => props.visible,
  async (visible) => {
    if (visible && props.code) {
      await nextTick();
      if (qrCanvas.value) {
        try {
          await QRCode.toCanvas(qrCanvas.value, shareUrl.value, {
            width: 180,
            margin: 1,
            color: { dark: "#2D6A4F", light: "#ffffff" },
          });
        } catch {
          // QR generation failed silently
        }
      }
    }
  },
  { immediate: true }
);

async function copyCode() {
  try {
    await navigator.clipboard.writeText(props.code);
    copied.value = true;
    ElMessage.success("密码已复制");
    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } catch {
    // Fallback
    const ta = document.createElement("textarea");
    ta.value = props.code;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    copied.value = true;
    ElMessage.success("密码已复制");
    setTimeout(() => {
      copied.value = false;
    }, 2000);
  }
}

async function copyShareLink() {
  try {
    await navigator.clipboard.writeText(shareUrl.value);
    linkCopied.value = true;
    ElMessage.success("链接已复制");
    setTimeout(() => {
      linkCopied.value = false;
    }, 2000);
  } catch {
    const ta = document.createElement("textarea");
    ta.value = shareUrl.value;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    linkCopied.value = true;
    ElMessage.success("链接已复制");
    setTimeout(() => {
      linkCopied.value = false;
    }, 2000);
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
