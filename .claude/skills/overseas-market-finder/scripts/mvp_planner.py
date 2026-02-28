#!/usr/bin/env python3
"""
MVP Validation Plan Generator

Generate minimum viable product testing plans across different budget levels
to validate market opportunities before full-scale investment.
"""

from typing import Dict, List
from datetime import datetime, timedelta


class MVPPlanner:
    """Generate MVP validation plans for market opportunities"""

    def __init__(self):
        self.budget_tiers = {
            'low': 5000,      # <$5K
            'medium': 15000,  # $5K-$20K
            'high': 50000     # $20K+
        }

    def generate_low_cost_plan(self, opportunity: Dict) -> Dict:
        """
        Generate low-cost validation plan (<$5K)

        Args:
            opportunity: Market opportunity data

        Returns:
            Low-cost validation plan
        """
        product_type = opportunity.get('product_type', 'physical')
        target_market = opportunity.get('target_market', '')

        plan = {
            'budget': '<$5,000',
            'duration': '4-8 weeks',
            'objective': '验证市场需求和产品概念',
            'methods': []
        }

        if product_type == 'physical':
            plan['methods'] = [
                {
                    'method': '阿里巴巴国际站询盘测试',
                    'cost': '$500-1,000',
                    'duration': '2-4 weeks',
                    'steps': [
                        '创建基础店铺页面',
                        '上传产品图片和描述（可使用供应商资料）',
                        '设置竞争力价格',
                        '监测询盘数量和质量'
                    ],
                    'success_criteria': '每周获得 5+ 有效询盘',
                    'kpis': ['询盘量', '询盘转化率', '目标市场占比']
                },
                {
                    'method': '社交媒体广告测试',
                    'cost': '$1,000-2,000',
                    'duration': '2 weeks',
                    'steps': [
                        '制作产品视频/图片素材',
                        '投放 Facebook/Instagram 广告（目标市场）',
                        '设置落地页收集意向客户',
                        '分析 CTR、CPC、转化率'
                    ],
                    'success_criteria': 'CTR ≥2%, CPC <$1, 转化率 ≥5%',
                    'kpis': ['CTR', 'CPC', '落地页转化率', 'CPL（每线索成本）']
                },
                {
                    'method': '众筹平台可行性测试',
                    'cost': '$500-1,500',
                    'duration': '4 weeks',
                    'steps': [
                        '准备 Kickstarter/Indiegogo 项目页面',
                        '拍摄产品演示视频',
                        '设置早鸟价格',
                        '观察预订量和用户反馈'
                    ],
                    'success_criteria': '30天内获得 50+ 预订',
                    'kpis': ['预订量', '平均客单价', '用户评论质量']
                }
            ]

        elif product_type == 'saas':
            plan['methods'] = [
                {
                    'method': 'Landing Page + Waitlist',
                    'cost': '$500-1,000',
                    'duration': '2 weeks',
                    'steps': [
                        '使用 Webflow/Carrd 搭建落地页',
                        '描述产品价值主张',
                        '设置邮件收集表单',
                        '投放小额 Google Ads'
                    ],
                    'success_criteria': '收集 100+ 邮箱，10%+ 转化率',
                    'kpis': ['访问量', '邮箱转化率', '用户来源']
                },
                {
                    'method': 'Product Hunt 发布测试',
                    'cost': '$200-500',
                    'duration': '1 week',
                    'steps': [
                        '准备 Product Hunt 发布资料',
                        '邀请早期用户投票',
                        '收集用户反馈和评论',
                        '分析用户画像'
                    ],
                    'success_criteria': '进入当日 TOP 10，获得 50+ upvotes',
                    'kpis': ['Upvotes', '评论数', '外部访问量']
                }
            ]

        plan['total_estimated_cost'] = '$2,000-4,500'
        plan['risk_level'] = '低风险 ✅'
        plan['recommendation'] = '适合快速验证概念，风险极小'

        return plan

    def generate_medium_cost_plan(self, opportunity: Dict) -> Dict:
        """
        Generate medium-cost validation plan ($5K-$20K)

        Args:
            opportunity: Market opportunity data

        Returns:
            Medium-cost validation plan
        """
        product_type = opportunity.get('product_type', 'physical')

        plan = {
            'budget': '$5,000-$20,000',
            'duration': '8-12 weeks',
            'objective': '小规模实际销售验证',
            'methods': []
        }

        if product_type == 'physical':
            plan['methods'] = [
                {
                    'method': '小批量样品生产 + Amazon FBA 测试',
                    'cost': '$8,000-15,000',
                    'duration': '8-12 weeks',
                    'steps': [
                        '订购 50-100 件样品（含模具费）',
                        '注册 Amazon 卖家账号',
                        '发货到 FBA 仓库',
                        '优化 Listing（标题、图片、A+页面）',
                        '投放 Amazon PPC 广告',
                        '运营 3 个月，收集销售数据'
                    ],
                    'success_criteria': '月销量 ≥30 件，评分 ≥4.0 星',
                    'kpis': ['销量', 'BSR排名', '转化率', 'ACOS', '评论评分']
                },
                {
                    'method': '行业展会参展（小展位）',
                    'cost': '$5,000-10,000',
                    'duration': '1 week + 准备',
                    'steps': [
                        '选择目标市场行业展会（Canton Fair, CES）',
                        '租赁小展位（9㎡）',
                        '准备样品和宣传资料',
                        '现场收集买家名片和意向订单',
                        '展后跟进潜在客户'
                    ],
                    'success_criteria': '收集 50+ 有效买家联系方式，获得 3+ 试订单',
                    'kpis': ['收集名片数', '意向订单', '现场成交额']
                }
            ]

        elif product_type == 'saas':
            plan['methods'] = [
                {
                    'method': 'MVP 产品开发 + Beta 测试',
                    'cost': '$10,000-18,000',
                    'duration': '8-12 weeks',
                    'steps': [
                        '开发核心功能 MVP（外包或自研）',
                        '招募 20-50 名 Beta 用户',
                        '运营 2 个月，收集反馈',
                        '迭代优化产品',
                        '测试定价策略（Freemium/付费）'
                    ],
                    'success_criteria': 'Beta 用户留存率 ≥40%，10%+ 付费转化',
                    'kpis': ['DAU/MAU', '留存率', 'NPS', '付费转化率']
                }
            ]

        plan['total_estimated_cost'] = '$13,000-18,000'
        plan['risk_level'] = '中等风险 ⚠️'
        plan['recommendation'] = '适合验证商业模式，有一定资金投入'

        return plan

    def generate_high_cost_plan(self, opportunity: Dict) -> Dict:
        """
        Generate high-cost validation plan ($20K+)

        Args:
            opportunity: Market opportunity data

        Returns:
            High-cost validation plan
        """
        product_type = opportunity.get('product_type', 'physical')

        plan = {
            'budget': '$20,000-$50,000',
            'duration': '3-6 months',
            'objective': '规模化验证和市场渗透',
            'methods': []
        }

        if product_type == 'physical':
            plan['methods'] = [
                {
                    'method': '独立站 + Google Ads 全渠道运营',
                    'cost': '$25,000-40,000',
                    'duration': '3-6 months',
                    'steps': [
                        '搭建 Shopify 独立站（$3K）',
                        '海外仓备货 500-1000 件（$15K）',
                        '聘请海外营销团队（$5K/月 x 3月）',
                        '投放 Google Ads + Facebook Ads（$5K/月 x 3月）',
                        '运营社交媒体（Instagram, TikTok）',
                        '收集用户数据，优化转化漏斗'
                    ],
                    'success_criteria': '月销售额 ≥$20K，ROAS ≥3.0',
                    'kpis': ['GMV', 'ROAS', '重复购买率', 'LTV/CAC']
                },
                {
                    'method': 'B2B 平台旗舰店运营',
                    'cost': '$20,000-30,000',
                    'duration': '6 months',
                    'steps': [
                        '开通阿里巴巴国际站旗舰店（$5K/年）',
                        '拍摄专业产品视频和图片（$3K）',
                        '招聘外贸业务员（$3K/月 x 6月）',
                        '参加平台活动和推广（$2K/月）',
                        '处理询盘和样品订单'
                    ],
                    'success_criteria': '月询盘 ≥100 个，成单率 ≥5%',
                    'kpis': ['询盘量', '成单率', '客单价', '复购率']
                }
            ]

        elif product_type == 'saas':
            plan['methods'] = [
                {
                    'method': '完整产品上线 + Growth Hacking',
                    'cost': '$30,000-50,000',
                    'duration': '6 months',
                    'steps': [
                        '完整产品开发（$20K）',
                        '招聘 Growth Hacker（$5K/月 x 3月）',
                        '多渠道获客（SEO, SEM, Content, Partnership）',
                        '建立客户成功团队',
                        '数据分析和增长实验'
                    ],
                    'success_criteria': 'MRR ≥$10K，月增长率 ≥20%',
                    'kpis': ['MRR', 'CAC', 'LTV', 'Churn Rate', '增长率']
                }
            ]

        plan['total_estimated_cost'] = '$35,000-45,000'
        plan['risk_level'] = '较高风险 ⚠️⚠️'
        plan['recommendation'] = '适合已完成初步验证，准备规模化的项目'

        return plan

    def generate_validation_plan(self, opportunity: Dict, budget_level: str = 'low') -> Dict:
        """
        Generate complete MVP validation plan

        Args:
            opportunity: Market opportunity data
            budget_level: 'low', 'medium', or 'high'

        Returns:
            Complete validation plan
        """
        if budget_level == 'low':
            plan = self.generate_low_cost_plan(opportunity)
        elif budget_level == 'medium':
            plan = self.generate_medium_cost_plan(opportunity)
        elif budget_level == 'high':
            plan = self.generate_high_cost_plan(opportunity)
        else:
            raise ValueError("budget_level must be 'low', 'medium', or 'high'")

        # Add common elements
        plan['product'] = opportunity.get('product_name', 'Unknown')
        plan['target_market'] = opportunity.get('target_market', 'Unknown')
        plan['generated_at'] = datetime.now().isoformat()

        # Add timeline
        plan['timeline'] = self._generate_timeline(plan)

        # Add decision framework
        plan['decision_criteria'] = self._generate_decision_criteria(budget_level)

        return plan

    def _generate_timeline(self, plan: Dict) -> List[Dict]:
        """Generate week-by-week timeline"""
        duration_weeks = int(plan['duration'].split('-')[0])  # Get min weeks

        timeline = []
        start_date = datetime.now()

        for week in range(1, min(duration_weeks + 1, 13)):  # Max 12 weeks
            week_start = start_date + timedelta(weeks=week - 1)
            milestone = self._get_milestone(week, plan['methods'][0] if plan['methods'] else {})

            timeline.append({
                'week': week,
                'date': week_start.strftime('%Y-%m-%d'),
                'milestone': milestone
            })

        return timeline

    def _get_milestone(self, week: int, method: Dict) -> str:
        """Get milestone for specific week"""
        if week <= 2:
            return '准备阶段：搭建基础设施、制作素材'
        elif week <= 4:
            return '启动阶段：开始测试、收集初步数据'
        elif week <= 8:
            return '优化阶段：分析数据、调整策略'
        else:
            return '评估阶段：总结结果、做出决策'

    def _generate_decision_criteria(self, budget_level: str) -> Dict:
        """Generate go/no-go decision criteria"""
        if budget_level == 'low':
            return {
                'go_criteria': [
                    '询盘量或转化率达标',
                    '用户反馈积极（NPS ≥50）',
                    '初步验证产品市场契合度'
                ],
                'no_go_criteria': [
                    '完全无人问津（0 询盘/转化）',
                    '用户反馈极差',
                    '发现致命缺陷（法律、技术）'
                ],
                'pivot_criteria': [
                    '有兴趣但需求点不同',
                    '目标市场错位',
                    '定价策略需调整'
                ]
            }
        elif budget_level == 'medium':
            return {
                'go_criteria': [
                    '销量达标（月销 ≥30 件 或 MRR ≥$5K）',
                    '用户留存率 ≥40%',
                    '单位经济模型健康（LTV/CAC ≥3）'
                ],
                'no_go_criteria': [
                    '销量极低（<10 件/月）',
                    '用户流失率 >70%',
                    '无法找到产品市场契合点'
                ],
                'pivot_criteria': [
                    '销量一般但用户粘性强',
                    '特定细分市场表现突出',
                    '需要调整商业模式'
                ]
            }
        else:  # high
            return {
                'go_criteria': [
                    '月销售额 ≥$20K 或 MRR ≥$10K',
                    '增长曲线健康（月增长 ≥15%）',
                    'ROAS ≥3.0 或 CAC回本周期 <12 月'
                ],
                'no_go_criteria': [
                    '持续亏损无改善',
                    '市场天花板已现',
                    '竞争加剧无法突围'
                ],
                'pivot_criteria': [
                    '渠道或产品需调整',
                    '目标客群需重新定位',
                    '商业模式需转型'
                ]
            }

    def generate_report(self, plan: Dict) -> str:
        """
        Generate markdown MVP validation report

        Args:
            plan: Validation plan data

        Returns:
            Markdown formatted report
        """
        report = f"""# MVP 验证计划

**产品**: {plan['product']}
**目标市场**: {plan['target_market']}
**预算等级**: {plan['budget']}
**验证周期**: {plan['duration']}

---

## 验证目标

{plan['objective']}

---

## 验证方法

"""

        for idx, method in enumerate(plan['methods'], 1):
            report += f"""### 方法 {idx}: {method['method']}

**预算**: {method['cost']}
**周期**: {method['duration']}

**执行步骤**:
"""
            for step in method['steps']:
                report += f"{idx}. {step}\n"

            report += f"""
**成功标准**: {method['success_criteria']}

**关键指标 (KPIs)**:
"""
            for kpi in method['kpis']:
                report += f"- {kpi}\n"

            report += "\n---\n\n"

        report += f"""## 预算估算

**总预算**: {plan['total_estimated_cost']}
**风险等级**: {plan['risk_level']}

**建议**: {plan['recommendation']}

---

## Go/No-Go 决策标准

### ✅ 继续投入 (GO)
"""
        for criteria in plan['decision_criteria']['go_criteria']:
            report += f"- {criteria}\n"

        report += "\n### ❌ 停止项目 (NO-GO)\n"
        for criteria in plan['decision_criteria']['no_go_criteria']:
            report += f"- {criteria}\n"

        report += "\n### 🔄 调整方向 (PIVOT)\n"
        for criteria in plan['decision_criteria']['pivot_criteria']:
            report += f"- {criteria}\n"

        report += f"\n---\n\n生成时间: {plan['generated_at']}\n"

        return report


def main():
    """Example usage"""
    planner = MVPPlanner()

    opportunity = {
        'product_name': 'Smart Pet Collar',
        'product_type': 'physical',
        'target_market': 'North America'
    }

    # Generate low-cost plan
    plan = planner.generate_validation_plan(opportunity, 'low')
    report = planner.generate_report(plan)

    print(report)

    # Save to file
    with open('mvp_validation_plan_example.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print("\n✅ MVP validation plan saved to: mvp_validation_plan_example.md")


if __name__ == '__main__':
    main()
