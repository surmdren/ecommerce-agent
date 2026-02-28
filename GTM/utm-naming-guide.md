# ReplyMate UTM 命名规范

**重要：** 在任何渠道发布链接前，必须使用标准 UTM 参数，避免数据污染。

---

## UTM 参数规范

| 参数 | 说明 | 规范 |
|------|------|------|
| `utm_source` | 流量来源平台 | 全小写，无空格，用 `-` 连接 |
| `utm_medium` | 流量媒介类型 | 固定值（见下表） |
| `utm_campaign` | 推广活动名称 | 格式：`年月-主题` |
| `utm_content` | 区分同一活动不同创意 | 可选 |

---

## 各渠道标准 UTM 参数

### 🔴 P0 渠道

| 渠道 | utm_source | utm_medium | utm_campaign 示例 |
|------|-----------|-----------|-----------------|
| 微信群（跨境卖家群） | `wechat-group` | `social` | `2026q1-beta-recruit` |
| 小红书（自然发帖） | `xiaohongshu` | `social` | `2026q1-content` |
| 小红书（薯条推广） | `xiaohongshu` | `cpc` | `2026q2-boost` |

### 🟠 P1 渠道

| 渠道 | utm_source | utm_medium | utm_campaign 示例 |
|------|-----------|-----------|-----------------|
| V2EX | `v2ex` | `community` | `2026q1-launch` |
| 即刻 | `jike` | `social` | `2026q1-update` |
| 卖家之家论坛 | `maijiazhi` | `community` | `2026q1-forum` |
| 知乎（回答） | `zhihu` | `community` | `2026q1-qa` |
| KOL 测评帖 | `kol` | `referral` | `2026q2-review` |

### 🟡 P2 渠道

| 渠道 | utm_source | utm_medium | utm_campaign 示例 |
|------|-----------|-----------|-----------------|
| Facebook 群 | `facebook` | `social` | `2026q2-fb-group` |
| YouTube 华人频道 | `youtube` | `referral` | `2026q2-collab` |
| Google SEO | `google` | `organic` | —（无需添加，GA4自动识别）|
| 用户推荐链接 | `referral` | `referral` | `2026q1-share` |

### 邮件营销

| 类型 | utm_source | utm_medium | utm_campaign 示例 |
|------|-----------|-----------|-----------------|
| 注册欢迎邮件 | `email` | `email` | `onboarding-welcome` |
| 试用到期提醒 | `email` | `email` | `trial-ending` |
| 推荐活动邮件 | `email` | `email` | `referral-invite` |

---

## 完整 URL 示例

**微信群内测招募：**
```
https://replymate.cn?utm_source=wechat-group&utm_medium=social&utm_campaign=2026q1-beta-recruit
```

**小红书帖子底部链接：**
```
https://replymate.cn?utm_source=xiaohongshu&utm_medium=social&utm_campaign=2026q1-content
```

**KOL 测评帖专属折扣链接（带 KOL 标识）：**
```
https://replymate.cn?utm_source=kol&utm_medium=referral&utm_campaign=2026q2-review&utm_content=blogger-A
```

**推荐裂变链接（用户专属）：**
```
https://replymate.cn/ref/USER123?utm_source=referral&utm_medium=referral&utm_campaign=2026q1-share
```

---

## UTM 链接管理表（Google Sheet 模板）

| 渠道 | 完整 URL | 短链接 | 发布日期 | 备注 |
|------|---------|-------|---------|------|
| 微信群 Week 1 | https://replymate.cn?utm_source=wechat-group... | bit.ly/rm-wg1 | 2026-03-07 | 第1轮招募 |
| 小红书帖1 | https://replymate.cn?utm_source=xiaohongshu... | bit.ly/rm-xhs1 | 2026-03-17 | 痛点共鸣 |

---

## GA4 追踪路径

```
GA4 → 报告 → 获客 → 流量获取（Traffic Acquisition）
→ 按 Session source / medium 分组
→ 查看各渠道 注册量、付费转化、MRR 贡献
```

**关键转化事件（需在 GA4 中配置）：**
- `sign_up`：用户注册
- `shop_authorized`：完成 SP-API 授权
- `first_message_sent`：发出第一条 AI 回复
- `subscription_started`：开始付费订阅
- `subscription_upgraded`：从 Starter 升级到 Pro
