# Jira Planner

根据完整技术方案自动生成 Jira Epic 和 Tasks 层级结构。

## 功能特性

- 自动从技术方案识别模块（后端/前端/基础设施）
- 生成 Epic → Task 两层结构
- 自动设置标签（backend/frontend/database/api 等）
- 支持批量创建到 Jira
- 生成规划报告

## 快速开始

### 1. 准备技术方案

提供一个包含技术栈和模块划分的方案：

```
# 聊天应用技术方案

## 后端模块
- Node.js + Express + Prisma + PostgreSQL
- RESTful API + WebSocket
- JWT 认证

## 前端模块
- React + TypeScript + Tailwind
- Zustand 状态管理

## 基础设施
- Vercel + Railway 部署
- GitHub Actions CI/CD
```

### 2. 调用 Skill

```bash
/jira-planner 请根据上述技术方案生成 Jira tickets
```

### 3. 创建 Tickets

```bash
python scripts/create_jira_ticket.py \
    --email your@email.com \
    --file tickets.json \
    --project YP2
```

## 层级结构

采用 **Epic → Task** 两层结构，适合中小型团队：

```
Epic: 后端基础架构
├── Task: 设计数据库 Schema (Prisma)
├── Task: 实现 User Repository
├── Task: 实现用户注册 API
└── Task: 编写后端单元测试

Epic: 前端用户界面
├── Task: 配置 React 项目环境
├── Task: 实现登录页面
└── Task: 开发消息列表组件

Epic: 基础设施与部署
├── Task: 配置 GitHub Actions CI/CD
└── Task: 部署后端到 Railway
```

## 标签体系

| 标签 | 用途 |
|------|------|
| `backend` | 后端任务 |
| `frontend` | 前端任务 |
| `database` | 数据库相关 |
| `api` | API 开发 |
| `auth` | 认证授权 |
| `infrastructure` | 基础设施 |
| `deployment` | 部署配置 |
| `test` | 测试相关 |

## 输出文件

```
jira-plan/
├── tickets.json    # 批量创建用 JSON
├── epics.md       # Epic 列表
├── tasks.md       # Task 列表
└── report.md      # 规划报告
```

## 与其他 Skill 配合

- **tech-solution**: 生成完整技术方案 → 输入到 jira-planner
- **dev-planner**: 进一步拆分任务为开发步骤
