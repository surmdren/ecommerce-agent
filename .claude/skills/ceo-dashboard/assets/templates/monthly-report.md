# 管理层月报

> **月份**: {month}
> **生成时间**: {generated_at}

---

## 执行摘要

{executive_summary}

### 本月亮点
1. {highlight_1}
2. {highlight_2}
3. {highlight_3}

### 需关注事项
1. {concern_1}
2. {concern_2}

---

## 财务报告

### 损益概览
| 科目 | 本月 | 上月 | 同比 | 预算 | 预算完成率 |
|------|------|------|------|------|-----------|
| 收入 | {revenue} | {last_revenue} | {yoy_revenue} | {budget_revenue} | {pct_revenue} |
| 成本 | {cost} | {last_cost} | {yoy_cost} | {budget_cost} | {pct_cost} |
| 毛利 | {gross_profit} | {last_gp} | {yoy_gp} | {budget_gp} | {pct_gp} |
| 费用 | {opex} | {last_opex} | {yoy_opex} | {budget_opex} | {pct_opex} |
| 净利润 | {net_profit} | {last_np} | {yoy_np} | {budget_np} | {pct_np} |

### 现金流
```mermaid
xychart-beta
    title "月度现金流趋势"
    x-axis [Jan, Feb, Mar, Apr, May, Jun]
    y-axis "金额 (万元)" 0 --> 200
    bar [65, 78, 52, 85, 92, {current_month}]
    line [50, 55, 60, 65, 70, {target_line}]
```

### 支出分布
```mermaid
pie title 本月支出构成
    "人力成本" : {hr_cost_pct}
    "运营费用" : {ops_cost_pct}
    "营销推广" : {marketing_cost_pct}
    "研发投入" : {rd_cost_pct}
    "其他" : {other_cost_pct}
```

---

## 项目进度

### 进行中项目

| 项目 | 启动日期 | 预计完成 | 当前进度 | 状态 | 预算消耗 |
|------|---------|---------|---------|------|---------|
| {project_1} | {p1_start} | {p1_end} | {p1_progress} | {p1_status} | {p1_budget} |
| {project_2} | {p2_start} | {p2_end} | {p2_progress} | {p2_status} | {p2_budget} |

### 项目甘特图
```mermaid
gantt
    title 项目时间线
    dateFormat YYYY-MM-DD
    section {project_1}
    {p1_phase1}     :{p1_phase1_status}, {p1_phase1_start}, {p1_phase1_end}
    {p1_phase2}     :{p1_phase2_status}, {p1_phase2_start}, {p1_phase2_end}
    section {project_2}
    {p2_phase1}     :{p2_phase1_status}, {p2_phase1_start}, {p2_phase1_end}
```

### 本月里程碑
- ✅ {milestone_completed_1}
- ✅ {milestone_completed_2}
- ⏳ {milestone_pending_1} (预计: {milestone_pending_1_date})

---

## OKR 进度 ({okr_period})

### 整体完成度
```
O1: {o1_name}  {o1_bar} {o1_pct}%
O2: {o2_name}  {o2_bar} {o2_pct}%
O3: {o3_name}  {o3_bar} {o3_pct}%
```

### 详细进度

#### O1: {o1_name}

| Key Result | 目标 | 当前 | 进度 | 趋势 |
|------------|------|------|------|------|
| {kr1_1} | {kr1_1_target} | {kr1_1_actual} | {kr1_1_pct} | {kr1_1_trend} |
| {kr1_2} | {kr1_2_target} | {kr1_2_actual} | {kr1_2_pct} | {kr1_2_trend} |

**分析**: {o1_analysis}

---

## 团队状况

### 人员概况
| 部门 | 人数 | 本月变动 | 招聘中 |
|------|------|---------|--------|
| 研发 | {dev_count} | {dev_change} | {dev_hiring} |
| 销售 | {sales_count} | {sales_change} | {sales_hiring} |
| 运营 | {ops_count} | {ops_change} | {ops_hiring} |
| **合计** | **{total_count}** | **{total_change}** | **{total_hiring}** |

### 关键岗位
| 岗位 | 状态 | 备注 |
|------|------|------|
| {key_role_1} | {key_role_1_status} | {key_role_1_note} |
| {key_role_2} | {key_role_2_status} | {key_role_2_note} |

---

## 风险登记

### 风险矩阵
```
        │  低影响  │  中影响  │  高影响
────────┼──────────┼──────────┼──────────
高可能性│          │          │ {high_high}
中可能性│          │ {med_med}│ {med_high}
低可能性│ {low_low}│          │
```

### Top 3 风险

| 排名 | 风险 | 类别 | 影响 | 应对措施 | 负责人 | 状态 |
|------|------|------|------|---------|--------|------|
| 1 | {risk_1} | {risk_1_cat} | {risk_1_impact} | {risk_1_action} | {risk_1_owner} | {risk_1_status} |
| 2 | {risk_2} | {risk_2_cat} | {risk_2_impact} | {risk_2_action} | {risk_2_owner} | {risk_2_status} |
| 3 | {risk_3} | {risk_3_cat} | {risk_3_impact} | {risk_3_action} | {risk_3_owner} | {risk_3_status} |

---

## 重要决策

| 日期 | 议题 | 决定 | 后续行动 | 状态 |
|------|------|------|---------|------|
| {decision_1_date} | {decision_1_topic} | {decision_1_result} | {decision_1_action} | {decision_1_status} |
| {decision_2_date} | {decision_2_topic} | {decision_2_result} | {decision_2_action} | {decision_2_status} |

---

## 下月计划

### 关键目标
1. {next_goal_1}
2. {next_goal_2}
3. {next_goal_3}

### 重要事件
| 日期 | 事件 | 负责人 |
|------|------|--------|
| {event_1_date} | {event_1} | {event_1_owner} |
| {event_2_date} | {event_2} | {event_2_owner} |

### 预算预览
- 预计收入: {next_revenue}
- 预计支出: {next_expense}
- 重大支出: {major_expense}

---

## 附录

### 财务明细
[详见财务附表]

### 项目详情
[详见项目管理系统]

---

*本报告由 CEO Dashboard 自动生成*
*如有疑问请联系: {contact}*
