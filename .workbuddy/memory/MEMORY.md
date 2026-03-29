# 隧隧虫项目记忆

## 项目概述
- **项目名**: 隧隧虫 (SuiSuiChong) - 跨设备资源传输工具
- **路径**: /Users/lwang/myproject/suisui
- **创建日期**: 2026-03-28

## 技术栈
- **前端**: Vue 3 + TypeScript + Vite 5 + Element Plus + TailwindCSS + Lucide Icons + Axios
- **后端**: Python + FastAPI + Uvicorn + SQLAlchemy
- **数据库**: SQLite（默认）+ MySQL（可选），延迟初始化
- **存储**: 抽象存储层 (local / MinIO / 阿里云 OSS / 腾讯云 COS)
- **部署**: Docker 单镜像 + Web 安装向导（私有化部署，pull 即用）

## 关键决策
- 密码: 4 位数字 + 5 次错误后锁定 1 分钟（防爆破）
- 资源过期: 24 小时，每小时自动清理
- 数据库: SQLite（默认，Docker 镜像零配置）/ MySQL（可选，安装向导配置）
- 品牌风格: 有机自然风，森林绿(#2D6A4F) + 暖土橙(#E76F51)
- 存储后端: 自动检测 + 懒加载 SDK + 安装向导 Web 配置
- 配置管理: 开发用 `.env`，Docker 用 `config.json`（安装向导写入 `/app/data/config.json`）
- 延迟初始化: database.py engine/SessionLocal + transfer_service.py storage + main.py storage 都改为按需初始化
- Docker 依赖拆分: requirements.txt（完整，开发用）/ requirements-docker.txt（精简，镜像用，不含 pymysql 和云 SDK）

## 项目结构
- `client/` - Vue 3 前端 (Vite)
- `server/` - FastAPI 后端
- `server/routes/setup.py` - 安装向导 API（4 端点：status/test-db/test-storage/finish）
- `server/setup_config.py` - config.json 读写 + settings 热更新
- `server/services/storage/` - 存储抽象层 (base/local/minio_backend/alioss/tencentcos)
- `server/requirements-docker.txt` - Docker 镜像精简依赖
- `client/src/views/SetupView.vue` - 安装向导前端页面
- `docker/` - Dockerfile(多阶段构建), nginx.conf, entrypoint.sh
- `.dockerignore` - Docker 构建排除
- `docker-compose.yml` - 单服务编排

## 使用方式
- 开发: 前端 `cd client && npm run dev`, 后端 `cd server && python main.py`（使用 .env）
- Docker: `docker run -d -p 80:80 -v suisuichong_data:/app/data suisuichong`
- 首次启动: 访问 http://localhost 进入安装向导，配置数据库和存储
- 路由守卫: 前端检测 `/api/setup/status`，未初始化自动重定向到 `/setup`
