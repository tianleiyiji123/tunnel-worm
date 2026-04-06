# 隧隧虫 v2 迭代方案

> **状态：✅ 全部完成（2026-04-06）**
>
> 三个功能均已实现并通过测试：分享链接、二维码分享、端到端加密。

## 一、二维码分享

### 1.1 功能描述

发送成功后，在密码展示弹窗（CodeDisplay）中新增二维码，接收方扫码后直接跳转到提取页面并自动填入密码。

### 1.2 技术方案

**二维码生成**：前端使用 `qrcode` 库（轻量，~33KB gzip），纯浏览器端生成，不依赖后端。

**二维码内容**：`{当前域名}/retrieve?code=XXXX`

**安装依赖**：
```bash
cd client && npm install qrcode @types/qrcode
```

### 1.3 改动文件

| 文件 | 改动内容 |
|---|---|
| `client/package.json` | 新增 `qrcode` + `@types/qrcode` 依赖 |
| `client/src/components/CodeDisplay.vue` | 新增二维码展示区域（Canvas） |
| `client/src/views/RetrieveView.vue` | 路由读取 `?code=XXXX` 参数，自动填入密码 |

### 1.4 详细设计

#### CodeDisplay.vue 改动

在密码展示下方、复制按钮上方，新增二维码区域：

```
┌──────────────────────────────┐
│         资源已送达！          │
│   将以下密码发送给接收方即可提取  │
│                              │
│      ┌───┐ ┌───┐ ┌───┐ ┌───┐ │
│      │ A │ │ 3 │ │ K │ │ 7 │ │  ← 密码卡片（现有）
│      └───┘ └───┘ └───┘ └───┘ │
│                              │
│      ┌──────────────┐        │
│      │              │        │
│      │   [二维码]    │        │  ← 新增
│      │              │        │
│      └──────────────┘        │
│   扫码即可在另一台设备提取     │
│                              │
│     [ 📋 复制密码 ]           │  ← 现有
│   密码将在 XX 小时后过期       │
│        [ 完成 ]              │
└──────────────────────────────┘
```

核心代码逻辑：
```typescript
import QRCode from 'qrcode'

// 生成二维码
const qrCanvas = ref<HTMLCanvasElement | null>(null)
watch(() => props.visible, async (visible) => {
  if (visible && props.code) {
    const url = `${window.location.origin}/retrieve?code=${props.code}`
    await QRCode.toCanvas(qrCanvas.value, url, {
      width: 180,
      margin: 1,
      color: { dark: '#2D6A4F', light: '#ffffff' }
    })
  }
})
```

#### RetrieveView.vue 改动

路由初始化时检查 URL 参数：
```typescript
import { useRoute } from 'vue-router'
const route = useRoute()

onMounted(() => {
  const codeFromUrl = route.query.code as string
  if (codeFromUrl && codeFromUrl.length === 4) {
    code.value = codeFromUrl.toUpperCase()
    // 自动触发提取（可选，也可以等用户手动点击）
    // handleRetrieve()
  }
})
```

### 1.5 边界情况

| 场景 | 处理 |
|---|---|
| 二维码中的域名和实际访问域名不一致 | 始终使用 `window.location.origin`，确保链接有效 |
| 接收方在内网环境 | 二维码只含路径，不依赖外网，内网也能扫 |
| 密码已过期后扫码 | 正常跳转，由现有的过期检测逻辑处理 |

### 1.6 工作量

- 前端：约 1-2 小时
- 后端：无改动
- 测试：30 分钟

---

## 二、分享链接

### 2.1 功能描述

除了 4 位密码 + 二维码外，新增"复制分享链接"功能。接收方点击链接后直接打开提取页面，无需手动输入密码。

### 2.2 技术方案

分享链接格式：`{域名}/s/{code}`（短路径，便于分享）

这是一个**纯前端路由**，后端不需要新增 API。前端路由匹配 `/s/:code` 后，自动跳转到 `/retrieve?code=XXXX`，复用现有提取流程。

> 为什么用 `/s/{code}` 而不是直接 `/retrieve?code=XXXX`？
> - 更短、更适合复制分享
> - 链接不含 `?` 和 `=`，某些聊天工具（微信）不会对 URL 做额外处理
> - 未来可以在 `/s/{code}` 页面做专属的「分享落地页」设计

### 2.3 改动文件

| 文件 | 改动内容 |
|---|---|
| `client/src/router/index.ts` | 新增 `/s/:code` 路由 |
| `client/src/components/CodeDisplay.vue` | 新增"复制分享链接"按钮 |
| `client/src/views/RetrieveView.vue` | `onMounted` 读取 URL 参数（与二维码方案共用） |

### 2.4 详细设计

#### 路由新增

```typescript
// router/index.ts
{
  path: '/s/:code',
  name: 'share-link',
  redirect: (to) => `/retrieve?code=${to.params.code}`
}
```

#### CodeDisplay.vue 改动

在二维码区域下方，新增一个分享链接复制按钮：

```
│      ┌──────────────┐        │
│      │   [二维码]    │        │
│      └──────────────┘        │
│   扫码即可在另一台设备提取     │
│                              │
│  ───── 或复制分享链接 ─────   │  ← 新增分隔线
│                              │
│  https://xxx.com/s/A3K7      │  ← 新增链接展示
│      [ 📋 复制链接 ]         │  ← 新增按钮
│                              │
│     [ 📋 复制密码 ]           │  ← 现有
```

核心代码逻辑：
```typescript
const shareUrl = computed(() => {
  return `${window.location.origin}/s/${props.code}`
})

const linkCopied = ref(false)
async function copyShareLink() {
  await navigator.clipboard.writeText(shareUrl.value)
  linkCopied.value = true
  setTimeout(() => { linkCopied.value = false }, 2000)
}
```

### 2.5 边界情况

| 场景 | 处理 |
|---|---|
| 链接被人截获 | 与密码安全性一致（4 位密码，5 次锁定） |
| 微信内打开链接 | 路由 `/s/:code` 会被正常解析，无需额外处理 |
| 已过期的链接 | 跳转到提取页，由现有过期检测返回错误 |

### 2.6 工作量

- 前端：约 1 小时
- 后端：无改动
- 测试：30 分钟

---

## 三、端到端加密（E2EE）

### 3.1 功能描述

发送方在发送前可选择启用端到端加密。启用后，内容在**浏览器端加密**再上传，服务端只存储密文。接收方输入密码后，在**浏览器端解密**获取原始内容。服务端全程无法解密。

### 3.2 技术方案

#### 加密算法

| 步骤 | 算法 | 说明 |
|---|---|---|
| 密钥派生 | PBKDF2 | 密码 + 随机盐值 → 256 位 AES 密钥，迭代 10 万次 |
| 加密 | AES-256-GCM | 对称加密 + 认证标签（防篡改） |
| 盐值/IV | 随机生成 | 每条传输独立生成，16 字节盐 + 12 字节 IV |

#### 前端加密库

使用浏览器原生 **Web Crypto API**（`crypto.subtle`），零依赖，性能最佳。

#### 兼容性策略

- 加密为**可选功能**，默认关闭
- 开启加密的数据，`Transfer` 表新增 `encrypted = true` 标记
- 提取时根据 `encrypted` 字段决定是否触发前端解密
- 老数据（未加密）完全兼容，不受影响

### 3.3 改动文件

| 文件 | 改动内容 |
|---|---|
| **前端新增** | |
| `client/src/utils/crypto.ts` | 新增加密/解密工具函数（Web Crypto API 封装） |
| `client/src/views/HomeView.vue` | 新增加密开关；发送前加密文本/文件 |
| `client/src/views/RetrieveView.vue` | 提取成功后判断是否需要前端解密 |
| `client/src/components/ResourcePreview.vue` | 解密后展示明文内容 |
| **后端新增** | |
| `server/database.py` | Transfer 表新增 `encrypted`、`salt`、`iv` 字段 |
| `server/schemas.py` | TransferCreateRequest/Response 新增加密相关字段 |
| `server/routes/transfer.py` | 接收加密数据（salt/iv/密文），保存到数据库 |

### 3.4 详细设计

#### 数据库改动

```sql
ALTER TABLE transfer ADD COLUMN encrypted BOOLEAN DEFAULT FALSE;
ALTER TABLE transfer ADD COLUMN salt VARCHAR(32);      -- Base64 编码的 16 字节盐值
ALTER TABLE transfer ADD COLUMN iv VARCHAR(24);        -- Base64 编码的 12 字节 IV
```

对应 SQLAlchemy 模型：
```python
class Transfer(Base):
    # ... 现有字段 ...
    encrypted = Column(Boolean, default=False, server_default="0")
    salt = Column(String(32), nullable=True)    # Base64(16 bytes)
    iv = Column(String(24), nullable=True)       # Base64(12 bytes)
```

#### 前端加密工具 `client/src/utils/crypto.ts`

```typescript
const PBKDF2_ITERATIONS = 100000
const AES_KEY_LENGTH = 256
const IV_LENGTH = 12
const SALT_LENGTH = 16

/**
 * 从密码派生 AES 密钥
 */
export async function deriveKey(password: string, salt: Uint8Array): Promise<CryptoKey> {
  const encoder = new TextEncoder()
  const keyMaterial = await crypto.subtle.importKey(
    'raw', encoder.encode(password), 'PBKDF2', false, ['deriveKey']
  )
  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: PBKDF2_ITERATIONS, hash: 'SHA-256' },
    keyMaterial,
    { name: 'AES-GCM', length: AES_KEY_LENGTH },
    false,
    ['encrypt', 'decrypt']
  )
}

/**
 * 加密文本，返回 { ciphertext, salt, iv }（均为 Base64）
 */
export async function encryptText(plaintext: string, password: string) {
  const salt = crypto.getRandomValues(new Uint8Array(SALT_LENGTH))
  const iv = crypto.getRandomValues(new Uint8Array(IV_LENGTH))
  const key = await deriveKey(password, salt)
  const encoder = new TextEncoder()
  const ciphertext = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    key,
    encoder.encode(plaintext)
  )
  return {
    ciphertext: btoa(String.fromCharCode(...new Uint8Array(ciphertext))),
    salt: btoa(String.fromCharCode(...salt)),
    iv: btoa(String.fromCharCode(...iv)),
  }
}

/**
 * 解密文本
 */
export async function decryptText(ciphertext: string, password: string, salt: string, iv: string) {
  const key = await deriveKey(password, Uint8Array.from(atob(salt), c => c.charCodeAt(0)))
  const decrypted = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: Uint8Array.from(atob(iv), c => c.charCodeAt(0)) },
    key,
    Uint8Array.from(atob(ciphertext), c => c.charCodeAt(0))
  )
  return new TextDecoder().decode(decrypted)
}

/**
 * 加密文件（分块处理，避免大文件占满内存）
 * 返回 ArrayBuffer 密文
 */
export async function encryptFile(
  file: File, password: string, salt: Uint8Array, iv: Uint8Array,
  onProgress?: (percent: number) => void
): Promise<ArrayBuffer> {
  const key = await deriveKey(password, salt)
  const buffer = await file.arrayBuffer()
  const ciphertext = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    key,
    buffer
  )
  return ciphertext
}

/**
 * 解密文件
 */
export async function decryptFile(
  encryptedData: ArrayBuffer, password: string, salt: string, iv: string
): Promise<ArrayBuffer> {
  const key = await deriveKey(password, Uint8Array.from(atob(salt), c => c.charCodeAt(0)))
  return crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: Uint8Array.from(atob(iv), c => c.charCodeAt(0)) },
    key,
    encryptedData
  )
}
```

#### 发送流程改动（HomeView.vue）

```
用户点击「生成密码」
    │
    ├── 加密关闭（默认）
    │   └── 正常发送（现有流程）
    │
    └── 加密开启
        ├── 1. 生成随机 salt + iv
        ├── 2. 文本：encryptText(text, code) → 密文
        ├── 3. 文件：encryptFile(file, code, salt, iv) → 密文 Blob
        ├── 4. FormData 追加 encrypted=true, salt, iv, text_content=密文
        ├── 5. 文件用密文 Blob 替代原始文件上传
        └── 6. 后端正常存储（不关心是否加密）
```

> 注意：使用传输密码（code）作为加密密码，用户不需要额外输入。

#### 提取流程改动（RetrieveView.vue）

```
用户输入密码提取
    │
    ├── encrypted = false（老数据 / 未加密）
    │   └── 正常展示（现有流程）
    │
    └── encrypted = true
        ├── 文本：decryptText(ciphertext, code, salt, iv) → 明文
        ├── 文件：下载密文 → decryptFile(blob, code, salt, iv) → 明文 Blob → 触发下载
        └── 密码错误：AES-GCM 认证失败 → 提示"密码错误"
```

#### 后端改动（transfer.py）

```python
# create_transfer 接收新增字段
async def create_transfer(
    type: str = Form(...),
    text_content: Optional[str] = Form(None),
    files: List[UploadFile] = File(default=[]),
    encrypted: bool = Form(False),        # 新增
    salt: Optional[str] = Form(None),      # 新增
    iv: Optional[str] = Form(None),        # 新增
    # ...
):
    # ...
    transfer = Transfer(
        # ... 现有字段 ...
        encrypted=encrypted,
        salt=salt,
        iv=iv,
    )
```

后端只做存储，不参与加解密。密文对后端来说和普通文本/文件没有区别。

#### TransferResponse 新增字段

```python
class TransferResponse(BaseModel):
    # ... 现有字段 ...
    encrypted: bool = False
    salt: Optional[str] = None    # 提取时需要，传给前端解密
    iv: Optional[str] = None      # 提取时需要，传给前端解密
```

### 3.5 UI 设计

#### 发送页面（HomeView.vue）- 加密开关

在"生成密码"按钮上方，新增一个开关：

```
┌──────────────────────────────────┐
│  ☐ 启用端到端加密                 │
│  加密后服务端无法查看内容，         │
│  只有持有密码的人才能解密           │
│                                  │
│     [ 🐛 生成密码 ]               │
└──────────────────────────────────┘
```

使用 Element Plus 的 `el-switch` 组件，带说明文字。

#### 提取页面 - 解密中状态

如果检测到 `encrypted = true`，在提取成功后显示解密状态：

```
┌──────────────────────────────────┐
│  ✓ 资源提取成功                    │
│  🔒 内容已加密，正在解密...         │  ← loading 状态
│                                  │
│  （解密完成后正常展示内容）          │
└──────────────────────────────────┘
```

#### 解密失败

```
┌──────────────────────────────────┐
│  ⚠ 解密失败                       │
│  内容已启用端到端加密，请确认密码     │
│  是否正确后重试                    │
│                                  │
│     [ 重新输入密码 ]               │
└──────────────────────────────────┘
```

### 3.6 边界情况

| 场景 | 处理 |
|---|---|
| 用户忘了密码 | 与现有行为一致：无法找回，24 小时后自动过期删除 |
| 加密的大文件（>100MB） | Web Crypto API 的 `encrypt` 一次性处理，100MB 约需 2-3 秒，可接受。未来可优化为分块加密 |
| 浏览器不支持 Web Crypto | 现代浏览器（Chrome 37+、Firefox 34+、Safari 7+）均支持，覆盖 99%+ 用户 |
| 部分内容加密、部分不加密 | 每条传输整体加密（要么全加密要么不加密），不存在混合情况 |
| 管理后台查看加密内容 | 管理后台只能看到密文，无法解密（这是设计目标） |
| 下载密文文件 | 文件下载 API 返回的是密文，前端需要先下载到内存再解密。大文件场景需注意内存占用 |

### 3.7 工作量

- 前端：约 4-6 小时（crypto 工具 + 发送端加密 + 提取端解密 + UI 状态）
- 后端：约 1-2 小时（数据库迁移 + 接口字段 + schema）
- 测试：约 1-2 小时（加密/解密正确性 + 大文件 + 边界情况）

---

## 实施顺序建议

| 顺序 | 功能 | 工作量 | 依赖 | 状态 |
|---|---|---|---|---|
| 1️⃣ | 分享链接 | ~1.5h | 无 | ✅ 已完成 |
| 2️⃣ | 二维码 | ~2h | 无（与分享链接共用 RetrieveView URL 参数） | ✅ 已完成 |
| 3️⃣ | 端到端加密 | ~8h | 建议 1、2 完成后做 | ✅ 已完成（含 salt/iv bug 修复） |

### 实际改动文件

| 文件 | 改动 |
|---|---|
| `client/package.json` | 新增 qrcode 依赖 |
| `client/src/router/index.ts` | 新增 `/s/:code` 路由 |
| `client/src/utils/crypto.ts` | **新增** - E2EE 加解密工具 (Web Crypto API) |
| `client/src/api/index.ts` | 新增 `reserveCode()` API |
| `client/src/components/CodeDisplay.vue` | 二维码 + 分享链接 + 复制按钮 |
| `client/src/components/ResourcePreview.vue` | 加密文件解密下载 |
| `client/src/views/HomeView.vue` | E2EE 开关 + reserve→encrypt→upload 流程 |
| `client/src/views/RetrieveView.vue` | URL 参数自动提交 + E2EE 解密 |
| `server/database.py` | Transfer 表新增 encrypted, salt, iv 字段 |
| `server/schemas.py` | TransferResponse 新增加密字段 |
| `server/routes/transfer.py` | reserve-code 接口 + 加密参数 + reserved_code |
| `server/services/transfer_service.py` | reserve_code() + create_transfer 支持预留密码 |
