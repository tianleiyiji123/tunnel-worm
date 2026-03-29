---
name: storage-auto-detect
overview: 将存储后端选择逻辑从手动设置 `STORAGE_TYPE` 改为自动检测：优先级 MinIO > 阿里云OSS > 腾讯云COS > 本地存储，根据凭证是否已配置自动选择，同时保留 `STORAGE_TYPE` 手动覆盖能力。
todos:
  - id: auto-detect-storage
    content: 修改 config.py（MinIO 默认值改空）、storage/__init__.py（自动检测+懒加载）、main.py（日志）、.env.example 和 README.md（文档更新）
    status: completed
---

## Product Overview

当前隧隧虫项目的存储后端选择依赖手动设置 `STORAGE_TYPE` 环境变量。用户希望改为自动检测逻辑：如果配置了第三方存储凭证就自动使用对应三方后端，如果没有配置则默认使用本地磁盘存储。同时保留 `STORAGE_TYPE` 手动覆盖能力。

## Core Features

- 自动检测存储后端：按优先级依次检查阿里云 OSS、腾讯云 COS、MinIO 的凭证是否已配置（所有必需字段非空），已配置则自动选用
- 未配置任何三方存储时，自动回退到本地磁盘存储（`./uploads/`）
- 保留 `STORAGE_TYPE` 手动指定能力：如果用户显式设置了 `STORAGE_TYPE`，则优先使用手动值
- MinIO 默认凭证改为空字符串，与三方存储保持一致，确保自动检测准确
- 三方存储 SDK 改为懒加载导入，避免未安装时启动报错
- 启动日志输出当前使用的存储后端类型

## Tech Stack

- Python + FastAPI（后端）
- pydantic-settings（配置管理）

## Implementation Approach

### 整体策略

修改存储工厂函数 `get_storage()` 为自动检测模式，同时保持向后兼容。优先级：`STORAGE_TYPE` 手动指定 > 自动检测三方凭证 > 默认 local。

### 关键技术决策

1. **MinIO 默认值修正**：将 `config.py` 中 MinIO 的 `ENDPOINT`、`ACCESS_KEY`、`SECRET_KEY`、`BUCKET` 默认值全部改为空字符串，使自动检测能准确区分"用户已配置"和"未配置"。使用 MinIO 的用户必须在 `.env` 中填写这些值。

2. **自动检测逻辑**：在 `get_storage()` 中，先检查 `STORAGE_TYPE` 是否非 `"local"`（手动覆盖）；否则依次检测三方凭证完整性：

- 阿里云 OSS：`ALIOSS_ACCESS_KEY_ID` + `ALIOSS_ACCESS_KEY_SECRET` + `ALIOSS_BUCKET` + `ALIOSS_ENDPOINT` 全非空
- 腾讯云 COS：`TENCENTCOS_SECRET_ID` + `TENCENTCOS_SECRET_KEY` + `TENCENTCOS_BUCKET` + `TENCENTCOS_REGION` 全非空
- MinIO：`MINIO_ENDPOINT` + `MINIO_ACCESS_KEY` + `MINIO_SECRET_KEY` + `MINIO_BUCKET` 全非空
- 都未配置：回退 `LocalStorage()`

3. **懒加载导入**：三方存储的 import 放在工厂函数内部，避免未安装 SDK 时导致 `ImportError`。启动时只在确定了存储类型后才导入对应的模块。

## Directory Structure

```
/Users/lwang/myproject/suisui/
├── server/
│   ├── config.py                      # [MODIFY] MinIO 默认值改为空字符串
│   ├── main.py                        # [MODIFY] 启动日志增加存储后端类型输出
│   └── services/storage/
│       └── __init__.py                # [MODIFY] 工厂函数改为自动检测 + 懒加载导入
├── .env.example                       # [MODIFY] 更新注释说明自动检测逻辑，移除 MinIO 默认值
└── README.md                          # [MODIFY] 更新存储配置说明
```

## Implementation Notes

- 只改 4 个文件，每个文件改动量极小（10-30 行）
- 不改变任何已有的存储后端实现代码（base.py、local.py、minio_backend.py、alioss.py、tencentcos.py 均不动）
- 不改变 API 接口、前端代码、Docker 配置
- 检测函数应输出日志方便排查，如 `print("📦 Storage backend: alioss (auto-detected)")`