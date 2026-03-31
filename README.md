<div align="center">

# 🐛 隧隧虫 (SuiSuiChong)

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
- **🔐 密码保护** — 大写字母+数字混合密码（排除易混淆字符），5 次错误后锁定 1 分钟
- **⏰ 自动过期** — 资源 24 小时后自动删除，登录用户文本永久保存
- **👤 可选登录** — 不登录也能用；登录后可查看操作记录，文本永久保存
- **💾 多存储后端** — 本地存储 / MinIO / 阿里云 OSS / 腾讯云 COS
- **🐳 一键部署** — Docker 单镜像，pull 即用，内置 Web 安装向导
- **📱 响应式设计** — 适配桌面端和移动端，随时随刻传输

## 🚀 快速开始

### Docker 部署（推荐）

```bash
# 1. 启动服务
docker compose up -d

# 2. 访问安装向导
open http://localhost:7895
```

首次启动会进入安装向导，配置数据库和存储后即可使用。数据存储在 Docker Volume `suisuichong_data` 中。

> 💡 安装向导支持 SQLite（零配置）和 MySQL，存储支持本地 / MinIO / 阿里云 OSS / 腾讯云 COS。

### 本地开发

**前置要求**: Python 3.10+, Node.js 18+

```bash
# 克隆项目
git clone https://github.com/yourname/suisuichong.git
cd suisuichong

# ---- 后端 ----
cd server
pip install -r requirements.txt
cp .env.example .env   # 编辑数据库和存储配置
python main.py          # 启动后端 http://localhost:7895

# ---- 前端（新终端） ----
cd client
npm install
npm run dev             # 启动前端 http://localhost:5173
```

> 开发模式下前端通过 Vite proxy 转发 API 到后端。

### Docker 自定义构建

```bash
# 重新构建镜像（代码变更后）
docker compose build --no-cache

# 重建并启动
docker compose up -d
```

## 📖 使用指南

### 发送资源

1. 选择传输类型：**文本** / **文件** / **文本 + 文件**
2. 输入内容或上传文件
3. 点击「生成密码」，获得 4 位密码（大写字母 + 数字）
4. 将密码告诉对方

### 提取资源

1. 输入发送方提供的密码
2. 点击「提取资源」
3. 查看文本内容或下载文件

> ⚠️ 密码连续错误 5 次后锁定 1 分钟，防止暴力破解。

### 登录用户特权

| 功能 | 未登录 | 已登录 |
|------|--------|--------|
| 发送/提取 | ✅ | ✅ |
| 文本过期 | 24 小时自动删除 | **永久保存** |
| 文件过期 | 24 小时自动删除 | 24 小时自动删除 |
| 查看发送记录 | ❌ | ✅ |
| 查看提取记录 | ❌ | ✅ |

## 🏗️ 架构

```
┌─────────────────────────────────────────┐
│              Frontend (Vue 3)           │
│         Vite + TypeScript               │
│    Element Plus + TailwindCSS           │
└──────────────────┬──────────────────────┘
                   │ REST API
┌──────────────────▼──────────────────────┐
│            Backend (FastAPI)            │
│         Python + SQLAlchemy ORM         │
│  ┌─────────┬──────────┬──────────────┐  │
│  │  Auth   │ Transfer │  Records     │  │
│  │  JWT    │  CRUD    │  Operation   │  │
│  └─────────┴──────────┴──────────────┘  │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│              Storage Layer              │
│  Local · MinIO · AliOSS · TencentCOS    │
└─────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | Vue 3 + TypeScript + Vite 5 |
| UI 组件 | Element Plus + TailwindCSS + Lucide Icons |
| 后端框架 | Python 3.10+ / FastAPI / Uvicorn |
| ORM | SQLAlchemy 2.0 |
| 数据库 | SQLite（默认）/ MySQL（可选） |
| 认证 | JWT (python-jose + passlib bcrypt) |
| 定时任务 | APScheduler |
| 部署 | Docker 多阶段构建 + Web 安装向导 |

## 📁 项目结构

```
suisuichong/
├── client/                  # Vue 3 前端
│   ├── src/
│   │   ├── api/             # Axios API 封装 + 拦截器
│   │   ├── components/      # 通用组件
│   │   │   ├── AppHeader.vue       # 顶部导航 + 用户菜单
│   │   │   ├── CodeDisplay.vue     # 密码展示弹窗
│   │   │   ├── LoginDialog.vue     # 登录/注册弹窗
│   │   │   ├── PasswordInput.vue   # 密码输入框
│   │   │   ├── ResourcePreview.vue # 资源预览
│   │   │   ├── SendText.vue        # 文本输入
│   │   │   └── SendFile.vue        # 文件上传
│   │   ├── composables/     # 组合式函数 (useAuth)
│   │   ├── views/           # 页面视图
│   │   │   ├── HomeView.vue       # 首页（发送资源）
│   │   │   ├── RetrieveView.vue   # 提取资源
│   │   │   ├── RecordsView.vue    # 操作记录
│   │   │   └── SetupView.vue      # 安装向导
│   │   ├── router/          # 路由配置 + 守卫
│   │   └── styles/          # 全局样式
│   └── public/              # 静态资源 (favicon.svg)
├── server/                  # FastAPI 后端
│   ├── routes/              # API 路由
│   │   ├── auth.py          # 认证 (注册/登录/用户信息)
│   │   ├── transfer.py      # 传输 (发送/验证/提取/下载)
│   │   ├── records.py       # 操作记录分页查询
│   │   └── setup.py         # 安装向导 (状态/测试/完成)
│   ├── services/            # 业务逻辑
│   │   ├── auth_service.py  # 密码哈希、JWT、用户 CRUD
│   │   ├── transfer_service.py  # 传输 CRUD + 过期清理
│   │   └── storage/         # 存储抽象层
│   │       ├── base.py            # 抽象接口
│   │       ├── local.py           # 本地文件存储
│   │       ├── minio_backend.py   # MinIO
│   │       ├── alioss.py          # 阿里云 OSS
│   │       └── tencentcos.py      # 腾讯云 COS
│   ├── database.py          # ORM 模型 (User, Transfer, TransferFile, TransferRecord)
│   ├── config.py            # 配置管理 (pydantic-settings)
│   ├── setup_config.py      # config.json 读写 + 热更新
│   ├── deps.py              # 依赖注入 (get_current_user)
│   ├── schemas.py           # Pydantic 请求/响应模型
│   ├── requirements.txt           # 完整依赖（开发用）
│   └── requirements-docker.txt    # 精简依赖（Docker 镜像用）
├── docker/
│   ├── Dockerfile           # 多阶段构建 (Node + Python)
│   └── entrypoint.sh        # 启动脚本
├── docker-compose.yml       # 单服务编排
└── README.md
```

## 🔌 API 接口

### 传输

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/transfer` | 发送资源（multipart/form-data） |
| POST | `/api/transfer/verify` | 验证密码是否有效 |
| GET | `/api/transfer/{code}` | 提取资源详情 |
| GET | `/api/transfer/{code}/download/{filename}` | 下载文件 |

### 认证（可选）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/register` | 注册 |
| POST | `/api/auth/login` | 登录 |
| GET | `/api/auth/me` | 获取当前用户信息 |

### 操作记录（需登录）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/records` | 分页查询操作记录 |

### 安装向导

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/setup/status` | 获取初始化状态 |
| POST | `/api/setup/test-db` | 测试数据库连接 |
| POST | `/api/setup/test-storage` | 测试存储连接 |
| POST | `/api/setup/finish` | 完成安装 |

### 健康检查

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 服务健康状态 |

## 🔧 配置

### 环境变量 / .env

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DB_TYPE` | 数据库类型 (sqlite/mysql) | 空（自动检测） |
| `DB_HOST` | MySQL 主机 | localhost |
| `DB_PORT` | MySQL 端口 | 3306 |
| `DB_USER` | MySQL 用户名 | suisuichong |
| `DB_PASSWORD` | MySQL 密码 | suisuichong123 |
| `DB_NAME` | MySQL 数据库名 | suisuichong |
| `STORAGE_TYPE` | 存储类型 (local/minio/alioss/tencentcos) | local |
| `TRANSFER_EXPIRE_HOURS` | 资源过期时间（小时） | 24 |
| `MAX_FILE_SIZE_MB` | 单文件最大大小 (MB) | 50 |
| `MAX_FILES_PER_TRANSFER` | 单次传输最大文件数 | 10 |
| `MAX_FAIL_ATTEMPTS` | 密码最大错误次数 | 5 |
| `LOCK_DURATION_MINUTES` | 锁定时长（分钟） | 1 |
| `JWT_SECRET` | JWT 签名密钥（自动生成） | — |
| `JWT_EXPIRE_HOURS` | Token 有效期（小时） | 168 (7天) |

> Docker 部署时通过 Web 安装向导配置，配置持久化到 `config.json`。

## 🛡️ 安全

- **密码保护**: 4 位字母数字密码（排除易混淆字符 O/0/I/1），5 次错误锁定
- **密码哈希**: 用户密码经 SHA-256 预哈希后再 bcrypt 存储，避免 bcrypt 72 字节限制
- **自动过期**: 资源 24 小时后自动清理，登录用户文本除外
- **JWT 认证**: HS256 算法，Token 有效期 7 天，密钥首次启动自动生成
- **私有化部署**: 数据完全存储在自己的服务器上，不经过第三方

## 📄 License

[MIT](LICENSE)

---

<div align="center">
Made with 🐛 by <a href="#">隧隧虫</a>
</div>
