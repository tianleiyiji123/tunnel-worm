---
name: setup-wizard-ux-polish
overview: 优化安装向导 UX：SQLite 也显示测试按钮，已初始化后禁止访问 /setup 页面（重定向到首页）
design:
  architecture:
    framework: vue
  styleKeywords:
    - Minimal
    - Interactive
todos:
  - id: fix-setup-test-btn
    content: SetupView.vue 去掉 SQLite 的 v-if 限制，handleTestDb 支持动态 db_type
    status: completed
  - id: fix-router-guard
    content: router/index.ts 去掉 skipInitCheck，守卫中已初始化访问 /setup 时重定向到首页
    status: completed
  - id: rebuild-and-verify
    content: 重新构建镜像并启动容器验证修改效果
    status: completed
    dependencies:
      - fix-setup-test-btn
      - fix-router-guard
---

## 用户需求

完善安装向导的交互流程，确保：

1. **每一步测试连接都有明确的成功/失败提示** - 当前 SQLite 选项下测试连接按钮被隐藏（`v-if="dbType === 'mysql'"`），需要 SQLite 也显示测试按钮并给出提示
2. **完成安装后给出提示并跳转到首页** - 已实现（ElMessage.success + 2s 跳转），无需修改
3. **初始化完成后禁止访问 /setup 页面** - 当前路由守卫 `skipInitCheck: true` 导致已初始化用户仍可访问 /setup，需要在路由守卫中增加反向拦截

## 核心要点

- SQLite 测试按钮：后端已支持 `db_type: sqlite` 的 test-db 请求，前端只需去掉 v-if 限制并调整 handler
- 路由守卫：去掉 `skipInitCheck`，改为在守卫中统一判断：未初始化 → /setup，已初始化且目标 /setup → /

## 修改方案

### 1. SetupView.vue - SQLite 显示测试连接按钮

**当前问题**：

- 模板第 92 行 `v-if="dbType === 'mysql'"` 隐藏了 SQLite 下的测试按钮
- 脚本第 326 行 `if (dbType.value !== 'mysql') return` 跳过 SQLite 测试

**修改**：

- 去掉按钮的 `v-if="dbType === 'mysql'"`，改为始终显示测试按钮
- `handleTestDb()` 根据 `dbType.value` 动态传参，SQLite 传 `{ db_type: 'sqlite' }`，MySQL 传完整表单
- 后端 test-db 端点已支持 sqlite 分支（第 92-102 行），无需修改

### 2. router/index.ts - 路由守卫反向拦截

**当前问题**：

- `/setup` 路由有 `meta: { skipInitCheck: true }`，守卫第 31 行直接 `next()` 放行
- 已初始化用户访问 `/setup` 不会被拦截

**修改**：

- 去掉 setup 路由的 `meta: { skipInitCheck: true }`
- 路由守卫统一逻辑：
- 先查询 `_initialized` 状态（带缓存）
- 目标是 `/setup` 且已初始化 → `next({ name: 'send' })`
- 目标非 `/setup` 且未初始化 → `next({ name: 'setup' })`
- 其他情况正常放行

### 目录结构

```
/Users/lwang/myproject/suisui/
├── client/src/views/SetupView.vue   # [MODIFY] 去掉 v-if 限制，handleTestDb 支持 SQLite
├── client/src/router/index.ts       # [MODIFY] 路由守卫增加已初始化时拦截 /setup
```

无需设计变更，仅修改已有交互逻辑。保留现有品牌配色（#2D6A4F 绿色系）和 Element Plus 组件风格。