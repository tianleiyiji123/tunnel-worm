<div align="center">

# 🐛 隧隧虫 (SuiSuiChong)

**跨设备，传什么都可以。**

一条隧道连接你的设备 —— 文本、文件，生成四位密码，另一台设备输入即可提取。

无需注册 · 无需安装客户端 · 数据不经过第三方

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![Vue](https://img.shields.io/badge/Vue-3.x-4FC08D.svg)](https://vuejs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)](https://docker.com)

</div>

---

## ✨ 特性

- **📱 跨设备传输** — 发送文本或文件，生成 4 位数字密码，任何设备均可提取
- **🔐 密码保护** — 4 位数字密码，5 次错误后锁定 1 分钟，防止暴力破解
- **⏰ 自动过期** — 资源 24 小时后自动删除，登录用户文本永久保存
- **👤 可选登录** — 不登录也能用；登录后可查看操作记录，文本永久保存
- **💾 多存储后端** — 本地存储 / MinIO / 阿里云 OSS / 腾讯云 COS
- **🐳 一键部署** — Docker 单镜像，pull 即用，内置 Web 安装向导
- **🎨 自然设计** — 有机自然风格 UI，支持中英文

## 🚀 快速开始

### Docker 部署（推荐）

```bash
# 1. 启动服务
docker compose up -d

# 2. 访问安装向导
open http://localhost:7895
```

首次启动会进入安装向导，配置数据库和存储后即可使用。数据存储在 Docker Volume `suisuichong_data` 中。

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

# ---- 前端 ----
cd client
npm install
npm run dev             # 启动前端 http://localhost:5173
```

> 开发模式下前端通过 Vite proxy 转发 API 到后端。

## 📖 使用指南

### 发送资源

1. 选择传输类型：**文本** / **文件** / **文本 + 文件**
2. 输入内容或上传文件
3. 点击「生成密码」，获得 4 位数字密码
4. 将密码告诉对方

### 提取资源

1. 输入发送方提供的 4 位数字密码
2. 点击「提取资源」
3. 查看文本内容或下载文件

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
│         Vite + TypeScript + TP          │
│         Element Plus + Tailwind         │
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
| 认证 | JWT (python-jose + passlib) |
| 定时任务 | APScheduler |
| 部署 | Docker 单镜像 + Web 安装向导 |

## 📁 项目结构

```
suisuichong/
├── client/                  # Vue 3 前端
│   ├── src/
│   │   ├── api/             # Axios API 封装
│   │   ├── components/      # 通用组件
│   │   ├── composables/     # 组合式函数 (useAuth)
│   │   ├── views/           # 页面视图
│   │   ├── router/          # 路由配置
│   │   └── styles/          # 全局样式
│   └── public/              # 静态资源
├── server/                  # FastAPI 后端
│   ├── routes/              # API 路由
│   │   ├── auth.py          # 认证 (注册/登录)
│   │   ├── transfer.py      # 传输 (发送/提取)
│   │   ├── records.py       # 操作记录
│   │   └── setup.py         # 安装向导
│   ├── services/            # 业务逻辑
│   │   ├── transfer_service.py
│   │   ├── auth_service.py
│   │   └── storage/         # 存储抽象层
│   ├── database.py          # ORM 模型
│   ├── config.py            # 配置管理
│   └── schemas.py           # Pydantic 模型
├── docker/                  # Docker 构建文件
│   └── Dockerfile           # 多阶段构建
├── docker-compose.yml       # 单服务编排
└── README.md
```

## 🔧 配置

### 环境变量 / .env

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DB_TYPE` | 数据库类型 (sqlite/mysql) | 空 (自动检测) |
| `DB_HOST` | MySQL 主机 | localhost |
| `DB_PORT` | MySQL 端口 | 3306 |
| `DB_USER` | MySQL 用户名 | suisuichong |
| `DB_PASSWORD` | MySQL 密码 | suisuichong123 |
| `DB_NAME` | MySQL 数据库名 | suisuichong |
| `STORAGE_TYPE` | 存储类型 (local/minio/alioss/tencentcos) | local |
| `TRANSFER_EXPIRE_HOURS` | 资源过期时间（小时） | 24 |
| `MAX_FILE_SIZE_MB` | 单文件最大大小 (MB) | 50 |
| `MAX_FILES_PER_TRANSFER` | 单次传输最大文件数 | 10 |

> Docker 部署时通过 Web 安装向导配置，配置持久化到 `config.json`。

## 🛡️ 安全

- **密码保护**: 4 位数字密码 + 5 次错误锁定
- **自动过期**: 资源 24 小时后自动清理
- **JWT 认证**: HS256 算法，Token 有效期 7 天
- **密码哈希**: bcrypt 加密存储
- **私有化部署**: 数据完全存储在自己的服务器上

## 📄 License

[MIT](LICENSE)

---

<div align="center">
Made with 🐛 by <a href="#">隧隧虫</a>
</div>
