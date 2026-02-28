# Project Manager - Master Checklist
# 项目名称: {PROJECT_NAME}
# 创建时间: {YYYY-MM-DD HH:mm}

## 进度总览

| Phase | 状态 | 完成时间 | 输出产物 |
|-------|------|----------|----------|
| Phase 1: PRD | [ ] | - | PRD/requirements.md |
| Phase 2: 架构图 | [ ] | - | Architecture/ |
| Phase 3: 技术方案 | [ ] | - | TechSolution/ |
| Phase 4: 设计系统 | [ ] | - | Design/design-system.md |
| Phase 5: 页面设计 | [ ] | - | Design/pages/ |
| Phase 6: 开发规划 | [ ] | - | DevPlan/ |
| Phase 7: 基础设施 | [ ] | - | infrastructure/ |
| Phase 8a: 开发实现(dev-executor) | [ ] | - | src/ + DevPlan/reports/ |
| Phase 8b: 自动巡检(dev-autopilot) | [ ] | - | DevPlan/autopilot.log |
| Phase 9: 技术验收 | [ ] | - | QA/release-qa-report.md |
| Phase 10: UAT | [ ] | - | UAT/uat-report.md |
| Phase 11: 安全扫描 | [ ] | - | Security/pentest-report.md |
| Phase 12: K8s 部署 | [ ] | - | - |
| Phase 13: 域名映射 | [ ] | - | {PROJECT_NAME}.wise-optics.com |

---

## 详细 Checklist

### [ ] Phase 1: 需求分析 → PRD
- [ ] 执行 /requirement-detail
- [ ] 生成 PRD/requirements.md
- [ ] 包含 8 个章节（背景/用户/范围/流程/功能/非功能/风险/迭代）

### [ ] Phase 2: 架构设计
- [ ] 执行 /tech-architecture
- [ ] 生成业务架构图
- [ ] 生成技术架构图
- [ ] 生成系统架构图
- [ ] 生成模块依赖图
- [ ] 生成数据流图
- [ ] 生成 API 架构图

### [ ] Phase 3: 技术方案
- [ ] 执行 /tech-solution
- [ ] 技术选型确定（前端/后端/数据库）
- [ ] 项目结构定义
- [ ] ER 图 + 表结构设计
- [ ] API 设计规范
- [ ] K8s 部署方案
- [ ] 成本估算

### [ ] Phase 4: 设计系统（Step 1）
- [ ] 执行 /ui-ux-pro-max（设计系统规范模式）
- [ ] 色彩体系定义
- [ ] 字体方案定义
- [ ] 核心组件样式定义
- [ ] 间距/圆角/阴影规范
- [ ] 输出 Design/design-system.md

### [ ] Phase 5: 页面设计（Step 2）
- [ ] 执行 /uiux-design（基于设计系统）
- [ ] 每个功能模块有对应页面设计文档
- [ ] 包含 UX Pilot 提示词
- [ ] 输出到 Design/pages/

### [ ] Phase 6: 开发规划
- [ ] 执行 /dev-planner
- [ ] 生成 DevPlan/checklist.md
- [ ] 每个模块有独立 md 文档
- [ ] 模块依赖关系清晰

### [ ] Phase 7: 基础设施
- [ ] 判断是否需要（检查 TechSolution/）
- [ ] 执行 /infrastructure-provisioner（需要时）
- [ ] 生成 infrastructure/ 目录
- [ ] 生成 .env 文件（加入 .gitignore）

### [ ] Phase 8a: 开发实现（dev-executor）
- [ ] 执行 /dev-executor 逐模块开发
- [ ] TDD：先写测试，再写代码（Red→Green→Refactor）
- [ ] 单元测试覆盖率 > 80%
- [ ] API 测试：真实接口，禁止 Mock，2-5 用例/接口
- [ ] 集成测试：多 API 业务场景，禁止 Mock
- [ ] DevPlan/reports/ 测试报告生成

### [ ] Phase 8b: 自动持续开发（dev-autopilot）
- [ ] 执行 /dev-autopilot 设置 30 分钟 cron
- [ ] 所有模块 checklist 标记 [x]
- [ ] DevPlan/autopilot.log 记录运行状态

### [ ] Phase 9: 技术验收测试
- [ ] 执行 /release-qa
- [ ] 功能完整性验证通过
- [ ] 技术正确性验证通过
- [ ] 数据流转正确性验证通过
- [ ] 生成 QA/release-qa-report.md

### [ ] Phase 10: 用户验收测试
- [ ] 执行 /uat-testing
- [ ] 核心用户路径 E2E 测试通过
- [ ] 生成 UAT/uat-report.md

### [ ] Phase 11: 安全扫描
- [ ] 执行 /security-pentest
- [ ] OWASP Top 10 检查通过
- [ ] 无高危漏洞
- [ ] 生成 Security/pentest-report.md

### [ ] Phase 12: K8s 部署
- [ ] 执行 /dev-deploy
- [ ] 镜像构建成功
- [ ] 镜像推送到仓库
- [ ] K8s Deployment 更新
- [ ] 数据库迁移完成
- [ ] 健康检查通过

### [ ] Phase 13: 域名映射
- [ ] cloudflared tunnel 创建
- [ ] DNS 路由绑定 wise-optics.com
- [ ] kubectl port-forward 运行中
- [ ] tunnel 运行中
- [ ] https://{PROJECT_NAME}.wise-optics.com 可访问

---

## 阻塞记录

> 此处记录所有阻塞项（或参见 ProjectManager/BLOCKED.md）

无

---

## 运行日志

> Cron job 自动追加到此处

```
{YYYY-MM-DD HH:mm} - PM Cron 启动，检查 checklist...
```
