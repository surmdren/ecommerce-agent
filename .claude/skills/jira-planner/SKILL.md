---
name: jira-planner
description: 读取 dev-planner 生成的开发模块规划，自动转换为 Jira Epic 和 Tasks 层级结构。每个模块对应 Epic，每个开发步骤对应 Task，支持批量创建、自动关联 Epic、设置标签和优先级。适用于Jira任务规划、项目进度跟踪、团队协作管理。当用户提到"Jira"、"tickets"、"任务拆分"、"创建工单"、"Jira规划"时触发。
---

# Jira Tickets 规划器

## Overview

读取 dev-planner 生成的开发模块规划，自动转换为 Jira tickets，采用 **Epic → Task** 两层结构：

```
DevPlan 模块规划
├── 模块 01: 数据模型 → Epic
│   ├── Step 1: 定义 Schema → Task
│   ├── Step 2: 创建迁移 → Task
│   └── Step 3: 编写测试 → Task
├── 模块 02: 认证授权 → Epic
│   ├── Step 1: 实现注册 API → Task
│   └── Step 2: 实现登录 API → Task
└── 模块 03: 前端页面 → Epic
    └── Step 1: 登录页面 → Task
```

## Jira 层级结构

```
Epic (史诗) - 一个开发模块
  └─ Task (任务) - 一个开发步骤
```

## Parameters

| 参数 | 必填 | 描述 |
|------|------|------|
| `DevPlan 目录` | ✅ | dev-planner 生成的规划目录路径 |
| `项目 Key` | ✅ | Jira 项目 Key（如 YP2） |
| `邮箱` | ✅ | Jira 账户邮箱 |
| `创建方式` | ❌ | dry-run(预览)/api(通过 API 创建) |

## Instructions

你是一名【项目管理专家 + Jira 管理员】，拥有 10 年敏捷项目管理经验。

### 工作流程

#### Step 1: 读取开发模块规划

读取 `DevPlan/` 目录下的规划文档：

```bash
# 读取模块列表和依赖关系
read DevPlan/modules.md

# 读取每个模块的详细开发文档
read DevPlan/modules/01-数据模型.md
read DevPlan/modules/02-认证授权.md
read DevPlan/modules/03-前端页面.md
# ...
```

**模块文档结构：**
```markdown
# 01-数据模型

## 模块概述
- 类型: Backend
- 优先级: P0 (High)
- 预估工时: 16h

## 开发步骤

### Step 1: 设计数据库 Schema (4h)
- [ ] 定义 User 实体
- [ ] 定义 Session 实体
- [ ] 定义 Message 实体

### Step 2: 创建数据库迁移 (2h)
- [ ] 生成 Prisma 迁移文件
- [ ] 执行迁移

### Step 3: 实现 Repository (4h)
- [ ] 实现 User Repository
- [ ] 实现 Session Repository

### Step 4: 编写单元测试 (6h)
- [ ] Repository 单元测试
- [ ] 数据模型验证测试
```

#### Step 2: 分析模块并生成 Epic

根据 dev-planner 的模块列表，为每个模块创建一个 Epic：

| DevPlan 模块 | Epic 名称 | 标签 |
|-------------|----------|------|
| 01-数据模型 | Epic: 01-数据模型模块 | database, backend, foundation |
| 02-认证授权 | Epic: 02-认证授权模块 | auth, backend, security |
| 03-前端页面 | Epic: 03-前端页面模块 | frontend, ui, react |
| 04-基础设施 | Epic: 04-基础设施模块 | infrastructure, devops |

#### Step 3: 转换开发步骤为 Tasks

将每个模块的 Step 直接转换为 Task：

**模块 01-数据模型 → Epic**
```json
{
  "summary": "Epic: 01-数据模型模块",
  "issue_type": "Epic",
  "description": "实现数据库模型设计，包括 User、Session、Message 等核心实体的 Schema 定义和 Repository 实现",
  "priority": "High",
  "labels": ["database", "backend", "foundation"]
}
```

**Step 1 → Task**
```json
{
  "summary": "Task: 设计数据库 Schema (Prisma)",
  "issue_type": "Task",
  "description": "定义 User、Session、Message 等核心实体的 Prisma Schema，设计实体间关系和索引",
  "priority": "High",
  "labels": ["backend", "database", "prisma"],
  "estimate": "4h"
}
```

**Step 2 → Task**
```json
{
  "summary": "Task: 创建数据库迁移",
  "issue_type": "Task",
  "description": "生成 Prisma 迁移文件并执行数据库迁移",
  "priority": "High",
  "labels": ["backend", "database", "migration"],
  "estimate": "2h"
}
```

#### Step 4: 设置依赖关系

根据 dev-planner 的依赖关系设置 Jira 依赖：

**dev-planner 依赖：**
```markdown
## 依赖关系
- 02-认证授权 依赖 → 01-数据模型
- 03-前端页面 依赖 → 02-认证授权
```

**转换为 Jira 依赖：**
```json
{
  "update": {
    "issuelinks": [
      {
        "add": {
          "type": {"name": "Dependency"},
          "inwardIssue": {"key": "EPIC-001"},  // 01-数据模型
          "outwardIssue": {"key": "EPIC-002"}  // 02-认证授权
        }
      }
    ]
  }
}
```

#### Step 5: 生成 Tickets JSON

生成符合 API 脚本格式的 JSON：

```json
[
  {
    "summary": "Epic: 01-数据模型模块",
    "issue_type": "Epic",
    "description": "实现数据库模型设计...",
    "priority": "High",
    "labels": ["database", "backend", "foundation"]
  },
  {
    "summary": "Task: 设计数据库 Schema (Prisma)",
    "issue_type": "Task",
    "description": "定义 User、Session、Message 实体...",
    "priority": "High",
    "labels": ["backend", "database", "prisma"],
    "estimate": "4h"
  },
  {
    "summary": "Task: 创建数据库迁移",
    "issue_type": "Task",
    "description": "生成并执行 Prisma 迁移文件...",
    "priority": "High",
    "labels": ["backend", "database"],
    "estimate": "2h"
  },
  {
    "summary": "Epic: 02-认证授权模块",
    "issue_type": "Epic",
    "description": "实现用户认证和授权功能...",
    "priority": "High",
    "labels": ["auth", "backend", "security"]
  },
  {
    "summary": "Task: 实现用户注册 API",
    "issue_type": "Task",
    "description": "实现 POST /api/auth/register...",
    "priority": "High",
    "labels": ["backend", "api", "auth"],
    "estimate": "3h"
  }
]
```

#### Step 6: 通过 API 创建 Tickets

```bash
# 1. 生成 tickets.json 文件
# 2. 执行创建命令
python scripts/create_jira_ticket.py \
    --email user@example.com \
    --file tickets.json \
    --project YP2
```

#### Step 7: 生成规划报告

```markdown
# Jira Tickets 规划报告

## 概览
- 项目 Key: YP2
- Epic 数量: 4
- Task 数量: 28
- 总预估工时: 96h

## Epic 列表

| Epic Key | Epic 名称 | Task 数 | 总工时 | 标签 |
|----------|----------|--------|--------|------|
| EPIC-001 | 01-数据模型模块 | 4 | 16h | database, backend |
| EPIC-002 | 02-认证授权模块 | 6 | 24h | auth, backend |
| EPIC-003 | 03-前端页面模块 | 8 | 32h | frontend, ui |
| EPIC-004 | 04-基础设施模块 | 6 | 18h | infrastructure |

## 依赖关系

```
EPIC-002 (认证授权) 依赖 → EPIC-001 (数据模型)
EPIC-003 (前端页面) 依赖 → EPIC-002 (认证授权)
EPIC-004 (基础设施) 依赖 → EPIC-001, EPIC-002
```

## 下一步
1. 在 Jira Board 中查看创建的 Tickets
2. 按 Epic 分配给对应开发人员
3. 设置 Sprint 并开始迭代
```

## 层级映射

| DevPlan | Jira | 说明 |
|---------|------|------|
| 模块 (01-数据模型) | Epic | 一个模块对应一个 Epic |
| Step (Step 1: 数据层) | Task | 一个开发步骤对应一个 Task |
| 预估工时 | estimate | 直接使用 Step 的预估工时 |
| 优先级 (P0/P1/P2) | Priority | P0=High, P1=Medium, P2=Low |
| 模块类型 | Labels | Backend → backend, Frontend → frontend |

## 标签体系

| DevPlan 模块类型 | Epic 标签 | Task 标签 |
|-----------------|----------|----------|
| Backend | backend, foundation | backend, {具体领域} |
| Frontend | frontend, ui | frontend, react, ui |
| Infrastructure | infrastructure, devops | infrastructure, cicd |

**具体领域标签：**
- 数据库: database, prisma, postgresql
- 认证: auth, security, jwt
- API: api, rest, websocket
- 前端: react, typescript, tailwind
- 部署: cicd, kubernetes, deployment

## 优先级映射

| DevPlan | Jira |
|---------|------|
| P0 | Highest |
| P1 | High |
| P2 | Medium |
| P3 | Low |

## Output

### 目录结构

```
jira-plan/
├── tickets.json       # 所有 tickets JSON（用于 API 创建）
├── epics.md          # Epic 列表文档
├── tasks.md          # Task 列表文档
└── report.md         # 规划报告
```

### tickets.json 格式

```json
[
  {
    "summary": "Epic: {模块名称}",
    "issue_type": "Epic",
    "description": "{模块描述}",
    "priority": "High/Medium/Low",
    "labels": ["{标签1}", "{标签2}"]
  },
  {
    "summary": "Task: {Step 描述}",
    "issue_type": "Task",
    "description": "{Step 详细说明}",
    "priority": "High/Medium/Low",
    "labels": ["{标签1}", "{标签2}"],
    "estimate": "2h"
  }
]
```

## Examples

### 示例 1: 从 DevPlan 生成 Tickets

**用户输入:**
```
请根据 DevPlan 目录生成 Jira tickets
```

**执行流程:**
1. 读取 DevPlan/modules.md 获取模块列表
2. 读取每个模块的详细文档
3. 为每个模块生成 Epic
4. 将每个 Step 转换为 Task
5. 生成 tickets.json
6. 执行 API 创建脚本

### 示例 2: 预览模式

**用户输入:**
```
请生成 Jira tickets 预览，不要实际创建
```

**执行流程:**
1. 读取 DevPlan 目录
2. 生成 tickets.json
3. 生成预览报告
4. 跳过 API 创建

### 示例 3: 直接创建

**用户输入:**
```
请根据 DevPlan 创建 Jira tickets 到 YP2 项目
邮箱: madongchn@gmail.com
```

**执行流程:**
1. 读取 DevPlan 目录
2. 生成 tickets.json
3. 调用创建脚本
4. 返回创建的 ticket keys

## 最佳实践

1. **Epic 规模**: 一个 Epic 对应 dev-planner 的一个模块
2. **Task 粒度**: 每个 Task 对应一个 Step，应该可独立完成
3. **依赖清晰**: 直接使用 dev-planner 的依赖关系
4. **工时估算**: 使用 Step 中已定义的预估工时
5. **标签一致**: 根据模块类型自动添加标签

## 与现有工具集成

- **dev-planner**: 读取开发模块规划作为输入（主要来源）
- **tech-solution**: 可选，如果 dev-planner 不存在可直接从技术方案生成
- **dev-executor**: 生成的 tickets 可被 dev-executor 直接开发
- **create_jira_ticket.py**: 调用脚本批量创建
