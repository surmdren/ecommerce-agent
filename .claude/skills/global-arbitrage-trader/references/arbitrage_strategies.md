# Global Arbitrage Trading Strategies

## 1. Cross-Market Arbitrage (跨市场套利)

### 1.1 ADR/ADS Arbitrage
**原理**: 同一公司在不同市场的价格差异
**常见标的**:
- Alibaba: BABA (US) vs 9988.HK (HK)
- Baidu: BIDU (US) vs 9888.HK (HK)
- JD.com: JD (US) vs 9618.HK (HK)

**执行步骤**:
1. 使用`fetch_market_data.py`获取跨市场报价
2. 计算价格差异（考虑汇率）
3. 当价差 > 交易成本（佣金+汇兑成本）时触发
4. 在低价市场买入，高价市场卖出

**风险点**:
- 汇率波动
- 交易时间差（时区不同）
- 流动性差异
- 监管政策变化

### 1.2 Dual-Listed Stocks (双重上市套利)
**案例**: A股/H股价差
**执行**: 通过沪港通/深港通进行
**监控指标**: AH股溢价指数

## 2. Time-Based Arbitrage (时间差套利)

### 2.1 Overnight News Arbitrage
**原理**: 利用时区差异，海外市场消息传导到国内市场的时间差

**执行流程**:
1. 监控美股盘后/亚洲时段重大新闻
2. 识别相关A股标的
3. 次日开盘前准备订单
4. 集合竞价或开盘后立即执行

**案例**:
- 美联储利率决议 → 国内金融股
- 美股半导体大跌 → A股芯片股
- 商品期货大幅波动 → 相关产业链公司

### 2.2 Earnings Announcement Lag
**原理**: 母公司/子公司财报发布时间差

**案例**:
- 腾讯港股财报 → A股腾讯概念股
- Apple财报 → A股苹果产业链
- Tesla财报 → A股锂电池/新能源车股

## 3. Regulatory Policy Arbitrage (监管政策差异)

### 3.1 IPO Lockup Expiry
**原理**: 不同市场的限售期规则不同

### 3.2 Short-Selling Restrictions
**原理**: A股做空限制较多，港股/美股相对宽松

**策略**: 通过跨市场对冲实现变相做空

##4. Market Sentiment Arbitrage (市场情绪差异)

### 4.1 Panic Selling vs Rational Market
**案例**: 某市场过度恐慌性抛售，其他市场反应理性

### 4.2 Hot Money Flow
**识别**: 北向资金/南向资金净流向突变

## Risk Management Rules

### Position Sizing
- 单笔交易风险: 不超过本金的2%
- 单一标的仓位: 不超过总资金的20%
- 跨市场对冲: 保持1:1对冲比例

### Stop Loss
- 技术止损: 跌破关键支撑位
- 时间止损: 持仓超过N天未盈利
- 价差收敛止损: 价差收窄至成本线

### Take Profit
- 目标价差收敛: 价差回归至历史均值
- 阶梯止盈: 50%仓位止盈后剩余持有
- 时间止盈: 套利窗口关闭前平仓

## Data Sources

### Free Sources
- Yahoo Finance: 实时报价
- TradingView: 图表和技术分析
- 东方财富: A股实时数据

### Paid Sources (Optional)
- Bloomberg Terminal: 专业级数据
- Wind: 中国金融数据终端
- Reuters Eikon: 全球市场数据

## Broker API Integration

### 支持的券商
- 富途证券 (Futu): 港美股
- 老虎证券 (Tiger): 港美股
- 雪盈证券: 美股
- 华泰证券: A股

**注意**: 在自动下单前，必须通过AskUserQuestion确认交易理由
