# ============================================================
# Tunnel Worm - Docker Image
# ============================================================
# Multi-stage build: Frontend (Node) + Backend (Python)
# Optimized for Docker Hub distribution
# ============================================================

# ---- Stage 1: 前端构建 ----
FROM node:20-alpine AS frontend-builder

WORKDIR /app/client
COPY client/package*.json ./
RUN npm ci
COPY client/ ./
RUN npx vite build

# ---- Stage 2: 运行阶段 ----
FROM python:3.11-slim

# Re-declare ARGs to use in this stage
ARG VERSION=1.0.0
ARG BUILD_DATE=unknown

# ---- Metadata Labels ----
LABEL maintainer="tianleiyiji123"
LABEL description="Tunnel Worm - 跨设备资源传输工具，一条隧道连接你的设备，Tunnel Worm - Cross-device resource transfer tool, one tunnel connects your devices"
LABEL version="${VERSION}"
LABEL org.opencontainers.image.title="Tunnel Worm"
LABEL org.opencontainers.image.description="Cross-device resource transfer tool"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.source="https://github.com/tianleiyiji123/tunnel-worm"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.vendor="Tunnel Worm"

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

# Expose port
EXPOSE 7895

# Environment variables
ENV DATA_DIR=/app/data
ENV PYTHONUNBUFFERED=1

# Data volume
VOLUME ["/app/data"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:7895/api/health')" || exit 1

# Start command
CMD ["/app/entrypoint.sh"]
