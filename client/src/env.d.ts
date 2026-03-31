/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Ignore lucide-vue-next type strict issues
declare module 'lucide-vue-next' {
  import { DefineComponent } from 'vue'
  type LucideIcon = DefineComponent<{ size?: number | string; class?: string; strokeWidth?: number | string }>
  export const Upload: LucideIcon
  export const Download: LucideIcon
  export const Copy: LucideIcon
  export const Check: LucideIcon
  export const CheckCircle: LucideIcon
  export const X: LucideIcon
  export const FileText: LucideIcon
  export const UploadCloud: LucideIcon
  export const AlertCircle: LucideIcon
  export const Unlock: LucideIcon
  export const Type: LucideIcon
  export const FileUp: LucideIcon
  export const Layers: LucideIcon
}
