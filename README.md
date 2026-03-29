# 🐛 隧隧虫 (SuiSuiChong)

跨设备资源传输工具 — 像虫子钻隧道一样，让数据在设备间快速传输。

## ✨ 功能

- **文本传输**：粘贴文本内容，生成密码，另一台设备输入密码即可复制
- **文件传输**：上传文件（支持多文件、拖拽），密码提取后可下载
- **混合传输**：同时发送文本和文件
- **多存储后端**：支持本地磁盘 / MinIO / 阿里云 OSS / 腾讯云 COS
- **安全机制**：4 位数字密码 + 24h 过期 + 防爆破锁定
- **一键部署**：Docker 单镜像，pull 即用，Web 安装向导完成配置

## 🛠 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Vite + Element Plus + TailwindCSS |
| 后端 | Python + FastAPI + Uvicorn |
| 数据库 | SQLite（默认）/ MySQL（可选） |
| 部署 | Docker 单镜像 + Nginx |

## 🚀 快速开始

### Docker 一键部署（推荐）

```bash
# 方式一：Docker Hub 拉取（发布后可用）
docker run -d -p 80:80 -v suisuichong_data:/app/data suisuichong

# 方式二：本地构建
git clone <repo-url> && cd suisui
docker-compose up -d

# 首次启动访问 http://localhost ，进入安装向导完成配置
# 配置数据保存在 /app/data/config.json，挂载 volume 后重启不丢失
```

### 安装向导

首次启动时，系统会自动进入安装向导页面：

1. **数据库配置**：选择 SQLite（推荐，零配置）或 MySQL（需填写连接信息）
2. **存储配置**：选择容器内部存储（推荐）或 MinIO / 阿里云 OSS / 腾讯云 COS

配置完成后，系统会自动初始化并进入正常使用页面。

### 开发模式

**后端**：
```bash
cd server
pip install -r requirements.txt
python main.py
# 访问 http://localhost:8000/docs 查看 API 文档
```

**前端**：
```bash
cd client
npm install
npm run dev
# 访问 http://localhost:5173
```

> 开发模式下使用 `.env` 文件配置，不经过安装向导。路由守卫在检测到 API 不可用时自动跳过。

## ⚙️ 存储配置

| 后端 | 说明 | 必需配置项 |
|---|---|---|
| 容器内部存储 | 默认，文件存于 `/app/data/uploads/` | 无 |
| MinIO | 自建对象存储 | Endpoint + Access Key + Secret Key + Bucket |
| 阿里云 OSS | 阿里云对象存储 | Access Key ID + Secret + Bucket + Endpoint |
| 腾讯云 COS | 腾讯云对象存储 | Secret ID + Secret Key + Bucket + Region |

存储配置可在安装向导中通过 Web 界面完成，支持测试连接验证。

## 📁 项目结构

```
suisui/
├── client/              # Vue 3 前端
│   └── src/
│       ├── views/
│       │   └── SetupView.vue    # 安装向导页面
│       ├── router/              # 路由（含初始化守卫）
│       └── api/                 # API 调用（含 setup API）
├── server/              # FastAPI 后端
│   ├── routes/
│   │   ├── transfer.py          # 业务 API
│   │   └── setup.py             # 安装向导 API
│   ├── services/
│   │   └── storage/             # 存储后端（local/minio/alioss/tencentcos）
│   ├── config.py                # 配置管理（支持 .env + config.json）
│   ├── database.py              # 数据库（SQLite/MySQL 延迟初始化）
│   ├── setup_config.py          # 安装向导配置读写
│   ├── requirements.txt         # 完整依赖（开发用）
│   └── requirements-docker.txt  # 精简依赖（Docker 镜像用）
├── docker/
│   ├── Dockerfile               # 多阶段构建
│   ├── nginx.conf               # Nginx 反向代理
│   └── entrypoint.sh            # 启动脚本
├── docker-compose.yml           # 编排文件
└── .dockerignore
```

## 📄 License

MIT
