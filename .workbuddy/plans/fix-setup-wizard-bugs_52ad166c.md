---
name: fix-setup-wizard-bugs
overview: 修复安装向导的 3 个 bug：1) test-db 的 pymysql ImportError 应返回友好提示而非报错；2) test-storage 对 local 类型不应触发 ImportError；3) finish 接口对 SQLite + local 组合抛异常导致无响应。
todos:
  - id: fix-backend-errors
    content: 修复 routes/setup.py 三个端点的异常处理：test-db/test-storage 区分 ImportError，finish 包裹 try-except
    status: completed
  - id: fix-frontend-catch
    content: 修复 SetupView.vue 三个 handler 添加 catch 块，HTTP 错误不再静默失败
    status: completed
    dependencies:
      - fix-backend-errors
  - id: rebuild-and-verify
    content: 重新构建镜像并启动容器验证三个 Bug 已修复
    status: completed
    dependencies:
      - fix-backend-errors
      - fix-frontend-catch
---

## 用户需求

修复安装向导的三个 Bug：

1. **数据库测试连接报错**：选择 MySQL 测试时容器内没有 pymysql，报 `No module named 'pymysql'`
2. **存储测试报错**：选择非 local 存储类型（MinIO/OSS/COS）测试时报 `缺少对应的存储 SDK`
3. **完成安装没反应**：选 SQLite + local 存储后点"完成安装"按钮无任何响应，页面无提示

## 根因分析

### Bug 1: pymysql ImportError

`routes/setup.py` 第 104 行 `test-db` 端点对 MySQL 分支直接构建 `mysql+pymysql://` URL 然后 `create_engine`，SQLAlchemy 尝试 `import pymysql` 失败。异常被第 115 行通用 `except Exception` 捕获返回了不友好的 ImportError 信息。

### Bug 2: 存储 SDK ImportError

`routes/setup.py` 第 127-171 行 `test-storage` 端点对 minio/oss2/cos-sdk 直接 import，`except ImportError` 第 174 行返回了通用提示。这本身是预期行为，但提示不够具体。

### Bug 3: 完成安装无响应（核心 Bug）

前端 `handleFinish()` 只有 `try/finally` 没有 `catch`，当 `finishSetup()` 抛出 HTTP 错误时（axios 对非 2xx 响应抛异常），异常未被捕获，`finishing` 被重置为 false，用户看不到任何反馈。

后端根因：`finish` 端点（setup.py 第 246 行）调用 `await storage.ensure_bucket()` 后返回成功，但 FastAPI 对 async generator 的 lifespan 机制导致 `finish` 端点内 `reset_db_engine()` 重置了 `_engine`，之后 `init_db()` 重新创建 engine，但 **lifespan 中持有的旧 storage 引用仍指向旧的 settings**。不过更关键的是：前端 `finishSetup` 在收到 500 时直接抛异常，没有 catch。

## 技术方案

### 修复策略

**Bug 1 & Bug 2**：优化后端 ImportError 的错误提示，分别处理 `test-db` 和 `test-storage` 的 ImportError，返回用户友好的中文提示。

**Bug 3（核心）**：两层修复：

1. 前端 `handleFinish()` 添加 `catch` 块，捕获 HTTP 异常并显示后端返回的错误信息
2. 前端 `finishSetup()` API 调用添加 axios 拦截或 try-catch，确保 4xx/5xx 错误不会静默失败
3. 后端 `finish` 端点添加顶层 try-except，确保任何异常都返回 `{"success": false, "message": "..."}` 而不是抛 500

### 实现细节

**server/routes/setup.py**：

- `test-db`：将 `except Exception` 拆分为 `except ImportError` + `except Exception`
- `test-storage`：ImportError 提示中说明缺少哪个 SDK 以及如何在 Docker 中安装
- `finish`：整体包裹 try-except，所有异常返回 `{"success": false, "message": str(e)}`

**client/src/views/SetupView.vue**：

- `handleFinish()` 添加 `catch (e: any)` 块
- `handleTestDb()` 和 `handleTestStorage()` 也添加 catch 防止静默失败
- catch 中从 `e.response?.data?.detail` 或 `e.message` 提取错误信息显示

### 目录结构

```
/Users/lwang/myproject/suisui/
├── server/
│   └── routes/setup.py       # [MODIFY] 三端点异常处理优化
├── client/
│   └── src/views/SetupView.vue  # [MODIFY] handleFinish/handleTestDb/handleTestStorage 添加 catch
```