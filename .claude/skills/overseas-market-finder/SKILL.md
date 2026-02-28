---
name: overseas-market-finder
description: 发现海外市场机会的产品调研工具。通过系统化web搜索和三维供需缺口分析，找出高潜力的出海产品机会，评估项目可行性（综合评分≥80分筛选），为海外市场推广和项目决策提供数据支持。适用场景：(1) 寻找出海产品机会 (2) 评估海外市场潜力 (3) 制定海外扩张决策 (4) 识别高综合评分项目。当用户提到"海外市场机会"、"出海产品调研"、"国外市场需求"、"项目可行性评估"、"海外商机发现"时触发。
---

# Overseas Market Finder

发现海外市场中的高潜力产品机会，为出海决策提供数据支持。

## Overview

该 skill 通过系统化调研，帮助识别在海外市场有潜力的产品机会，并进行量化评估：

1. **市场机会发现**：使用 web_search 系统化搜集海外需求数据
2. **供需缺口三维分析**：全球供给 vs 中国生产能力 vs 出口竞争度（核心优势）
3. **多维度评分**：市场规模30% + 竞争25% + 盈利25% + 执行难度20%
4. **综合评分计算**：量化项目机会指数（0-100分），筛选出≥80分的机会
5. **多格式输出**：生成 Markdown 报告、Excel表格、执行摘要

## ⚠️ 强制执行规则（必须遵守）

1. **最低搜索次数**：整个调研至少执行 **25 次 web_search**，每个 Step 有最低要求
2. **评分必须用 scripts 计算**：不允许 AI 主观打分，必须调用 `scripts/market_scorer.py` 和 `scripts/gap_analyzer.py`
3. **数据必须有来源**：每个数字必须标注搜索来源（URL 或报告名），不允许"估算"
4. **搜索结果必须用 web_fetch 深入读取**：对关键搜索结果，用 web_fetch 抓取页面获取具体数据，不能只看搜索摘要
5. **raw_data.json 必须包含每次搜索的原始结果**：query + results + source URL
6. **search_queries.md 必须记录所有已执行的搜索**：不允许列"待搜索"

## Workflow

### Step 1: 明确调研范围

询问用户以下信息：
1. **产品类型**：实体商品 / 数字产品(SaaS) / 服务 / 不限
2. **目标市场**：北美 / 欧洲 / 东南亚 / 全球
3. **行业偏好**：是否有特定行业偏好（可选）
4. **预算范围**：启动资金范围（影响执行难度评估）

### Step 2: 系统化数据搜集

使用 web_search 工具按以下模板搜集数据。

**⚠️ 最低要求：Step 2 至少执行 15 次 web_search，每个子类至少 3 次。对重要结果用 web_fetch 深入读取。**

#### 2.1 市场需求信号（至少 3 次搜索）
```
搜索模板：
"{industry} market trends 2024 2025"
"{product} global demand statistics"
"site:statista.com {product} market size"
"{product} import statistics {country}"
"amazon best sellers {category}"
"google trends {product} {region}"
```

#### 2.2 市场规模数据（至少 4 次搜索）
```
搜索模板：
"{industry} market size forecast {region}"
"site:grandviewresearch.com {product} market"
"site:ibisworld.com {industry} analysis"
"{product} TAM market research 2024"
"{country} import value {hs_code}"
```

**对搜到的市场规模数据，必须用 web_fetch 打开原始页面验证数字。**

#### 2.3 竞争情况分析（至少 3 次搜索）
```
搜索模板：
"{product} manufacturers {country} suppliers"
"top companies {industry} {region}"
"site:alibaba.com {product} suppliers count"
"{product} market share analysis competitors"
"new entrants {industry} barriers"
```

#### 2.4 价格与盈利数据（至少 3 次搜索）
```
搜索模板：
"{product} price range wholesale retail"
"{product} average selling price {region}"
"{product} gross margin industry average"
"{product} manufacturing cost China vs {country}"
```

#### 2.5 行业趋势与政策（至少 2 次搜索）
```
搜索模板：
"{industry} trade policy tariff {country}"
"{product} certification requirements {region}"
"{industry} technology trends forecast"
```

### Step 3: 供需缺口三维分析（核心优势）

**这是最关键的步骤！** 找出"全球缺口 + 中国能力 + 竞争小"的蓝海机会。

**⚠️ 最低要求：Step 3 至少执行 10 次 web_search，每个子类至少 3 次。**

#### 3.1 全球供给集中度分析（至少 3 次搜索）
```
搜索模板：
"{country} exports {product} to {target_market}"
"{product} global suppliers by country"
"UN Comtrade {product} export statistics"
"site:oec.world {product} exporters"
```

**必须获取具体数据**：
- 至少 3 个主要供应国的出口金额（用 web_fetch 从 OEC 或 UN Comtrade 获取）
- 计算各国市场份额，用 `scripts/gap_analyzer.py` 的 `calculate_hhi()` 计算 HHI 指数
- HHI指数：<0.15分散市场（好机会），>0.25寡头市场（有壁垒）
- 前3大供应商占比：<50%为分散，>70%为集中

#### 3.2 中国生产能力验证（至少 4 次搜索）
```
搜索模板：
"China {product} manufacturers directory"
"site:alibaba.com {product} suppliers China"
"中国{产品}生产商 产能 统计"
"{product} manufacturing capacity China vs global"
"China {industry} production statistics"
"site:made-in-china.com {product} suppliers"
```

**必须获取具体数字**：
- 阿里巴巴国际站供应商数量（用 web_fetch 抓取搜索结果页）
- 中国制造网供应商数量
- 国内生产商总数估算（>100家=强，10-100=中，<10=弱）
- 产能水平（leading/high/medium/low）

#### 3.3 中国出口竞争度评估（至少 3 次搜索）
```
搜索模板：
"China {product} exporters list"
"Chinese companies exporting {product}"
"China {product} export statistics by company"
"{product} Chinese suppliers overseas market"
"中国{产品}出口企业 数量"
```

**必须计算出口渗透率**：
- 出口渗透率 = 实际出口商 / 国内总生产商
- 用 `scripts/gap_analyzer.py` 的 `score_china_competition()` 计算得分
- <10%：蓝海市场 ✅✅✅ | 10-30%：竞争较小 ✅ | >50%：红海 ❌

### Step 4: 机会识别与数据整理

对每个发现的产品机会，整理以下信息：
```
opportunity = {
    'product_name': '产品名称',
    'industry': '所属行业',
    'target_market': '目标市场',
    
    # 市场规模维度
    'tam_usd': 总可寻址市场规模（美元）,
    'growth_rate': 年增长率（小数），
    
    # 竞争维度
    'num_competitors': 主要竞争对手数量,
    'market_concentration': 'fragmented/competitive/oligopoly',
    
    # 盈利维度
    'avg_order_value': 平均客单价（美元）,
    'gross_margin': 毛利率（小数）,
    'payback_months': CAC回本周期（月）,
    
    # 执行难度维度
    'tech_barrier': 'low/medium/high',
    'regulatory_complexity': 'low/medium/high',
    'resource_requirement': 'low/medium/high'
}
```

### Step 5: 综合评分计算

**⚠️ 必须调用 scripts 计算，不允许 AI 主观打分！**

用 Python 执行 `scripts/market_scorer.py`：

```python
import sys
sys.path.insert(0, '/path/to/overseas-market-finder/scripts')
from market_scorer import MarketScorer

scorer = MarketScorer()
result = scorer.score_opportunity({
    'product_name': '产品名',
    'industry': '行业',
    'segment': '细分',
    'tam_usd': 从Step2搜到的数字,
    'growth_rate': 从Step2搜到的数字,
    'num_competitors': 从Step2搜到的数字,
    'market_concentration': 'fragmented/competitive/oligopoly',
    'avg_order_value': 从Step2搜到的数字,
    'gross_margin': 从Step2搜到的数字,
    'payback_months': 从Step2搜到的数字,
    'tech_barrier': 'low/medium/high',
    'regulatory_complexity': 'low/medium/high',
    'resource_requirement': 'low/medium/high'
})
print(result)  # 包含 scores 和 success_rate
```

同样用 `scripts/gap_analyzer.py` 计算供需缺口：

```python
from gap_analyzer import SupplyDemandGapAnalyzer

analyzer = SupplyDemandGapAnalyzer()
gap_result = analyzer.analyze_opportunity({
    'product_name': '产品名',
    'hs_code': 'HS编码',
    'target_market': '目标市场',
    'import_value_usd': 从Step3搜到的进口总额,
    'import_by_country': {'Country': value_usd, ...},  # 从Step3搜到的各国数据
    'growth_rate': 增长率,
    'china_manufacturers': 中国生产商数量,
    'china_exporters': 中国出口商数量,
    'china_production_capacity': 'low/medium/high/leading'
})
print(gap_result)  # 包含 opportunity_index
```

**评分标准**：
- **85-100分**：⭐⭐⭐⭐⭐ 强烈推荐（立即进入）
- **80-84分**：⭐⭐⭐⭐ 推荐（优先考虑）
- **70-79分**：⭐⭐⭐ 可以考虑（需验证）
- **60-69分**：⭐⭐ 谨慎评估（有风险）
- **<60分**：⭐ 不建议（风险高）

### Step 6: 风险评估

**⚠️ 必须调用 `scripts/risk_assessor.py` 计算，不允许 AI 主观打分！**

```python
from risk_assessor import RiskAssessor

assessor = RiskAssessor()
risk_result = assessor.assess_opportunity({...})
```

四维度风险评估：
- **政策风险**：关税、贸易战、进口限制
- **运营风险**：汇率、物流、账期
- **合规风险**：知识产权、认证、监管
- **市场风险**：文化适配、竞争、品牌壁垒

### Step 7: 生成调研报告

#### 7.1 创建输出目录

输出到**当前项目目录**下新建的 `market-research/` 子目录：`{project_dir}/market-research/{industry}_YYYYMMDD/`

**目录结构**：
```
{project_dir}/market-research/{industry}_YYYYMMDD/
├── report.md              # 完整分析报告
├── executive_summary.md   # 一页纸决策摘要
├── dashboard.html         # 交互式决策面板（浏览器打开）
├── opportunities.xlsx     # Excel数据表（如果openpyxl可用）
├── opportunities.csv      # CSV备选
└── data/                  # 原始搜索数据备份
    ├── search_queries.md
    └── raw_data.json
```

**注意**：`{project_dir}` 为调用此 skill 时的当前工作目录。如果 `market-research/` 子目录不存在，首次执行时会自动创建。

#### 7.2 报告内容结构

**report.md**：
```markdown
# 海外市场机会调研报告

## 执行摘要
- 筛选出 X 个高潜力机会（综合评分 ≥80分）
- TOP 3 推荐：[按评分排序]
- 总体机会评估

## 高潜力机会清单（≥80分）

### 1. [产品名称] - 综合评分 XX分

**基本信息**：行业、市场、HS编码

**供需缺口分析**：
- 全球供给分散度：[HHI指数]
- 中国生产能力：[强/中/弱]
- 中国出口竞争度：[渗透率%]

**四维度评分**：
- 市场规模：XX/100
- 竞争强度：XX/100
- 盈利能力：XX/100
- 执行难度：XX/100

**风险评估**：政策/运营/合规/市场风险分析

**推荐理由**：3-5个关键优势
**执行建议**：具体行动计划

---
[重复结构列出所有≥80分机会]
```

**executive_summary.md**：
```markdown
# 海外市场机会 - 决策摘要

**调研时间**：YYYY-MM-DD
**目标市场**：[具体市场]
**调研范围**：[行业/产品类型]

## 核心发现

✅ **强烈推荐（≥85分）**：X个
- [产品A]：XX分 - [一句话优势]
- [产品B]：XX分 - [一句话优势]

⚠️ **值得考虑（80-84分）**：X个

## 决策建议

**立即行动**：[最高分产品]
**深入调研**：[需验证产品]  
**暂缓进入**：[风险过高产品]

**总体判断**：[整体机会评估]
```

#### 7.x 生成交互式 Dashboard

读取 `assets/templates/dashboard-template.html` 模板，将所有机会数据组装成 JSON 并替换模板中的 `__DASHBOARD_DATA_PLACEHOLDER__` 占位符。

**数据结构**：
```javascript
{
  "meta": {
    "title": "海外市场机会调研 - {industry}",
    "industry": "{industry}",
    "target_market": "{target_market}",
    "generated_at": "YYYY-MM-DD",
    "total_opportunities": N,
    "high_potential_count": N
  },
  "opportunities": [
    {
      "name": "产品名",
      "industry": "行业",
      "segment": "细分",
      "target_market": "目标市场",
      "scores": { "market_size": 85, "competition": 72, "profitability": 90, "execution": 68 },
      "composite_score": 81.5,
      "gap_analysis": { "hhi_index": 0.15, "china_capability": 80, "export_penetration": 0.08 },
      "risks": { "policy": 70, "operations": 85, "compliance": 60, "market": 75 },
      "mvp": { "recommended_budget": "low", "method": "验证方法描述", "timeline": "4-8周" }
    }
  ]
}
```

生成步骤：
1. 读取 dashboard 模板文件
2. 将所有机会数据按上述结构组装为 JSON
3. 替换 `__DASHBOARD_DATA_PLACEHOLDER__` 为实际 JSON
4. 写入 `dashboard.html`

Dashboard 包含 7 个模块：总览卡片、机会矩阵气泡图、四维雷达图、供需缺口面板、风险热力图、评分排行榜、MVP验证建议。浏览器直接打开即可使用。

### Step 8: MVP验证方案（可选）

使用 `scripts/mvp_planner.py` 针对高分机会生成验证计划：

**三个预算等级**：
- **低成本验证**（<$5K）：阿里巴巴询盘测试、社媒广告
- **中成本验证**（$5K-$20K）：样品+Amazon FBA测试
- **高成本验证**（$20K-$50K）：独立站全渠道运营

## 搜索策略指南

### 数据源优先级
1. **官方统计**：各国海关、UN Comtrade、ASEANstats
2. **商业数据库**：Statista、IBISWorld、Grand View Research
3. **B2B平台**：阿里巴巴国际站、中国制造网、Global Sources
4. **电商数据**：Amazon Best Sellers、Google Trends
5. **行业报告**：McKinsey、Deloitte、行业协会

### 搜索技巧
- 使用 `site:` 限定数据源网站
- 组合使用英文和中文关键词
- 关注最新数据（2024-2025年）
- 交叉验证多个数据源

## 评分算法说明

综合评分 = 市场规模得分×30% + 竞争强度得分×25% + 盈利能力得分×25% + 执行难度得分×20%

供需缺口加权：如果发现明显供需缺口（全球HHI<0.15且中国出口渗透率<10%），在综合评分基础上+10-15分。

## Notes

- **数据时效性**：优先使用2024-2025年数据
- **汇率影响**：所有金额换算为USD
- **本地化**：考虑目标市场文化差异
- **合规性**：重点关注高监管行业（食品、医疗、金融）

## Related Skills

- `market-research`: 深度分析特定行业
- `go-to-market`: 制定GTM计划
- `competitor-analysis`: 详细竞品分析