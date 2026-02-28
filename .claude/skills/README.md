# My Claude Skills

一组自定义的 Claude Code Skills，用于产品需求分析和方案输出。

## 快速开始

```bash
# 克隆仓库
git clone <repo-url> my-skills
cd my-skills

# 启动 Claude Code
claude

# 查看可用命令
/help
```

## Skills 列表

本项目包含 **27 个 Skills**，覆盖完整 SDLC 流程：

### 0. 前期准备（可选）
| Skill | 描述 |
|-------|------|
| [market-research](#market-research) | 行业资料 → 市场研究报告 + 赚钱机会 |
| [competitor-analysis](#competitor-analysis) | 竞品分析 → 超越策略 |
| [industry-sales-prep](#industry-sales-prep) | 产品文档 → 行业知识库 + 销售话术 |
| [go-to-market](#go-to-market) | 市场研究 → GTM执行计划（渠道+预算+时间线） |

### 1. 需求阶段
| Skill | 描述 |
|-------|------|
| [requirement-detail](#requirement-detail) | 需求概述 → PRD 文档 |

### 2. 设计阶段
| Skill | 描述 |
|-------|------|
| [compliance-check](#compliance-check) | 技术方案 → 法律合规评估文档 |
| [tech-architecture](#tech-architecture) | 业务需求 → 技术架构图（6张Mermaid） |
| [tech-solution](#tech-solution) | 业务需求 → 完整技术方案（前端+后端+云） |
| [uiux-design](#uiux-design) | 业务需求 → UIUX 设计文档 |

### 3. 规划阶段
| Skill | 描述 |
|-------|------|
| [dev-planner](#dev-planner) | PRD + 技术方案 → 开发模块规划 |
| [jira-planner](#jira-planner) | 开发模块规划 → Jira Tickets (Epic/Task) |

### 4. 基础设施准备
| Skill | 描述 |
|-------|------|
| [infrastructure-provisioner](#infrastructure-provisioner) | 技术方案 → K8s/Terraform配置 + 环境变量 |

### 5. 开发阶段
| Skill | 描述 |
|-------|------|
| [code-arch-analyzer](#code-arch-analyzer) | 现有代码 → 架构分析文档 |
| [dev-executor](#dev-executor) | 模块/Ticket → 编码 → 单元测试 → 调试 → 写回 Jira |

### 6. 测试阶段
| Skill | 描述 |
|-------|------|
| [testing-strategy](#testing-strategy) | 项目代码 → 测试策略 + 测试计划 |
| [unit-test-generator](#unit-test-generator) | 代码 → 单元测试（允许Mock） |
| [api-test-generator](#api-test-generator) | API代码 → API单端点测试（禁止Mock） |
| [integration-test-generator](#integration-test-generator) | API代码 → 业务场景测试（禁止Mock） |
| [e2e-test-generator](#e2e-test-generator) | 应用 → E2E测试（1-2条关键流程） |
| [dev-integration](#dev-integration) | 集成测试 + E2E 测试 → 定位问题 → 修复 → 验证 |

### 7. 部署阶段
| Skill | 描述 |
|-------|------|
| [dev-deploy](#dev-deploy) | 构建镜像 → 推送仓库 → K8s 部署 → 验证 → 报告 |
| [changelog](#changelog) | Git 提交 → 版本号计算 → CHANGELOG.md → 发布说明 |

### 8. 文档阶段
| Skill | 描述 |
|-------|------|
| [api-docs](#api-docs) | 扫描代码 → OpenAPI 规范 → 交互式文档 → SDK |
| [prd-to-ppt](#prd-to-ppt) | PRD 文档 → PPT 方案 |

### 9. 辅助工具
| Skill | 描述 |
|-------|------|
| [save-context](#save-context) | 当前对话 → 上下文文件 |
| [load-context](#load-context) | 上下文文件 → 恢复对话 |
| [skill-creator](#skill-creator) | 创建或更新 Skill 的指南 |

## 推荐工作流

```
                                    ┌──→ /tech-architecture ──→ 技术架构图
                                    │
                                    ├──→ /tech-solution ──→ 技术方案（前端+后端+云）
需求概述 ──→ /requirement-detail ──→ PRD文档 ──┤
                                    ├──→ /uiux-design ──→ UIUX设计 ──→ UX Pilot
                                    │
                                    ├──→ /prd-to-ppt ──→ PPT方案
                                    │
                                    ├──→ /dev-planner ──→ 开发模块规划 ──┬─→ /jira-planner ──→ Jira Tickets
                                    │                                        │
                                    │                                        └─→ /dev-executor ──→ 编码 + 测试
                                    │                                                              │
                                    │                                                              └──→ /api-docs ──→ API 文档
                                    │
                                    ├──→ /dev-integration ──→ 集成测试 → E2E测试 → 修复
                                    │
                                    └──→ /dev-deploy ──→ 构建镜像 → K8s部署 → 验证
                                                │
                                                └──→ /changelog ──→ 版本发布 + CHANGELOG
```

## 输出目录结构

每个 skill 的输出文件都保存在各自的目录中：

```
项目根目录/
├── PRD/                    # /requirement-detail 输出
│   └── [项目名称]-PRD.md
│
├── Architecture/           # /tech-architecture 输出
│   ├── README.md
│   ├── Architecture.md
│   └── diagrams/*.mmd
│
├── TechSolution/           # /tech-solution 输出
│   ├── README.md
│   ├── frontend/           # 前端技术方案
│   ├── backend/            # 后端技术方案
│   └── infrastructure/     # 云基础设施方案
│
├── UIUX/                   # /uiux-design 输出
│   ├── README.md
│   ├── design-system.md
│   └── pages/*.md
│
└── PPT/                    # /prd-to-ppt 输出
    ├── [项目名称]-方案.pptx
    ├── [项目名称]-大纲.md
    └── thumbnails/

└── DevPlan/                # /dev-planner 输出
    ├── README.md           # 开发计划总览
    ├── modules.md          # 模块列表和依赖关系
    ├── checklist.md        # 开发进度检查清单
    ├── modules/
    │   ├── 01-模块名称.md   # 每个模块的详细开发文档
    │   ├── 02-模块名称.md
    │   └── ...
    └── jira/               # /jira-planner 输出
        ├── tickets.json    # 所有 tickets JSON（用于 API 创建）
        ├── epics.md        # Epic 列表
        ├── tasks.md        # Task 列表
        └── report.md       # 规划报告

└── DevPlan/Reports/         # 测试报告输出
    └── {模块名称}-测试报告.md           # /dev-executor 输出
    └── 集成测试报告.md                  # /dev-integration 输出
    └── E2E测试报告.md                    # /dev-integration 输出

└── backend/src/integration/ # /dev-integration 输出
└── frontend/src/e2e/        # /dev-integration 输出

└── infrastructure/k8s/      # /dev-deploy 输出
    ├── base/                # 基础 K8s 配置
    ├── overlays/            # 多环境配置
    └── scripts/             # 部署脚本

└── infrastructure/reports/  # /dev-deploy 输出
    └── deployment-{ENV}-{VERSION}.md

└── api-docs/                # /api-docs 输出
    ├── README.md            # 文档概览
    ├── openapi.yaml         # OpenAPI 规范
    ├── openapi.json         # OpenAPI JSON
    ├── index.html           # Swagger UI
    ├── redoc.html           # ReDoc
    ├── postman_collection.json
    └── sdk/                 # 客户端 SDK
        ├── typescript/
        └── python/

项目根目录/
└── CHANGELOG.md             # /changelog 输出
└── RELEASE_NOTES.md         # /changelog 输出
```

---

# Skills 详细说明

---

## requirement-detail

将碎片化的业务需求转化为专业的产品需求文档（PRD）。

### 用法

```bash
/requirement-detail <需求概述>
```

### 参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `需求概述` | string | ✅ | 业务需求的文字描述 |

### 示例

```bash
/requirement-detail 我们需要一个商品评价系统，支持买家上传图片和视频评价，卖家可以回复评价
```

### 输出

生成包含以下 8 个章节的 PRD 文档：

1. **项目背景与目标** - 核心痛点与业务价值
2. **目标用户与角色定义** - 买家/卖家/管理员权限
3. **业务范围说明（Scope）** - 功能边界定义
4. **核心业务流程** - 主路径 + 异常处理
5. **功能模块需求** - 模块/子功能/交互逻辑
6. **非功能性需求** - 性能/安全/扩展性
7. **风险与不确定性提示** - 风险评估与应对
8. **后续迭代建议** - MVP 与 Phase 2 规划

### 适用场景

- 产品经理整理初期业务想法
- 技术评审前的需求规范化
- B2B/B2C 电商平台功能需求分析

---

## tech-architecture

根据业务需求生成完整的技术架构方案和 Mermaid 架构图。

### 用法

```bash
/tech-architecture <业务需求描述>
```

### 参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `业务需求` | string | ✅ | 业务需求描述或 PRD 文档路径 |

### 示例

```bash
/tech-architecture 商品评价系统，支持买家发布图文评价、卖家回复、平台审核
```

### 输出

生成完整的架构目录：

```
architecture/
├── README.md                              # 架构目录入口
├── Architecture.md                        # 核心架构说明文档
└── diagrams/
    ├── 01-business-architecture.mmd       # 业务架构图
    ├── 02-technical-architecture.mmd      # 技术架构图
    ├── 03-system-architecture.mmd         # 系统架构图
    ├── 04-module-dependencies.mmd         # 模块依赖图
    ├── 05-data-flow.mmd                   # 数据流图
    └── 06-api-architecture.mmd            # API/能力架构图
```

**Architecture.md 包含**：

1. 架构背景与目标
2. 架构设计原则与约束
3. 业务架构说明
4. 系统架构说明
5. 技术架构说明
6. 模块拆分与职责边界
7. 核心数据流说明
8. API / 能力暴露方式
9. 关键架构决策记录（ADR）
10. 架构风险与假设
11. 架构演进方向

### 适用场景

- 架构评审会议
- ToB 项目技术方案交付
- CTO / 技术委员会决策支持
- 技术文档归档

---

## tech-solution

一站式生成完整技术方案，包含前端、后端、云基础设施三部分。

### 用法

```bash
/tech-solution <业务需求描述>
```

### 参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `业务需求` | string | ✅ | 业务需求描述或 PRD 文档路径 |
| `云平台` | string | ❌ | 默认 AWS，可指定"阿里云" |

### 示例

```bash
# 默认使用 AWS
/tech-solution 商品评价系统，支持图文评价、卖家回复，预计日活 1 万

# 指定阿里云
/tech-solution 商品评价系统，使用阿里云
```

### 输出

生成完整技术方案目录：

```
TechSolution/
├── README.md                     # 技术方案总览
├── frontend/
│   ├── tech-stack.md             # 前端技术选型
│   ├── project-structure.md      # 项目结构
│   └── dev-guide.md              # 开发规范
├── backend/
│   ├── tech-stack.md             # 后端技术选型
│   ├── project-structure.md      # 项目结构
│   ├── api-design.md             # API 设计规范
│   └── dev-guide.md              # 开发规范
└── infrastructure/
    ├── architecture.md           # 基础设施架构
    ├── kubernetes.md             # K8s 部署方案
    └── cost-estimate.md          # 成本估算
```

### 技术选型原则

**前端**（只选必要的）：
| 场景 | 推荐 |
|------|------|
| 通用 Web | React 18 + Vite + Tailwind |
| 需要 SEO | Next.js 14 |
| 轻量项目 | Vue 3 |

**后端**（只选一套）：
| 场景 | 推荐 |
|------|------|
| 快速开发 | Node.js + Express/Fastify |
| 企业级 | Java 17 + Spring Boot 3 |
| 高性能 | Go + Gin |

**数据库**：
| 类型 | 推荐 |
|------|------|
| 关系型 | PostgreSQL（首选）/ MySQL |
| 缓存 | Redis |
| 文件 | S3 / OSS |

**云基础设施**：
| AWS | 阿里云 |
|-----|--------|
| EKS | ACK |
| RDS | RDS |
| ElastiCache | Redis |
| S3 | OSS |
| CloudFront | CDN |

### 适用场景

- 新项目技术选型
- 技术方案评审
- 架构设计文档
- 云资源规划与成本估算

---

## uiux-design

根据业务需求生成 UIUX 设计文档，输出格式适配 UX Pilot 等 AI 设计工具。

### 用法

```bash
/uiux-design <业务需求描述>
```

### 参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `业务需求` | string | ✅ | 业务需求描述或 PRD 文档路径 |

### 示例

```bash
/uiux-design 商品评价系统：买家可以发布图文评价、查看评价列表、卖家可以回复评价
```

### 输出

生成完整的 UIUX 设计文档：

```
uiux-design/
├── README.md                    # 设计文档总览
├── design-system.md             # 设计系统规范
└── pages/
    ├── 01-评价列表页.md          # 每个页面独立文档
    ├── 02-发布评价页.md
    ├── 03-评价详情页.md
    └── 04-卖家回复页.md
```

**每个页面文档包含**：

| 内容 | 说明 |
|------|------|
| UX Pilot Prompt | 可直接复制到 UX Pilot 使用 |
| 页面信息 | 名称、路径、类型、权限 |
| 布局结构 | 页面布局描述 |
| 组件清单 | 组件类型、状态、交互说明 |
| 交互说明 | 用户操作与反馈 |
| 异常状态 | 空状态/加载/错误 |
| 响应式断点 | Desktop/Tablet/Mobile 适配 |

**design-system.md 包含**：

- 色彩系统（主色/辅助色/语义色）
- 字体系统（字号/字重规范）
- 间距系统（基于 8px 网格）
- 圆角/阴影规范
- 基础组件库定义

### 与 UX Pilot 配合使用

1. 运行 `/uiux-design` 生成设计文档
2. 打开页面文档，复制 "UX Pilot Prompt" 部分
3. 粘贴到 UX Pilot，生成设计图
4. 根据需要微调 prompt 或使用 follow-up 编辑

### 适用场景

- 产品设计文档输出
- AI 设计工具输入准备（UX Pilot / Figma AI）
- 设计师交接文档
- 前端开发设计参考

---

## prd-to-ppt

根据 PRD 或业务描述文档生成 PPT 演示方案。

### 用法

```bash
/prd-to-ppt <文档路径> [--style <图片>] [--slides <数量>] [--output <路径>]
```

### 参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `文档路径` | string | ✅ | PRD 或业务描述文档路径 |
| `--style` | string | ❌ | 风格参考图片（提取配色） |
| `--slides` | number | ❌ | PPT 页数，默认 8-12 页 |
| `--output` | string | ❌ | 输出文件路径，默认 `output.pptx` |

### 示例

```bash
# 基础用法
/prd-to-ppt ./docs/PRD.md

# 指定风格和页数
/prd-to-ppt ./docs/PRD.md --style ./brand/logo.png --slides 10

# 完整参数
/prd-to-ppt ./docs/PRD.md --style ./ref.png --slides 15 --output ./方案.pptx
```

### 输出

生成的 PPT 包含：

| 页面 | 内容 |
|------|------|
| 封面 | 项目名称、日期、团队 |
| 目录 | 章节导航 |
| 背景 | 痛点与业务价值 |
| 角色 | 用户角色定义 |
| 范围 | MVP vs Phase 2 |
| 流程 | 核心业务流程图 |
| 功能 | 功能模块架构 |
| 非功能 | 性能·安全·扩展 |
| 风险 | 风险与应对策略 |
| 计划 | 迭代路线图 |

### 依赖安装

生成实际 `.pptx` 文件需要安装：

```bash
pip install "markitdown[pptx]"
npm install -g pptxgenjs playwright sharp
```

### 适用场景

- 产品方案汇报
- 项目提案演示
- 业务需求评审会议

---

## dev-planner

根据业务需求文档和技术方案生成开发模块规划文档，然后按模块逐个开发。

### 用法

```bash
/dev-planner <PRD文档路径> <技术方案路径>
```

### 参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `PRD文档路径` | string | ✅ | 产品需求文档路径 |
| `技术方案路径` | string | ✅ | TechSolution/ 目录路径 |

### 示例

```bash
# 基础用法
/dev-planner PRD/智能客服系统-PRD.md TechSolution/

# 开发特定模块
/dev-planner develop 01
```

### 输出

生成完整的开发模块规划：

```
DevPlan/
├── README.md                    # 开发计划总览
├── modules.md                   # 模块列表和依赖关系图
├── checklist.md                 # 开发进度检查清单
└── modules/
    ├── 01-数据模型.md
    ├── 02-认证授权.md
    ├── 03-会话管理.md
    └── ...
```

**每个模块文档包含**：

| 内容 | 说明 |
|------|------|
| 模块概述 | 类型、优先级、预估工时 |
| 功能需求 | 用户故事、功能清单 |
| 技术实现 | 数据模型、API 设计、代码结构 |
| 测试方案 | 单元测试、集成测试 |
| 开发步骤 | 按 Step 拆解开发任务 |
| 验收标准 | 功能、质量、性能标准 |
| 依赖关系 | 前置依赖、被依赖模块 |

### 模块拆解原则

| 原则 | 说明 |
|------|------|
| 单一职责 | 每个模块只负责一个核心功能 |
| 高内聚低耦合 | 模块内部紧密相关，模块间最小依赖 |
| 可独立测试 | 每个 module 可独立运行和测试 |
| 依赖清晰 | 识别模块间依赖，基础模块优先 |
| 可增量交付 | 每个模块完成后都有价值 |

### 模块分类

```
【基础模块】(Foundation)
- 数据模型和数据库
- 认证授权
- 配置管理
- 日志系统

【核心模块】(Core)
- 会话管理
- 消息处理
- 实时通信
- 文件上传

【业务模块】(Business)
- AI 回复
- 客服分配
- 快捷回复
- 历史记录

【接口模块】(Interface)
- REST API
- WebSocket
- 前端组件
```

### 适用场景

- 新项目开发规划
- 功能模块拆解
- 敏捷开发迭代
- 技术债务重构

---

## jira-planner

读取 dev-planner 生成的开发模块规划，自动转换为 Jira Epic 和 Tasks 层级结构。

### 用法

```bash
# 从 DevPlan 目录生成 tickets
/jira-planner 请根据 DevPlan 目录生成 Jira tickets

# 预览模式（不实际创建）
/jira-planner 请根据 DevPlan 生成 Jira tickets 预览

# 创建到指定项目
/jira-planner 请根据 DevPlan 创建 Jira tickets 到 YP2 项目，邮箱 user@example.com
```

### Jira 层级结构

采用 **Epic → Task** 两层结构：

```
DevPlan 模块 → Epic
├── Step 1 → Task
├── Step 2 → Task
└── Step 3 → Task
```

### 层级映射

| DevPlan | Jira | 说明 |
|---------|------|------|
| 模块 (01-数据模型) | Epic | 一个模块对应一个 Epic |
| Step (Step 1: 数据层) | Task | 一个开发步骤对应一个 Task |
| 预估工时 | estimate | 直接使用 Step 的预估工时 |
| 优先级 (P0/P1/P2) | Priority | P0=High, P1=Medium, P2=Low |
| 模块类型 | Labels | Backend → backend, Frontend → frontend |

### 示例结构

**DevPlan 模块:**
```markdown
# 01-数据模型

## 开发步骤
### Step 1: 设计数据库 Schema (4h)
- [ ] 定义 User 实体
- [ ] 定义 Session 实体

### Step 2: 创建数据库迁移 (2h)
- [ ] 生成 Prisma 迁移文件
```

**转换为 Jira:**
```
Epic: 01-数据模型模块 (database, backend, foundation)
├── Task: 设计数据库 Schema (Prisma) [4h]
├── Task: 创建数据库迁移 [2h]
└── Task: 实现 User Repository [3h]
```

### 标签体系

| DevPlan 模块类型 | Epic 标签 | Task 标签 |
|-----------------|----------|----------|
| Backend | backend, foundation | backend, {具体领域} |
| Frontend | frontend, ui | frontend, react, ui |
| Infrastructure | infrastructure, devops | infrastructure, cicd |

**具体领域标签：**
- 数据库: database, prisma, postgresql
- 认证: auth, security, jwt
- API: api, rest, websocket

### 依赖关系

直接使用 DevPlan 中的依赖关系：

**DevPlan 依赖：**
```markdown
## 依赖关系
- 02-认证授权 依赖 → 01-数据模型
- 03-前端页面 依赖 → 02-认证授权
```

**转换为 Jira 依赖：**
```
EPIC-002 (认证授权) 依赖 → EPIC-001 (数据模型)
EPIC-003 (前端页面) 依赖 → EPIC-002 (认证授权)
```

### 输出文件

```
DevPlan/jira/
├── tickets.json        # 所有 tickets JSON（用于 API 创建）
├── epics.md            # Epic 列表
├── tasks.md            # Task 列表
└── report.md           # 规划报告
```

### 创建方式

**使用项目脚本创建：**
```bash
python scripts/create_jira_ticket.py \
    --email user@example.com \
    --file DevPlan/jira/tickets.json \
    --project YP2
```

### 适用场景

- 项目启动时的 Jira 配置
- Sprint 规划会议准备
- 任务分配和跟踪
- 团队协作管理
- 项目进度可视化

---

## dev-executor

按模块或 Jira ticket 逐个实现代码、编写单元测试、自动调试修复问题、生成测试报告。

支持两种工作模式：
- **模块规划模式**: 读取 dev-planner 生成的开发模块规划
- **Jira Ticket 模式**: 直接指定 Jira ticket URL，根据 ticket 描述开发

### 用法

```bash
# 模式 1: 开发指定模块
/dev-executor 请帮我开发 01-数据模型模块

# 模式 2: 使用 Jira Ticket 开发
/dev-executor https://dreamai.atlassian.net/browse/YP2-1

# 只运行测试
/dev-executor 请运行 01-数据模型模块的测试

# 修复失败的测试
/dev-executor 01-数据模型模块的测试失败了，请帮我修复

# 生成测试报告
/dev-executor 生成 01-数据模型模块的测试报告
```

### 参数

| 参数 | 必填 | 描述 |
|------|------|------|
| `模块编号/Jira Ticket URL` | ✅ | 要开发的模块编号或 Jira ticket URL |
| `操作类型` | ❌ | 可选：develop(开发)/test(测试)/fix(修复)/report(报告) |

### Jira Ticket 模式

当输入是 Jira ticket URL 时，执行以下流程：

```
1. 读取 Jira ticket 内容
   ├─ 提取 Ticket Key (如 YP2-1)
   ├─ 获取 Summary、Description、Labels
   └─ 判断模块类型

2. 分析需求
   ├─ 根据 Summary 理解功能
   ├─ 根据 Description 分析实现
   └─ 根据 Labels 确定输出目录

3. TDD 开发
   ├─ 编写测试
   ├─ 实现代码
   └─ 运行测试

4. 写回 Jira ticket
   ├─ 添加评论（测试结果）
   └─ 更新状态为 Done
```

**模块类型判断：**

| Labels | 输出目录 |
|--------|----------|
| backend | `backend/src/modules/` |
| frontend | `frontend/src/modules/` |
| infrastructure | `infrastructure/` |

**测试结果评论格式：**

```markdown
## 开发完成 ✅

### 实现内容
- 实现了用户认证功能
- 添加了单元测试

### 测试结果
- 测试用例: 8 个
- 通过: 8 个 ✅
- 失败: 0 个
- 覆盖率: 92%

### 代码质量
- Lint 检查: ✅ 通过
- 类型检查: ✅ 通过

### 交付物
- 源代码: backend/src/modules/auth/
- 测试文件: backend/src/modules/auth/auth.spec.ts
```

### 输出

```
DevPlan/Reports/
└── {模块名称}-测试报告.md

项目源代码/
└── src/
    └── modules/
        └── {模块名称}/
            ├── *.service.ts
            ├── *.repository.ts
            ├── *.controller.ts
            └── *.spec.ts
```

### 工作流程

1. **读取输入** - Jira ticket URL 或模块编号
2. **分析需求** - 从 ticket 或规划文档中获取
3. **TDD 开发** - 红-绿-重构循环
4. **单元测试** - 覆盖率要求 > 80%
5. **自动调试** - 分析失败原因并修复
6. **写回结果** - 更新 Jira ticket 或生成报告

### 开发规范

- 遵循单一职责、测试驱动开发(TDD)原则
- 代码质量检查（Lint + 类型检查）
- 测试覆盖率必须 > 80%
- Git 提交遵循约定式提交规范

---

## dev-integration

在所有模块开发完成后，执行集成测试和 E2E 测试，验证系统整体功能正确性。

### 用法

```bash
# 执行集成测试
/dev-integration 请执行集成测试

# 执行 E2E 测试
/dev-integration 请执行 E2E 测试

# 执行全部测试
/dev-integration 请执行集成测试和 E2E 测试

# 修复测试失败
/dev-integration 集成测试失败了，请帮我修复
```

### 测试金字塔

```
           E2E Tests
          /   少量     \        ← dev-integration 负责
        /______________\
       /  Integration  \      ← dev-integration 负责
      /      Tests      \
     /____________________\
    /    Unit Tests        \   ← dev-executor 负责
   /      大量              \
  /__________________________\
```

### 测试内容

**集成测试**:
- API 端到端流程测试
- 模块间交互测试
- 数据库集成测试
- 第三方服务集成测试

**E2E 测试**:
- 完整用户场景测试
- 跨页面业务流程测试
- 真实浏览器环境测试

### 工作流程

1. **读取规划** - 加载 DevPlan/ 确认所有模块完成
2. **设计测试** - 根据 API 设计和 PRD 设计测试用例
3. **生成测试** - 生成集成测试和 E2E 测试代码
4. **运行测试** - 执行测试套件
5. **问题定位** - 分析失败，定位具体模块
6. **修复问题** - 修复代码并重新测试
7. **生成报告** - 输出测试报告

### 自动修复流程

```
while 有失败测试:
    1. 分析失败日志
    2. 定位问题模块
    3. 读取该模块代码
    4. 修复代码
    5. 重新运行测试
    6. until 所有测试通过
```

### 测试工具

| 类型 | 工具 |
|------|------|
| 集成测试 | Vitest + Supertest |
| E2E 测试 | Playwright |

### 输出

```
backend/src/integration/
├── auth.integration.spec.ts
├── chat.integration.spec.ts
└── fixtures/

frontend/src/e2e/
├── scenarios/
│   ├── user-chat.e2e.spec.ts
│   └── agent-handle.e2e.spec.ts
├── pages/
│   ├── LoginPage.ts
│   └── ChatPage.ts
└── fixtures/

DevPlan/reports/
├── 集成测试报告.md
└── E2E测试报告.md
```

### 适用场景

- 所有模块开发完成后
- 发布前的回归测试
- 验证系统整体功能
- 测试跨模块业务流程

---

## dev-deploy

将应用部署到 Kubernetes 集群，支持多环境部署和回滚。

### 用法

```bash
# 部署到开发环境
/dev-deploy 请部署到开发环境

# 部署到生产环境
/dev-deploy 请部署到生产环境

# 部署特定服务
/dev-deploy 请部署 backend 服务到 staging

# 回滚
/dev-deploy 部署有问题，请回滚
```

### 部署流程

```
1. 部署前检查
   ├─ 确认所有模块完成
   ├─ 确认测试通过
   └─ 确认 K8s 配置

2. 构建容器镜像
   ├─ Frontend 镜像
   └─ Backend 镜像

3. 推送镜像仓库
   ├─ AWS ECR / 阿里云 ACR
   └─ 标签管理

4. 更新 K8s 配置
   ├─ Deployment
   ├─ Service
   └─ Ingress

5. 执行数据库迁移
   └─ Prisma Migrate

6. 滚动更新部署
   └─ 监控更新状态

7. 验证部署
   ├─ 健康检查
   ├─ API 测试
   └─ E2E 验证

8. 生成部署报告
```

### 多环境支持

| 环境 | Namespace | 副本数 | 用途 |
|------|-----------|--------|------|
| dev | dev | 1 | 开发测试 |
| staging | staging | 2 | 预发布 |
| prod | prod | 3+HPA | 生产环境 |

### 回滚策略

```bash
# 查看部署历史
kubectl rollout history deployment/backend -n ${ENV}

# 回滚到上一版本
kubectl rollout undo deployment/backend -n ${ENV}

# 回滚到指定版本
kubectl rollout undo deployment/backend -n ${ENV} --to-revision=3
```

### 安全配置

- Secrets 管理（K8s Secrets / External Secrets）
- 镜像扫描（Trivy）
- 镜像签名验证（Cosign）
- 健康检查端点
- 资源限制配置

### 监控与告警

- Prometheus + Grafana
- ServiceMonitor 配置
- 健康检查端点（/health, /ready）
- 资源使用监控

### 输出

```
infrastructure/k8s/
├── base/                    # 基础配置
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── overlays/                # 多环境配置
│   ├── dev/
│   ├── staging/
│   └── prod/
└── scripts/
    ├── build.sh
    ├── deploy.sh
    └── rollback.sh

infrastructure/reports/
└── deployment-{ENV}-{VERSION}.md
```

### 适用场景

- 首次部署到 K8s
- 日常版本发布
- 紧急热修复部署
- 多环境部署
- 金丝雀/蓝绿部署

---

## api-docs

根据后端代码和 API 设计自动生成专业的 API 文档。

### 用法

```bash
# 生成完整 API 文档
/api-docs 请生成 API 文档

# 更新文档
/api-docs API 有更新，请刷新文档

# 指定格式
/api-docs 生成 swagger 格式的文档
```

### 支持的框架

| 后端框架 | 支持情况 |
|---------|---------|
| Fastify (Node.js) | ✅ 原生支持 |
| Express (Node.js) | ✅ 通过注解 |
| NestJS (Node.js) | ✅ 原生支持 |
| Spring Boot (Java) | ✅ SpringDoc |
| Gin (Go) | ✅ Swaggo |
| FastAPI (Python) | ✅ 原生支持 |

### 生成内容

```
1. OpenAPI 3.0 规范
   ├─ openapi.yaml
   └─ openapi.json

2. 交互式文档
   ├─ Swagger UI (可测试)
   └─ ReDoc (只读)

3. Postman Collection
   └─ postman_collection.json

4. 客户端 SDK
   ├─ TypeScript
   └─ Python
```

### OpenAPI 规范示例

```yaml
openapi: 3.0.0
info:
  title: 智能客服系统 API
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
security:
  - BearerAuth: []
paths:
  /sessions:
    post:
      tags: [Sessions]
      summary: 创建会话
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateSessionRequest'
      responses:
        '201':
          description: 会话创建成功
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
```

### 输出目录

```
api-docs/
├── README.md                # 文档概览
├── openapi.yaml             # OpenAPI 规范
├── openapi.json             # OpenAPI JSON
├── index.html               # Swagger UI
├── redoc.html               # ReDoc
├── postman_collection.json  # Postman Collection
└── sdk/
    ├── typescript/          # TypeScript SDK
    └── python/              # Python SDK
```

### 代码注解规范

**Fastify Schema**:
```typescript
app.post('/sessions', {
  schema: {
    tags: ['Sessions'],
    summary: '创建会话',
    security: [{ bearerAuth: [] }],
    body: { /* ... */ },
    response: { /* ... */ }
  }
}, handler);
```

**NestJS DTO**:
```typescript
@ApiTags('Sessions')
export class CreateSessionDto {
  @ApiProperty({ description: '用户 ID', format: 'uuid' })
  @IsUUID()
  userId: string;
}
```

### 适用场景

- API 文档生成
- 前后端协作
- 第三方接入
- API 测试
- SDK 生成

---

## changelog

根据 Git 提交记录自动生成符合规范的 CHANGELOG.md。

### 用法

```bash
# 自动生成 changelog
/changelog 请生成 changelog

# 指定版本类型
/changelog 请发布 minor 版本

# 指定范围
/changelog 请生成从 v1.0.0 到现在的 changelog
```

### 语义化版本

```
MAJOR.MINOR.PATCH

例：1.2.3
- MAJOR (1): 不兼容的 API 变更
- MINOR (2): 向后兼容的功能新增
- PATCH (3): 向后兼容的问题修复
```

### Conventional Commits

支持的提交类型：

| 类型 | 说明 | 版本影响 |
|------|------|----------|
| `feat` | 新功能 | MINOR + 1 |
| `fix` | 问题修复 | PATCH + 1 |
| `docs` | 文档变更 | 无 |
| `style` | 代码格式 | 无 |
| `refactor` | 重构 | 无 |
| `perf` | 性能优化 | PATCH + 1 |
| `BREAKING CHANGE` | 破坏性变更 | MAJOR + 1 |

### CHANGELOG 格式

```markdown
# Changelog

## [1.2.0] - 2024-01-15

### Added
- **auth**: JWT token refresh mechanism
- **chat**: Support for file attachments

### Fixed
- **chat**: Message order issue in conversations
- **auth**: Token expiration not working

### Performance
- Database query optimization - 40% faster

### Documentation
- Updated API documentation

[1.2.0]: https://github.com/example/myapp/compare/v1.1.0...v1.2.0
```

### Commit 消息规范

```bash
# 基本格式
<type>(<scope>): <subject>

# 示例
feat(auth): add JWT token refresh
fix(chat): resolve message order issue
docs(api): update authentication docs
```

### 输出文件

```
项目根目录/
├── CHANGELOG.md              # 主变更日志
└── RELEASE_NOTES.md          # 本次发布说明
```

### Git Tag

```bash
# 创建 tag
git tag -a v1.2.0 -m "Release v1.2.0"

# 推送 tag
git push origin v1.2.0
```

### 自动化集成

支持与 GitHub Actions 集成，自动创建 Release。

### 适用场景

- 版本发布
- 生成发布说明
- 变更历史管理
- GitHub Release
- NPM 包发布

---

# 开发指南

## 复用到其他项目

这些 skills 可以复用到任何项目中，以下是几种推荐方式：

### 方案 1: Git Subtree（推荐）

适合需要独立提交和更新的场景。

```bash
# 在你的项目中
cd /path/to/your-project

# 添加 subtree
git subtree add --prefix=.claude/skills https://github.com/your-username/my-skills.git main

# 更新 skills
git subtree pull --prefix=.claude/skills https://github.com/your-username/my-skills.git main
```

### 方案 2: Git Submodule

适合多项目共享同一套 skills。

```bash
# 在你的项目中
git submodule add https://github.com/your-username/my-skills.git .claude/skills
git submodule update --init --recursive

# 克隆包含 submodule 的项目
git clone --recurse-submodules https://github.com/your-username/your-project.git
```

### 方案 3: 直接复制

适合快速试用或小项目。

```bash
# 复制整个 skills 目录
cp -r /path/to/my-skills/.claude/skills /path/to/your-project/.claude/
```

### 方案 4: 使用安装脚本

在 my-skills 根目录执行：

```bash
# 安装到指定项目
./scripts/install.sh /path/to/your-project
```

### 选择建议

| 场景 | 推荐方案 |
|------|----------|
| 个人项目，想随时更新 | Git Subtree |
| 公司团队，统一管理 | Git Submodule |
| 快速试用 | 直接复制 |
| 需要定制化 | Fork 后修改 |

## 本项目目录结构

```
my-skills/
├── README.md                    # 本文件
├── CLAUDE.md                    # Claude Code 项目配置
├── Prompts/                     # 原始提示词存档
└── .claude/
    └── skills/
        └── <skill-name>/        # 每个 skill 一个目录
            └── SKILL.md         # skill 定义文件
```

## 创建新 Skill

1. 在 `.claude/skills/` 下创建新目录：
   ```bash
   mkdir -p .claude/skills/my-new-skill
   ```

2. 创建 `SKILL.md` 文件：
   ```markdown
   ---
   name: my-new-skill
   description: 简短描述，帮助 Claude 判断何时使用
   ---

   # Skill 标题

   ## Instructions
   具体执行指令...

   ## Examples
   使用示例...
   ```

3. 更新 `README.md` 添加新 skill 的说明

## 参考资料

- [Claude Code Skills 官方文档](https://code.claude.com/docs/en/skills)
- [Anthropic 官方 Skills 仓库](https://github.com/anthropics/skills)

---

## License

MIT
