# ---- Stage 1: 前端构建 ----
FROM node:20-alpine AS frontend-builder

WORKDIR /app/client
COPY client/package*.json ./
RUN npm ci
COPY client/ ./
RUN npx vite build

# ---- Stage 2: 运行阶段 ----
FROM python:3.11-slim

WORKDIR /app

# 安装 Python 基础依赖（不含 MySQL SDK 和云存储 SDK）
COPY server/requirements-docker.txt ./requirements-docker.txt
RUN pip install --no-cache-dir -r requirements-docker.txt

# 复制后端代码
COPY server/ ./server/

# 复制前端构建产物到 static 目录（FastAPI StaticFiles 服务）
COPY --from=frontend-builder /app/client/dist ./static

# 复制启动脚本
COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 创建数据目录
RUN mkdir -p /app/data /app/data/uploads

EXPOSE 7895

ENV DATA_DIR=/app/data
VOLUME ["/app/data"]

CMD ["/app/entrypoint.sh"]
