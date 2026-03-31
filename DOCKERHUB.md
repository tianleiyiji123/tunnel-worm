<div align="center">

# 🐛 Tunnel Worm

**跨设备，传什么都可以。**

一条隧道连接你的设备 —— 文本、文件，生成密码，另一台设备输入即可提取。

无需注册 · 无需安装客户端 · 数据不经过第三方

[![Docker Pulls](https://img.shields.io/docker/pulls/lwang/tunnel-worm?style=flat-square)](https://hub.docker.com/r/lwang/tunnel-worm)
[![Docker Image Size](https://img.shields.io/docker/image-size/lwang/tunnel-worm?style=flat-square)](https://hub.docker.com/r/lwang/tunnel-worm)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)

</div>

---

## ✨ 特性

- **📱 跨设备传输** — 发送文本或文件，生成 4 位字母数字密码，任何设备均可提取
- **🔐 密码保护** — 大写字母+数字混合密码（排除易混淆字符），5 次错误后锁定 1 分钟
- **⏰ 自动过期** — 资源 24 小时后自动删除，登录用户文本永久保存
- **💾 多存储后端** — 本地存储 / MinIO / 阿里云 OSS / 腾讯云 COS
- **🐳 一键部署** — Docker 单镜像，pull 即用，内置 Web 安装向导
- **🔒 数据隐私** — 私有化部署，数据完全存储在自己的服务器上

---

## 🚀 快速开始

### 方法 1: Docker Run（最快）

```bash
docker run -d \
  --name tunnel-worm \
  -p 7895:7895 \
  -v tunnel-worm_data:/app/data \
  lwang/tunnel-worm:latest
```

### 方法 2: Docker Compose（推荐）

创建 `docker-compose.yml`:

```yaml
services:
  tunnel-worm:
    image: lwang/tunnel-worm:latest
    container_name: tunnel-worm
    restart: unless-stopped
    ports:
      - "7895:7895"
    volumes:
      - tunnel-worm_data:/app/data
    environment:
      - DATA_DIR=/app/data

volumes:
  tunnel-worm_data:
```

启动服务:

```bash
docker compose up -d
```

### 首次访问

打开浏览器访问: **http://localhost:7895**

首次启动会自动进入**安装向导**，配置数据库和存储后即可使用。

> 💡 **零配置方案**: 安装向导支持 SQLite（默认，无需配置）和 MySQL（可选）
>
> 💡 **存储选择**: 支持本地存储 / MinIO / 阿里云 OSS / 腾讯云 COS

---

## 📖 使用指南

### 发送资源

1. 选择传输类型: **文本** / **文件** / **文本 + 文件**
2. 输入内容或上传文件
3. 点击「生成密码」，获得 4 位密码（大写字母 + 数字）
4. 将密码告诉对方

### 提取资源

1. 输入发送方提供的密码
2. 点击「提取资源」
3. 查看文本内容或下载文件

> ⚠️ 密码连续错误 5 次后锁定 1 分钟，防止暴力破解。

### 登录用户特权

| 功能         | 未登录          | 已登录          |
| ------------ | --------------- | --------------- |
| 发送/提取    | ✅              | ✅              |
| 文本过期     | 24 小时自动删除 | **永久保存**    |
| 文件过期     | 24 小时自动删除 | 24 小时自动删除 |
| 查看发送记录 | ❌              | ✅              |
| 查看提取记录 | ❌              | ✅              |

---

## 🔧 配置选项

### 环境变量

| 变量                     | 说明                                     | 默认值         |
| ------------------------ | ---------------------------------------- | -------------- |
| `DATA_DIR`               | 数据目录                                 | /app/data      |
| `DB_TYPE`                | 数据库类型 (sqlite/mysql)                | 空（自动检测） |
| `DB_HOST`                | MySQL 主机                               | localhost      |
| `DB_PORT`                | MySQL 端口                               | 3306           |
| `DB_USER`                | MySQL 用户名                             | tunnelworm     |
| `DB_PASSWORD`            | MySQL 密码                               | tunnelworm123  |
| `DB_NAME`                | MySQL 数据库名                           | tunnelworm     |
| `STORAGE_TYPE`           | 存储类型 (local/minio/alioss/tencentcos) | local          |
| `TRANSFER_EXPIRE_HOURS`  | 资源过期时间（小时）                     | 24             |
| `MAX_FILE_SIZE_MB`       | 单文件最大大小 (MB)                      | 50             |
| `MAX_FILES_PER_TRANSFER` | 单次传输最大文件数                       | 10             |

> 💡 通过 Web 安装向导配置，设置持久化到 `config.json`

---

## 🏗️ 技术架构

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

**技术栈**:
- 前端: Vue 3 + TypeScript + Vite 5
- UI: Element Plus + TailwindCSS
- 后端: Python 3.11 + FastAPI + Uvicorn
- 数据库: SQLite / MySQL
- 认证: JWT (HS256)
- 部署: Docker 多阶段构建

---

## 🛡️ 安全特性

- **密码保护**: 4 位字母数字密码（排除易混淆字符 O/0/I/1）
- **防暴力破解**: 密码错误 5 次后锁定 1 分钟
- **密码哈希**: 用户密码经 SHA-256 预哈希后再 bcrypt 存储
- **自动过期**: 资源 24 小时后自动清理
- **私有化部署**: 数据完全存储在自己的服务器上

---

## 📁 数据持久化

数据存储在 Docker Volume `tunnel-worm_data` 中，包括:

```
/app/data/
├── config.json          # 配置文件（安装向导生成）
├── app.db               # SQLite 数据库（如果使用 SQLite）
└── uploads/             # 本地存储文件（如果使用本地存储）
```

**备份 Volume**:

```bash
docker run --rm -v tunnel-worm_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/tunnel-worm-backup.tar.gz /data
```

---

## 🔄 版本更新

```bash
# 拉取最新镜像
docker pull lwang/tunnel-worm:latest

# 重建容器
docker compose up -d

# 或使用 docker run
docker stop tunnel-worm
docker rm tunnel-worm
docker run -d --name tunnel-worm -p 7895:7895 -v tunnel-worm_data:/app/data lwang/tunnel-worm:latest
```

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/lwang/suisuichong
- **完整文档**: 查看 GitHub README.md 了解更多详情
- **问题反馈**: https://github.com/lwang/suisuichong/issues

---

## 📄 License

[MIT](LICENSE)

---

<div align="center">
Made with 🐛 by <a href="https://github.com/lwang/suisuichong">Tunnel Worm</a>
</div>
