---
name: docker-env-optimize
overview: 优化 Docker 部署的 .env 模板和文档，确保存储配置的一致性和易用性。
todos:
  - id: fix-env-example
    content: 重构 .env.example 为 Docker-first 模板，DB_HOST 改 db，MinIO 凭证改为注释示例
    status: completed
  - id: fix-compose-minio
    content: 调整 docker-compose.yml MinIO 服务环境变量，去掉 :-minioadmin 默认值
    status: completed
    dependencies:
      - fix-env-example
  - id: update-readme
    content: README.md 补充 Docker 存储配置操作指引和各后端最小配置示例
    status: completed
    dependencies:
      - fix-env-example
  - id: update-memory
    content: 同步更新 MEMORY.md 中的存储配置说明
    status: completed
---

## 用户需求

优化 Docker 部署时存储配置的用户体验，让用户只需编辑 `.env` 文件即可配置存储后端，确保模板、文档、Docker 配置三者一致。

## 现存问题

1. `.env.example` 中 MinIO 凭证仍写着 `minioadmin` 默认值，但 `config.py` 已改为空字符串（自动检测依赖空字符串判断是否配置），两者不一致会导致 Docker 部署时 MinIO 被意外自动启用
2. `.env.example` 中 `DB_HOST=localhost`，但 Docker 环境中应为 `DB_HOST=db`（MySQL 容器名），用户直接 `cp .env.example .env` 后数据库连不上
3. `docker-compose.yml` 中 MinIO 服务引用 `${MINIO_ACCESS_KEY:-minioadmin}`，与 config.py 空字符串默认值矛盾
4. README 的 Docker 部署章节缺少存储配置的具体操作指引，用户不知道如何从默认 local 切换到三方存储
5. MEMORY.md 中仍写着"设置 `STORAGE_TYPE=minio`"，与新自动检测逻辑不一致

## 核心功能

- `.env.example` 作为 Docker 部署的标准化模板，注释清晰，直接复制即可用
- 各存储后端示例值明确标注占位性质（`your_xxx` 或注释掉），不会误触发自动检测
- README 提供完整的 Docker 存储配置操作指引

## 技术方案

### 修改范围

仅涉及配置文件和文档，不涉及业务逻辑代码。

### 关键改动点

#### 1. `.env.example` — 重新设计为 Docker-first 模板

- `DB_HOST` 默认值改为 `db`（Docker MySQL 容器名），与 docker-compose.yml 一致
- MinIO 凭证值改为注释状态（带示例值），避免误触发自动检测
- 三方存储凭证保持 `your_xxx` 占位值不变（已经是空字符串等价的占位）
- 增加分组注释：`[必需]`、`[可选-本地存储]`、`[可选-MinIO]`、`[可选-阿里云OSS]`、`[可选-腾讯云COS]`，让用户一目了然
- 顶部增加简短说明：默认使用本地存储，取消注释对应区块即可启用

#### 2. `docker-compose.yml` — MinIO 服务环境变量调整

- `MINIO_ROOT_USER` 改为 `${MINIO_ACCESS_KEY}`（去掉 `:-minioadmin` 默认值），与 config.py 空字符串策略一致
- `MINIO_ROOT_PASSWORD` 同理去掉默认值
- 这样 MinIO profile 只有在用户显式配置了凭证后才能正常启动，逻辑闭环

#### 3. `README.md` — Docker 存储配置指引

- 在 Docker Compose 部署章节补充"配置存储后端"子章节
- 提供每种存储后端的最小 `.env` 配置示例
- 说明自动检测机制和手动覆盖方式
- 更新 MinIO 使用说明（不再需要 `STORAGE_TYPE=minio`）

#### 4. `.workbuddy/memory/MEMORY.md` — 同步更新

- 移除 `STORAGE_TYPE=minio` 的描述，改为自动检测说明

### 文件清单

```
/Users/lwang/myproject/suisui/
├── .env.example                       # [MODIFY] Docker-first 模板，分组注释
├── docker-compose.yml                 # [MODIFY] MinIO 环境变量去掉默认值
├── README.md                          # [MODIFY] 补充 Docker 存储配置指引
└── .workbuddy/memory/MEMORY.md        # [MODIFY] 同步更新记忆
```

### 实现说明

- 不改 config.py、storage/**init**.py、main.py（上次已完成自动检测逻辑）
- 不改 Dockerfile、entrypoint.sh、nginx.conf（与存储配置无关）
- 不改前端代码
- 改动量小，每个文件 5-20 行调整