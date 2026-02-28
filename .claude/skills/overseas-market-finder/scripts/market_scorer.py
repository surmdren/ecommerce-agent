#!/usr/bin/env python3
"""
Market Opportunity Scorer

Calculate success probability for overseas market opportunities based on:
- TAM/SAM (Total/Serviceable Addressable Market)
- Competition intensity
- Profitability potential
- Execution difficulty
"""

import json
from typing import Dict, List


class MarketScorer:
    """Score market opportunities with weighted criteria"""

    # Default weights for scoring dimensions
    WEIGHTS = {
        'market_size': 0.30,      # 30% - Market demand (TAM/SAM)
        'competition': 0.25,      # 25% - Competition intensity
        'profitability': 0.25,    # 25% - Profit potential
        'execution': 0.20         # 20% - Execution difficulty
    }

    def __init__(self, custom_weights: Dict[str, float] = None):
        """Initialize scorer with optional custom weights"""
        if custom_weights:
            self.weights = custom_weights
        else:
            self.weights = self.WEIGHTS

    def score_market_size(self, tam_usd: float, growth_rate: float) -> float:
        """
        Score market size (0-100)

        Args:
            tam_usd: Total addressable market in USD
            growth_rate: Annual growth rate (e.g., 0.15 for 15%)

        Returns:
            Score from 0-100
        """
        # TAM score (0-60 points)
        if tam_usd >= 10_000_000_000:  # $10B+
            tam_score = 60
        elif tam_usd >= 1_000_000_000:  # $1B+
            tam_score = 50
        elif tam_usd >= 100_000_000:    # $100M+
            tam_score = 40
        elif tam_usd >= 10_000_000:     # $10M+
            tam_score = 30
        else:
            tam_score = 20

        # Growth score (0-40 points)
        if growth_rate >= 0.30:         # 30%+ growth
            growth_score = 40
        elif growth_rate >= 0.20:       # 20%+ growth
            growth_score = 35
        elif growth_rate >= 0.10:       # 10%+ growth
            growth_score = 25
        elif growth_rate >= 0.05:       # 5%+ growth
            growth_score = 15
        else:
            growth_score = 5

        return tam_score + growth_score

    def score_competition(self, num_competitors: int, market_concentration: str) -> float:
        """
        Score competition intensity (0-100, higher = less competition)

        Args:
            num_competitors: Number of major competitors
            market_concentration: 'monopoly', 'oligopoly', 'competitive', 'fragmented'

        Returns:
            Score from 0-100 (higher is better - less competition)
        """
        # Competitor count score (0-50 points)
        if num_competitors <= 3:
            competitor_score = 50  # Easy to enter if few competitors
        elif num_competitors <= 10:
            competitor_score = 40
        elif num_competitors <= 30:
            competitor_score = 25
        else:
            competitor_score = 10  # Saturated market

        # Concentration score (0-50 points)
        concentration_scores = {
            'fragmented': 50,    # Best - room for new players
            'competitive': 35,   # Moderate competition
            'oligopoly': 20,     # Dominated by few players
            'monopoly': 5        # Hardest to enter
        }
        concentration_score = concentration_scores.get(market_concentration.lower(), 25)

        return competitor_score + concentration_score

    def score_profitability(self, avg_order_value: float, gross_margin: float,
                           payback_months: int) -> float:
        """
        Score profitability potential (0-100)

        Args:
            avg_order_value: Average order value in USD
            gross_margin: Gross profit margin (0-1, e.g., 0.4 for 40%)
            payback_months: Customer acquisition cost payback period

        Returns:
            Score from 0-100
        """
        # AOV score (0-35 points)
        if avg_order_value >= 1000:
            aov_score = 35
        elif avg_order_value >= 500:
            aov_score = 30
        elif avg_order_value >= 100:
            aov_score = 20
        elif avg_order_value >= 50:
            aov_score = 10
        else:
            aov_score = 5

        # Margin score (0-40 points)
        if gross_margin >= 0.60:
            margin_score = 40
        elif gross_margin >= 0.40:
            margin_score = 35
        elif gross_margin >= 0.25:
            margin_score = 25
        elif gross_margin >= 0.15:
            margin_score = 15
        else:
            margin_score = 5

        # Payback score (0-25 points)
        if payback_months <= 6:
            payback_score = 25
        elif payback_months <= 12:
            payback_score = 20
        elif payback_months <= 18:
            payback_score = 12
        else:
            payback_score = 5

        return aov_score + margin_score + payback_score

    def score_execution(self, tech_barrier: str, regulatory_complexity: str,
                       resource_requirement: str) -> float:
        """
        Score execution difficulty (0-100, higher = easier)

        Args:
            tech_barrier: 'low', 'medium', 'high'
            regulatory_complexity: 'low', 'medium', 'high'
            resource_requirement: 'low', 'medium', 'high'

        Returns:
            Score from 0-100 (higher is better - easier execution)
        """
        tech_scores = {'low': 40, 'medium': 25, 'high': 10}
        regulatory_scores = {'low': 35, 'medium': 20, 'high': 5}
        resource_scores = {'low': 25, 'medium': 15, 'high': 5}

        return (tech_scores.get(tech_barrier.lower(), 20) +
                regulatory_scores.get(regulatory_complexity.lower(), 15) +
                resource_scores.get(resource_requirement.lower(), 10))

    def calculate_success_rate(self, scores: Dict[str, float]) -> float:
        """
        Calculate overall success probability

        Args:
            scores: Dict with keys 'market_size', 'competition', 'profitability', 'execution'

        Returns:
            Success probability (0-100%)
        """
        weighted_score = sum(
            scores[dimension] * self.weights[dimension]
            for dimension in self.weights
        )

        return round(weighted_score, 1)

    def score_opportunity(self, opportunity: Dict) -> Dict:
        """
        Score a complete market opportunity

        Args:
            opportunity: Dict with all scoring parameters

        Returns:
            Dict with scores and success rate
        """
        scores = {
            'market_size': self.score_market_size(
                opportunity['tam_usd'],
                opportunity['growth_rate']
            ),
            'competition': self.score_competition(
                opportunity['num_competitors'],
                opportunity['market_concentration']
            ),
            'profitability': self.score_profitability(
                opportunity['avg_order_value'],
                opportunity['gross_margin'],
                opportunity['payback_months']
            ),
            'execution': self.score_execution(
                opportunity['tech_barrier'],
                opportunity['regulatory_complexity'],
                opportunity['resource_requirement']
            )
        }

        success_rate = self.calculate_success_rate(scores)

        return {
            'product': opportunity.get('product_name', 'Unknown'),
            'industry': opportunity.get('industry', 'Unknown'),
            'segment': opportunity.get('segment', 'Unknown'),
            'scores': scores,
            'success_rate': success_rate,
            'meets_threshold': success_rate >= 80.0
        }


def main():
    """Example usage"""
    scorer = MarketScorer()

    # Example opportunity
    opportunity = {
        'product_name': 'Smart Home Sensors',
        'industry': 'IoT',
        'segment': 'Home Automation',
        'tam_usd': 5_000_000_000,
        'growth_rate': 0.25,
        'num_competitors': 15,
        'market_concentration': 'competitive',
        'avg_order_value': 150,
        'gross_margin': 0.45,
        'payback_months': 8,
        'tech_barrier': 'medium',
        'regulatory_complexity': 'low',
        'resource_requirement': 'medium'
    }

    result = scorer.score_opportunity(opportunity)
    print(json.dumps(result, indent=2))


class EnhancedMarketScorer(MarketScorer):
    """
    增强版市场评分器 - 整合供需缺口分析

    结合传统评分 + 供需缺口三维分析
    """

    def __init__(self):
        super().__init__()
        # 导入供需缺口分析器
        try:
            from gap_analyzer import SupplyDemandGapAnalyzer
            self.gap_analyzer = SupplyDemandGapAnalyzer()
        except ImportError:
            self.gap_analyzer = None

    def score_with_gap_analysis(self, opportunity: Dict, gap_data: Dict = None) -> Dict:
        """
        综合评分：传统评分 + 供需缺口分析

        Args:
            opportunity: 传统评分所需数据
            gap_data: 供需缺口分析数据（可选）

        Returns:
            综合评分结果
        """
        # 传统评分
        traditional_score = self.score_opportunity(opportunity)

        result = {
            'product': opportunity.get('product_name', 'Unknown'),
            'traditional_scores': traditional_score['scores'],
            'traditional_success_rate': traditional_score['success_rate']
        }

        # 如果提供了供需缺口数据，进行增强分析
        if gap_data and self.gap_analyzer:
            gap_result = self.gap_analyzer.analyze_opportunity(gap_data)

            # 综合两种评分
            # 传统评分权重 50%，供需缺口分析权重 50%
            combined_score = (
                traditional_score['success_rate'] * 0.5 +
                gap_result['opportunity_assessment']['opportunity_index'] * 0.5
            )

            result.update({
                'gap_analysis': gap_result,
                'combined_success_rate': round(combined_score, 1),
                'final_recommendation': combined_score >= 80,
                'recommendation_level': self._get_recommendation_level(combined_score)
            })
        else:
            result['combined_success_rate'] = traditional_score['success_rate']
            result['final_recommendation'] = traditional_score['meets_threshold']

        return result

    def _get_recommendation_level(self, score: float) -> str:
        """获取推荐等级"""
        if score >= 85:
            return '⭐⭐⭐⭐⭐ 强烈推荐（立即进入）'
        elif score >= 80:
            return '⭐⭐⭐⭐ 推荐（优先考虑）'
        elif score >= 70:
            return '⭐⭐⭐ 可以考虑（需验证）'
        elif score >= 60:
            return '⭐⭐ 谨慎评估（有风险）'
        else:
            return '⭐ 不建议（风险高）'


if __name__ == '__main__':
    main()
