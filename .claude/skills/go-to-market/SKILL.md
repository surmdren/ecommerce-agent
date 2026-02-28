---
name: go-to-market
description: 生成海外市场进入(GTM)执行计划，将市场研究和行业知识转化为可执行的上市路线图。输出包括渠道策略矩阵、时间线甘特图、预算分配、每周任务清单、风险应对方案。支持ToB制造业和ToC消费品，覆盖独立站、B2B平台(阿里国际站/中国制造网)、展会、社媒等渠道。适用场景：(1) 产品出海市场拓展 (2) 基于market-research制定执行计划 (3) 渠道选择和预算分配 (4) 制定6-12个月上市路线图。当用户提到"行动计划"、"执行计划"、"出海"、"GTM"、"go-to-market"、"上市计划"、"渠道策略"时触发。
---

# Go-To-Market (GTM) Skill

Transform market insights into executable overseas expansion plans with channel strategies, timelines, budgets, and risk mitigation.

## Overview

This skill generates comprehensive Go-To-Market execution plans for overseas market expansion. It bridges the gap between market research (understanding opportunities) and execution (taking action).

**Workflow Position**:
```
market-research → industry-sales-prep → go-to-market → Execution
(知道机会)     → (学会说话)        → (开始行动)   → (跟踪进度)
```

## Input Requirements

### Required Inputs

1. **Business Context**
   - Product/service description
   - Business model (ToB/ToC)
   - Target market (geography)
   - Budget range
   - Timeline (3/6/12 months)

2. **From Previous Skills** (if available)
   - `market-research` output: industry analysis, opportunities, target customers
   - `industry-sales-prep` output: terminology, customer pain points, value propositions

3. **User Preferences**
   - Priority: quick traction vs brand building
   - Team size and capabilities
   - Risk tolerance

### Optional Inputs
- Existing channels/presence
- Competitor benchmarks
- Special requirements (certifications, compliance)

## Workflow

### Phase 1: Strategy Formulation

**Step 1: Determine Market Entry Strategy**

Based on business model, automatically select appropriate strategy:

**ToB Manufacturing** (e.g., optical equipment, machinery):
- Core channels: Alibaba International, Made-in-China, GlobalSources
- Support channels: Independent website (SEO), LinkedIn, Trade shows
- Sales cycle: 3-6 months, relationship-driven

**ToC Consumer Products**:
- Core channels: Amazon, Shopify独立站, Social media (TikTok/Instagram)
- Support channels: Local e-commerce platforms, Deal sites, KOL partnerships
- Sales cycle: instant to weeks, conversion-driven

**Hybrid/B2B2C**:
- Combine strategies based on customer mix

**Step 2: Channel Selection Matrix**

Use `references/channel-strategies.md` to evaluate channels:

Scoring criteria (1-5 scale):
- Fit with product type
- Startup cost
- Time to first sale
- Scaling potential
- Competition level

Select **3-5 core channels** + **2-3 support channels** based on:
- Budget constraints
- Team capability
- Timeline urgency
- Market characteristics

Consult `references/platform-comparison.md` for detailed platform comparison data.

**Step 3: Timeline and Milestones**

Create 6-12 month roadmap with phases:

**Phase 1: Launch** (Month 1-2)
- Infrastructure setup (domain, email, website)
- Initial channel activation
- Content creation

**Phase 2: Ramp Up** (Month 3-4)
- Traffic acquisition
- Conversion optimization
- Initial sales

**Phase 3: Scale** (Month 5-6+)
- Channel expansion
- Budget reallocation
- Team scaling

Define **key milestones** for each phase (e.g., "First inquiry", "First order", "Break-even").

**Step 4: Infrastructure Setup (Week 1)**

Before activating any channel, set up the basic infrastructure. Use `references/infrastructure-setup.md` for detailed guides.

**Core Infrastructure (Free/Low-Cost)**:

| 基础设施 | 推荐方案 | 成本 | 时间 |
|---------|---------|------|------|
| 域名 | Cloudflare Registrar | $10-15/年 | 30分钟 |
| 企业邮箱 | Zoho Mail Free (5用户) | 免费 | 1小时 |
| 独立站 | Carrd (单页) / Webflow (多页) | 免费-$19/年 | 2-8小时 |
| 询盘表单 | Formspree / Google Forms | 免费 | 30分钟 |
| 即时通讯 | WhatsApp Business | 免费 | 15分钟 |
| 数据分析 | Google Analytics 4 | 免费 | 30分钟 |

**企业邮箱配置要点**:
- 建议账户: sales@, info@, support@
- 配置 SPF/DKIM 防止进垃圾箱
- 备选: Cloudflare Email Routing (仅转发)

**独立站快速搭建路径**:
```
ToB制造业: Carrd单页站(1天) → Webflow多页站(1周) → WordPress完整站
ToC消费品: Shopify试用(14天) → 正式订阅或转WooCommerce
```

**最低预算**: ~$12/年 (域名) + 免费工具 = 完整专业形象

### Step 4.5: UTM 追踪规范（渠道激活前必须完成）

UTM 参数是衡量各渠道真实 ROI 的唯一可靠方式。**在投放任何链接或发布任何渠道内容前，先定义好命名规范**，避免数据污染。

#### UTM 参数说明

| 参数 | 说明 | 命名规范 |
|------|------|---------|
| `utm_source` | 流量来源平台 | 小写，无空格，用 `-` 连接（如 `alibaba`、`google`、`linkedin`）|
| `utm_medium` | 流量媒介类型 | 固定值：`cpc` / `organic` / `email` / `social` / `referral` / `offline` |
| `utm_campaign` | 推广活动名称 | 格式：`年月-主题`（如 `2024q2-spring-sale`）|
| `utm_content` | 区分同一活动的不同创意 | 可选，如 `banner-v1` / `text-ad` |
| `utm_term` | 付费搜索关键词 | 可选，仅 Google Ads 关键词广告使用 |

> **注意**：UTM 参数**大小写敏感**，全部使用小写，空格用 `-` 代替，保持全局一致性。

#### 各渠道标准 UTM 示例

| 渠道 | utm_source | utm_medium | utm_campaign | 示例参数 |
|------|-----------|-----------|--------------|---------|
| 阿里国际站 | `alibaba` | `b2b` | `2024q2-product` | `?utm_source=alibaba&utm_medium=b2b&utm_campaign=2024q2-product` |
| Google Ads | `google` | `cpc` | `2024q2-product` | `?utm_source=google&utm_medium=cpc&utm_campaign=2024q2-product` |
| LinkedIn | `linkedin` | `social` | `2024q2-product` | `?utm_source=linkedin&utm_medium=social&utm_campaign=2024q2-product` |
| TikTok | `tiktok` | `social` | `2024q2-product` | `?utm_source=tiktok&utm_medium=social&utm_campaign=2024q2-product` |
| 邮件营销 | `newsletter` | `email` | `2024q2-product` | `?utm_source=newsletter&utm_medium=email&utm_campaign=2024q2-product` |
| 展会 QR Code | `trade-show` | `offline` | `canton-fair-2024` | `?utm_source=trade-show&utm_medium=offline&utm_campaign=canton-fair-2024` |
| 独立站 SEO | `google` | `organic` | —（不加，SEO 流量自然识别）| — |

#### UTM 链接生成 & 管理

- **生成工具**：Google Campaign URL Builder（批量生成）
- **管理方式**：在 Google Sheet 统一维护所有渠道的 UTM 链接，不同成员用同一份表格
- **短链接**：展会、社媒等场景用 `bit.ly` 或 `short.io` 缩短带 UTM 的长链接

#### 在 Google Analytics 4 中追踪 UTM 数据

GA4 自动识别 UTM 参数，无需额外配置。关键报告路径：
```
报告 → 获客 → 流量获取（Traffic Acquisition）
→ 按 Session source / medium 分组
→ 查看各渠道的转化率和收入贡献
```

### Phase 2: Tactical Planning

**Step 5: Channel Execution Plans**

For each selected channel, generate detailed playbook from `assets/channel-playbooks/`:

Available playbooks:
- `alibaba-international.md` - 阿里巴巴国际站 SOP
- `independent-website.md` - 独立站搭建+SEO
- `trade-shows.md` - 展会参展指南
- `amazon-b2b.md` - 亚马逊B2B运营
- `linkedin-sales.md` - LinkedIn获客
- `google-ads.md` - Google广告投放

Each playbook contains:
- Setup checklist (Week-by-week)
- Optimization tactics
- Budget recommendations
- Common pitfalls
- Success metrics

**Step 6: Budget Allocation**

Use `scripts/budget_calculator.py` (or manual calculation) to allocate budget:

Typical allocation (adjust based on strategy):
- Channel setup: 20-30%
- Marketing/ads: 30-40%
- Content creation: 10-15%
- Personnel: 15-25%
- Contingency: 10-20%

Generate `budget-breakdown.csv` with:
- Category breakdown
- Monthly cash flow projection
- ROI expectations (conservative/base/optimistic)

Consult `assets/budget-templates/budget-spreadsheet.csv` for template.

**Step 7: Risk Identification and Mitigation**

Use `references/risk-mitigation.md` to identify common risks:

Risk categories:
- Channel performance risks (low inquiry volume, poor conversion)
- Market risks (regulation changes, currency fluctuation)
- Operational risks (logistics delays, quality issues)
- Competition risks (price war, IP infringement)

For each identified risk:
- Assess likelihood (Low/Medium/High)
- Assess impact (Low/Medium/High)
- Define mitigation strategies
- Assign owner

Output to `risk-register.md`.

### Phase 3: Output Generation

**Step 8: Generate Main GTM Plan**

Use `assets/gtm-plan-template.md` as base structure, fill in:

1. **Executive Summary**
   - Strategic positioning
   - Channel mix rationale
   - Key milestones
   - Budget overview

2. **Market Analysis Summary**
   - Pull insights from `market-research` output (if available)
   - Target customer profile
   - Competitive landscape

3. **Channel Strategy Matrix**
   - Table: Channel | Priority | Budget | Expected ROI | Timeline | Owner
   - Detailed plan for each core channel
   - Reference to specific playbooks

4. **Timeline Visualization**
   - Generate Mermaid gantt chart using `scripts/timeline_generator.py`
   - Show parallel and sequential activities
   - Highlight key milestones

5. **Budget and ROI Analysis**
   - Budget breakdown table
   - ROI projections (P70/P50/P30 scenarios)
   - Break-even analysis

6. **Risk Register**
   - Risk matrix
   - Mitigation plans
   - Contingency budget allocation

7. **Execution Checklist**
   - Month-by-month tasks
   - Week-by-week breakdown for Month 1-2
   - Responsibility assignments

8. **Vendor/Service Provider List**
   - Recommended tools and platforms
   - Pricing information
   - Integration requirements

**Step 9: Generate Supporting Documents**

Create additional files in `gtm-plan/` directory:

- `gtm-strategy.md` - Main plan document
- `timeline-gantt.md` - Mermaid gantt chart code
- `budget-breakdown.csv` - Detailed budget spreadsheet
- `weekly-tasks.md` - Week-by-week task breakdown (first 3 months), use `assets/weekly-tasks-template.md` as template
- `vendor-list.md` - Service provider contacts and pricing
- `risk-register.md` - Risk log with mitigation plans
- `kpi-dashboard.md` - Metrics tracking template（含各渠道 UTM 归因数据）
- `utm-naming-guide.md` - UTM 命名规范表（所有渠道标准 UTM 参数）

**Step 10: Presentation to User**

Summarize the plan with:
- Top 3 recommended channels and why
- Critical path milestones (what must happen when)
- Budget requirement and expected ROI
- Biggest risks and how to address them
- Next immediate actions (Week 1 checklist)

Offer to:
- Adjust channel mix
- Expand specific channel playbooks
- Modify budget allocation
- Add region-specific considerations

## Output Quality Standards

### Must Include
- ✅ Clear channel selection rationale (why these channels)
- ✅ Realistic timeline with dependencies
- ✅ Budget allocation with ROI projections
- ✅ Actionable week-by-week tasks (at least first month)
- ✅ Risk assessment with mitigation plans
- ✅ Success metrics/KPIs for each channel

### Best Practices
- 🎯 **Specific**: Avoid vague statements like "do marketing" → "Launch P4P campaign with $50/day budget on 5 keywords"
- 📊 **Data-driven**: Include benchmarks (e.g., "Industry average inquiry volume: 20-30/month")
- ⏱️ **Time-bound**: Every task has a deadline or time range
- 💰 **Budget-conscious**: Show cost breakdown and expected returns
- 🔄 **Iterative**: Include review points to adjust strategy

### Avoid
- ❌ One-size-fits-all plans (must adapt to ToB vs ToC)
- ❌ Overly optimistic ROI without risk scenarios
- ❌ Missing dependencies (can't run ads before website is ready)
- ❌ Ignoring local market specifics (regulations, payment methods)
- ❌ No clear owner/responsibility for tasks

## Integration with Other Skills

### Receiving Input from Previous Skills

**From market-research**:
- Industry size and growth → Budget sizing
- Target customer profile → Channel selection
- Competitive landscape → Differentiation strategy
- Identified opportunities → GTM focus areas

**From industry-sales-prep**:
- Product terminology → Content creation keywords
- Customer pain points → Messaging and positioning
- Objection handling → FAQ and sales enablement
- Value propositions → Ad copy and landing pages

### Example Integration

```
User runs market-research on "optical inspection equipment"
↓
Learns: $2B market, 15% CAGR, target customers are LCD panel manufacturers
↓
User runs industry-sales-prep with product manual
↓
Masters: "extinction ratio", "polarizer detection", key value props
↓
User runs go-to-market
↓
Generates: GTM plan with Alibaba International + trade shows + independent website
         Budget: $50K for 6 months
         Timeline: First inquiry Month 1, First order Month 3
         Tasks: Week 1 - Domain registration, product photography
```

## Localization Considerations

For overseas markets, always include:

**North America** (use `references/overseas-expansion-guide.md`):
- English website is mandatory
- Pricing in USD
- PayPal + Credit card payments
- FedEx/UPS logistics
- Sales tax/import duty considerations

**Europe**:
- Multi-language (at minimum English + German)
- GDPR compliance
- CE/RoHS certifications
- VAT registration
- Stripe/local payment methods

**Southeast Asia**:
- Mobile-first approach
- Local e-commerce platforms (Lazada/Shopee)
- COD (Cash on Delivery) popular
- WeChat/WhatsApp for customer service

Consult `references/overseas-expansion-guide.md` for detailed regional playbooks.

## Examples

### Example 1: ToB Manufacturing Equipment

**Input**:
- Product: Polarizer detection system ($50K-100K unit price)
- Budget: $50,000
- Timeline: 12 months
- Target: LCD panel manufacturers in Asia/US

**Output**:
- Core channels: Alibaba International ($5K/year) + independent website ($10K setup) + 2 trade shows ($15K total)
- Phase 1 (M1-3): Platform setup, content creation, first trade show
- Phase 2 (M4-6): Lead nurturing, sample requests, first order target
- Phase 3 (M7-12): Scale leads, add distributors, break-even
- Expected: 50 inquiries, 5 orders, $300K revenue, 5x ROI

### Example 2: ToC Consumer Product

**Input**:
- Product: Smart home gadget ($30-50 unit price)
- Budget: $30,000
- Timeline: 6 months
- Target: US consumers

**Output**:
- Core channels: Amazon ($10K inventory + ads) + TikTok Shop ($5K creator partnerships) + Shopify独立站 ($5K setup + ads)
- Month 1: Amazon listing optimization, first 100 units sold
- Month 2-3: TikTok viral push, Shopify launch
- Month 4-6: Scale winners, cut losers
- Expected: 1000 units, $40K revenue, 1.3x ROI (year 1 reinvestment phase)

## Reference Files

- **Infrastructure Setup**: `references/infrastructure-setup.md` - 免费企业邮箱、独立站搭建指南
- **Channel Strategies**: `references/channel-strategies.md` - Detailed channel pros/cons
- **Platform Comparison**: `references/platform-comparison.md` - Platform comparison table
- **Overseas Guide**: `references/overseas-expansion-guide.md` - Region-specific playbooks
- **Risk Library**: `references/risk-mitigation.md` - Common risks and solutions

## Scripts

- **Budget Calculator**: `scripts/budget_calculator.py` - Calculate budget allocation and ROI
- **Timeline Generator**: `scripts/timeline_generator.py` - Generate Mermaid gantt charts

## Templates

- **GTM Plan**: `assets/gtm-plan-template.md` - Main plan structure
- **Executive Checklist**: `assets/gtm-checklist.md` - One-page execution overview (4 phases, key milestones)
- **Task Tracking**: `assets/weekly-tasks-template.md` - Detailed task tracking (56 tasks across 3 months)
- **Channel Playbooks**: `assets/channel-playbooks/*.md` - Channel-specific SOPs
- **Budget Template**: `assets/budget-templates/budget-spreadsheet.csv` - Budget worksheet

## Important Notes

1. **Adapt to Context**: ToB and ToC require very different strategies - always ask business model if unclear
2. **Be Realistic**: First overseas expansion often breaks even in year 1, profits in year 2+
3. **Start Small**: Better to dominate 2 channels than spread thin across 5
4. **Local Partners**: Consider distributors/agents for complex markets (Japan, Middle East)
5. **Compliance First**: Check certifications (CE/FCC/UL) and regulations before launch
6. **Iterate**: Plan for monthly reviews and quarterly strategy adjustments
