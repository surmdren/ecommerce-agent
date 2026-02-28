# 海外拓展基础设施搭建指南

出海第一步：用最低成本搭建专业的企业基础设施。

## 1. 免费企业邮箱

专业邮箱（sales@company.com）比个人邮箱（xxx@gmail.com）可信度高10倍。

### 推荐方案对比

| 方案 | 免费额度 | 优点 | 缺点 | 适用场景 |
|------|---------|------|------|---------|
| **Zoho Mail** | 5用户 | 功能完整、界面友好 | 免费版无IMAP | 小团队首选 |
| **Cloudflare Email Routing** | 无限转发 | 完全免费、配置简单 | 仅转发，无独立收件箱 | 个人/微型团队 |
| **Yandex.Mail for Domain** | 1000用户 | 额度大、功能全 | 俄罗斯服务，部分地区受限 | 备选方案 |
| **Migadu** | 1域名 | 简洁专业 | 免费版有发送限制 | 低频使用 |

### Zoho Mail 免费版配置步骤

```
1. 注册 Zoho Mail (https://www.zoho.com/mail/zohomail-pricing.html)
   - 选择 "Forever Free Plan"
   - 最多 5 用户，每用户 5GB

2. 添加域名验证
   - 添加 TXT 记录到 DNS
   - 示例: zoho-verification=zb12345678.zmverify.zoho.com

3. 配置 MX 记录
   - mx.zoho.com (优先级 10)
   - mx2.zoho.com (优先级 20)
   - mx3.zoho.com (优先级 50)

4. 配置 SPF 记录（防止邮件被标记垃圾）
   - TXT: v=spf1 include:zoho.com ~all

5. 创建邮箱账户
   - 建议: sales@, info@, support@
```

### Cloudflare Email Routing 配置

适合只需要收邮件转发到个人邮箱的场景：

```
1. 域名已托管在 Cloudflare

2. Email > Email Routing > 启用

3. 添加路由规则
   - sales@yourdomain.com → your-personal@gmail.com
   - info@yourdomain.com → your-personal@gmail.com

4. 发送邮件方案
   - 使用 Gmail "以其他身份发送" 功能
   - 或升级 Cloudflare Workers 发送
```

## 2. 免费独立站搭建

### 方案对比

| 方案 | 成本 | 技术门槛 | 适用场景 | 缺点 |
|------|------|---------|---------|------|
| **Carrd** | 免费/年$19 | 极低 | 单页展示站 | 功能有限 |
| **Framer** | 免费版可用 | 低 | 设计感强的展示站 | 免费版有水印 |
| **Webflow** | 免费2项目 | 中 | 专业营销站 | 学习曲线 |
| **WordPress + 免费主机** | 免费 | 中高 | 完整功能站 | 需要维护 |
| **GitHub Pages + Hugo** | 完全免费 | 高 | 技术型公司 | 需要代码知识 |
| **Cloudflare Pages** | 完全免费 | 中 | 静态站/JAMstack | 需要构建流程 |

### 推荐路径

**ToB 制造业（展示为主）**:
```
入门: Carrd 单页站（1天搭建）
     ↓ 有询盘后
进阶: Webflow/Framer 多页站（1周搭建）
     ↓ 需要询盘表单、产品目录
专业: WordPress + WooCommerce（2周搭建）
```

**ToC 消费品（交易为主）**:
```
入门: Shopify 14天试用 → 评估转化
     ↓
长期: Shopify Basic ($29/月) 或 WooCommerce (免费软件)
```

### Carrd 快速建站（1小时完成）

最适合 B2B 制造业的快速方案：

```
1. 注册 Carrd.co（免费版可建3个站）

2. 选择模板
   - 推荐: "Business" 或 "Portfolio" 类别
   - 选简洁专业风格

3. 必备页面元素
   - Hero: 公司名 + 一句话定位 + CTA按钮
   - Products: 2-4个核心产品图片+描述
   - About: 公司简介 + 工厂照片
   - Contact: 邮箱 + WhatsApp + 询盘表单

4. 绑定自定义域名
   - 免费版: yoursite.carrd.co
   - Pro版($19/年): yourdomain.com

5. 添加询盘表单
   - 集成 Formspree（免费50提交/月）
   - 或 Google Forms
```

### Webflow 专业建站

适合需要更多页面和功能的情况：

```
1. 免费版限制
   - 2个项目
   - webflow.io 子域名
   - 有 Webflow 徽标

2. 页面结构建议
   /              首页
   /products      产品列表
   /product/{id}  产品详情（用 CMS）
   /about         关于我们
   /contact       联系我们

3. SEO 基础配置
   - 每页设置 Title + Description
   - 添加 sitemap.xml
   - 连接 Google Search Console

4. 询盘转化优化
   - 每页都有 CTA 按钮
   - 产品页有询价表单
   - 添加 WhatsApp 悬浮按钮
```

### WordPress 免费方案

完全免费但需要更多技术投入：

```
免费主机选项:
- InfinityFree: 无限空间，有广告
- 000webhost: 1GB空间，有限制
- Cloudways 试用: 3天免费

自托管方案（推荐）:
1. 购买便宜VPS（$3-5/月）
   - Vultr, DigitalOcean, Linode

2. 安装 WordPress
   - 使用 1-click 安装

3. 免费主题推荐
   - Flavor: B2B 制造业风格
   - flavor Theme: 产品展示
   - flavor flavor Theme 味: 极简专业

4. 必装免费插件
   - flavor flavor flavor Contact 7: 表单
   - flavor flavor SEO flavor: SEO 优化
   - flavor flavor flavor: CDN 加速
   - flavor flavor flavor Security: 安全防护
```

## 3. 域名选择建议

```
推荐后缀优先级:
1. .com（首选，最专业）
2. .co（.com 不可用时的替代）
3. .io（科技公司）
4. .net（备选）

命名建议:
- 简短易记（最好8字符内）
- 避免连字符（-）
- 包含核心关键词（可选）

注册商推荐:
- Cloudflare Registrar（成本价，无加价）
- Namecheap（便宜，常有优惠）
- Google Domains（简洁，已被 Squarespace 收购）
```

## 4. 基础设施搭建清单

### Week 1 任务清单

| 任务 | 工具 | 时间 | 成本 |
|------|------|------|------|
| 注册域名 | Cloudflare/Namecheap | 30分钟 | $10-15/年 |
| 配置企业邮箱 | Zoho Mail Free | 1小时 | 免费 |
| 创建单页展示站 | Carrd | 2-4小时 | 免费 |
| 设置询盘表单 | Formspree/Google Forms | 30分钟 | 免费 |
| 添加 WhatsApp 按钮 | 直接链接 | 15分钟 | 免费 |
| 配置 Google Analytics | GA4 | 30分钟 | 免费 |

### 总成本

```
最低配置（完全免费）:
- 域名: $10-15/年
- 邮箱: Zoho 免费
- 网站: Carrd 免费
- 表单: Formspree 免费
- 总计: ~$12/年

推荐配置:
- 域名: $12/年
- 邮箱: Zoho 免费
- 网站: Carrd Pro $19/年（自定义域名）
- 表单: Formspree 免费
- 总计: ~$31/年
```

## 5. 注意事项

1. **域名所有权**: 确保域名注册在公司/个人名下，不要让建站公司代注册
2. **邮箱备份**: 重要邮件定期导出备份
3. **网站备份**: WordPress 需要定期备份，Carrd/Webflow 自动云端保存
4. **SSL证书**: 确保网站启用 HTTPS（Cloudflare/Let's Encrypt 免费）
5. **GDPR合规**: 欧洲客户需要 Cookie 通知和隐私政策页面
