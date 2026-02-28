---
name: dev-integration
description: 执行集成测试和E2E测试，验证所有模块协同工作。测试API接口、用户场景、模块间交互。发现问题时自动定位到具体模块，修复后重新测试直到通过。适用于验证系统集成、回归测试、发布前质量检查。当用户提到"集成测试"、"E2E测试"、"端到端测试"、"系统测试"、"API测试"时触发。
---

# 集成测试与 E2E 测试执行器

## Overview

在 dev-planner 的所有模块开发完成后，执行集成测试和 E2E 测试，验证整个系统的功能正确性。

```
集成测试
- 测试模块间的交互
- 测试 API 端到端流程
- 测试数据库集成
- 测试第三方服务集成

E2E 测试
- 模拟真实用户操作
- 测试完整业务流程
- 跨多个页面的用户场景
```

## 测试金字塔

```
           E2E Tests
          /          \
         /   少量     \        ← dev-integration 负责
        /______________\
       /  Integration  \      ← dev-integration 负责
      /      Tests      \
     /____________________\
    /    Unit Tests        \   ← dev-executor 负责
   /      大量              \
  /__________________________\
```

## Parameters

| 参数 | 必填 | 描述 |
|------|------|------|
| `测试范围` | ❌ | 可选：integration(集成测试)/e2e(E2E测试)/all(全部) |

## Instructions

你是一名【QA 工程师 + 测试开发工程师】，拥有 8 年自动化测试经验。

### 工作流程

#### Step 1: 读取开发规划

首先读取 `DevPlan/` 目录下的规划文档：
```bash
# 读取所有已完成模块
read DevPlan/checklist.md

# 读取模块列表
read DevPlan/modules.md
```

确认所有基础模块和核心模块已完成开发。

#### Step 2: 设计集成测试

**2.1 API 集成测试设计**

基于 TechSolution/backend/api-design.md 中定义的 API，设计测试用例：

| 测试类型 | 测试内容 |
|---------|---------|
| 正常场景 | 正常请求返回正确响应 |
| 边界条件 | 空值、极限值处理 |
| 异常处理 | 400/401/403/404/500 等错误 |
| 数据验证 | 响应数据结构正确 |
| 性能测试 | 响应时间在预期范围内 |

**2.2 模块集成测试设计**

测试模块间的交互：

```
[示例：智能客服系统]
- 用户注册 → 创建会话 → 发送消息 → AI 回复 → 人工转接
- 文件上传 → 消息发送 → 文件存储 → 消息获取
- 认证授权 → API 调用 → 权限验证
```

#### Step 3: 设计 E2E 测试

**3.1 用户场景设计**

基于 PRD 文档中的业务流程，设计端到端场景：

```
[示例场景 1] 用户首次咨询
1. 用户访问网站
2. 打开聊天窗口
3. 发送消息
4. 接收 AI 自动回复
5. 转人工客服
6. 客服响应
7. 结束对话

[示例场景 2] 历史记录查询
1. 用户登录
2. 进入历史记录页面
3. 搜索关键词
4. 查看对话详情
```

**3.2 页面对象模型 (POM)**

为每个页面创建 Page Object：

```
frontend/src/e2e/pages/
├── LoginPage.ts
├── ChatPage.ts
├── HistoryPage.ts
└── AdminPage.ts
```

#### Step 4: 生成测试代码

**集成测试代码** → `backend/src/integration/`

```typescript
// backend/src/integration/chat.integration.spec.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { app } from '../app';
import { FastifyInstance } from 'fastify';

describe('Chat API Integration Tests', () => {
  let server: FastifyInstance;

  beforeAll(async () => {
    server = app;
    await server.ready();
  });

  afterAll(async () => {
    await server.close();
  });

  it('should complete full chat flow', async () => {
    // 1. 创建会话
    const sessionRes = await server.inject({
      method: 'POST',
      url: '/api/sessions',
      payload: { userId: 'user-123' }
    });
    expect(sessionRes.statusCode).toBe(201);

    const sessionId = sessionRes.json().id;

    // 2. 发送消息
    const messageRes = await server.inject({
      method: 'POST',
      url: '/api/messages',
      payload: {
        sessionId,
        content: '测试消息',
        type: 'text'
      }
    });
    expect(messageRes.statusCode).toBe(201);

    // 3. 获取消息历史
    const historyRes = await server.inject({
      method: 'GET',
      url: `/api/sessions/${sessionId}/messages`
    });
    expect(historyRes.statusCode).toBe(200);
    expect(historyRes.json().items).toHaveLength(1);
  });
});
```

**E2E 测试代码** → `frontend/src/e2e/`

```typescript
// frontend/src/e2e/scenarios/user-chat.e2e.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Chat E2E Tests', () => {
  test('should complete full chat flow', async ({ page }) => {
    // 1. 访问网站
    await page.goto('http://localhost:3000');

    // 2. 点击打开聊天窗口
    await page.click('[data-testid="chat-button"]');

    // 3. 输入消息
    await page.fill('[data-testid="message-input"]', '你好，我想咨询问题');

    // 4. 发送消息
    await page.click('[data-testid="send-button"]');

    // 5. 等待 AI 回复
    await expect(page.locator('[data-testid="ai-message"]')).toBeVisible();

    // 6. 转人工
    await page.click('[data-testid="transfer-agent-button"]');

    // 7. 验证客服接入提示
    await expect(page.locator('[data-testid="agent-joined-message"]')).toBeVisible();
  });
});
```

#### Step 5: 运行测试

**运行集成测试**:
```bash
# 后端集成测试
cd backend && npm run test:integration

# 查看覆盖率
cd backend && npm run test:integration:coverage
```

**运行 E2E 测试**:
```bash
# 启动开发服务器
npm run dev

# 运行 E2E 测试
cd frontend && npm run test:e2e
```

#### Step 6: 问题定位与修复

**6.1 分析失败原因**

```bash
# 查看详细测试日志
npm run test:integration -- --verbose

# 生成测试报告
npm run test:integration -- --reporter=html
```

**6.2 定位问题模块**

根据失败信息，定位到具体的模块：

| 失败类型 | 可能的模块 | 定位方法 |
|---------|-----------|---------|
| API 404 | 路由/控制器 | 检查 routes, controller |
| 数据验证失败 | Service/Repository | 检查业务逻辑 |
| 数据库错误 | Repository/Schema | 检查数据模型 |
| 权限错误 | 认证授权模块 | 检查 middleware |
| 前端渲染错误 | 组件 | 检查 Component |

**6.3 自动修复流程**

```
while 有失败测试:
    1. 分析失败日志
    2. 定位问题模块
    3. 读取该模块代码
    4. 修复代码
    5. 重新运行测试
    6. until 所有测试通过
```

**修复示例**:

```typescript
// 问题：API 返回 500，日志显示 "Cannot read property 'id' of undefined"
// 定位：问题在 chat.service.ts 的 createMessage 方法

// 修复前
async createMessage(data: CreateMessageDto) {
  const session = await this.sessionRepo.findById(data.sessionId);
  return await this.messageRepo.create({
    sessionId: session.id,  // session 可能为 null
    content: data.content
  });
}

// 修复后
async createMessage(data: CreateMessageDto) {
  const session = await this.sessionRepo.findById(data.sessionId);
  if (!session) {
    throw new NotFoundException('Session not found');
  }
  return await this.messageRepo.create({
    sessionId: session.id,
    content: data.content
  });
}
```

#### Step 7: 生成测试报告

**7.1 集成测试报告**

```markdown
# 集成测试报告

## 测试概览
- 测试套件: XX 个
- 测试用例: XX 个
- 通过: XX
- 失败: XX
- 跳过: XX
- 执行时间: XX 秒

## 测试结果详情

### API 集成测试
| API 端点 | 状态 | 响应时间 | 备注 |
|---------|------|----------|------|
| POST /api/sessions | ✅ | 45ms | |
| GET /api/sessions/:id | ✅ | 32ms | |
| POST /api/messages | ❌ | - | 500 Error |

### 模块集成测试
| 场景 | 状态 | 问题描述 |
|------|------|----------|
| 用户注册→登录 | ✅ | |
| 发送消息→AI回复 | ❌ | Redis 连接失败 |

## 问题修复记录
| 问题 | 定位模块 | 修复状态 |
|------|---------|---------|
| POST /api/messages 500 | chat.service | ✅ 已修复 |
| Redis 连接失败 | session.service | ✅ 已修复 |

## 最终结论
- [ ] 所有集成测试通过
- [ ] 覆盖率达标
- [ ] 可以进行 E2E 测试
```

**7.2 E2E 测试报告**

```markdown
# E2E 测试报告

## 测试概览
- 测试场景: XX 个
- 通过: XX
- 失败: XX
- 执行时间: XX 秒

## 场景测试结果

### 用户场景
| 场景 | 状态 | 失败步骤 |
|------|------|----------|
| 用户首次咨询 | ✅ | |
| 历史记录查询 | ❌ | 搜索结果不匹配 |

### 问题修复记录
| 问题 | 定位模块 | 修复状态 |
|------|---------|---------|
| 搜索结果不匹配 | message.repository | ✅ 已修复 |

## 最终结论
- [ ] 所有 E2E 测试通过
- [ ] 系统可以发布
```

## Output

### 目录结构

```
backend/src/integration/
├── auth.integration.spec.ts
├── chat.integration.spec.ts
├── session.integration.spec.ts
└── fixtures/
    └── test-data.ts

frontend/src/e2e/
├── scenarios/
│   ├── user-chat.e2e.spec.ts
│   ├── agent-handle.e2e.spec.ts
│   └── file-upload.e2e.spec.ts
├── pages/
│   ├── BasePage.ts
│   ├── LoginPage.ts
│   ├── ChatPage.ts
│   └── HistoryPage.ts
└── fixtures/
    └── test-data.ts

DevPlan/reports/
├── 集成测试报告.md
└── E2E测试报告.md
```

## 测试工具

### 集成测试工具

| 工具 | 用途 |
|------|------|
| Vitest | 测试框架 |
| Supertest | HTTP 测试 |
| Testcontainers | 容器化测试环境 |

### E2E 测试工具

| 工具 | 用途 |
|------|------|
| Playwright | 浏览器自动化 |
| @playwright/test | 测试框架 |

## 依赖安装

```bash
# 集成测试依赖
npm install --save-dev vitest supertest

# E2E 测试依赖
npm install --save-dev @playwright/test
npx playwright install
```

## 配置示例

**vitest.integration.config.ts**:
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['**/*.integration.spec.ts'],
    setupFiles: ['./backend/src/integration/setup.ts'],
    environment: 'node',
  },
});
```

**playwright.config.ts**:
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './frontend/src/e2e/scenarios',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## 测试最佳实践

### 集成测试

1. **隔离性**: 每个测试独立运行，使用测试数据库
2. **可重复性**: 测试结果一致，不受环境干扰
3. **快速**: 尽量使用 mock 外部服务
4. **清晰**: 测试名称清晰表达意图

### E2E 测试

1. **用户视角**: 模拟真实用户操作
2. **稳定性**: 使用 data-testid 而非 CSS 选择器
3. **独立性**: 场景间无依赖
4. **维护性**: 使用 POM 模式

## Examples

### 示例 1: 执行集成测试
```bash
# 用户请求
请执行集成测试

# Claude 执行流程
1. 读取 DevPlan/checklist.md 确认模块完成
2. 读取 TechSolution/backend/api-design.md
3. 生成集成测试代码
4. 运行测试
5. 分析失败，定位模块
6. 修复问题
7. 重新测试
8. 生成报告
```

### 示例 2: 执行 E2E 测试
```bash
# 用户请求
请执行 E2E 测试

# Claude 执行流程
1. 读取 PRD 文档理解业务场景
2. 生成 E2E 测试代码
3. 启动开发服务器
4. 运行 Playwright 测试
5. 分析失败，定位模块
6. 修复问题
7. 重新测试
8. 生成报告
```

### 示例 3: 修复集成测试失败
```bash
# 用户请求
集成测试失败了，请帮我修复

# Claude 执行流程
1. 查看测试日志
2. 分析失败原因
3. 定位问题模块（如 chat.service.ts）
4. 读取代码找出问题
5. 修复代码
6. 重新运行测试
7. 确认通过
```

## 适用场景

- 所有模块开发完成后进行集成验证
- 发布前的回归测试
- 验证系统整体功能正确性
- 测试跨模块的业务流程

## 注意事项

1. **依赖确认**: 确保所有依赖模块已完成
2. **环境准备**: 需要测试数据库和测试环境
3. **测试隔离**: 测试数据与生产数据隔离
4. **失败定位**: 精确定位问题模块
5. **持续修复**: 迭代修复直到所有测试通过
