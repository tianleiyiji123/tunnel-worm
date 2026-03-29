# ---- Stage 1: 前端构建 ----
FROM node:20-alpine AS frontend-builder

WORKDIR /app/client
COPY client/package*.json ./
RUN npm ci
COPY client/ ./
RUN npm run build

# ---- Stage 2: 运行阶段 ----
FROM python:3.11-slim

# 安装 Nginx
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装 Python 基础依赖（不含 MySQL SDK 和云存储 SDK）
COPY server/requirements-docker.txt ./requirements-docker.txt
RUN pip install --no-cache-dir -r requirements-docker.txt

# 复制后端代码
COPY server/ ./server/

# 复制前端构建产物
COPY --from=frontend-builder /app/client/dist /usr/share/nginx/html

# 复制配置文件
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 创建数据目录
RUN mkdir -p /app/data /app/data/uploads

EXPOSE 80

ENV DATA_DIR=/app/data
VOLUME ["/app/data"]

CMD ["/app/entrypoint.sh"]
