---
name: integration-test-generator
description: 生成多 API 组合的业务场景集成测试代码。测试多个 API 端点之间的协作，验证完整的业务流程。不涉及 UI，纯后端集成测试。禁止使用 Mock。适用于验证 API 间协作、业务流程集成、回归测试。当用户提到"集成测试"、"API流程测试"、"业务场景测试"、"多API测试"时触发。
---

# API 集成测试生成器

## Overview

生成跨多个 API 端点的业务场景集成测试代码，验证 API 之间的协作是否正确。

```
┌─────────────────────────────────────────────────────────────────┐
│                     测试层级对比                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  E2E Tests (e2e-test-generator)                                │
│  └─ 浏览器 UI → 多页面 → 完整用户流程                             │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │  Integration Tests (integration-test-generator)            │   │
│  │  └─ API → API → API : 多端点协作，业务流程                 │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                 │
│  API Tests (api-test-generator)                                 │
│  └─ 单个 API 端点 : 多种场景                                    │
│                                                                 │
│  Unit Tests (unit-test-generator)                               │
│  └─ 函数/类 : 内部逻辑                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 核心原则

- **禁止 Mock**：调用真实的 API 端点
- **业务流程**：测试完整的 API 调用链
- **数据清理**：每个测试负责自己的数据准备和清理
- **可重复性**：测试之间相互独立，可重复执行

## 输入要求

生成测试前，确认以下信息（如缺失则主动询问）：

| 必需信息 | 说明 | 示例 |
|----------|------|------|
| API 流程定义 | 按顺序调用的 API 列表 | `POST /users → POST /orders → POST /payments` |
| 技术栈 | 语言和框架 | Python + FastAPI |
| 环境配置 | 测试环境地址 | `http://localhost:8000` |
| 鉴权方式 | 如何获取 Token | Bearer Token |

## 测试流程设计模板

每个集成测试包含以下步骤：

```
## 测试场景：{场景名称}

### 步骤
1. {前置条件} - 调用 API A
2. {业务动作} - 调用 API B，使用 API A 的返回值
3. {后续操作} - 调用 API C，使用 API B 的返回值
4. {验证} - 验证最终状态

### 测试用例
- 正常流程：所有步骤成功
- 边界条件：某个步骤返回错误
- 数据验证：最终数据正确性
```

## 代码模板

### Python (pytest + httpx)

```python
"""
Integration Tests: {场景名称}
测试流程：{API1} → {API2} → {API3}
"""
import pytest
import httpx
from typing import Generator

# ============ Fixtures ============

@pytest.fixture(scope="module")
def base_url() -> str:
    return "http://localhost:8000"

@pytest.fixture(scope="module")
def auth_headers(base_url: str) -> dict:
    """获取认证 Token"""
    response = httpx.post(f"{base_url}/api/auth/login", json={
        "username": "test_user",
        "password": "test_password"
    })
    assert response.status_code == 200
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def client() -> Generator[httpx.Client, None, None]:
    with httpx.Client(timeout=30.0) as client:
        yield client

# ============ Integration Tests: Happy Path ============

def test_{scenario_name}_success(client: httpx.Client, base_url: str, auth_headers: dict):
    """
    测试场景：{场景描述}

    步骤：
    1. {步骤1}
    2. {步骤2}
    3. {步骤3}
    """
    # Step 1: {步骤1描述}
    response_1 = client.post(
        f"{base_url}/api/{endpoint1}",
        json={{"field1": "value1"}},
        headers=auth_headers
    )
    assert response_1.status_code == 201, f"Step 1 failed: {response_1.text}"
    data_1 = response_1.json()
    resource_id = data_1["id"]

    # Step 2: {步骤2描述}
    response_2 = client.post(
        f"{base_url}/api/{endpoint2}",
        json={{"ref_id": resource_id, "field2": "value2"}},
        headers=auth_headers
    )
    assert response_2.status_code == 201, f"Step 2 failed: {response_2.text}"
    data_2 = response_2.json()

    # Step 3: {步骤3描述}
    response_3 = client.get(
        f"{base_url}/api/{endpoint3}/{data_2['id']}",
        headers=auth_headers
    )
    assert response_3.status_code == 200, f"Step 3 failed: {response_3.text}"
    data_3 = response_3.json()

    # 验证最终状态
    assert data_3["status"] == "expected_status"

# ============ Integration Tests: Error Handling ============

def test_{scenario_name}_step2_fails(client: httpx.Client, base_url: str, auth_headers: dict):
    """
    测试场景：{步骤2} 失败时的处理
    """
    # Step 1: 创建资源
    response_1 = client.post(
        f"{base_url}/api/{endpoint1}",
        json={{"field1": "value1"}},
        headers=auth_headers
    )
    assert response_1.status_code == 201
    resource_id = response_1.json()["id"]

    # Step 2: 故意传无效数据
    response_2 = client.post(
        f"{base_url}/api/{endpoint2}",
        json={{"ref_id": resource_id, "field2": "invalid_value"}},
        headers=auth_headers
    )
    assert response_2.status_code == 400
```

### Node.js (Vitest + supertest)

```typescript
/**
 * Integration Tests: {场景名称}
 * 测试流程：{API1} → {API2} → {API3}
 */
import { describe, it, expect, beforeAll, afterEach } from 'vitest';
import request from 'supertest';

const BASE_URL = process.env.TEST_API_URL || 'http://localhost:3000';
let authToken: string;

beforeAll(async () => {
  // 获取认证 Token
  const response = await request(BASE_URL)
    .post('/api/auth/login')
    .send({ username: 'test_user', password: 'test_password' });
  authToken = response.body.token;
});

describe('{场景名称}', () => {
  let createdResourceId: string;

  afterEach(async () => {
    // 清理测试数据
    if (createdResourceId) {
      await request(BASE_URL)
        .delete(`/api/resources/${createdResourceId}`)
        .set('Authorization', `Bearer ${authToken}`);
      createdResourceId = '';
    }
  });

  it('完整流程：所有步骤成功', async () => {
    // Step 1: {步骤1描述}
    const response1 = await request(BASE_URL)
      .post('/api/{endpoint1}')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ field1: 'value1' });

    expect(response1.status).toBe(201);
    expect(response1.body).toHaveProperty('id');
    createdResourceId = response1.body.id;

    // Step 2: {步骤2描述}
    const response2 = await request(BASE_URL)
      .post('/api/{endpoint2}')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ refId: createdResourceId, field2: 'value2' });

    expect(response2.status).toBe(201);
    expect(response2.body).toHaveProperty('id');
    const relatedId = response2.body.id;

    // Step 3: {步骤3描述}
    const response3 = await request(BASE_URL)
      .get(`/api/{endpoint3}/${relatedId}`)
      .set('Authorization', `Bearer ${authToken}`);

    expect(response3.status).toBe(200);
    expect(response3.body.status).toBe('expected_status');
  });

  it('错误处理：中间步骤失败', async () => {
    // Step 1: 创建资源
    const response1 = await request(BASE_URL)
      .post('/api/{endpoint1}')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ field1: 'value1' });

    expect(response1.status).toBe(201);
    const resourceId = response1.body.id;

    // Step 2: 传无效数据
    const response2 = await request(BASE_URL)
      .post('/api/{endpoint2}')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ refId: resourceId, field2: 'invalid' });

    expect(response2.status).toBe(400);
  });
});
```

### Go (testing + testify)

```go
// {scenario_name}_integration_test.go
// Integration Tests: {场景名称}
// 测试流程：{API1} → {API2} → {API3}
package integration_test

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

var baseURL = "http://localhost:8080"
var authToken string

func TestMain(m *testing.M) {
	// 获取 Token
	resp, _ := http.Post(baseURL+"/api/auth/login", "application/json",
		bytes.NewReader([]byte(`{"username":"test","password":"test"}`)))
	var tokenResp map[string]string
	json.NewDecoder(resp.Body).Decode(&tokenResp)
	authToken = tokenResp["token"]

	m.Run()
}

func Test{ScenarioName}_Success(t *testing.T) {
	// Step 1: 创建资源
	body1, _ := json.Marshal(map[string]string{"field1": "value1"})
	req1, _ := http.NewRequest("POST", baseURL+"/api/{endpoint1}", bytes.NewBuffer(body1))
	req1.Header.Set("Authorization", "Bearer "+authToken)
	req1.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp1, err := client.Do(req1)
	require.NoError(t, err)
	defer resp1.Body.Close()

	assert.Equal(t, 201, resp1.StatusCode)

	var data1 map[string]interface{}
	json.NewDecoder(resp1.Body).Decode(&data1)
	resourceID := data1["id"].(string)

	// Step 2: 关联操作
	body2, _ := json.Marshal(map[string]string{
		"ref_id":  resourceID,
		"field2":  "value2",
	})
	req2, _ := http.NewRequest("POST", baseURL+"/api/{endpoint2}", bytes.NewBuffer(body2))
	req2.Header.Set("Authorization", "Bearer "+authToken)
	req2.Header.Set("Content-Type", "application/json")

	resp2, err := client.Do(req2)
	require.NoError(t, err)
	defer resp2.Body.Close()

	assert.Equal(t, 201, resp2.StatusCode)

	var data2 map[string]interface{}
	json.NewDecoder(resp2.Body).Decode(&data2)
	relatedID := data2["id"].(string)

	// Step 3: 验证结果
	req3, _ := http.NewRequest("GET", baseURL+"/api/{endpoint3}/"+relatedID, nil)
	req3.Header.Set("Authorization", "Bearer "+authToken)

	resp3, err := client.Do(req3)
	require.NoError(t, err)
	defer resp3.Body.Close()

	assert.Equal(t, 200, resp3.StatusCode)

	var data3 map[string]interface{}
	json.NewDecoder(resp3.Body).Decode(&data3)
	assert.Equal(t, "expected_status", data3["status"])
}
```

### Java (JUnit 5 + REST Assured)

```java
/**
 * Integration Tests: {场景名称}
 * 测试流程：{API1} → {API2} → {API3}
 */
package com.example.integration;

import io.restassured.RestAssured;
import io.restassured.response.Response;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.TestMethodOrder;

import static io.restassured.RestAssured.*;
import static io.restassured.matcher.Matchers.*;
import static org.hamcrest.Matchers.notNullValue;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class {ScenarioName}IntegrationTest {

    private static String authToken;
    private static String createdResourceId;

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = "http://localhost:8080";

        // 获取 Token
        authToken = given()
            .contentType("application/json")
            .body("{\"username\":\"test\",\"password\":\"test\"}")
            .when()
            .post("/api/auth/login")
            .then()
            .extract()
            .path("token");
    }

    @Test
    @Order(1)
    @DisplayName("完整流程：所有步骤成功")
    void testSuccess() {
        // Step 1: 创建资源
        Response response1 = given()
            .contentType("application/json")
            .header("Authorization", "Bearer " + authToken)
            .body("{\"field1\":\"value1\"}")
            .when()
            .post("/api/{endpoint1}")
            .then()
            .statusCode(201)
            .body("id", notNullValue())
            .extract()
            .response();

        createdResourceId = response1.path("id");

        // Step 2: 关联操作
        String relatedId = given()
            .contentType("application/json")
            .header("Authorization", "Bearer " + authToken)
            .body(String.format("{\"ref_id\":\"%s\",\"field2\":\"value2\"}", createdResourceId))
            .when()
            .post("/api/{endpoint2}")
            .then()
            .statusCode(201)
            .body("id", notNullValue())
            .extract()
            .path("id");

        // Step 3: 验证结果
        given()
            .header("Authorization", "Bearer " + authToken)
            .when()
            .get("/api/{endpoint3}/" + relatedId)
            .then()
            .statusCode(200)
            .body("status", equalTo("expected_status"));
    }

    @AfterAll
    static void cleanup() {
        if (createdResourceId != null) {
            given()
                .header("Authorization", "Bearer " + authToken)
                .when()
                .delete("/api/resources/" + createdResourceId);
        }
    }
}
```

---

## 测试代码目录结构

### 项目根目录检测

首先检测项目根目录（包含以下任一文件的最近上级目录）：
- `package.json` (Node.js)
- `pyproject.toml` / `setup.py` (Python)
- `go.mod` (Go)
- `pom.xml` / `build.gradle` (Java)

### 项目类型检测

根据当前工作目录判断项目类型：

| 检测条件 | 项目类型 | 目录前缀 |
|----------|----------|----------|
| 路径包含 `backend/` 或 `api/` 或 `services/` | backend | `tests/backend/integration` |
| 路径包含 `frontend/` 或 `web/` 或 `ui/` 或 `client/` | frontend | `tests/frontend/integration` |
| 根目录下直接有 `src/` | 默认 | `tests/integration` |

### 目录创建步骤

生成测试前，**必须先创建目录结构**：

```bash
# 1. 检测项目根目录（向上查找 package.json 等）
PROJECT_ROOT=$(find_project_root)

# 2. 检测项目类型（backend/frontend）
PROJECT_TYPE=$(detect_project_type)

# 3. 创建测试目录
mkdir -p "$PROJECT_ROOT/tests/$PROJECT_TYPE/integration"

# 4. 创建测试报告目录
mkdir -p "$PROJECT_ROOT/test_reports/$PROJECT_TYPE/integration_test_reports"
```

### 目录结构示例

**Monorepo 项目**（后端 + 前端）：
```
my-project/                     # 项目根目录（有 package.json）
├── backend/
│   ├── serviceA/src/          # 后端服务代码
│   └── serviceB/src/
├── frontend/
│   └── src/                   # 前端代码
├── tests/                      # 测试代码（按类型分类）
│   ├── backend/
│   │   └── integration/       # 后端集成测试
│   │       └── test_order_flow_integration.py
│   └── frontend/
│       └── integration/       # 前端集成测试
│           └── test_cart_flow_integration.test.ts
└── test_reports/               # 测试报告（按类型分类）
    ├── backend/
    │   └── integration_test_reports/
    │       └── order_flow_integration_test_report.md
    └── frontend/
        └── integration_test_reports/
            └── cart_flow_integration_test_report.md
```

**关键规则**：
- 测试代码路径：`{项目根目录}/tests/{backend|frontend}/integration/test_{scenario}_integration.py`
- 测试报告路径：`{项目根目录}/test_reports/{backend|frontend}/integration_test_reports/{scenario}_integration_test_report.md`

---

## 输出格式

### 文件命名

根据项目类型按以下命名规范保存：

| 项目类型 | Python | Node.js | Go | Java |
|----------|--------|---------|-----|------|
| backend | `tests/backend/integration/test_{scenario_name}_integration.py` | `tests/backend/integration/{scenario}.integration.test.ts` | `tests/backend/integration/{scenario_name}_integration_test.go` | `src/test/java/.../integration/{ScenarioName}IntegrationTest.java` |
| frontend | `tests/frontend/integration/test_{scenario_name}_integration.py` | `tests/frontend/integration/{scenario}.integration.test.ts` | - | - |
| 默认 | `tests/integration/test_{scenario_name}_integration.py` | `tests/integration/{scenario}.integration.test.ts` | `tests/integration/{scenario_name}_integration_test.go` | `src/test/java/.../integration/{ScenarioName}IntegrationTest.java` |

### 测试说明表

```markdown
| 测试函数 | 场景 | 覆盖的 API |
|----------|------|-----------|
| test_{scenario}_success | 完整流程成功 | POST /api/e1 → POST /api/e2 → GET /api/e3 |
| test_{scenario}_step2_fails | 步骤2失败处理 | POST /api/e1 → POST /api/e2 |
```

### 测试报告

根据项目类型生成测试报告：

```
test_reports/
├── backend/
│   └── integration_test_reports/
│       └── {scenario_name}_integration_test_report.md
└── frontend/
    └── integration_test_reports/
        └── {scenario_name}_integration_test_report.md
```

**报告命名规范**：`{scenario_name}_integration_test_report.md`

**测试报告模板**：

```markdown
# {场景名称} 集成测试报告

## 概述

| 项目 | 内容 |
|------|------|
| 业务场景 | {场景描述} |
| 测试目标 | {保护目标说明} |
| 生成时间 | {YYYY-MM-DD HH:mm} |
| 测试框架 | {pytest/supertest/go test/junit} |

## 测试流程

```
API1 → API2 → API3 → 验证
```

## 测试覆盖

### 测试文件
- `{test_file_path}`

### 测试用例统计

| 测试函数 | 场景 | 覆盖的 API |
|----------|------|-----------|
| test_{scenario}_success | 完整流程成功 | POST /api/e1 → POST /api/e2 → GET /api/e3 |
| test_{scenario}_step2_fails | 步骤2失败处理 | POST /api/e1 → POST /api/e2 |

## 运行方式

```bash
{运行命令}
```

## 成功标准

- [x] 覆盖完整业务流程的 Happy Path
- [x] 覆盖关键步骤的失败场景
- [x] 没有使用任何 Mock
- [x] 测试数据有清理策略
```

## 运行命令

```bash
# Python
pytest tests/integration/test_{scenario}_integration.py -v

# Node.js
pnpm test tests/integration/{scenario}.integration.test.ts

# Go
go test ./tests/integration/... -v -run Test{ScenarioName}

# Java
mvn test -Dtest={ScenarioName}IntegrationTest
```

## 常见业务场景模板

### 用户注册 → 创建订单 → 支付

```yaml
场景: 用户下单支付
流程:
  - POST /api/users (注册)
  - POST /api/auth/login (登录获取 Token)
  - POST /api/orders (创建订单)
  - POST /api/orders/{id}/pay (支付)

测试用例:
  - 正常流程: 新用户注册到支付成功
  - 用户已存在: 直接登录后下单
  - 订单创建失败: 库存不足
  - 支付失败: 余额不足
```

### 商户创建 → 商品上架 → 库存设置

```yaml
场景: 商户配置商品
流程:
  - POST /api/merchants (创建商户)
  - POST /api/merchants/{id}/products (添加商品)
  - PATCH /api/inventory/{product_id} (设置库存)

测试用例:
  - 正常流程: 完整配置流程
  - 商品已存在: 更新商品信息
  - 库存为0: 下单时提示缺货
```

## 禁止事项

- ❌ 使用任何 Mock（数据库、HTTP、服务）
- ❌ 跳过某个 API 调用
- ❌ 测试之间存在数据依赖
- ❌ 硬编码敏感信息（Token、密码）
- ❌ 使用 sleep / 固定时间等待

## 成功标准

生成测试后，自检以下各项：

- [ ] 覆盖了完整业务流程的 Happy Path
- [ ] 覆盖了关键步骤的失败场景
- [ ] 没有使用任何 Mock
- [ ] 测试数据有清理策略
- [ ] 可以独立运行，不依赖其他测试
- [ ] 每个流程 2-4 个测试用例（不过度测试）
