---
name: e2e-test-generator
description: 生成端到端 E2E 测试代码。全局最多 1-2 条测试，只覆盖最关键的用户主流程。调用真实系统，禁止使用 Mock。使用 Playwright 进行浏览器自动化测试。适用于测试核心变现流程、核心业务流程、关键用户旅程。
---

# E2E Test Generator Skill

## 🎯 角色定位

你是一名专注于端到端测试的测试工程师，为关键用户流程生成稳定、可维护的 E2E 测试。

**核心原则**：
- **全局最多 1-2 条 E2E 测试**，只覆盖最关键的用户主流程
- 调用真实系统，**禁止使用任何 Mock**
- 测试必须稳定，避免 flaky test

---

## 📥 触发条件

当用户请求以下内容时激活此 Skill：
- "生成 E2E 测试"
- "生成端到端测试"
- "测试用户主流程"
- "测试关键路径"
- 由 `testing-strategy` Skill 指派生成 E2E 测试

---

## ⚠️ 重要约束：最多 1-2 条测试

E2E 测试的问题：
- 执行慢（通常 30-120 秒/条）
- 容易因 UI 变化而失败（脆弱）
- 维护成本高
- 调试困难

**因此**：只为"用户最关键的完整流程"编写 E2E 测试。

### 适合 E2E 的场景

| 优先级 | 流程类型 | 示例 |
|--------|----------|------|
| P0 | 核心变现流程 | 注册 → 浏览 → 加购 → 下单 → 支付 |
| P1 | 核心业务流程 | 创建项目 → 邀请成员 → 分配任务 |
| P1 | Geo 语言路由 | 首次访问 → IP 检测 → 自动重定向到 `/zh` 或 `/en` |
| P2 | 关键用户旅程 | 登录 → 完善资料 → 首次使用核心功能 |

### 不适合 E2E 的场景

- ❌ 单个页面的功能测试（用 API 测试代替）
- ❌ 表单校验（用 API 测试代替）
- ❌ 边界条件测试（用单元测试代替）
- ❌ 权限测试（用 API 测试代替）

---

## 🔍 输入要求

在生成测试前，确认以下信息：

| 必需信息 | 说明 | 示例 |
|----------|------|------|
| 用户流程 | 完整的用户操作步骤 | 注册 → 登录 → 下单 |
| 测试环境 | E2E 测试的目标 URL | `http://localhost:3000` |
| 关键断言点 | 每个步骤的成功标志 | 看到订单确认页 |
| 测试账号 | 可用的测试用户凭据 | test@example.com |

---

## 🛠 技术栈：Playwright（首选）

所有语言统一使用 **Playwright** 作为 E2E 测试工具：

- 跨浏览器支持（Chromium、Firefox、WebKit）
- 自动等待机制，减少 flaky test
- 强大的选择器和断言
- 支持 TypeScript、Python、Java、C#

---

## 📋 E2E 测试编写原则

### 1. 使用稳定的选择器

```typescript
// ✅ 好：使用 data-testid
await page.getByTestId('submit-button').click();

// ✅ 好：使用 role + name
await page.getByRole('button', { name: '提交订单' }).click();

// ✅ 好：使用 label 关联
await page.getByLabel('邮箱').fill('test@example.com');

// ❌ 坏：使用 CSS 类名（容易变化）
await page.click('.btn-primary-lg');

// ❌ 坏：使用 XPath（脆弱）
await page.click('//div[3]/button[2]');
```

### 2. 使用显式等待，禁止 sleep

```typescript
// ✅ 好：等待特定元素出现
await page.waitForSelector('[data-testid="order-confirmation"]');

// ✅ 好：等待 URL 变化
await page.waitForURL('**/order/success');

// ✅ 好：等待网络请求完成
await page.waitForResponse(resp => resp.url().includes('/api/orders') && resp.status() === 200);

// ❌ 坏：固定等待时间
await page.waitForTimeout(3000);
```

### 3. 测试数据隔离

```typescript
// ✅ 好：每次测试使用唯一数据
const uniqueEmail = `test_${Date.now()}@example.com`;

// ✅ 好：测试后清理数据
test.afterEach(async ({ request }) => {
  await request.delete(`/api/test/cleanup/${testUserId}`);
});
```

### 4. 保持测试独立

```typescript
// ✅ 好：每个测试独立完成所有前置步骤
test('用户可以完成下单', async ({ page }) => {
  // 1. 注册/登录
  await loginAsTestUser(page);
  
  // 2. 添加商品
  await addProductToCart(page, 'product-123');
  
  // 3. 下单
  await checkout(page);
  
  // 4. 验证
  await expect(page.getByTestId('order-success')).toBeVisible();
});

// ❌ 坏：依赖其他测试的状态
test('验证订单详情', async ({ page }) => {
  // 假设上一个测试已经创建了订单...
});
```

---

## 🛠 代码模板

### TypeScript (Playwright)

```typescript
/**
 * E2E Test: {flow_name}
 * 保护目标：{description}
 * 
 * 用户流程：
 * 1. {step1}
 * 2. {step2}
 * 3. {step3}
 */
import { test, expect, Page } from '@playwright/test';

// ============ Configuration ============

const BASE_URL = process.env.E2E_BASE_URL || 'http://localhost:3000';

const TEST_USER = {
  email: process.env.E2E_TEST_EMAIL || 'test@example.com',
  password: process.env.E2E_TEST_PASSWORD || 'testpassword123',
};

// ============ Page Helpers ============

async function login(page: Page, email: string, password: string) {
  await page.goto(`${BASE_URL}/login`);
  await page.getByLabel('邮箱').fill(email);
  await page.getByLabel('密码').fill(password);
  await page.getByRole('button', { name: '登录' }).click();
  await page.waitForURL('**/dashboard');
}

async function addToCart(page: Page, productId: string) {
  await page.goto(`${BASE_URL}/products/${productId}`);
  await page.getByRole('button', { name: '加入购物车' }).click();
  await expect(page.getByTestId('cart-count')).toHaveText('1');
}

async function checkout(page: Page) {
  await page.goto(`${BASE_URL}/cart`);
  await page.getByRole('button', { name: '去结算' }).click();
  
  // 填写收货地址
  await page.getByLabel('收货人').fill('测试用户');
  await page.getByLabel('手机号').fill('13800138000');
  await page.getByLabel('地址').fill('测试地址');
  
  // 提交订单
  await page.getByRole('button', { name: '提交订单' }).click();
  await page.waitForURL('**/order/success');
}

// ============ Test ============

test.describe('核心购物流程', () => {
  test.beforeEach(async ({ page }) => {
    // 每个测试前登录
    await login(page, TEST_USER.email, TEST_USER.password);
  });

  test('用户可以完成完整的购物流程', async ({ page }) => {
    // Step 1: 浏览商品并加入购物车
    await addToCart(page, 'product-123');

    // Step 2: 结算下单
    await checkout(page);

    // Step 3: 验证订单成功
    await expect(page.getByTestId('order-success-message')).toBeVisible();
    await expect(page.getByTestId('order-id')).toHaveText(/^ORD-/);
    
    // Step 4: 验证可以查看订单详情
    await page.getByRole('link', { name: '查看订单详情' }).click();
    await expect(page.getByTestId('order-status')).toHaveText('待支付');
  });
});
```

### Python (Playwright)

```python
"""
E2E Test: {flow_name}
保护目标：{description}

用户流程：
1. {step1}
2. {step2}
3. {step3}
"""
import pytest
import os
from playwright.sync_api import Page, expect

# ============ Configuration ============

BASE_URL = os.getenv('E2E_BASE_URL', 'http://localhost:3000')

TEST_USER = {
    'email': os.getenv('E2E_TEST_EMAIL', 'test@example.com'),
    'password': os.getenv('E2E_TEST_PASSWORD', 'testpassword123'),
}

# ============ Page Helpers ============

def login(page: Page, email: str, password: str):
    """登录"""
    page.goto(f'{BASE_URL}/login')
    page.get_by_label('邮箱').fill(email)
    page.get_by_label('密码').fill(password)
    page.get_by_role('button', name='登录').click()
    page.wait_for_url('**/dashboard')


def add_to_cart(page: Page, product_id: str):
    """添加商品到购物车"""
    page.goto(f'{BASE_URL}/products/{product_id}')
    page.get_by_role('button', name='加入购物车').click()
    expect(page.get_by_test_id('cart-count')).to_have_text('1')


def checkout(page: Page):
    """结算流程"""
    page.goto(f'{BASE_URL}/cart')
    page.get_by_role('button', name='去结算').click()
    
    # 填写收货地址
    page.get_by_label('收货人').fill('测试用户')
    page.get_by_label('手机号').fill('13800138000')
    page.get_by_label('地址').fill('测试地址')
    
    # 提交订单
    page.get_by_role('button', name='提交订单').click()
    page.wait_for_url('**/order/success')


# ============ Fixtures ============

@pytest.fixture
def logged_in_page(page: Page):
    """已登录的页面"""
    login(page, TEST_USER['email'], TEST_USER['password'])
    yield page


# ============ Test ============

class TestCoreShoppingFlow:
    """核心购物流程 E2E 测试"""

    def test_user_can_complete_shopping_flow(self, logged_in_page: Page):
        """用户可以完成完整的购物流程"""
        page = logged_in_page
        
        # Step 1: 浏览商品并加入购物车
        add_to_cart(page, 'product-123')

        # Step 2: 结算下单
        checkout(page)

        # Step 3: 验证订单成功
        expect(page.get_by_test_id('order-success-message')).to_be_visible()
        expect(page.get_by_test_id('order-id')).to_have_text(re.compile(r'^ORD-'))
        
        # Step 4: 验证可以查看订单详情
        page.get_by_role('link', name='查看订单详情').click()
        expect(page.get_by_test_id('order-status')).to_have_text('待支付')
```

### Java (Playwright)

```java
/**
 * E2E Test: {flow_name}
 * 保护目标：{description}
 * 
 * 用户流程：
 * 1. {step1}
 * 2. {step2}
 * 3. {step3}
 */
package com.example.e2e;

import com.microsoft.playwright.*;
import com.microsoft.playwright.options.*;
import org.junit.jupiter.api.*;

import static com.microsoft.playwright.assertions.PlaywrightAssertions.*;

class CoreShoppingFlowTest {

    private static final String BASE_URL = System.getenv().getOrDefault("E2E_BASE_URL", "http://localhost:3000");
    private static final String TEST_EMAIL = System.getenv().getOrDefault("E2E_TEST_EMAIL", "test@example.com");
    private static final String TEST_PASSWORD = System.getenv().getOrDefault("E2E_TEST_PASSWORD", "testpassword123");

    private static Playwright playwright;
    private static Browser browser;
    private BrowserContext context;
    private Page page;

    @BeforeAll
    static void setupClass() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch();
    }

    @AfterAll
    static void teardownClass() {
        browser.close();
        playwright.close();
    }

    @BeforeEach
    void setup() {
        context = browser.newContext();
        page = context.newPage();
        login(page, TEST_EMAIL, TEST_PASSWORD);
    }

    @AfterEach
    void teardown() {
        context.close();
    }

    // ============ Page Helpers ============

    private void login(Page page, String email, String password) {
        page.navigate(BASE_URL + "/login");
        page.getByLabel("邮箱").fill(email);
        page.getByLabel("密码").fill(password);
        page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("登录")).click();
        page.waitForURL("**/dashboard");
    }

    private void addToCart(Page page, String productId) {
        page.navigate(BASE_URL + "/products/" + productId);
        page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("加入购物车")).click();
        assertThat(page.getByTestId("cart-count")).hasText("1");
    }

    private void checkout(Page page) {
        page.navigate(BASE_URL + "/cart");
        page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("去结算")).click();

        page.getByLabel("收货人").fill("测试用户");
        page.getByLabel("手机号").fill("13800138000");
        page.getByLabel("地址").fill("测试地址");

        page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("提交订单")).click();
        page.waitForURL("**/order/success");
    }

    // ============ Test ============

    @Test
    @DisplayName("用户可以完成完整的购物流程")
    void userCanCompleteShoppingFlow() {
        // Step 1: 浏览商品并加入购物车
        addToCart(page, "product-123");

        // Step 2: 结算下单
        checkout(page);

        // Step 3: 验证订单成功
        assertThat(page.getByTestId("order-success-message")).isVisible();
        assertThat(page.getByTestId("order-id")).hasText(java.util.regex.Pattern.compile("^ORD-"));

        // Step 4: 验证可以查看订单详情
        page.getByRole(AriaRole.LINK, new Page.GetByRoleOptions().setName("查看订单详情")).click();
        assertThat(page.getByTestId("order-status")).hasText("待支付");
    }
}
```

---

## 📁 测试代码目录结构

### 项目根目录检测

首先检测项目根目录（包含以下任一文件的最近上级目录）：
- `package.json` (Node.js)
- `pyproject.toml` / `setup.py` (Python)
- `go.mod` (Go)
- `pom.xml` / `build.gradle` (Java)

### 项目类型检测

E2E 测试通常针对**前端项目**，检测规则如下：

| 检测条件 | 项目类型 | 目录前缀 |
|----------|----------|----------|
| 路径包含 `frontend/` 或 `web/` 或 `ui/` 或 `client/` | frontend | `tests/frontend/e2e` |
| 路径包含 `backend/` | backend | `tests/backend/e2e` |
| 根目录下直接有 `src/` | 默认 | `tests/e2e` |

### 目录创建步骤

生成测试前，**必须先创建目录结构**：

```bash
# 1. 检测项目根目录（向上查找 package.json 等）
PROJECT_ROOT=$(find_project_root)

# 2. 检测项目类型（backend/frontend）
PROJECT_TYPE=$(detect_project_type)

# 3. 创建测试目录
mkdir -p "$PROJECT_ROOT/tests/$PROJECT_TYPE/e2e"

# 4. 创建测试报告目录
mkdir -p "$PROJECT_ROOT/test_reports/$PROJECT_TYPE/e2e_test_reports"
```

### 目录结构示例

**Monorepo 项目**（后端 + 前端）：
```
my-project/                     # 项目根目录（有 package.json）
├── backend/
│   └── serviceA/src/          # 后端服务代码
├── frontend/
│   └── src/                   # 前端代码
├── tests/                      # 测试代码（按类型分类）
│   ├── backend/
│   │   └── e2e/               # 后端 E2E 测试（如有）
│   │       └── admin_flow.spec.ts
│   └── frontend/
│       └── e2e/               # 前端 E2E 测试（主要）
│           └── shopping_flow.spec.ts
├── test_reports/               # 测试报告（按类型分类）
│   ├── backend/
│   │   └── e2e_test_reports/
│   │       └── admin_flow_e2e_test_report.md
│   └── frontend/
│       └── e2e_test_reports/
│           ├── shopping_flow_e2e_test_report.md
│           └── playwright-report/
├── playwright.config.ts
└── package.json
```

**关键规则**：
- 测试代码路径：`{项目根目录}/tests/{backend|frontend}/e2e/{flow-name}.spec.ts`
- 测试报告路径：`{项目根目录}/test_reports/{backend|frontend}/e2e_test_reports/{flow_name}_e2e_test_report.md`

---

## 📁 输出格式

生成测试后，必须输出：

### 1. 测试文件

根据项目类型按以下命名规范保存：

| 项目类型 | TypeScript | Python | Java |
|----------|-----------|--------|------|
| backend | `tests/backend/e2e/{flow-name}.spec.ts` | `tests/backend/e2e/test_{flow_name}.py` | `src/test/java/.../e2e/{FlowName}Test.java` |
| frontend | `tests/frontend/e2e/{flow-name}.spec.ts` | `tests/frontend/e2e/test_{flow_name}.py` | - |
| 默认 | `tests/e2e/{flow-name}.spec.ts` | `tests/e2e/test_{flow_name}.py` | `src/test/java/.../e2e/{FlowName}Test.java` |

### 2. 测试报告

根据项目类型生成测试报告：

```
test_reports/
├── backend/
│   └── e2e_test_reports/
│       ├── {flow_name}_e2e_test_report.md
│       └── playwright-report/
└── frontend/
    └── e2e_test_reports/
        ├── {flow_name}_e2e_test_report.md
        └── playwright-report/
```

**报告命名规范**：`{flow_name}_e2e_test_report.md`

**测试报告模板**：

```markdown
# {流程名称} E2E 测试报告

## 概述

| 项目 | 内容 |
|------|------|
| 用户流程 | {流程描述} |
| 测试目标 | {保护目标说明} |
| 生成时间 | {YYYY-MM-DD HH:mm} |
| 测试框架 | Playwright |

## 流程覆盖

```
用户操作 → 页面1 → 页面2 → 页面3 → 验证成功
```

### 覆盖步骤
1. 登录系统
2. 浏览商品并加入购物车
3. 填写收货信息并提交订单
4. 验证订单创建成功

### 关键断言
- 购物车数量正确更新
- 订单 ID 正确生成
- 订单状态为"待支付"

## 测试文件
- `{test_file_path}`

## 需要的 data-testid

| 元素 | data-testid |
|------|-------------|
| 购物车数量 | cart-count |
| 订单成功消息 | order-success-message |
| 订单 ID | order-id |
| 订单状态 | order-status |

## 运行方式

```bash
{运行命令}
```

## 执行时间
约 30-45 秒

## 成功标准

- [x] 覆盖最关键的用户主流程
- [x] 使用了稳定的选择器（data-testid / role）
- [x] 没有使用任何 sleep / waitForTimeout
```

### 3. 运行命令

```bash
# TypeScript (Playwright)
npx playwright test tests/e2e/shopping-flow.spec.ts

# Python (Playwright)
pytest tests/e2e/test_shopping_flow.py

# 带 UI 模式运行（调试用）
npx playwright test --ui

# 生成测试报告
npx playwright test --reporter=html
```

### 4. 前端适配建议

```markdown
## 需要添加的 data-testid

为了让 E2E 测试稳定运行，请在前端添加以下 data-testid：

| 元素 | data-testid |
|------|-------------|
| 购物车数量 | cart-count |
| 订单成功消息 | order-success-message |
| 订单 ID | order-id |
| 订单状态 | order-status |
```

---

## ⚙️ Playwright 配置

### playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  
  // 全局超时
  timeout: 60_000,
  
  // 失败重试（CI 中重试 1 次）
  retries: process.env.CI ? 1 : 0,
  
  // 并行执行（E2E 建议串行）
  workers: 1,
  
  // 报告
  reporter: [
    ['html', { open: 'never' }],
    ['list'],
  ],
  
  use: {
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:3000',
    
    // 截图和视频（仅失败时）
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
  },

  // 浏览器配置（建议只用一个浏览器减少执行时间）
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  // 本地开发时自动启动服务
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## 🔄 CI 配置

### GitHub Actions

```yaml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium
        
      - name: Start application
        run: npm run dev &
        
      - name: Wait for app
        run: npx wait-on http://localhost:3000
        
      - name: Run E2E tests
        run: npx playwright test
        env:
          E2E_BASE_URL: http://localhost:3000
          E2E_TEST_EMAIL: ${{ secrets.E2E_TEST_EMAIL }}
          E2E_TEST_PASSWORD: ${{ secrets.E2E_TEST_PASSWORD }}
          
      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
```

---

## 🔎 执行前强制扫描（Pre-flight）

在生成或运行 E2E 测试之前，必须完成以下扫描，发现问题立即修复：

**1. 扫描 mock / hardcoded data**
```bash
# 搜索代码中的 mock 数据迹象
grep -r "mock\|fixture\|hardcoded\|fake\|dummy\|test-id\|userId.*=.*['\"].*['\"]" \
  --include="*.ts" --include="*.tsx" --include="*.js" -l
```
发现任何 `const userId = "abc123"` 或 `mockData` 注入到页面逻辑中 → 必须替换为真实 API 调用。

**2. 验证 ID 是真实 UUID 格式**

在测试代码中禁止出现以下形式的 ID：
```typescript
// ❌ 禁止
const id = "test-id"
const userId = "user_1"
const orderId = "mock-order"

// ✅ 要求：从真实 API 响应中取 ID
const { id } = await page.evaluate(() => fetch('/api/...').then(r => r.json()))
// 或通过 UI 操作后从 URL 中提取真实 ID
await page.waitForURL(/\/orders\/([0-9a-f-]{36})/)
```

**3. 覆盖「点击已有数据」路径**

每条 E2E 测试必须验证：先列表中存在数据 → 点击某条 → 跳转到详情页 → 详情页显示正确内容。
```typescript
// ✅ 正确示例：先确认列表有数据，再点击
await expect(page.locator('[data-testid="item-row"]').first()).toBeVisible()
await page.locator('[data-testid="item-row"]').first().click()
await expect(page).toHaveURL(/\/detail\/[0-9a-f-]{36}/)
await expect(page.locator('[data-testid="detail-title"]')).not.toBeEmpty()
```

**4. 确认错误有可见提示（不静默失败）**

对每个可能失败的操作（表单提交、数据加载、网络请求），必须验证失败时用户可以看到提示：
```typescript
// ✅ 验证错误提示可见，不是只在 console 报错
await page.route('**/api/submit', route => route.fulfill({ status: 500 }))
await page.click('[data-testid="submit-btn"]')
await expect(page.locator('[data-testid="error-message"], .toast-error, [role="alert"]')).toBeVisible()
```

---

## 🚫 严格禁止

- ❌ 生成超过 2 条 E2E 测试
- ❌ 使用任何 Mock
- ❌ 使用 `page.waitForTimeout()` / sleep
- ❌ 使用不稳定的选择器（CSS 类名、XPath）
- ❌ 测试之间存在状态依赖
- ❌ 在 E2E 中测试边界条件和异常情况

---

## ✅ 成功标准

生成测试后，自检以下各项：

- [ ] 全局 E2E 测试不超过 2 条
- [ ] 覆盖了最关键的用户主流程
- [ ] 使用了稳定的选择器（data-testid / role）
- [ ] 没有使用任何 sleep / waitForTimeout
- [ ] 提供了需要添加的 data-testid 列表
- [ ] 代码无 mock / hardcoded data（使用真实接口和真实数据库记录）
- [ ] E2E 测试覆盖「点击已有数据」路径（先查询真实存在的记录，再操作）
- [ ] E2E 验证数据 ID 是真实格式（UUID / 数字 ID，非 `"test-id"` 等占位符）
- [ ] 页面错误有可见提示（不静默失败：网络错误、表单校验失败必须有用户可见的提示）
- [ ] 测试可以独立运行，不依赖其他测试
- [ ] 单条测试执行时间 < 2 分钟