# ============================================================
# Tunnel Worm - Docker Image (Ultra Optimized)
# ============================================================
# Multi-stage build: Frontend (Node) + Backend (Python Alpine)
# Target image size: <150MB
# ============================================================

# ---- Stage 1: 前端构建 ----
FROM node:20-alpine AS frontend-builder

WORKDIR /app/client
COPY client/package*.json ./
RUN npm ci --prefer-offline --no-audit
COPY client/ ./
RUN npx vite build && \
  rm -rf node_modules

# ---- Stage 2: 运行阶段 (Alpine + Python) ----
FROM python:3.12-alpine

# Re-declare ARGs to use in this stage
ARG VERSION=1.0.0
ARG BUILD_DATE=unknown

# ---- Metadata Labels ----
LABEL maintainer="tianleiyiji123"
LABEL description="Tunnel Worm - Cross-device resource transfer tool"
LABEL version="${VERSION}"
LABEL org.opencontainers.image.title="Tunnel Worm"
LABEL org.opencontainers.image.description="Cross-device resource transfer tool"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.source="https://github.com/tianleiyiji123/tunnel-worm"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.vendor="Tunnel Worm"

WORKDIR /app

# Install Python dependencies in a single layer (build deps installed and removed)
COPY server/requirements-docker.txt ./requirements-docker.txt
RUN apk add --no-cache --virtual .build-deps \
  gcc musl-dev libffi-dev rust cargo && \
  pip install --no-cache-dir --compile -r requirements-docker.txt && \
  apk del .build-deps && \
  find /usr/local -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true && \
  find /usr/local -type d -name 'tests' -exec rm -rf {} + 2>/dev/null || true && \
  rm -rf /root/.cache

# Runtime dependencies (minimal)
RUN apk add --no-cache libstdc++ curl

# Copy backend code (exclude unnecessary files)
COPY server/ ./server/

# Copy frontend build output
COPY --from=frontend-builder /app/client/dist ./static

# Copy entrypoint script
COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create data directory with proper permissions
RUN mkdir -p /app/data/uploads

# Expose port
EXPOSE 7895

# Environment variables
ENV DATA_DIR=/app/data \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1

# Data volume
VOLUME ["/app/data"]

# Health check (using curl instead of requests)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:7895/api/health || exit 1

# Start command
CMD ["/app/entrypoint.sh"]
