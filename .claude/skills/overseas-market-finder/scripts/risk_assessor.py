#!/usr/bin/env python3
"""
Risk Assessment for Overseas Market Opportunities

Evaluate multi-dimensional risks including policy, operational, compliance,
and cultural factors for international market entry.
"""

from typing import Dict, List
from datetime import datetime


class RiskAssessor:
    """Assess risks for overseas market opportunities"""

    # Risk scoring: 0-100 (higher = lower risk, better)
    RISK_WEIGHTS = {
        'policy_risk': 0.25,      # 25% - Tariff, trade policy
        'operational_risk': 0.25,  # 25% - Currency, logistics, payment
        'compliance_risk': 0.25,   # 25% - IP, certification, legal
        'market_risk': 0.25       # 25% - Cultural fit, competition
    }

    def __init__(self):
        self.risk_categories = list(self.RISK_WEIGHTS.keys())

    def assess_policy_risk(self, opportunity: Dict) -> Dict:
        """
        Assess policy and trade risks

        Args:
            opportunity: Market opportunity data with target_market, product_category

        Returns:
            Dict with policy risk score and details
        """
        target_market = opportunity.get('target_market', '')
        product_category = opportunity.get('product_category', '')
        source_country = opportunity.get('source_country', 'China')

        score = 100  # Start with perfect score
        risks = []
        mitigations = []

        # Tariff risk
        tariff_rate = opportunity.get('tariff_rate', 0)
        if tariff_rate >= 0.25:  # 25%+ tariff
            score -= 30
            risks.append(f"高关税风险: {tariff_rate*100:.0f}% 关税")
            mitigations.append("考虑在目标国本地组装以降低关税")
        elif tariff_rate >= 0.10:
            score -= 15
            risks.append(f"中等关税: {tariff_rate*100:.0f}%")
            mitigations.append("优化供应链以吸收关税成本")

        # Trade war risk (China -> US)
        if source_country == 'China' and 'US' in target_market:
            if product_category in ['electronics', 'machinery', 'automotive']:
                score -= 20
                risks.append("中美贸易摩擦高风险品类")
                mitigations.append("考虑东南亚代工以规避301关税")

        # Anti-dumping risk
        if opportunity.get('low_price_strategy', False):
            score -= 15
            risks.append("低价策略可能引发反倾销调查")
            mitigations.append("维持合理定价，避免倾销嫌疑")

        # Import quota/restrictions
        if opportunity.get('import_quota', False):
            score -= 25
            risks.append("目标市场有进口配额限制")
            mitigations.append("提前申请配额或寻找配额合作伙伴")

        return {
            'score': max(0, score),
            'level': self._get_risk_level(score),
            'risks': risks,
            'mitigations': mitigations
        }

    def assess_operational_risk(self, opportunity: Dict) -> Dict:
        """
        Assess operational risks (currency, logistics, payment)

        Args:
            opportunity: Market opportunity data

        Returns:
            Dict with operational risk score and details
        """
        target_market = opportunity.get('target_market', '')
        product_type = opportunity.get('product_type', 'physical')

        score = 100
        risks = []
        mitigations = []

        # Currency risk
        currency_volatility = opportunity.get('currency_volatility', 'low')
        if currency_volatility == 'high':
            score -= 25
            risks.append("汇率波动大（新兴市场货币）")
            mitigations.append("使用远期外汇合约锁定汇率")
        elif currency_volatility == 'medium':
            score -= 10
            risks.append("汇率有一定波动")
            mitigations.append("采用多币种定价策略")

        # Logistics cost/complexity
        if product_type == 'physical':
            logistics_cost_ratio = opportunity.get('logistics_cost_ratio', 0.1)
            if logistics_cost_ratio >= 0.20:  # >20% of product value
                score -= 20
                risks.append(f"物流成本高({logistics_cost_ratio*100:.0f}% of value)")
                mitigations.append("考虑海外仓或本地化生产")
            elif logistics_cost_ratio >= 0.10:
                score -= 10
                risks.append("物流成本占比中等")

        # Payment cycle risk
        payment_terms = opportunity.get('payment_terms', 'T/T')
        if payment_terms == 'OA60' or payment_terms == 'OA90':
            score -= 15
            risks.append(f"账期长({payment_terms})，现金流压力大")
            mitigations.append("使用信用保险或保理融资")
        elif payment_terms == 'OA30':
            score -= 5
            risks.append("30天账期需注意现金流")

        # Supply chain stability
        if opportunity.get('single_supplier', False):
            score -= 15
            risks.append("单一供应商风险")
            mitigations.append("建立备用供应商体系")

        return {
            'score': max(0, score),
            'level': self._get_risk_level(score),
            'risks': risks,
            'mitigations': mitigations
        }

    def assess_compliance_risk(self, opportunity: Dict) -> Dict:
        """
        Assess compliance risks (IP, certification, legal)

        Args:
            opportunity: Market opportunity data

        Returns:
            Dict with compliance risk score and details
        """
        target_market = opportunity.get('target_market', '')
        product_category = opportunity.get('product_category', '')

        score = 100
        risks = []
        mitigations = []

        # IP risk
        ip_status = opportunity.get('ip_status', 'unknown')
        if ip_status == 'high_risk':
            score -= 30
            risks.append("知识产权侵权风险高（竞品有强专利）")
            mitigations.append("进行FTO分析，设计规避方案或购买专利授权")
        elif ip_status == 'medium_risk':
            score -= 15
            risks.append("存在专利风险")
            mitigations.append("委托律师进行专利检索")

        # Certification complexity
        cert_requirements = opportunity.get('certifications', [])
        if len(cert_requirements) >= 3:
            score -= 20
            risks.append(f"认证要求多({len(cert_requirements)}项)")
            mitigations.append("提前6-12个月启动认证流程")
        elif len(cert_requirements) >= 1:
            score -= 10
            risks.append("需要强制性认证")

        # High-risk categories
        if product_category in ['medical', 'food', 'pharmaceutical']:
            score -= 25
            risks.append(f"{product_category}行业监管极严")
            mitigations.append("聘请当地合规顾问，预留12-18个月准备期")

        # Data privacy (for SaaS/digital products)
        if opportunity.get('product_type') == 'saas':
            if 'Europe' in target_market:
                score -= 15
                risks.append("GDPR合规要求（欧洲市场）")
                mitigations.append("部署欧洲数据中心，通过GDPR审核")

        # Export control (sensitive tech)
        if product_category in ['encryption', 'drone', 'ai']:
            score -= 20
            risks.append("出口管制产品，需特殊许可")
            mitigations.append("提前申请出口许可证")

        return {
            'score': max(0, score),
            'level': self._get_risk_level(score),
            'risks': risks,
            'mitigations': mitigations
        }

    def assess_market_risk(self, opportunity: Dict) -> Dict:
        """
        Assess market and cultural risks

        Args:
            opportunity: Market opportunity data

        Returns:
            Dict with market risk score and details
        """
        target_market = opportunity.get('target_market', '')
        product_category = opportunity.get('product_category', '')

        score = 100
        risks = []
        mitigations = []

        # Cultural fit
        cultural_adaptation = opportunity.get('cultural_adaptation_needed', 'low')
        if cultural_adaptation == 'high':
            score -= 25
            risks.append("产品需大幅本地化改造（设计、营销、功能）")
            mitigations.append("聘请当地设计师和营销团队")
        elif cultural_adaptation == 'medium':
            score -= 10
            risks.append("需一定程度本地化")
            mitigations.append("进行用户调研，优化产品适配性")

        # Competition intensity
        num_competitors = opportunity.get('num_competitors', 0)
        if num_competitors > 50:
            score -= 25
            risks.append(f"竞争激烈({num_competitors}+竞品)")
            mitigations.append("寻找细分市场切入点")
        elif num_competitors > 20:
            score -= 15
            risks.append("竞争较为激烈")
            mitigations.append("强化差异化优势")

        # Brand barrier
        if opportunity.get('strong_incumbent_brands', False):
            score -= 20
            risks.append("现有品牌壁垒高")
            mitigations.append("采用性价比策略或创新突破")

        # Market education needed
        if opportunity.get('market_education_needed', False):
            score -= 15
            risks.append("市场教育成本高（全新品类）")
            mitigations.append("预留充足营销预算，联合KOL推广")

        return {
            'score': max(0, score),
            'level': self._get_risk_level(score),
            'risks': risks,
            'mitigations': mitigations
        }

    def _get_risk_level(self, score: float) -> str:
        """Convert risk score to risk level"""
        if score >= 80:
            return '低风险 ✅'
        elif score >= 60:
            return '中等风险 ⚠️'
        elif score >= 40:
            return '较高风险 ⚠️⚠️'
        else:
            return '高风险 ❌'

    def calculate_overall_risk(self, risk_scores: Dict) -> Dict:
        """
        Calculate weighted overall risk score

        Args:
            risk_scores: Dict with scores for each risk category

        Returns:
            Overall risk assessment
        """
        total_score = sum(
            risk_scores[category]['score'] * self.RISK_WEIGHTS[category]
            for category in self.risk_categories
        )

        return {
            'overall_score': round(total_score, 1),
            'overall_level': self._get_risk_level(total_score),
            'recommendation': self._get_risk_recommendation(total_score)
        }

    def _get_risk_recommendation(self, overall_score: float) -> str:
        """Generate risk-based recommendation"""
        if overall_score >= 80:
            return '风险可控，建议进入'
        elif overall_score >= 60:
            return '风险中等，建议充分准备后进入'
        elif overall_score >= 40:
            return '风险较高，需制定详细风险缓解方案'
        else:
            return '风险过高，不建议进入或需大幅调整策略'

    def assess_opportunity(self, opportunity: Dict) -> Dict:
        """
        Complete risk assessment

        Args:
            opportunity: Complete market opportunity data

        Returns:
            Comprehensive risk assessment
        """
        risk_scores = {
            'policy_risk': self.assess_policy_risk(opportunity),
            'operational_risk': self.assess_operational_risk(opportunity),
            'compliance_risk': self.assess_compliance_risk(opportunity),
            'market_risk': self.assess_market_risk(opportunity)
        }

        overall = self.calculate_overall_risk(risk_scores)

        return {
            'product': opportunity.get('product_name', 'Unknown'),
            'target_market': opportunity.get('target_market', 'Unknown'),
            'risk_scores': risk_scores,
            'overall_assessment': overall,
            'timestamp': datetime.now().isoformat()
        }

    def generate_risk_report(self, assessment: Dict) -> str:
        """
        Generate markdown risk assessment report

        Args:
            assessment: Risk assessment results

        Returns:
            Markdown formatted report
        """
        report = f"""# 风险评估报告

**产品**: {assessment['product']}
**目标市场**: {assessment['target_market']}
**评估时间**: {assessment['timestamp']}

---

## 综合风险评估

- **总分**: {assessment['overall_assessment']['overall_score']}/100
- **风险等级**: {assessment['overall_assessment']['overall_level']}
- **建议**: {assessment['overall_assessment']['recommendation']}

---

## 分类风险分析

"""

        risk_names = {
            'policy_risk': '政策风险',
            'operational_risk': '运营风险',
            'compliance_risk': '合规风险',
            'market_risk': '市场风险'
        }

        for category, name in risk_names.items():
            data = assessment['risk_scores'][category]
            report += f"""### {name}

**得分**: {data['score']}/100 - {data['level']}

"""
            if data['risks']:
                report += "**主要风险**:\n"
                for risk in data['risks']:
                    report += f"- ❌ {risk}\n"
                report += "\n"

            if data['mitigations']:
                report += "**缓解措施**:\n"
                for mitigation in data['mitigations']:
                    report += f"- ✅ {mitigation}\n"
                report += "\n"

            report += "---\n\n"

        return report


def main():
    """Example usage"""
    assessor = RiskAssessor()

    # Example opportunity
    opportunity = {
        'product_name': 'Smart Home Security Camera',
        'target_market': 'United States',
        'source_country': 'China',
        'product_category': 'electronics',
        'product_type': 'physical',
        'tariff_rate': 0.25,
        'currency_volatility': 'low',
        'logistics_cost_ratio': 0.08,
        'payment_terms': 'T/T',
        'certifications': ['FCC', 'UL'],
        'ip_status': 'medium_risk',
        'cultural_adaptation_needed': 'low',
        'num_competitors': 30,
        'strong_incumbent_brands': True
    }

    assessment = assessor.assess_opportunity(opportunity)

    # Generate report
    report = assessor.generate_risk_report(assessment)
    print(report)

    # Save to file
    with open('risk_assessment_example.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print("\n✅ Risk assessment saved to: risk_assessment_example.md")


if __name__ == '__main__':
    main()
