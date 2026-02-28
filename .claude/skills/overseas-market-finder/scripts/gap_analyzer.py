#!/usr/bin/env python3
"""
Supply-Demand Gap Analyzer

Three-dimensional opportunity analysis:
1. Target market import demand (by country breakdown)
2. Global supply concentration (HHI index)
3. China manufacturing capability vs export penetration
"""

import json
from typing import Dict, List, Tuple


class SupplyDemandGapAnalyzer:
    """三维供需缺口分析器"""

    def __init__(self):
        self.opportunities = []

    def calculate_hhi(self, market_shares: Dict[str, float]) -> float:
        """
        计算 HHI (Herfindahl-Hirschman Index) 市场集中度指数

        Args:
            market_shares: {'Country': share} 各国市场份额（0-1）

        Returns:
            HHI 指数 (0-1)，越高越集中
        """
        return sum(share ** 2 for share in market_shares.values())

    def calculate_top_n_share(self, market_shares: Dict[str, float], n: int = 3) -> float:
        """
        计算前 N 大供应商的市场份额总和

        Args:
            market_shares: 各国市场份额
            n: 取前 N 个国家

        Returns:
            前 N 国的市场份额总和
        """
        sorted_shares = sorted(market_shares.values(), reverse=True)
        return sum(sorted_shares[:n])

    def score_global_supply_gap(self, hhi_index: float, top3_share: float) -> float:
        """
        评估全球供给缺口（0-100分）

        分数越高，说明全球供给缺口越大（机会越好）

        Args:
            hhi_index: HHI市场集中度指数（0-1）
            top3_share: 前3大出口国占比（0-1）

        Returns:
            供给缺口得分 (0-100)
        """
        # HHI 评分（0-50分）
        if hhi_index < 0.10:      # 极度分散
            hhi_score = 50
        elif hhi_index < 0.15:    # 分散
            hhi_score = 40
        elif hhi_index < 0.25:    # 中等集中
            hhi_score = 25
        else:                     # 高度集中（寡头）
            hhi_score = 10

        # TOP3占比评分（0-50分）
        if top3_share < 0.30:     # 极度分散
            top3_score = 50
        elif top3_share < 0.50:   # 分散
            top3_score = 40
        elif top3_share < 0.70:   # 中等集中
            top3_score = 25
        else:                     # 高度集中
            top3_score = 10

        return hhi_score + top3_score

    def score_china_capability(self,
                              num_manufacturers: int,
                              production_capacity: str = 'unknown') -> float:
        """
        评估中国生产能力（0-100分）

        Args:
            num_manufacturers: 国内生产商数量
            production_capacity: 产能水平 ('low', 'medium', 'high', 'leading', 'unknown')

        Returns:
            生产能力得分 (0-100)
        """
        # 生产商数量评分（0-60分）
        if num_manufacturers >= 500:
            mfg_score = 60
        elif num_manufacturers >= 200:
            mfg_score = 50
        elif num_manufacturers >= 100:
            mfg_score = 40
        elif num_manufacturers >= 50:
            mfg_score = 30
        elif num_manufacturers >= 10:
            mfg_score = 20
        else:
            mfg_score = 10

        # 产能水平评分（0-40分）
        capacity_scores = {
            'leading': 40,    # 全球领先
            'high': 30,       # 产能高
            'medium': 20,     # 中等
            'low': 10,        # 低
            'unknown': 15     # 未知（给中间分）
        }
        capacity_score = capacity_scores.get(production_capacity.lower(), 15)

        return mfg_score + capacity_score

    def score_china_competition(self,
                               num_exporters: int,
                               num_manufacturers: int) -> float:
        """
        评估中国出口商竞争度（0-100分）

        分数越高，说明竞争越小（出口渗透率低=好机会）

        Args:
            num_exporters: 实际出口商数量
            num_manufacturers: 国内总生产商数量

        Returns:
            竞争度得分 (0-100)，分数越高竞争越小
        """
        if num_manufacturers == 0:
            return 0

        penetration_rate = num_exporters / num_manufacturers

        # 出口渗透率越低，机会越大
        if penetration_rate < 0.05:      # <5%
            return 100  # 蓝海
        elif penetration_rate < 0.10:    # 5-10%
            return 90   # 竞争极小
        elif penetration_rate < 0.15:    # 10-15%
            return 80   # 竞争小
        elif penetration_rate < 0.30:    # 15-30%
            return 60   # 中等竞争
        elif penetration_rate < 0.50:    # 30-50%
            return 40   # 竞争较大
        else:                            # >50%
            return 20   # 红海

    def analyze_opportunity(self, data: Dict) -> Dict:
        """
        完整的三维机会分析

        Args:
            data: 包含所有必要数据的字典
                {
                    'product_name': str,
                    'hs_code': str,
                    'target_market': str,
                    'import_value_usd': float,
                    'import_by_country': {'Country': value_usd},
                    'growth_rate': float,
                    'china_manufacturers': int,
                    'china_exporters': int,
                    'china_production_capacity': str  # 'low/medium/high/leading'
                }

        Returns:
            分析结果字典
        """
        # 计算市场份额
        total_import = data['import_value_usd']
        market_shares = {
            country: value / total_import
            for country, value in data['import_by_country'].items()
        }

        # 计算全球供给集中度指标
        hhi_index = self.calculate_hhi(market_shares)
        top3_share = self.calculate_top_n_share(market_shares, n=3)

        # 中国在目标市场的份额
        china_share = market_shares.get('China', 0)

        # 评分
        gap_score = self.score_global_supply_gap(hhi_index, top3_share)
        capability_score = self.score_china_capability(
            data['china_manufacturers'],
            data.get('china_production_capacity', 'unknown')
        )
        competition_score = self.score_china_competition(
            data['china_exporters'],
            data['china_manufacturers']
        )

        # 综合机会指数
        opportunity_index = (
            gap_score * 0.35 +           # 全球供给缺口权重35%
            capability_score * 0.35 +    # 中国生产能力权重35%
            competition_score * 0.30     # 中国竞争度权重30%
        )

        # 判断机会等级
        if opportunity_index >= 80:
            opportunity_level = '⭐⭐⭐⭐⭐ 顶级机会'
        elif opportunity_index >= 70:
            opportunity_level = '⭐⭐⭐⭐ 优质机会'
        elif opportunity_index >= 60:
            opportunity_level = '⭐⭐⭐ 中等机会'
        elif opportunity_index >= 50:
            opportunity_level = '⭐⭐ 潜在机会'
        else:
            opportunity_level = '⭐ 机会较小'

        return {
            'product_name': data['product_name'],
            'hs_code': data.get('hs_code', 'N/A'),
            'target_market': data['target_market'],
            'market_analysis': {
                'import_value_usd': total_import,
                'growth_rate': data['growth_rate'],
                'china_share': china_share,
                'hhi_index': round(hhi_index, 4),
                'top3_share': round(top3_share, 4),
                'market_concentration': self._interpret_hhi(hhi_index)
            },
            'supply_gap_analysis': {
                'global_supply_gap_score': round(gap_score, 1),
                'interpretation': self._interpret_gap(gap_score)
            },
            'china_analysis': {
                'manufacturers': data['china_manufacturers'],
                'exporters': data['china_exporters'],
                'penetration_rate': round(
                    data['china_exporters'] / max(data['china_manufacturers'], 1),
                    4
                ),
                'capability_score': round(capability_score, 1),
                'competition_score': round(competition_score, 1),
                'production_capacity': data.get('china_production_capacity', 'unknown')
            },
            'opportunity_assessment': {
                'opportunity_index': round(opportunity_index, 1),
                'opportunity_level': opportunity_level,
                'recommended': opportunity_index >= 70
            },
            'top_suppliers': self._get_top_suppliers(data['import_by_country'], n=5)
        }

    def _interpret_hhi(self, hhi: float) -> str:
        """解释 HHI 指数"""
        if hhi < 0.10:
            return '极度分散（全球缺口大）'
        elif hhi < 0.15:
            return '分散（有供给缺口）'
        elif hhi < 0.25:
            return '中等集中'
        else:
            return '高度集中（寡头市场）'

    def _interpret_gap(self, gap_score: float) -> str:
        """解释供给缺口得分"""
        if gap_score >= 80:
            return '全球供给严重不足，巨大机会'
        elif gap_score >= 60:
            return '全球供给缺口明显，值得进入'
        elif gap_score >= 40:
            return '全球供给相对平衡'
        else:
            return '市场已被少数国家主导，进入壁垒高'

    def _get_top_suppliers(self, import_by_country: Dict[str, float], n: int = 5) -> List[Dict]:
        """获取前N大供应国"""
        sorted_countries = sorted(
            import_by_country.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n]

        total = sum(import_by_country.values())
        return [
            {
                'country': country,
                'value_usd': value,
                'share': round(value / total, 4)
            }
            for country, value in sorted_countries
        ]

    def generate_gap_report(self, analysis_result: Dict) -> str:
        """
        生成供需缺口分析报告（Markdown格式）

        Args:
            analysis_result: analyze_opportunity() 返回的结果

        Returns:
            Markdown格式的报告
        """
        report = f"""# 供需缺口分析报告

## {analysis_result['product_name']}

**HS编码**: {analysis_result['hs_code']}
**目标市场**: {analysis_result['target_market']}

---

## 📊 市场概况

- **市场规模**: ${analysis_result['market_analysis']['import_value_usd']:,.0f}
- **年增长率**: {analysis_result['market_analysis']['growth_rate']*100:.1f}%
- **中国份额**: {analysis_result['market_analysis']['china_share']*100:.1f}%

### 市场集中度分析

- **HHI指数**: {analysis_result['market_analysis']['hhi_index']:.4f}
- **前3大供应商占比**: {analysis_result['market_analysis']['top3_share']*100:.1f}%
- **市场结构**: {analysis_result['market_analysis']['market_concentration']}

### 主要供应国

| 排名 | 国家 | 出口额 (USD) | 市场份额 |
|------|------|-------------|---------|
"""
        for i, supplier in enumerate(analysis_result['top_suppliers'], 1):
            report += f"| {i} | {supplier['country']} | ${supplier['value_usd']:,.0f} | {supplier['share']*100:.1f}% |\n"

        report += f"""
---

## 🌍 全球供给缺口分析

**缺口得分**: {analysis_result['supply_gap_analysis']['global_supply_gap_score']:.1f}/100

**分析**: {analysis_result['supply_gap_analysis']['interpretation']}

---

## 🇨🇳 中国供给分析

### 生产能力

- **国内生产商**: {analysis_result['china_analysis']['manufacturers']} 家
- **产能水平**: {analysis_result['china_analysis']['production_capacity']}
- **能力得分**: {analysis_result['china_analysis']['capability_score']:.1f}/100

### 出口竞争度

- **实际出口商**: {analysis_result['china_analysis']['exporters']} 家
- **出口渗透率**: {analysis_result['china_analysis']['penetration_rate']*100:.1f}%
- **竞争得分**: {analysis_result['china_analysis']['competition_score']:.1f}/100

**解读**: {'蓝海市场，竞争极小' if analysis_result['china_analysis']['penetration_rate'] < 0.1 else '红海市场，竞争激烈' if analysis_result['china_analysis']['penetration_rate'] > 0.5 else '中等竞争'}

---

## 🎯 机会评估

**综合机会指数**: {analysis_result['opportunity_assessment']['opportunity_index']:.1f}/100

**机会等级**: {analysis_result['opportunity_assessment']['opportunity_level']}

**建议**: {'✅ 强烈推荐进入' if analysis_result['opportunity_assessment']['recommended'] else '⚠️ 建议谨慎评估'}

---

## 💡 战略建议

"""
        # 根据分析结果给出建议
        china_share = analysis_result['market_analysis']['china_share']
        hhi = analysis_result['market_analysis']['hhi_index']
        penetration = analysis_result['china_analysis']['penetration_rate']

        if china_share < 0.10 and hhi < 0.25 and penetration < 0.15:
            report += """
### 进入策略

这是一个**供需缺口型机会**：
- ✅ 全球供给分散，无明显主导国
- ✅ 中国生产能力强，但出口商少
- ✅ 蓝海市场，竞争压力小

**建议行动**：
1. 快速进入，抢占先机
2. 建立差异化品牌定位
3. 利用中国供应链优势
4. 重点投入市场教育和渠道建设
"""
        elif hhi > 0.25:
            report += """
### 进入策略

这是一个**寡头主导型市场**：
- ⚠️ 市场被少数国家主导，可能存在技术/品牌壁垒
- 建议深入分析主导国的优势来源

**建议行动**：
1. 分析主导国的核心竞争力
2. 寻找细分市场或利基领域
3. 通过创新或成本优势差异化竞争
4. 谨慎评估进入壁垒
"""
        elif penetration > 0.5:
            report += """
### 进入策略

这是一个**红海竞争市场**：
- ❌ 中国出口商众多，竞争激烈
- ⚠️ 需要强差异化或成本优势

**建议行动**：
1. 寻找细分市场机会
2. 提升产品附加值
3. 建立品牌差异化
4. 考虑其他目标市场
"""
        else:
            report += """
### 进入策略

**建议行动**：
1. 进一步调研市场需求细节
2. 验证中国生产能力是否匹配
3. 小规模测试市场反应
4. 评估投资回报周期
"""

        return report


def main():
    """示例用法"""
    analyzer = SupplyDemandGapAnalyzer()

    # 示例数据：实验室培育钻石
    example_data = {
        'product_name': 'Laboratory Grown Diamonds',
        'hs_code': '7104.21',
        'target_market': 'USA',
        'import_value_usd': 4_600_000_000,  # $4.6B
        'import_by_country': {
            'China': 3_500_000_000,     # 76%
            'India': 690_000_000,       # 15%
            'South Korea': 368_000_000, # 8%
            'Others': 42_000_000        # 1%
        },
        'growth_rate': 0.10,  # 10%
        'china_manufacturers': 122,  # 仅郑州地区
        'china_exporters': 10,       # 估算
        'china_production_capacity': 'leading'  # 全球70%产量
    }

    result = analyzer.analyze_opportunity(example_data)
    report = analyzer.generate_gap_report(result)

    print(report)
    print("\n" + "="*60)
    print("JSON Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
