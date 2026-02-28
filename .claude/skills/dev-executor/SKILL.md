---
name: dev-executor
description: 按模块或Jira ticket逐个实现代码、编写单元测试、自动调试修复问题、生成测试报告。支持两种输入方式：1)读取dev-planner生成的开发模块规划；2)直接指定Jira ticket URL，根据ticket描述开发功能并将测试结果写回ticket。遵循单一职责、测试驱动开发(TDD)原则。当用户提到"开始开发"、"实现模块"、"运行测试"、"修复bug"、"生成测试报告"或提供Jira ticket链接时触发。
---

# 开发模块执行器

## Overview

支持两种工作模式：

**模式 1: 开发模块规划**
执行 dev-planner 生成的开发模块规划，按照模块顺序逐个开发：
1. 实现代码
2. 编写单元测试
3. 运行测试
4. 自动调试修复
5. 生成测试报告

**模式 2: Jira Ticket 驱动**
根据 Jira ticket 的描述直接开发功能：
1. 读取 Jira ticket 内容
2. 分析需求和技术实现
3. TDD 开发功能
4. 编写并运行测试
5. 将测试结果写回 Jira ticket

## 代码输出目录

遵循 tech-solution 定义的项目结构：

```
项目根目录/
├── backend/src/modules/          # 后端模块代码
│   └── {模块名称}/
│       ├── {entity}.repository.ts
│       ├── {entity}.service.ts
│       ├── {entity}.controller.ts
│       ├── {entity}.schema.ts
│       └── {entity}.spec.ts
│
├── frontend/src/modules/          # 前端模块代码
│   └── {模块名称}/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       └── {模块名称}.spec.tsx
│
└── infrastructure/                # 云基础设施部署脚本
    └── {模块名称}/
        ├── k8s/
        │   ├── deployment.yaml
        │   └── service.yaml
        └── terraform/
            └── main.tf
```

## Parameters

| 参数 | 必填 | 描述 |
|------|------|------|
| `模块编号` | ❌ | 要开发的模块编号（如 "01"），或 Jira ticket URL |
| `操作` | ❌ | 可选：develop(开发)/test(测试)/fix(修复)/report(报告) |

**支持两种输入方式：**

1. **模块编号**: `01`、`02-数据模型` 等
2. **Jira Ticket URL**: `https://dreamai.atlassian.net/browse/YP2-1`

## Instructions

你是一名【全栈开发工程师 + 测试工程师 + DevOps 工程师】，拥有 10 年项目开发经验。

### 工作流程

首先判断输入类型：

**如果是 Jira Ticket URL** → 跳转到【Jira Ticket 模式】
**如果是模块编号** → 跳转到【开发模块规划模式】

---

## Jira Ticket 模式

#### Step 1: 读取 Jira Ticket

解析 Jira ticket URL 并获取内容：

```bash
# 示例 URL: https://dreamai.atlassian.net/browse/YP2-1
# 提取: Base URL = dreamai.atlassian.net, Ticket Key = YP2-1

# 使用 Jira API 读取 ticket
# GET /rest/api/3/issue/{ticketKey}
```

**获取的信息：**
- Ticket Key (如 YP2-1)
- Summary (标题)
- Description (描述)
- Issue Type (Epic/Task)
- Priority (优先级)
- Labels (标签)
- Custom Fields (自定义字段)

#### Step 2: 分析需求

根据 ticket 信息分析开发需求：

| Ticket 信息 | 用途 |
|-------------|------|
| Summary | 理解要实现的功能 |
| Description | 详细需求分析 |
| Labels | 判断模块类型 (backend/frontend/infrastructure) |
| Priority | 确定开发优先级 |

**模块类型判断：**
```
包含标签: backend → 后端模块 → backend/src/modules/
包含标签: frontend → 前端模块 → frontend/src/modules/
包含标签: infrastructure → 基础设施 → infrastructure/
```

#### Step 3: TDD 开发

按照模块类型进行开发，流程与【开发模块规划模式】相同。

#### Step 4: 更新 Jira Ticket

**4.1 添加评论**

测试完成后，向 Jira ticket 添加评论：

```markdown
## 开发完成 ✅

### 实现内容
- 实现了 {功能描述}
- 添加了单元测试

### 测试结果
- 测试用例: XX 个
- 通过: XX 个 ✅
- 失败: 0 个
- 覆盖率: XX%

### 代码质量
- Lint 检查: ✅ 通过
- 类型检查: ✅ 通过

### 交付物
- 源代码: {文件路径}
- 测试文件: {文件路径}

---
由 dev-executor 自动生成
```

**4.2 更新状态（可选）**

如果配置允许，将 ticket 状态更新为：
- `To Do` → `In Progress` (开发开始时)
- `In Progress` → `Done` (测试通过后)

**4.3 使用脚本更新**

```bash
python scripts/update_jira_ticket.py \
    --ticket-key YP2-1 \
    --comment "开发完成，测试通过" \
    --transition "Done" \
    --email your@email.com
```

---

## 开发模块规划模式

#### Step 1: 读取开发规划

首先读取 `DevPlan/` 目录下的规划文档：
```bash
# 读取模块列表
read DevPlan/modules.md

# 读取要开发的模块详情
read DevPlan/modules/{模块编号}-{模块名称}.md

# 读取当前进度
read DevPlan/checklist.md
```

#### Step 2: 开发模块（develop）

**2.1 确定模块类型与输出目录**

根据模块类型选择输出目录：

| 模块类型 | 输出目录 | 说明 |
|---------|---------|------|
| 后端模块 (Backend) | `backend/src/modules/{模块名称}/` | API、Service、Repository |
| 前端模块 (Frontend) | `frontend/src/modules/{模块名称}/` | Components、Hooks、Services |
| 基础设施模块 (Infrastructure) | `infrastructure/{模块名称}/` | K8s、Terraform 配置 |

**2.2 分析模块需求**
- 读取模块的功能需求
- 理解数据模型、API 设计、技术实现
- 确认依赖模块已完成

**2.3 TDD 开发流程**
遵循红-绿-重构循环：

```
Red:   编写失败的测试
Green: 编写最少代码使测试通过
Refactor: 重构优化代码
```

**2.4 实现代码**

按照模块类型和开发步骤实现：

**Backend 模块** → `backend/src/modules/{模块名称}/`
- Step 1: 数据层（Schema/Repository）
- Step 2: 服务层
- Step 3: 控制层（Controller/Routes）
- Step 4: 单元测试

**Frontend 模块** → `frontend/src/modules/{模块名称}/`
- Step 1: 类型定义
- Step 2: API 服务层
- Step 3: 组件层（Components）
- Step 4: 单元测试

**Infrastructure 模块** → `infrastructure/{模块名称}/`
- Step 1: K8s 配置
- Step 2: Terraform 配置（可选）
- Step 3: 部署文档

**2.5 代码质量检查**
```bash
# 代码格式化
npm run format

# 代码检查
npm run lint

# 类型检查
npm run type-check
```

#### Step 3: 单元测试（test）

**3.1 编写测试用例**
测试覆盖：
- 正常场景
- 边界条件
- 异常处理
- 并发场景

**3.2 运行测试**
```bash
# 单元测试
npm test

# 测试覆盖率
npm run test:coverage

# 要求覆盖率 > 80%
```

**3.3 记录测试结果**
- 通过的测试
- 失败的测试
- 覆盖率报告

#### Step 4: 自动调试（fix）

**4.1 分析失败原因**
```bash
# 查看详细错误日志
npm test -- --verbose

# 生成覆盖率报告查看未覆盖代码
npm run test:coverage
```

**4.2 修复策略**
- **测试失败**：检查测试用例是否合理，修复代码或测试
- **覆盖率不足**：补充测试用例
- **类型错误**：修复类型定义
- **Lint 错误**：修复代码风格问题

**4.3 迭代修复**
```
while 有失败测试:
    分析失败原因
    修复代码
    运行测试验证
    until 所有测试通过
```

#### Step 5: 生成测试报告（report）

**5.1 报告内容**
```markdown
# {模块名称} 测试报告

## 测试概览
- 测试用例总数: XX
- 通过: XX
- 失败: XX
- 覆盖率: XX%
- 执行时间: XX秒

## 测试结果详情
### ✅ 通过的测试
- test_case_1: 描述
- test_case_2: 描述

### ❌ 失败的测试
（如果有）

## 代码质量
- Lint 检查: 通过/失败
- 类型检查: 通过/失败
- 代码规范: 符合

## 验收标准
- [ ] 所有功能正常工作
- [ ] 单元测试覆盖率 > 80%
- [ ] 所有测试通过
- [ ] 代码审查通过
- [ ] 无已知 Bug

## 交付物
- 源代码文件
- 单元测试文件
- API 文档（如适用）
```

**5.2 更新 checklist.md**
标记该模块为已完成。

### 开发规范

#### 业界最佳实践

**1. SOLID 原则**
```
S - 单一职责原则 (SRP): 类/函数只负责一件事
O - 开闭原则 (OCP): 对扩展开放，对修改关闭
L - 里氏替换原则 (LSP): 子类可替换父类
I - 接口隔离原则 (ISP): 客户端不应依赖它不需要的接口
D - 依赖倒置原则 (DIP): 依赖抽象而非具体实现
```

**2. Clean Code 原则**
- 函数保持短小（不超过 20 行）
- 有意义的命名
- 避免深层嵌套（不超过 3 层）
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)

**3. 设计模式应用**
| 场景 | 推荐模式 |
|------|---------|
| 数据访问 | Repository Pattern |
| 依赖注入 | Dependency Injection |
| 对象创建 | Factory / Builder |
| 行为变化 | Strategy Pattern |
| 状态管理 | Observer / Pub-Sub |

**4. TDD 开发流程**
```
Red:   先写失败的测试
Green: 编写最少代码使测试通过
Refactor: 重构优化代码
```

**5. 代码审查清单**
- [ ] 代码符合团队规范
- [ ] 测试覆盖率 > 80%
- [ ] 无硬编码配置
- [ ] 错误处理完善
- [ ] 性能考虑合理
- [ ] 安全漏洞检查
- [ ] 注释清晰必要

#### 代码规范

**命名规范**:
```typescript
// 类名: PascalCase
class UserService {}

// 函数/变量: camelCase
const getUserById = async (id: string) => {};

// 常量: UPPER_SNAKE_CASE
const MAX_RETRY_COUNT = 3;

// 私有成员: # 或 _
class Example {
  #privateField = '';
}
```

**注释规范**:
```typescript
/**
 * 获取用户信息
 * @param userId - 用户ID
 * @returns 用户对象
 */
async getUser(userId: string) {
  // 实现
}
```

#### 测试规范

**测试文件命名**: `{源文件名}.spec.ts` 或 `{源文件名}.test.ts`

**测试结构**:
```typescript
describe('UserService', () => {
  describe('getUserById', () => {
    it('should return user when valid id provided', async () => {
      // Arrange
      const userId = 'user-123';

      // Act
      const result = await userService.getUserById(userId);

      // Assert
      expect(result).toBeDefined();
      expect(result.id).toBe(userId);
    });

    it('should throw error when user not found', async () => {
      // 测试不存在的情况
    });

    it('should throw error when invalid id provided', async () => {
      // 测试无效输入
    });
  });

  describe('createUser', () => {
    // 测试创建用户的场景
  });
});
```

**Mock 策略**:
```typescript
// Mock 外部依赖
jest.mock('../lib/database');
jest.mock('../lib/email');

// Mock 函数
const mockDb = database as jest.Mocked<typeof database>;
mockDb.query.mockResolvedValue(expectedUser);
```

#### Git 提交规范

每个模块完成后提交代码：
```bash
git add .
git commit -m "feat(module): implement {模块名称}

- 实现核心功能
- 添加单元测试（覆盖率 > 80%）
- 通过代码审查

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 错误处理策略

#### 编译错误
```bash
# 查看具体错误
npm run build

# 常见问题：
# - TypeScript 类型错误：检查类型定义
# - 依赖缺失：npm install
# - 配置错误：检查 tsconfig.json
```

#### 测试失败
```typescript
// 1. 分析失败原因
// 使用 only 单独运行失败的测试
it.only('failing test', () => {
  // ...
});

// 2. 添加调试日志
console.log('Expected:', expected);
console.log('Actual:', actual);

// 3. 检查 Mock 配置
// 确保外部依赖正确 Mock

// 4. 逐步验证
// 分步骤调试，找出问题点
```

#### 覆盖率不足
```bash
# 生成详细覆盖率报告
npm run test:coverage -- --verbose

# 查看未覆盖的代码
open coverage/lcov-report/index.html

# 补充测试用例：
# - 分支覆盖：if/else 的所有分支
# - 条件覆盖：复杂的条件表达式
# - 行覆盖：未执行的代码行
```

## Examples

### 示例 1: 使用 Jira Ticket 开发

```bash
# 用户请求
/dev-executor https://dreamai.atlassian.net/browse/YP2-1

# Claude 执行流程
1. 解析 URL，提取 Base URL 和 Ticket Key (YP2-1)
2. 通过 Jira API 读取 ticket 内容
3. 根据 Summary 和 Description 分析需求
4. 根据 Labels 判断模块类型（如 backend）
5. TDD 开发功能
6. 编写并运行测试
7. 使用脚本更新 Jira ticket：
   - 添加评论（包含测试结果）
   - 更新状态为 Done
```

### 示例 2: 开发单个模块
```bash
# 用户请求
请帮我开发 01-数据模型模块

# Claude 执行流程
1. 读取 DevPlan/modules/01-数据模型.md
2. 分析需求和技术实现
3. 创建 Prisma Schema
4. 编写 Repository 类
5. 编写单元测试
6. 运行测试，确保覆盖率 > 80%
7. 生成测试报告
8. 更新 DevPlan/checklist.md
```

### 示例 2: 只运行测试
```bash
# 用户请求
请运行 01-数据模型模块的测试

# Claude 执行流程
1. 运行 npm test
2. 生成覆盖率报告
3. 输出测试结果
4. 如有失败，询问是否修复
```

### 示例 3: 修复失败的测试
```bash
# 用户请求
01-数据模型模块的测试失败了，请帮我修复

# Claude 执行流程
1. 查看测试失败日志
2. 分析失败原因
3. 修复代码或测试
4. 重新运行测试
5. 确保所有测试通过
6. 生成新的测试报告
```

## Output

### 文件输出

根据模块类型，代码输出到对应目录：

#### Backend 模块输出
```
backend/src/modules/{模块名称}/
├── {entity}.repository.ts       # 数据访问层
├── {entity}.service.ts          # 业务逻辑层
├── {entity}.controller.ts       # API 控制层
├── {entity}.schema.ts           # 数据模型/DTO
├── {entity}.routes.ts           # 路由定义
└── {entity}.spec.ts             # 单元测试
```

#### Frontend 模块输出
```
frontend/src/modules/{模块名称}/
├── components/
│   ├── {Component}.tsx          # React 组件
│   └── {Component}.module.css   # 样式文件
├── hooks/
│   └── use{Hook}.ts             # 自定义 Hooks
├── services/
│   └── {module}.api.ts          # API 调用
├── types/
│   └── {module}.types.ts        # TypeScript 类型
└── {模块名称}.spec.tsx           # 组件测试
```

#### Infrastructure 模块输出
```
infrastructure/{模块名称}/
├── k8s/
│   ├── deployment.yaml          # K8s 部署配置
│   ├── service.yaml             # K8s Service
│   └── ingress.yaml             # K8s Ingress (可选)
├── terraform/
│   └── main.tf                  # Terraform 配置 (可选)
└── README.md                    # 部署说明
```

#### 测试报告输出
```
DevPlan/reports/
└── {模块名称}-测试报告.md
```

### 更新 checklist.md
```markdown
- [x] 01-数据模型
  - [x] 定义 Prisma Schema
  - [x] 创建数据库迁移
  - [x] 编写基础 Repository
  - [x] 编写单元测试
  - [x] 验收通过
```

## 依赖工具

```bash
# 测试框架
npm install --save-dev vitest @vitest/ui

# 覆盖率
npm install --save-dev @vitest/coverage-v8

# 类型检查
npm install --save-dev typescript

# 代码检查
npm install --save-dev eslint prettier

# Git 钩子（可选）
npm install --save-dev husky lint-staged
```

## 注意事项

1. **遵循模块文档**: 严格按照 `DevPlan/modules/{模块编号}.md` 中的要求实现
2. **TDD 原则**: 先写测试，再写代码
3. **质量第一**: 不达标不交付，覆盖率必须 > 80%
4. **及时提交**: 每个模块完成后立即提交代码
5. **文档同步**: 代码完成后更新 API 文档
6. **目录组织**: 严格按模块类型输出到对应目录
   - Backend → `backend/src/modules/`
   - Frontend → `frontend/src/modules/`
   - Infrastructure → `infrastructure/`
7. **遵循最佳实践**: SOLID、Clean Code、设计模式、代码审查清单

## 适用场景

- 执行 dev-planner 生成的开发计划
- 按模块逐步实现功能
- 自动化单元测试和调试
- 生成测试报告和验收文档
