<div align="center">

# 🐛 隧隧虫 (Tunnel Worm)

**跨设备，传什么都可以。**

一条隧道连接你的设备 —— 文本、文件，生成密码，另一台设备输入即可提取。

无需注册 · 无需安装客户端 · 数据不经过第三方

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![Vue](https://img.shields.io/badge/Vue-3.x-4FC08D.svg)](https://vuejs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)](https://docker.com)

</div>

---

## ✨ 特性

- **📱 跨设备传输** — 发送文本或文件，生成 4 位字母数字密码，任何设备均可提取
- **🔗 分享链接** — 一键生成短链接 `/s/{code}`，接收方点击即可提取，无需手动输入密码
- **📷 二维码分享** — 发送成功后展示二维码，接收方扫码直达提取页
- **🔐 端到端加密** — 可选开启，浏览器端 AES-256-GCM 加密，服务端只存密文，无法解密
- **🔐 密码保护** — 大写字母+数字混合密码（排除易混淆字符），5 次错误后锁定 1 分钟
- **⏰ 自动过期** — 资源 24 小时后自动删除，登录用户文本永久保存
- **👤 可选登录** — 不登录也能用；登录后可查看操作记录，文本永久保存
- **💾 多存储后端** — 本地存储 / MinIO / 阿里云 OSS / 腾讯云 COS
- **🐳 一键部署** — Docker 单镜像，pull 即用，内置 Web 安装向导
- **📱 响应式设计** — 适配桌面端和移动端，随时随刻传输

## 📸 界面预览

| 首页                           | 提取资源                      | 二维码 & 分享链接              |
| ------------------------------ | ----------------------------- | ------------------------------ |
| ![首页](/images/send-text.png) | ![提取](/images/retrieve.png) | ![首页](/images/home.png) |

---

## 🚀 快速开始

### 方法 1：Docker Hub 拉取（推荐）

```bash
docker run -d \
  --name tunnel-worm \
  -p 7895:7895 \
  -v tunnel-worm_data:/app/data \
  tianleiyiji123/tunnel-worm:latest
```

### 方法 2：Docker Compose

克隆仓库并启动：

```bash
git clone https://github.com/tianleiyiji123/tunnel-worm.git
cd tunnel-worm
docker compose up -d
```

### 方法 3：Docker 自定义构建

```bash
git clone https://github.com/tianleiyiji123/tunnel-worm.git
cd tunnel-worm
docker compose build --no-cache && docker compose up -d
```

启动后打开浏览器访问 **http://localhost:7895**，进入安装向导。

---

## 🛠️ 安装向导

首次启动时，应用会自动进入 **Web 安装向导**，通过浏览器完成所有配置，无需编辑任何配置文件。

安装向导分两步：

### 第一步：数据库配置

| 选项               | 说明                                       | 适用场景                    |
| ------------------ | ------------------------------------------ | --------------------------- |
| **SQLite（推荐）** | 零配置，数据文件存储在数据卷中             | 个人使用、轻量部署          |
| **MySQL**          | 需要填写主机、端口、用户名、密码、数据库名 | 已有 MySQL 服务、高并发场景 |

选择 MySQL 时，向导页面会展开表单，填写连接信息后点击「测试连接」验证是否可用。

> 💡 Docker 默认镜像不包含 MySQL 驱动，如需使用 MySQL 请自行安装 `pymysql`。

### 第二步：存储配置

| 选项                     | 说明                       | 需要填写的凭证                                     |
| ------------------------ | -------------------------- | -------------------------------------------------- |
| **本地存储（推荐）**     | 零配置，文件存储在数据卷中 | 无                                                 |
| **MinIO**                | 兼容 S3 的自建对象存储     | Endpoint、Access Key、Secret Key、Bucket           |
| **阿里云 OSS**           | 阿里云对象存储             | Access Key ID、Access Key Secret、Endpoint、Bucket |
| **腾讯云 COS**           | 腾讯云对象存储             | Secret ID、Secret Key、Region、Bucket              |

选择对象存储后，同样可以点击「测试连接」验证凭证是否正确。

> 💡 Docker 默认镜像不包含云存储 SDK。如需使用对象存储，需要在容器内手动安装对应 SDK，或自行构建包含 SDK 的镜像。

### 配置持久化

安装向导完成后，所有配置写入 `data/config.json`，后续启动自动加载，无需重新配置。

数据目录结构：

```
data/
├── config.json          # 安装向导生成的配置（数据库 + 存储凭证）
├── suisuichong.db       # SQLite 数据库文件（选择 SQLite 时）
└── uploads/             # 本地存储的文件（选择本地存储时）
```

> ⚠️ 以上数据通过 Docker Volume `tunnel-worm_data` 持久化，`docker rm` 不会丢失数据。

### 重新配置

如需重新运行安装向导，删除 Volume 中的配置文件后重启容器：

```bash
# 进入容器删除配置
docker exec tunnel-worm rm /app/data/config.json

# 重启容器
docker restart tunnel-worm
```

重启后会自动重新进入安装向导。

### 备份数据

```bash
# 备份整个数据目录
docker run --rm -v tunnel-worm_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/tunnel-worm-backup.tar.gz /data
```

---

## 💻 本地开发

**前置要求**: Python 3.10+, Node.js 18+

```bash
git clone https://github.com/tianleiyiji123/tunnel-worm.git
cd tunnel-worm

# ---- 后端 ----
cd server
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py              # 启动后端 http://localhost:7895

# ---- 前端（新终端） ----
cd client
npm install
npm run dev                 # 启动前端 http://localhost:5173
```

首次启动后端后，访问 **http://localhost:7895** 进入安装向导，配置数据库和存储方式。配置完成后重新启动后端即可使用。

> 开发模式下数据库和存储同样通过安装向导配置（保存在 `server/data/config.json`）。也可通过 `.env` 预配置应用参数（如过期时间、文件大小限制等）。

---

## 📖 使用指南

### 发送资源

1. 选择传输类型：**文本** / **文件** / **文本 + 文件**
2. 输入内容或上传文件
3. （可选）开启 **端到端加密** — 加密后服务端无法查看内容，只有持有密码的人才能解密
4. 点击「生成密码」，获得 4 位密码（大写字母 + 数字）
5. 将密码、**分享链接** 或 **二维码** 发送给对方

### 提取资源

**方式一：手动输入密码**

1. 输入发送方提供的 4 位密码
2. 点击「提取资源」
3. 查看文本内容或下载文件

**方式二：分享链接**

接收方点击分享链接（如 `https://your-domain.com/s/A3K7`），自动跳转到提取页并自动提交，直接展示提取结果。

**方式三：二维码**

接收方扫码后跳转到提取页并自动提交，直接展示提取结果。

> ⚠️ 密码连续错误 5 次后锁定 1 分钟，防止暴力破解。

### 端到端加密

发送方在发送前可开启「端到端加密」开关：

| | 未加密 | 端到端加密 |
| --- | --- | --- |
| 加密位置 | 无 | 浏览器端 |
| 服务端存储 | 明文 | 密文 |
| 服务端可读 | ✅ 是 | ❌ 否 |
| 解密位置 | — | 接收方浏览器 |
| 加密算法 | — | AES-256-GCM + PBKDF2 |
| 性能影响 | — | 几乎无感（加密 < 100ms） |

加密使用传输密码作为密钥，接收方提取时浏览器自动解密，无需额外操作。如果密码错误，GCM 认证失败会提示解密失败。

### 登录用户特权

| 功能         | 未登录          | 已登录          |
| ------------ | --------------- | --------------- |
| 发送/提取    | ✅              | ✅              |
| 文本过期     | 24 小时自动删除 | **永久保存**    |
| 文件过期     | 24 小时自动删除 | 24 小时自动删除 |
| 查看发送记录 | ❌              | ✅              |
| 查看提取记录 | ❌              | ✅              |

## 🏗️ 架构

```
┌─────────────────────────────────────────┐
│              Frontend (Vue 3)           │
│         Vite + TypeScript               │
│    Element Plus + TailwindCSS           │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │     E2EE (Web Crypto API)        │   │
│  │  AES-256-GCM + PBKDF2            │   │
│  └──────────────────────────────────┘   │
└──────────────────┬──────────────────────┘
                   │ REST API
┌──────────────────▼──────────────────────┐
│            Backend (FastAPI)            │
│         Python + SQLAlchemy ORM         │
│  ┌─────────┬──────────┬──────────────┐  │
│  │  Auth   │ Transfer │  Records     │  │
│  │  JWT    │  CRUD    │  Operation   │  │
│  └─────────┴──────────┴──────────────┘  │
│  ┌──────────────────────────────────┐   │
│  │       Web 安装向导 (Setup)       │   │
│  │  数据库配置 / 存储配置 / 测试连接 │   │
│  └──────────────────────────────────┘   │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│              Storage Layer              │
│  Local · MinIO · AliOSS · TencentCOS    │
└─────────────────────────────────────────┘
```

### 技术栈

| 层级     | 技术                                      |
| -------- | ----------------------------------------- |
| 前端框架 | Vue 3 + TypeScript + Vite 5               |
| UI 组件  | Element Plus + TailwindCSS + Lucide Icons |
| 加密     | Web Crypto API (AES-256-GCM + PBKDF2)     |
| 二维码   | qrcode (浏览器端生成)                      |
| 后端框架 | Python 3.10+ / FastAPI / Uvicorn          |
| ORM      | SQLAlchemy 2.0                            |
| 数据库   | SQLite（默认）/ MySQL（可选）             |
| 认证     | JWT (python-jose + passlib bcrypt)        |
| 定时任务 | APScheduler                               |
| 部署     | Docker 多阶段构建 + Web 安装向导          |

## 🛡️ 安全

- **密码保护**: 4 位字母数字密码（排除易混淆字符 O/0/I/1），5 次错误锁定
- **端到端加密**: 可选开启，AES-256-GCM + PBKDF2（10 万次迭代），浏览器端加解密，服务端无法解密
- **密码哈希**: 用户密码经 SHA-256 预哈希后再 bcrypt 存储，避免 bcrypt 72 字节限制
- **自动过期**: 资源 24 小时后自动清理，登录用户文本除外
- **JWT 认证**: HS256 算法，Token 有效期 7 天，密钥首次启动自动生成
- **私有化部署**: 数据完全存储在自己的服务器上，不经过第三方

## 📄 License

[MIT](LICENSE)

---

<div align="center">
Made with 🐛 by <a href="https://github.com/tianleiyiji123/tunnel-worm">Tunnel Worm</a>
</div>
