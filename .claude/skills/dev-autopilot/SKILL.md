---
name: dev-autopilot
description: 自动持续执行 dev-planner 生成的开发计划。读取 DevPlan/*/checklist.md，按序找出未完成的 phase 和 module，严格按照 dev-executor 的 TDD 标准逐个自动执行（实现代码→单元测试→运行测试→调试修复→更新checklist）。遇到需要用户提供的凭据（数据库密码、API密钥、第三方账号等）时，写入 DevPlan/BLOCKED.md 并继续执行其他可执行任务。支持设置 cron job 每 30 分钟自动检查并继续开发，直到所有模块完成。应在 dev-planner 生成计划后使用，作为 dev-executor 的自动化版本。当用户提到"自动执行开发计划"、"自动开发"、"后台执行"、"autopilot"、"持续开发"、"无人值守开发"、"cron开发"时触发。
---

# 开发自动驾驶 (Dev Autopilot)

## Overview

读取 `DevPlan/*/checklist.md`，按 Phase→Module 顺序自动完成所有未开发的模块。
每个模块严格遵循 dev-executor 的 TDD 工作流，遇到阻塞项记录后继续执行。

## 首次运行流程

### Step 1: 扫描开发计划

```bash
# 找到所有 checklist 文件
python3 scripts/parse_checklist.py DevPlan/
```

输出格式：
```
APP: backend-api
  PHASE 1 - 数据库设计:
    [PENDING] 01-数据模型
    [DONE]    02-认证授权
  PHASE 2 - 后端开发:
    [PENDING] 03-会话管理
    [BLOCKED] 04-第三方集成 → 需要 STRIPE_API_KEY
```

### Step 2: 按序执行 dev-executor 工作流

对每个 `[PENDING]` 模块，严格按以下步骤执行：

```
1. 读取 DevPlan/modules/{编号}-{模块名}.md
2. 确认依赖模块已完成（blockedBy 检查）
3. TDD 开发：
   Red   → 先写失败的测试
   Green → 最少代码使测试通过
   Refactor → 重构优化
4. 代码质量检查：npm run format && npm run lint && npm run type-check
5. 运行测试：npm test && npm run test:coverage（要求覆盖率 > 80%）
6. 如有失败：分析原因 → 修复 → 重新运行，直到全部通过
7. 生成测试报告 → DevPlan/reports/{模块名}-测试报告.md
8. 提交代码：git commit -m "feat(module): implement {模块名}"
9. 更新 checklist.md：将该模块所有子项标记为 [x]
```

### Step 3: 遇到阻塞时

遇到需要用户提供的信息时（API Key、账号密码、配置值等）：

1. **不停止执行**，跳过该模块，继续下一个可执行模块
2. 将阻塞信息追加写入 `DevPlan/BLOCKED.md`：

```markdown
## [时间戳] 模块 {编号}-{模块名} 被阻塞

**需要提供的信息：**
| 变量名 | 说明 | 获取方式 |
|--------|------|----------|
| STRIPE_API_KEY | Stripe 支付 API 密钥 | https://dashboard.stripe.com/apikeys |
| DATABASE_URL | 生产数据库连接串 | 联系 DBA |

**阻塞原因：** {具体原因描述}

**解除阻塞后操作：** 将上述变量添加到 .env 文件，然后重新运行 `/dev-autopilot` 或等待下次 cron 检查。
```

3. 当所有可执行模块完成后，汇报 BLOCKED.md 的内容，提示用户填写

### Step 4: 设置 cron job（可选）

完成首次运行后，提示用户是否设置定时检查：

```bash
bash scripts/setup_cron.sh /path/to/project 30
```

这会添加 cron 条目：每 30 分钟检查 checklist，若有未完成项则自动继续开发。

## Cron 触发运行流程

当 cron 调用时（非用户直接触发），执行简化流程：

1. 运行 `parse_checklist.py`，检查是否有 `[PENDING]` 项
2. 若无 → 记录日志 `[DONE] 所有模块已完成` → 退出（可选：发邮件通知）
3. 若有 → 执行 Step 2 的 dev-executor 工作流
4. 更新 `DevPlan/autopilot.log`

## 阻塞模块恢复

用户填写 `.env` 或提供所需信息后：

```bash
# 手动触发恢复
/dev-autopilot resume 04-第三方集成
```

或等待下次 cron 自动检测并继续。

## 输出产物

| 产物 | 路径 | 说明 |
|------|------|------|
| 代码文件 | `backend/src/modules/{name}/` | 按 dev-executor 目录规范 |
| 测试文件 | `{模块目录}/{entity}.spec.ts` | 覆盖率 > 80% |
| 测试报告 | `DevPlan/reports/{name}-测试报告.md` | 每模块一份 |
| 阻塞记录 | `DevPlan/BLOCKED.md` | 需要用户提供的信息 |
| 运行日志 | `DevPlan/autopilot.log` | 每次运行记录 |
| 更新后的 checklist | `DevPlan/{app}/checklist.md` | 已完成项标记为 [x] |

## 开发规范（继承自 dev-executor）

- SOLID 原则 + Clean Code（函数 ≤ 20 行，嵌套 ≤ 3 层）
- TDD：先写测试，再写代码
- 覆盖率 > 80%，不达标不标记完成
- 每模块完成后立即 git commit
- 无硬编码配置，敏感信息写入 BLOCKED.md 等待用户填写

## 使用示例

```bash
# 首次运行，自动执行所有未完成模块
/dev-autopilot

# 指定应用
/dev-autopilot DevPlan/backend-api/

# 恢复被阻塞的模块（提供信息后）
/dev-autopilot resume

# 只检查状态，不执行
/dev-autopilot status
```
