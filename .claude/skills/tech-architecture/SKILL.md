---
name: tech-architecture
description: 生成【架构评审级】Mermaid 架构图（6张标准图），用于架构评审和 ToB 咨询交付。输出：业务架构图、技术架构图、系统架构图、模块依赖图、数据流图、API架构图。⚠️ 不含技术选型和具体实现方案（见 tech-solution）。适用于架构评审会议、技术委员会决策、ToB 项目架构交付。当用户提到"架构图"、"架构评审"、"系统架构"、"业务架构"时触发。
---

# 业务需求 → 技术架构方案

## Overview

将业务需求转化为完整的技术架构方案，包括：
- 架构规范文档（Architecture.md）
- 6 张标准 Mermaid 架构图
- 架构决策记录（ADR）

## Parameters

| 参数 | 必填 | 描述 |
|------|------|------|
| `$ARGUMENTS` | ✅ | 业务需求概述或 PRD 文档路径 |

## Instructions

你是一名【资深系统架构师 + 企业级技术顾问 + 提示词工程专家】。

请基于用户提供的【业务需求概述】，生成一套【架构规范文档 + 架构图】。

### 用户需求输入

$ARGUMENTS

### 全局规范

1. 标准输出为以下 6 张架构图；复杂项目（分布式系统、多区域部署等）可按需增加其他图表（部署拓扑图、故障转移图、时序图等）
2. Architecture.md 是主架构说明文档
3. diagrams/ 目录主要输出 Mermaid 架构图（.mmd），必要时可补充文字说明文件
4. 架构图用于表达"结构事实"，文字用于表达"设计意图"
5. 不输出代码实现
6. 输出内容面向：架构评审、ToB 咨询交付、CTO / 技术委员会决策
7. 每个文件输出时，明确标注【文件路径】

### 输出目录结构

```
Architecture/
├── README.md                              # 架构目录入口说明
├── Architecture.md                        # 核心架构说明文档
└── diagrams/
    ├── 01-business-architecture.mmd       # 业务架构图
    ├── 02-technical-architecture.mmd      # 技术架构图
    ├── 03-system-architecture.mmd         # 系统架构图
    ├── 04-module-dependencies.mmd         # 模块依赖图
    ├── 05-data-flow.mmd                   # 数据流图
    └── 06-api-architecture.mmd            # API/能力架构图
```

### 文件 1：README.md

**路径**: `Architecture/README.md`

**内容要求**:
- 本架构规范的目的
- 适用场景
- 架构文档阅读顺序说明
- Architecture.md 与 diagrams/ 的关系说明
- 架构变更与维护原则（高层）

### 文件 2：Architecture.md（核心）

**路径**: `Architecture/Architecture.md`

**内容结构**（必须清晰分节）:

## 目录

- [架构背景与目标](#架构背景与目标)
- [架构设计原则与约束](#架构设计原则与约束)
- [业务架构说明](#业务架构说明)
- [系统架构说明](#系统架构说明)
- [技术架构说明](#技术架构说明)
- [模块拆分与职责边界](#模块拆分与职责边界)
- [核心数据流说明](#核心数据流说明)
- [API能力暴露方式说明](#api能力暴露方式说明)
- [关键架构决策记录](#关键架构决策记录)
- [架构风险与假设](#架构风险与假设)
- [架构演进方向](#架构演进方向)

---

1. **架构背景与目标**
2. **架构设计原则与约束**
3. **业务架构说明**（对应图 01）
4. **系统架构说明**（对应图 03）
5. **技术架构说明**（对应图 02）
6. **模块拆分与职责边界**（对应图 04）
7. **核心数据流说明**（对应图 05）
8. **API / 能力暴露方式说明**（对应图 06）
9. **关键架构决策记录**（ADR 风格）
10. **架构风险与假设**
11. **架构演进方向**

⚠️ 要求：
- 每一节必须明确引用对应的 diagrams/*.mmd 文件
- 不重复画图，只解释图中表达的含义

### 架构图规范

#### 图 01：业务架构图
**路径**: `Architecture/diagrams/01-business-architecture.mmd`
- 表达业务域划分
- 展示业务能力之间的关系
- 不体现技术实现
- 使用 Mermaid，业务视角

#### 图 02：技术架构图
**路径**: `Architecture/diagrams/02-technical-architecture.mmd`
- 表达技术栈与基础设施
- 展示运行时组件关系
- 体现计算、存储、网络、基础设施
- **AI SaaS 标准栈（Vercel + Supabase）拓扑**：前端/API → Vercel CDN + Serverless/Edge Functions → Supabase（PostgreSQL + Auth + Storage + Realtime）；K8s 方案时体现 EKS/ACK 集群 + RDS + ElastiCache

#### 图 03：系统架构图
**路径**: `Architecture/diagrams/03-system-architecture.mmd`
- 展示系统边界
- 子系统/服务之间的关系
- 强调系统间交互

#### 图 04：模块依赖图
**路径**: `Architecture/diagrams/04-module-dependencies.mmd`
- 展示模块拆分
- 展示依赖方向
- 帮助评估耦合度

#### 图 05：数据流图
**路径**: `Architecture/diagrams/05-data-flow.mmd`
- 展示关键业务场景下的数据流动
- 支撑性能、安全、合规分析
- 标注同步 / 异步

#### 图 06：API / 能力架构图
**路径**: `Architecture/diagrams/06-api-architecture.mmd`
- 展示系统能力如何被暴露和调用
- 体现对内 / 对外接口边界
- 能力视角而非实现视角

## Examples

**输入**:
```bash
/tech-architecture 商品评价系统，支持买家发布图文评价、卖家回复、平台审核
```

**输出**: 完整的架构目录，包含：
- `Architecture/README.md`
- `Architecture/Architecture.md`
- `Architecture/diagrams/01-business-architecture.mmd`
- `Architecture/diagrams/02-technical-architecture.mmd`
- `Architecture/diagrams/03-system-architecture.mmd`
- `Architecture/diagrams/04-module-dependencies.mmd`
- `Architecture/diagrams/05-data-flow.mmd`
- `Architecture/diagrams/06-api-architecture.mmd`

---

## 多语言 / i18n 架构（当需求涉及多语言时）

当业务需求涉及多语言、多地区用户时，Architecture.md 中必须包含 **i18n 架构决策** 章节：

### Architecture.md 需新增章节

**国际化架构说明**（插入在"API能力暴露方式说明"之后）

必须说明：
1. **语言路由策略** — URL 前缀 (`/zh/`、`/en/`) vs 子域名 (`zh.example.com`) vs 查询参数
2. **内容分层模型** — UI 文案（静态翻译） vs CMS 动态内容（多 locale） vs 用户生成内容
3. **翻译管理架构** — 集中式翻译文件 vs CMS 内置 i18n vs 第三方翻译平台
4. **SEO 多语言策略** — hreflang 标签、sitemap 分语言、canonical URL
5. **构建 vs 运行时** — 静态生成多语言页面（SSG）vs 服务端按请求切换语言（SSR）

### 架构图中的体现

#### 业务架构图 (01)
- 标注哪些业务域需要多语言支持
- 标注内容创作 → 翻译 → 发布的业务流程

#### 系统架构图 (03)
- 展示翻译文件/服务的位置
- 展示 CMS 多 locale 数据流

#### 数据流图 (05)
- 展示用户请求 → 语言检测 → 内容路由 → 翻译合并 → 响应 的完整链路
- 标注哪些节点是构建时确定、哪些是运行时确定

#### API架构图 (06)
- API 如何支持 `?locale=zh` 或 `Accept-Language` header
- CMS API 的多语言内容查询模式

### 关键架构决策记录（ADR 补充）

i18n 相关的 ADR 通常包括：

| 决策项 | 常见选项 | 决策依据 |
|--------|----------|----------|
| URL 策略 | 路径前缀 vs 子域名 vs 参数 | SEO 需求、CDN 缓存策略 |
| 翻译存储 | 代码内 JSON vs CMS vs 翻译平台 | 翻译频率、翻译人员技术水平 |
| 默认语言回退 | 显示 key vs 回退到默认语言 | 用户体验 vs 翻译覆盖率 |
| 构建方式 | 每语言独立构建 vs 运行时切换 | 页面数量、更新频率 |

## 适用场景

- 架构评审会议
- ToB 项目技术方案交付
- CTO / 技术委员会决策支持
- 技术文档归档
