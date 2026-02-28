---
name: project-manager
description: 全自动项目经理，将碎片需求转化为完整产品并自动部署上线。编排所有 SDLC skills 按序执行：需求→架构→技术方案→UI/UX设计→开发规划→基础设施→开发（TDD）→测试→安全扫描→部署→域名映射。生成主 checklist，设置 cron job 每 10 分钟检查一次，无需人工干预自动推进直到产品上线。域名使用 cloudflared tunnel 映射到 dreamwiseai.com。当用户提到"全自动开发"、"自动做产品"、"project manager"、"项目经理"、"全流程开发"、"一键开发上线"、"无人值守开发"、"自动项目"时触发。
---

# 全自动项目经理 (Project Manager)

## Overview

接收碎片化需求，编排所有 SDLC Skills，自动推进直到产品完整部署到 `{项目名}.dreamwiseai.com`。

**核心原则：**
- 每个 Phase 完成后立即更新 `ProjectManager/master-checklist.md`
- 遇到阻塞（凭据、外部账号）→ 写入 `ProjectManager/BLOCKED.md`，继续下一可执行 Phase
- cron job 每 10 分钟检查 checklist，自动继续未完成的 Phase

## 启动

### Step 0: 初始化

```bash
mkdir -p ProjectManager
PROJECT_NAME=$(basename $(pwd))
```

**1. 保存初始需求**（供 cron 断点续传时使用）：

```bash
# 将用户的碎片需求写入文件
cat > ProjectManager/initial-requirements.md << 'EOF'
{用户提供的原始需求，原文保存}
EOF
```

**2. 初始化 master-checklist**：

复制 `references/master-checklist-template.md` 到 `ProjectManager/master-checklist.md`，填写项目名。

**3. 立即设置 Dispatcher Cron**（不等开发完成，Phase 1 开始前就启动）：

```bash
bash .claude/skills/project-manager/scripts/setup_pm_cron.sh $(pwd)
```

**Dispatcher 工作原理：**
- 每 10 分钟读取 `master-checklist.md`，找第一个 `[ ]` Phase
- 用 `claude --print "/skill-name ..."` 触发对应 skill 执行
- 检测产物是否生成（如 `PRD/requirements.md`）→ 标记 `[x]`
- 下次 cron 自动进入下一 Phase
- Phase 9（release-qa）有前置检查：等 DevPlan 所有模块完成才触发
- Phase 13 完成后自动取消 cron

---

## 13 个执行阶段

### Phase 1: 需求分析 → PRD

调用 `/requirement-detail`，输入碎片需求，生成专业 PRD。

**输出：** `PRD/requirements.md`
**完成标记：** `[x] Phase 1`

---

### Phase 2: 架构设计

调用 `/tech-architecture`，基于 PRD 生成 6 张 Mermaid 架构图。

**输出：** `Architecture/`
**完成标记：** `[x] Phase 2`

---

### Phase 3: 技术方案

调用 `/tech-solution`，生成技术选型、项目结构、ER图、API设计、K8s方案、成本估算。

**输出：** `TechSolution/`
**完成标记：** `[x] Phase 3`

---

### Phase 4: 设计系统（Step 1 - 规范定义）

调用 `/ui-ux-pro-max`，基于 PRD 定义设计系统规范。

提示词：
```
基于 PRD/requirements.md，定义设计系统规范：
1. 色彩体系（主色/辅色/中性色/语义色）
2. 字体方案（标题/正文/代码）
3. 核心组件样式（按钮/表单/卡片/导航）
4. 间距/圆角/阴影规范
输出到 Design/design-system.md
```

**输出：** `Design/design-system.md`
**完成标记：** `[x] Phase 4`

---

### Phase 5: 页面设计（Step 2 - 具体页面）

调用 `/uiux-design`，基于 Phase 4 设计系统生成各功能页面的详细设计文档（适配 UX Pilot）。

提示词：
```
基于 PRD/requirements.md 和 Design/design-system.md，
严格遵循已定义的设计系统，为每个功能模块生成详细页面设计规格。
```

**输出：** `Design/pages/`
**完成标记：** `[x] Phase 5`

---

### Phase 6: 开发规划

调用 `/dev-planner`，将 PRD + 技术方案拆解为可执行的开发模块。

**输出：** `DevPlan/`（checklist.md + 各模块 md）
**完成标记：** `[x] Phase 6`

---

### Phase 7: 基础设施（按需）

**判断：** 读取 `TechSolution/`，若包含 PostgreSQL/Redis/MongoDB 等 → 执行；否则标记 SKIP。

调用 `/infrastructure-provisioner` 准备本地 K8s 环境。

**输出：** `infrastructure/` + `.env`
**完成标记：** `[x] Phase 7`（或 `[SKIP] 无需基础设施`）

---

### Phase 8a: 开发实现（dev-executor TDD）

调用 `/dev-executor`，按模块逐个实现，严格按 skill 要求执行：

- TDD：Red → Green → Refactor（先写测试，再写代码）
- 单元测试：覆盖高风险/复杂逻辑，覆盖率 > 80%
- API 测试：调用真实接口，禁止 Mock，每接口 2-5 个用例（Happy Path/参数校验/鉴权）
- 集成测试：多 API 组合的业务场景验证，禁止 Mock
- 每模块完成后生成测试报告到 `DevPlan/reports/`
- 遇阻塞写入 `DevPlan/BLOCKED.md`，继续其他模块

**输出：** 完整代码 + 测试文件 + `DevPlan/reports/`
**完成标记：** `[x] Phase 8a`

---

### Phase 8b: 自动持续开发（dev-autopilot 30分钟巡检）

调用 `/dev-autopilot`，设置 30 分钟 cron，自动检查 `DevPlan/*/checklist.md`：

- 发现未完成模块 → 按 dev-executor 标准继续开发
- 遇阻塞 → 记录 `DevPlan/BLOCKED.md` → 继续其他可执行模块
- 所有模块完成 → 更新 checklist → 通知 PM 10 分钟 cron 进入 Phase 9

**输出：** `DevPlan/autopilot.log`（运行记录）
**完成标记：** `[x] Phase 8b`（所有模块 `[x]` 后自动标记）

---

### Phase 9: 技术验收测试

调用 `/release-qa`，以 PRD + Architecture + TechSolution 为基准做全面验收测试（禁止 Mock）。

**输出：** `QA/release-qa-report.md`
**完成标记：** `[x] Phase 9`

---

### Phase 10: 用户验收测试

调用 `/uat-testing`，Playwright E2E 测试核心用户路径。

**输出：** `UAT/uat-report.md`
**完成标记：** `[x] Phase 10`

---

### Phase 11: 安全扫描

调用 `/security-pentest`，扫描 OWASP Top 10。

**输出：** `Security/pentest-report.md`
**完成标记：** `[x] Phase 11`

---

### Phase 12: K8s 部署

调用 `/dev-deploy`，构建镜像 → 推送仓库 → 部署 K8s → 验证。

**输出：** 应用运行在 K8s 集群
**完成标记：** `[x] Phase 12`

---

### Phase 13: 域名映射（Cloudflared Tunnel）

```bash
PROJECT_NAME=$(basename $(pwd))

# 创建 tunnel（已存在则跳过）
cloudflared tunnel list | grep -q "${PROJECT_NAME}" || \
  cloudflared tunnel create "${PROJECT_NAME}"

TUNNEL_ID=$(cloudflared tunnel list | grep "${PROJECT_NAME}" | awk '{print $1}')

# 绑定子域名到 dreamwiseai.com
cloudflared tunnel route dns "${TUNNEL_ID}" "${PROJECT_NAME}.dreamwiseai.com"

# 写配置文件
cat > ~/.cloudflared/config.yml << EOF
tunnel: ${TUNNEL_ID}
credentials-file: ${HOME}/.cloudflared/${TUNNEL_ID}.json
ingress:
  - hostname: ${PROJECT_NAME}.dreamwiseai.com
    service: http://localhost:8080
  - service: http_status:404
EOF

# 端口转发 K8s frontend service（后台运行）
kubectl port-forward -n "${PROJECT_NAME}-prod-frontend" \
  svc/frontend 8080:80 &

# 启动 tunnel（后台运行）
cloudflared tunnel --config ~/.cloudflared/config.yml \
  run "${TUNNEL_ID}" &

echo "✅ 域名已映射: https://${PROJECT_NAME}.dreamwiseai.com"
```

**完成标记：** `[x] Phase 13`

---

## 阻塞处理

遇到需要用户输入时，**不停止**，写入 `ProjectManager/BLOCKED.md` 并继续其他 Phase：

```markdown
## [Phase N] YYYY-MM-DD HH:mm

**需要：** {具体说明需要什么凭据/信息}
**影响：** Phase N 暂停，其他 Phase 继续执行
**解除：** 提供信息后等待下次 cron（10分钟内自动继续）
```

## 完成标准

所有 Phase 标记 `[x]` 且 `BLOCKED.md` 为空 → 输出完成汇报：

```
✅ 项目完成！

产品地址：https://{项目名}.dreamwiseai.com
PRD：      PRD/requirements.md
架构：     Architecture/
技术方案：  TechSolution/
测试报告：  QA/release-qa-report.md
UAT 报告：  UAT/uat-report.md
安全报告：  Security/pentest-report.md
```

## 参考文件

- Master Checklist 模板：`references/master-checklist-template.md`（初始化时复制）
- Cron 脚本：`scripts/setup_pm_cron.sh`（启动时运行）
