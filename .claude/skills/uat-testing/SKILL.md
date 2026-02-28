---
name: uat-testing
description: 用户验收测试（UAT）。从真实用户视角出发，基于 PRD 用户故事和用户角色定义，执行端到端浏览器自动化测试（Playwright），验证产品功能符合用户期望，操作流程自然顺畅，关键业务路径无阻断。输出用户视角的验收报告，存放到 UAT/ 目录。应在 release-qa 技术验收通过后、正式发布前执行。当用户提到"UAT"、"用户验收"、"用户测试"、"用户侧测试"、"uat testing"、"用户场景测试"、"验收用户故事"时触发。
---

# UAT Testing - 用户验收测试

## 定位

**前提**：release-qa 技术验收已通过，服务已在测试环境运行。
**视角**：以真实用户身份操作，不关注技术实现，只关注体验和结果。
**目标**：确保用户能完成 PRD 中描述的每一个用户故事，流程无阻断，结果符合预期。

与其他测试 Skill 的区别：

| Skill | 驱动源 | 视角 | 关注点 |
|-------|--------|------|--------|
| `release-qa` | PRD + 技术文档 | 技术 | API 契约、数据流、代码正确性 |
| `dev-integration` | DevPlan 模块 | 技术 | 模块集成 |
| **uat-testing** | PRD 用户故事 + 用户角色 | 用户 | 操作体验、业务流程完整性 |

## 工作流程

### Step 1: 解析 PRD，构建用户场景清单

读取 PRD 文档，提取四类场景：

**① 正向用户故事**（每角色的核心任务）
```
"作为 [角色]，我希望 [操作]，以便 [价值]"
→ 每条用户故事 = 一个 UAT 场景
```

**② 跨角色交互链条**（识别角色间的依赖顺序）
```
识别模式："[角色A] 完成后，[角色B] 才能继续"
示例：商家发布商品 → 管理员审核通过 → 买家才能购买
→ 每条链条 = 一个多角色联动场景
```

**③ 权限边界（负向场景）**
```
对每个角色，列出"不该做到的事"：
  - 买家不能访问商家后台
  - 未登录用户不能进入需鉴权页面
  - 普通用户不能执行管理员操作
→ 每条限制 = 一个权限边界测试
```

**④ 异步结果验收**
```
识别操作完成后有延迟副作用的场景：
  - 下单 → 用户收到确认邮件
  - 申请提交 → 状态变为"审核中"
→ 每条异步流 = 轮询验证 + 最终状态断言
```

构建**用户场景清单**（见 `references/uat-scenario-template.md`），每行包含：
- 用户角色（可以是多角色）
- 场景类型（正向 / 跨角色 / 权限边界 / 异步）
- 测试步骤（模拟真实操作）
- 通过标准（用户视角可观察的结果）

### Step 2: 确认测试环境 + 数据播种 + 执行前扫描

**环境确认：**
```
1. 确认前端 URL（如 http://localhost:3000）
2. 确认各角色测试账号（管理员/商家/买家/游客）
3. 确认 Playwright 已安装（npx playwright install）
```

**数据播种（Test Data Seeding）** — 在运行 Playwright 之前，通过 API 或脚本确保数据库中有可操作的真实数据：

```typescript
// UAT/scripts/seed-data.ts
// 运行：npx ts-node UAT/scripts/seed-data.ts

const BASE_URL = 'http://localhost:3000'

async function seed() {
  // 1. 用商家账号创建商品（确保列表有数据可点）
  const sellerToken = await login('seller@test.com', 'Test1234!')
  const product = await fetch(`${BASE_URL}/api/products`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${sellerToken}` },
    body: JSON.stringify({ name: 'UAT测试商品', price: 99, stock: 10 })
  }).then(r => r.json())

  // 2. 用管理员账号审核通过（确保买家能看到商品）
  const adminToken = await login('admin@test.com', 'Admin1234!')
  await fetch(`${BASE_URL}/api/admin/products/${product.id}/approve`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${adminToken}` }
  })

  // 3. 用买家账号创建订单（确保订单列表有数据）
  const buyerToken = await login('buyer@test.com', 'Test1234!')
  await fetch(`${BASE_URL}/api/orders`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${buyerToken}` },
    body: JSON.stringify({ productId: product.id, quantity: 1 })
  })

  console.log('✅ 测试数据播种完成')
}
seed()
```

播种失败 → 写入 `UAT/BLOCKED.md` 并停止，不能在空数据库上跑 UAT。

若测试环境未准备好，输出到 `UAT/BLOCKED.md` 并停止。

**执行前强制扫描（Pre-flight）** — 在写测试代码之前完成：

**① 扫描 mock / hardcoded data**
```bash
grep -r "mock\|fixture\|hardcoded\|fake\|dummy\|test-id" \
  --include="*.ts" --include="*.tsx" --include="*.js" -l
```
发现前端代码中有写死的假数据渲染到页面 → 记录到 `UAT/BLOCKED.md`，要求开发先修复。

**② 验证数据 ID 是真实格式**

测试代码中禁止硬编码 ID，必须从真实系统获取：
```typescript
// ❌ 禁止
await page.goto('/orders/test-order-id')

// ✅ 从列表页取真实 ID 再跳转
await page.goto('/orders')
const firstOrderLink = page.locator('[data-testid="order-row"] a').first()
const href = await firstOrderLink.getAttribute('href')
// href 应为 /orders/550e8400-e29b-41d4-a716-446655440000 （真实 UUID）
expect(href).toMatch(/\/orders\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/)
```

**③ 覆盖「点击已有数据」跳转路径**

每个涉及详情页的场景必须验证：列表有数据 → 点击 → 跳转 → 详情内容正确显示：
```typescript
await expect(page.locator('[data-testid="list-item"]').first()).toBeVisible()
await page.locator('[data-testid="list-item"]').first().click()
await expect(page).toHaveURL(/\/detail\/[0-9a-f-]{36}/)
await expect(page.locator('[data-testid="detail-content"]')).not.toBeEmpty()
```

**④ 确认页面错误有可见提示**

对核心操作（提交表单、加载数据），验证失败时用户能看到提示，不是静默失败：
```typescript
// 模拟网络错误，确认错误提示出现
await page.route('**/api/**', route => route.abort())
await page.click('[data-testid="submit-btn"]')
await expect(page.locator('[role="alert"], .error-toast, [data-testid="error-msg"]')).toBeVisible()
```

### Step 3: 生成并执行 Playwright 测试

对每个用户场景生成 Playwright 测试文件，保存到 `UAT/tests/`：

```typescript
// 文件命名：UAT/tests/{角色}-{场景编号}-{场景名}.spec.ts
// 示例：UAT/tests/buyer-01-register-and-purchase.spec.ts

test('买家可以注册账号并完成首次购买', async ({ page }) => {
  // 模拟真实用户操作，不调用 API
  await page.goto('http://localhost:3000/register')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'SecurePass123!')
  await page.click('button[type="submit"]')
  // 验证用户视角可见的结果
  await expect(page.locator('.welcome-message')).toBeVisible()
})
```

**测试原则**：
- 只用浏览器 UI 操作，不直接调用 API（用户不知道有 API）
- 使用真实账号，不 Mock 数据
- 验证用户看到的内容（文字、元素可见、跳转页面）
- 每个场景测试完整的用户旅程，从入口到结果

**跨角色交互链条示例**（商家→管理员→买家）：
```typescript
// UAT/tests/cross-role-01-product-lifecycle.spec.ts
test('商家发布 → 管理员审核 → 买家购买 完整链条', async ({ browser }) => {
  // Role 1: 商家发布商品
  const sellerCtx = await browser.newContext()
  const sellerPage = await sellerCtx.newPage()
  await loginAs(sellerPage, 'seller@test.com')
  await sellerPage.goto('/seller/products/new')
  await sellerPage.fill('[name="name"]', '链条测试商品')
  await sellerPage.click('[data-testid="submit"]')
  await expect(sellerPage.locator('text=待审核')).toBeVisible()

  // Role 2: 管理员审核通过
  const adminCtx = await browser.newContext()
  const adminPage = await adminCtx.newPage()
  await loginAs(adminPage, 'admin@test.com')
  await adminPage.goto('/admin/products?status=pending')
  await adminPage.locator('text=链条测试商品').first().click()
  await adminPage.click('[data-testid="approve-btn"]')
  await expect(adminPage.locator('text=已上架')).toBeVisible()

  // Role 3: 买家能搜到并购买
  const buyerCtx = await browser.newContext()
  const buyerPage = await buyerCtx.newPage()
  await loginAs(buyerPage, 'buyer@test.com')
  await buyerPage.goto('/')
  await buyerPage.fill('[placeholder="搜索"]', '链条测试商品')
  await buyerPage.press('[placeholder="搜索"]', 'Enter')
  await expect(buyerPage.locator('text=链条测试商品')).toBeVisible()
})
```

**权限边界（负向场景）示例**：
```typescript
// UAT/tests/permission-boundary.spec.ts
test('买家无法访问商家后台', async ({ page }) => {
  await loginAs(page, 'buyer@test.com')
  await page.goto('/seller/dashboard')
  // 应跳转到首页或显示 403，不能直接渲染后台
  await expect(page).not.toHaveURL('/seller/dashboard')
})

test('未登录用户访问个人中心应跳转到登录页', async ({ page }) => {
  await page.goto('/profile')
  await expect(page).toHaveURL(/\/login/)
})
```

**异步副作用验证示例**（轮询状态变更）：
```typescript
// UAT/tests/buyer-04-order-status.spec.ts
test('下单后订单状态变为处理中', async ({ page }) => {
  await loginAs(page, 'buyer@test.com')
  // 下单
  await page.goto('/cart')
  await page.click('[data-testid="checkout-btn"]')
  await page.click('[data-testid="confirm-order"]')
  // 等待异步状态更新（轮询最多 10 秒）
  await expect(async () => {
    await page.reload()
    await expect(page.locator('[data-testid="order-status"]')).toHaveText('处理中')
  }).toPass({ timeout: 10000 })
})
```

**i18n 语言切换场景**（必须覆盖）：
```typescript
// UAT/tests/i18n-01-language-switch.spec.ts
test('用户可以切换语言，所有文案正确变换', async ({ page }) => {
  await page.goto('http://localhost:3000/zh')
  // 验证默认中文
  await expect(page.locator('[data-testid="nav-home"]')).toHaveText('首页')

  // 切换到英文
  await page.click('[data-testid="lang-switcher"]')
  await page.click('[data-testid="lang-en"]')
  await expect(page).toHaveURL(/\/en\//)
  await expect(page.locator('[data-testid="nav-home"]')).toHaveText('Home')

  // 切回中文
  await page.click('[data-testid="lang-switcher"]')
  await page.click('[data-testid="lang-zh"]')
  await expect(page).toHaveURL(/\/zh\//)
  await expect(page.locator('[data-testid="nav-home"]')).toHaveText('首页')
})

test('语言偏好在刷新后保持', async ({ page }) => {
  await page.goto('http://localhost:3000/zh')
  // 切换到英文
  await page.click('[data-testid="lang-switcher"]')
  await page.click('[data-testid="lang-en"]')
  await expect(page).toHaveURL(/\/en\//)

  // 刷新页面，应保持英文（cookie 持久化）
  await page.reload()
  await expect(page).toHaveURL(/\/en\//)
  await expect(page.locator('[data-testid="nav-home"]')).toHaveText('Home')
})
```

**移动端视口测试**（在 playwright.config.ts 中配置，或单独指定）：
```typescript
// 在关键场景上追加移动端测试
test('买家可在手机端完成购买', async ({ browser }) => {
  const ctx = await browser.newContext({
    viewport: { width: 390, height: 844 },  // iPhone 14
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'
  })
  const page = await ctx.newPage()
  // 同样的购买流程在移动端验证
})
```

执行测试：

```bash
cd UAT/tests && npx playwright test --reporter=html
```

### Step 4: 分析结果，修复关键阻断

```
对每个失败场景：
  1. 截图 + 录屏查看用户看到了什么
  2. 判断类型：
     - UI 阻断（按钮不见、页面空白、无法提交）→ 修复前端
     - 功能缺失（操作完成但无结果）→ 修复业务逻辑
     - 流程中断（某步骤后无法继续）→ 修复流程
     - 文案/体验问题（非阻断）→ 记录为偏差
  3. 修复后重新执行该场景
```

**原则**：不降低通过标准，不跳过阻断场景。

### Step 5: 生成 UAT 验收报告

输出到 `UAT/uat-report.md`：

```markdown
# UAT 用户验收报告

测试时间：{date}
测试环境：{url}
测试版本：{git hash}

## 执行概览

| 用户角色 | 场景总数 | 通过 | 失败 | 偏差 |
|---------|---------|------|------|------|
| 买家 | N | N | N | N |
| 商家 | N | N | N | N |
| 管理员 | N | N | N | N |

## 用户场景详情

[每个场景的测试结果、截图链接]

## 问题清单

### 🚫 阻断问题（用户无法完成核心操作）
### ⚠️ 体验偏差（功能可用但与预期不符）
### 📝 建议改进（非阻断的体验优化）

## 修复记录

[已修复问题及验证截图]

## 结论

- [ ] 所有用户角色可完成其核心任务
- [ ] 关键购买/注册/核心业务流程无阻断
- [ ] 无用户视角的严重体验问题
- [ ] ✅ 可以进行 dev-deploy 部署
```

## 输出产物

| 产物 | 路径 |
|------|------|
| 用户场景清单 | `UAT/uat-scenarios.md` |
| 数据播种脚本 | `UAT/scripts/seed-data.ts` |
| Playwright 测试代码 | `UAT/tests/` |
| 测试报告（HTML） | `UAT/playwright-report/` |
| 验收报告 | `UAT/uat-report.md` |
| 阻断记录 | `UAT/BLOCKED.md`（若有） |

## 参考资源

- **用户场景模板**：见 `references/uat-scenario-template.md`

## 注意事项

1. **用户视角优先**：测试时想象自己是第一次使用产品的用户，不带技术知识
2. **完整旅程**：每个场景从用户的进入点开始，测试完整操作流程，不只测单个页面
3. **真实数据**：使用真实账号和测试数据，不绕过正常流程
4. **截图留存**：所有关键步骤自动截图，方便问题复现和报告
5. **阻断优先**：优先修复阻止用户完成核心操作的问题

## ✅ 测试完成自检清单

**数据质量**
- [ ] 数据播种脚本已运行，列表页有真实数据可操作
- [ ] 代码无 mock / hardcoded data（所有数据来自真实系统）
- [ ] 测试覆盖「点击已有数据」路径（先通过 UI 查询到真实存在的记录，再点击操作）
- [ ] 验证数据 ID 是真实格式（UUID / 数字 ID，非 `"test-id"` 等占位符）

**场景覆盖**
- [ ] 所有用户角色的核心正向路径已测试
- [ ] 跨角色交互链条已测试（A 角色操作后，B 角色能继续的完整链路）
- [ ] 权限边界已验证（各角色无法访问非授权页面 / 操作）
- [ ] 异步副作用已验证（状态变更、后台任务最终结果）

**体验质量**
- [ ] 页面错误有可见提示（网络失败、操作失败不静默消失）
- [ ] 移动端视口（390px）核心流程已测试

**i18n 双语验收（必须）**
- [ ] 语言切换后所有页面文案切换为对应语言（无遗漏硬编码文字）
- [ ] 切换语言后刷新页面，语言偏好保持不变（cookie 持久化）
