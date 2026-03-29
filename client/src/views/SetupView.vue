<template>
  <div class="max-w-2xl mx-auto px-4 sm:px-6 py-12 sm:py-20">
    <!-- Header -->
    <div class="text-center mb-8 animate-tunnel-emerge">
      <div class="w-20 h-20 mx-auto mb-5 bg-gradient-to-br from-[#52B788]/20 to-[#2D6A4F]/20 rounded-3xl flex items-center justify-center animate-worm-wiggle">
        <svg width="44" height="44" viewBox="0 0 24 24" fill="none">
          <path d="M12 4C9 4 6 6 6 10c0 3 2 5 4 7 1-1 2-1 2-1s1 0 2 1c2-2 4-4 4-7 0-4-3-6-6-6z" fill="#2D6A4F" opacity="0.3"/>
          <path d="M12 2c-2 0-4 1-5 3l-1 2c-1 2-1 4 0 6l3 5c1 2 3 3 5 3s4-1 5-3l3-5c1-2 1-4 0-6l-1-2c-1-2-3-3-5-3h-4z" stroke="#2D6A4F" stroke-width="1.5" stroke-linecap="round" fill="none"/>
          <circle cx="10" cy="9" r="1.2" fill="#2D6A4F"/>
          <circle cx="14" cy="9" r="1.2" fill="#2D6A4F"/>
          <path d="M10 12c0 0 1 1.5 2 1.5s2-1.5 2-1.5" stroke="#2D6A4F" stroke-width="1.2" stroke-linecap="round" fill="none"/>
        </svg>
      </div>
      <h1 class="text-3xl sm:text-4xl font-bold text-[#1B1B1B] mb-2">欢迎使用隧隧虫</h1>
      <p class="text-[#6B705C] text-base sm:text-lg">首次使用，请完成以下配置</p>
    </div>

    <!-- Steps Indicator -->
    <div class="brand-card p-6 sm:p-8 mb-6 animate-tunnel-emerge" style="animation-delay: 0.1s">
      <el-steps :active="currentStep" align-center finish-status="success">
        <el-step title="数据库配置" description="选择存储数据的数据库" />
        <el-step title="存储配置" description="选择文件存储方式" />
      </el-steps>
    </div>

    <!-- Step 1: Database -->
    <div v-show="currentStep === 0" class="brand-card p-6 sm:p-8 animate-tunnel-emerge" style="animation-delay: 0.2s">
      <h2 class="text-lg font-semibold text-[#1B1B1B] mb-6 flex items-center gap-2">
        <Database :size="20" class="text-[#2D6A4F]" />
        数据库配置
      </h2>

      <el-radio-group v-model="dbType" class="w-full mb-6" @change="onDbTypeChange">
        <div class="space-y-3 w-full">
          <div
            class="p-4 rounded-xl border-2 cursor-pointer transition-all duration-200"
            :class="dbType === 'sqlite'
              ? 'border-[#2D6A4F] bg-[#2D6A4F]/5'
              : 'border-[#2D6A4F]/15 hover:border-[#2D6A4F]/30'"
          >
            <el-radio value="sqlite" size="large">
              <span class="font-medium">SQLite（推荐）</span>
              <span class="text-[#6B705C] text-sm ml-2">零配置，数据存储在容器内部</span>
            </el-radio>
          </div>

          <div
            class="p-4 rounded-xl border-2 cursor-pointer transition-all duration-200"
            :class="dbType === 'mysql'
              ? 'border-[#2D6A4F] bg-[#2D6A4F]/5'
              : 'border-[#2D6A4F]/15 hover:border-[#2D6A4F]/30'"
          >
            <el-radio value="mysql" size="large">
              <span class="font-medium">MySQL</span>
              <span class="text-[#6B705C] text-sm ml-2">需要已有的 MySQL 服务</span>
            </el-radio>
          </div>
        </div>
      </el-radio-group>

      <!-- MySQL config form -->
      <div v-if="dbType === 'mysql'" class="space-y-4 ml-1">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">主机</label>
            <input v-model="mysqlForm.db_host" class="brand-input" placeholder="localhost" />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">端口</label>
            <input v-model.number="mysqlForm.db_port" class="brand-input" placeholder="3306" type="number" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">用户名</label>
            <input v-model="mysqlForm.db_user" class="brand-input" placeholder="root" />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">密码</label>
            <input v-model="mysqlForm.db_password" class="brand-input" type="password" placeholder="••••••" />
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-[#6B705C] mb-1.5">数据库名</label>
          <input v-model="mysqlForm.db_name" class="brand-input" placeholder="suisuichong" />
        </div>
      </div>

      <!-- Action -->
      <div class="flex items-center justify-between mt-8">
        <button
          v-if="dbType === 'mysql'"
          @click="handleTestDb"
          :disabled="testing"
          class="px-5 py-2.5 text-sm font-medium text-[#2D6A4F] bg-[#2D6A4F]/10 rounded-xl
                 cursor-pointer transition-all duration-200
                 hover:bg-[#2D6A4F]/20 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="testing" class="flex items-center gap-1.5">
            <div class="w-4 h-4 border-2 border-[#2D6A4F]/30 border-t-[#2D6A4F] rounded-full animate-spin"></div>
            测试中...
          </span>
          <span v-else class="flex items-center gap-1.5">
            <Wifi :size="16" />
            测试连接
          </span>
        </button>
        <div v-else></div>

        <button @click="nextStep" class="brand-btn-primary flex items-center gap-2">
          下一步
          <ChevronRight :size="18" />
        </button>
      </div>
    </div>

    <!-- Step 2: Storage -->
    <div v-show="currentStep === 1" class="brand-card p-6 sm:p-8 animate-tunnel-emerge" style="animation-delay: 0.2s">
      <h2 class="text-lg font-semibold text-[#1B1B1B] mb-6 flex items-center gap-2">
        <HardDrive :size="20" class="text-[#2D6A4F]" />
        存储配置
      </h2>

      <el-radio-group v-model="storageType" class="w-full mb-6" @change="onStorageTypeChange">
        <div class="space-y-3 w-full">
          <div
            v-for="opt in storageOptions"
            :key="opt.value"
            class="p-4 rounded-xl border-2 cursor-pointer transition-all duration-200"
            :class="storageType === opt.value
              ? 'border-[#2D6A4F] bg-[#2D6A4F]/5'
              : 'border-[#2D6A4F]/15 hover:border-[#2D6A4F]/30'"
          >
            <el-radio :value="opt.value" size="large">
              <span class="font-medium">{{ opt.label }}</span>
              <span class="text-[#6B705C] text-sm ml-2">{{ opt.desc }}</span>
            </el-radio>
          </div>
        </div>
      </el-radio-group>

      <!-- MinIO form -->
      <div v-if="storageType === 'minio'" class="space-y-4 ml-1">
        <div>
          <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Endpoint</label>
          <input v-model="storageForm.minio_endpoint" class="brand-input" placeholder="http://minio:9000" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Access Key</label>
            <input v-model="storageForm.minio_access_key" class="brand-input" placeholder="minioadmin" />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Secret Key</label>
            <input v-model="storageForm.minio_secret_key" class="brand-input" type="password" placeholder="••••••" />
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Bucket 名称</label>
          <input v-model="storageForm.minio_bucket" class="brand-input" placeholder="suisuichong" />
        </div>
      </div>

      <!-- Aliyun OSS form -->
      <div v-if="storageType === 'alioss'" class="space-y-4 ml-1">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Access Key ID</label>
            <input v-model="storageForm.alioss_access_key_id" class="brand-input" placeholder="LTAI..." />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Access Key Secret</label>
            <input v-model="storageForm.alioss_access_key_secret" class="brand-input" type="password" placeholder="••••••" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Endpoint</label>
            <input v-model="storageForm.alioss_endpoint" class="brand-input" placeholder="oss-cn-hangzhou.aliyuncs.com" />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Bucket 名称</label>
            <input v-model="storageForm.alioss_bucket" class="brand-input" placeholder="suisuichong" />
          </div>
        </div>
      </div>

      <!-- Tencent COS form -->
      <div v-if="storageType === 'tencentcos'" class="space-y-4 ml-1">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Secret ID</label>
            <input v-model="storageForm.tencentcos_secret_id" class="brand-input" placeholder="AKID..." />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Secret Key</label>
            <input v-model="storageForm.tencentcos_secret_key" class="brand-input" type="password" placeholder="••••••" />
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Region</label>
            <input v-model="storageForm.tencentcos_region" class="brand-input" placeholder="ap-guangzhou" />
          </div>
          <div>
            <label class="block text-sm font-medium text-[#6B705C] mb-1.5">Bucket 名称</label>
            <input v-model="storageForm.tencentcos_bucket" class="brand-input" placeholder="suisuichong-1234567890" />
          </div>
        </div>
      </div>

      <!-- Action -->
      <div class="flex items-center justify-between mt-8">
        <div class="flex items-center gap-3">
          <button @click="prevStep" class="px-5 py-2.5 text-sm font-medium text-[#6B705C] bg-[#F5F0E8] rounded-xl cursor-pointer transition-all duration-200 hover:bg-[#F5F0E8]/80 flex items-center gap-1.5">
            <ChevronLeft :size="16" />
            上一步
          </button>
          <button
            v-if="storageType !== 'local'"
            @click="handleTestStorage"
            :disabled="testing"
            class="px-5 py-2.5 text-sm font-medium text-[#2D6A4F] bg-[#2D6A4F]/10 rounded-xl
                   cursor-pointer transition-all duration-200
                   hover:bg-[#2D6A4F]/20 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="testing" class="flex items-center gap-1.5">
              <div class="w-4 h-4 border-2 border-[#2D6A4F]/30 border-t-[#2D6A4F] rounded-full animate-spin"></div>
              测试中...
            </span>
            <span v-else class="flex items-center gap-1.5">
              <Wifi :size="16" />
              测试连接
            </span>
          </button>
        </div>

        <button
          @click="handleFinish"
          :disabled="finishing"
          class="brand-btn-primary flex items-center gap-2"
        >
          <span v-if="finishing" class="flex items-center gap-2">
            <div class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            正在初始化...
          </span>
          <span v-else class="flex items-center gap-2">
            <Check :size="18" />
            完成安装
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Database, HardDrive, Wifi, ChevronLeft, ChevronRight, Check } from 'lucide-vue-next'
import { testDbConnection, testStorageConnection, finishSetup } from '../api'

const router = useRouter()

const currentStep = ref(0)
const testing = ref(false)
const finishing = ref(false)

// Database
const dbType = ref('sqlite')
const mysqlForm = reactive({
  db_host: 'localhost',
  db_port: 3306,
  db_user: 'root',
  db_password: '',
  db_name: 'suisuichong',
})

// Storage
const storageType = ref('local')
const storageOptions = [
  { value: 'local', label: '容器内部存储', desc: '推荐 · 文件存储在容器内部' },
  { value: 'minio', label: 'MinIO', desc: '需要已有的 MinIO 服务' },
  { value: 'alioss', label: '阿里云 OSS', desc: '使用阿里云对象存储' },
  { value: 'tencentcos', label: '腾讯云 COS', desc: '使用腾讯云对象存储' },
]
const storageForm = reactive({
  minio_endpoint: '',
  minio_access_key: '',
  minio_secret_key: '',
  minio_bucket: '',
  alioss_access_key_id: '',
  alioss_access_key_secret: '',
  alioss_bucket: '',
  alioss_endpoint: '',
  tencentcos_secret_id: '',
  tencentcos_secret_key: '',
  tencentcos_bucket: '',
  tencentcos_region: '',
})

function onDbTypeChange() {
  // reset test status
}

function onStorageTypeChange() {
  // reset test status
}

function nextStep() {
  if (dbType.value === 'mysql') {
    if (!mysqlForm.db_host || !mysqlForm.db_user || !mysqlForm.db_password || !mysqlForm.db_name) {
      ElMessage.warning('请填写完整的 MySQL 连接信息')
      return
    }
  }
  currentStep.value = 1
}

function prevStep() {
  currentStep.value = 0
}

async function handleTestDb() {
  if (dbType.value !== 'mysql') return
  testing.value = true
  try {
    const result = await testDbConnection({
      db_type: 'mysql',
      ...mysqlForm,
    })
    if (result.success) {
      ElMessage.success(result.message)
    } else {
      ElMessage.error(result.message)
    }
  } finally {
    testing.value = false
  }
}

async function handleTestStorage() {
  testing.value = true
  try {
    const payload: Record<string, string> = { storage_type: storageType.value }
    if (storageType.value === 'minio') {
      payload.minio_endpoint = storageForm.minio_endpoint
      payload.minio_access_key = storageForm.minio_access_key
      payload.minio_secret_key = storageForm.minio_secret_key
      payload.minio_bucket = storageForm.minio_bucket
    } else if (storageType.value === 'alioss') {
      payload.alioss_access_key_id = storageForm.alioss_access_key_id
      payload.alioss_access_key_secret = storageForm.alioss_access_key_secret
      payload.alioss_bucket = storageForm.alioss_bucket
      payload.alioss_endpoint = storageForm.alioss_endpoint
    } else if (storageType.value === 'tencentcos') {
      payload.tencentcos_secret_id = storageForm.tencentcos_secret_id
      payload.tencentcos_secret_key = storageForm.tencentcos_secret_key
      payload.tencentcos_bucket = storageForm.tencentcos_bucket
      payload.tencentcos_region = storageForm.tencentcos_region
    }
    const result = await testStorageConnection(payload)
    if (result.success) {
      ElMessage.success(result.message)
    } else {
      ElMessage.error(result.message)
    }
  } finally {
    testing.value = false
  }
}

async function handleFinish() {
  finishing.value = true
  try {
    const payload: Record<string, unknown> = {
      db_type: dbType.value,
      storage_type: storageType.value,
    }

    if (dbType.value === 'mysql') {
      Object.assign(payload, mysqlForm)
    }

    if (storageType.value === 'minio') {
      Object.assign(payload, {
        minio_endpoint: storageForm.minio_endpoint,
        minio_access_key: storageForm.minio_access_key,
        minio_secret_key: storageForm.minio_secret_key,
        minio_bucket: storageForm.minio_bucket,
      })
    } else if (storageType.value === 'alioss') {
      Object.assign(payload, {
        alioss_access_key_id: storageForm.alioss_access_key_id,
        alioss_access_key_secret: storageForm.alioss_access_key_secret,
        alioss_bucket: storageForm.alioss_bucket,
        alioss_endpoint: storageForm.alioss_endpoint,
      })
    } else if (storageType.value === 'tencentcos') {
      Object.assign(payload, {
        tencentcos_secret_id: storageForm.tencentcos_secret_id,
        tencentcos_secret_key: storageForm.tencentcos_secret_key,
        tencentcos_bucket: storageForm.tencentcos_bucket,
        tencentcos_region: storageForm.tencentcos_region,
      })
    }

    const result = await finishSetup(payload)
    if (result.success) {
      ElMessage.success('初始化完成！即将跳转...')
      setTimeout(() => {
        router.push('/')
      }, 2000)
    } else {
      ElMessage.error(result.message)
    }
  } finally {
    finishing.value = false
  }
}
</script>
