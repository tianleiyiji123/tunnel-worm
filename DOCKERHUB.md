<div align="center">

# 🐛 Tunnel Worm

**跨设备，传什么都可以。**

一条隧道连接你的设备 —— 文本、文件，生成密码，另一台设备输入即可提取。

无需注册 · 无需安装客户端 · 数据不经过第三方

[![Docker Pulls](https://img.shields.io/docker/pulls/tianleiyiji123/tunnel-worm?style=flat-square)](https://hub.docker.com/r/tianleiyiji123/tunnel-worm)
[![Docker Image Size](https://img.shields.io/docker/image-size/tianleiyiji123/tunnel-worm?style=flat-square)](https://hub.docker.com/r/tianleiyiji123/tunnel-worm)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)

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

---

## 🚀 快速开始

### 方法 1：Docker Run（最快）

```bash
docker run -d \
  --name tunnel-worm \
  -p 7895:7895 \
  -v tunnel-worm_data:/app/data \
  tianleiyiji123/tunnel-worm:latest
```

### 方法 2：Docker Compose（推荐）

创建 `docker-compose.yml`:

```yaml
services:
  tunnel-worm:
    image: tianleiyiji123/tunnel-worm:latest
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

首次启动会自动进入 **安装向导**，配置数据库和存储后即可使用。

---

## 🛠️ 安装向导

首次启动时，应用会自动进入 **Web 安装向导**，通过浏览器完成所有配置，无需编辑任何配置文件。

安装向导分两步：

### 第一步：数据库配置

| 选项               | 说明                                       | 适用场景                    |
| ------------------ | ------------------------------------------ | --------------------------- |
| **SQLite（推荐）** | 零配置，数据文件存储在容器内部             | 个人使用、轻量部署          |
| **MySQL**          | 需要填写主机、端口、用户名、密码、数据库名 | 已有 MySQL 服务、高并发场景 |

选择 MySQL 时，向导页面会展开表单，填写连接信息后点击「测试连接」验证是否可用。

> 💡 Docker 默认镜像不包含 MySQL 驱动，如需使用 MySQL 请自行安装 `pymysql`。

### 第二步：存储配置

| 选项                     | 说明                       | 需要填写的凭证                                     |
| ------------------------ | -------------------------- | -------------------------------------------------- |
| **容器内部存储（推荐）** | 零配置，文件存储在容器内部 | 无                                                 |
| **MinIO**                | 兼容 S3 的自建对象存储     | Endpoint、Access Key、Secret Key、Bucket           |
| **阿里云 OSS**           | 阿里云对象存储             | Access Key ID、Access Key Secret、Endpoint、Bucket |
| **腾讯云 COS**           | 腾讯云对象存储             | Secret ID、Secret Key、Region、Bucket              |

选择对象存储后，同样可以点击「测试连接」验证凭证是否正确。

> 💡 Docker 默认镜像不包含云存储 SDK。如需使用对象存储，需要在容器内手动安装对应 SDK，或自行构建包含 SDK 的镜像。

### 配置持久化

安装向导完成后，所有配置写入 `/app/data/config.json`，后续启动自动加载，无需重新配置。

数据目录结构：

```
/app/data/
├── config.json          # 安装向导生成的配置（数据库 + 存储凭证）
├── app.db               # SQLite 数据库文件（选择 SQLite 时）
└── uploads/             # 本地存储的文件（选择容器内部存储时）
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

---

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

| 功能         | 未登录          | 已登录          |
| ------------ | --------------- | --------------- |
| 发送/提取    | ✅              | ✅              |
| 文本过期     | 24 小时自动删除 | **永久保存**    |
| 文件过期     | 24 小时自动删除 | 24 小时自动删除 |
| 查看发送记录 | ❌              | ✅              |
| 查看提取记录 | ❌              | ✅              |

---

## 🔧 配置选项

### 配置方式

| 方式             | 说明                                 |
| ---------------- | ------------------------------------ |
| **Web 安装向导** | 浏览器中完成配置，写入 `config.json` |
| **环境变量**     | `docker run -e DB_TYPE=mysql ...`    |

> 💡 **推荐使用安装向导**，无需手动编辑任何文件。安装向导的配置优先级高于环境变量。

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
| `MAX_FAIL_ATTEMPTS`      | 密码最大错误次数                         | 5              |
| `LOCK_DURATION_MINUTES`  | 锁定时长（分钟）                         | 1              |
| `JWT_SECRET`             | JWT 签名密钥（自动生成）                 | —              |
| `JWT_EXPIRE_HOURS`       | Token 有效期（小时）                     | 168 (7 天)     |

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

**技术栈**:

| 层级     | 技术                                      |
| -------- | ----------------------------------------- |
| 前端框架 | Vue 3 + TypeScript + Vite 5               |
| UI 组件  | Element Plus + TailwindCSS + Lucide Icons |
| 后端框架 | Python 3.10+ / FastAPI / Uvicorn          |
| ORM      | SQLAlchemy 2.0                            |
| 数据库   | SQLite（默认）/ MySQL（可选）             |
| 认证     | JWT (python-jose + passlib bcrypt)        |
| 定时任务 | APScheduler                               |
| 部署     | Docker 多阶段构建 + Web 安装向导          |

---

## 🛡️ 安全特性

- **密码保护**: 4 位字母数字密码（排除易混淆字符 O/0/I/1），5 次错误锁定
- **密码哈希**: 用户密码经 SHA-256 预哈希后再 bcrypt 存储，避免 bcrypt 72 字节限制
- **自动过期**: 资源 24 小时后自动清理，登录用户文本除外
- **JWT 认证**: HS256 算法，Token 有效期 7 天，密钥首次启动自动生成
- **私有化部署**: 数据完全存储在自己的服务器上，不经过第三方

---

## 📁 数据备份与恢复

数据存储在 Docker Volume `tunnel-worm_data` 中。

**备份数据**:

```bash
docker run --rm -v tunnel-worm_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/tunnel-worm-backup.tar.gz /data
```

**恢复数据**:

```bash
docker run --rm -v tunnel-worm_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/tunnel-worm-backup.tar.gz -C /
```

---

## 🔄 版本更新

```bash
# 拉取最新镜像
docker pull tianleiyiji123/tunnel-worm:latest

# 重建容器
docker compose up -d

# 或使用 docker run
docker stop tunnel-worm
docker rm tunnel-worm
docker run -d --name tunnel-worm -p 7895:7895 -v tunnel-worm_data:/app/data \
  tianleiyiji123/tunnel-worm:latest
```

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/tianleiyiji123/tunnel-worm
- **完整文档**: 查看 [GitHub README](https://github.com/tianleiyiji123/tunnel-worm#readme) 了解本地开发、API 接口、项目结构等更多详情
- **问题反馈**: https://github.com/tianleiyiji123/tunnel-worm/issues

---

## 📄 License

[MIT](LICENSE)

---

<div align="center">
Made with 🐛 by <a href="https://github.com/tianleiyiji123/tunnel-worm">Tunnel Worm</a>
</div>
