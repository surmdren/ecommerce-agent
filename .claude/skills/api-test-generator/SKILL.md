---
name: api-test-generator
description: 生成单个 API 端点的集成测试代码。调用真实接口，禁止使用任何 Mock。每个接口 2-5 个测试用例，覆盖 Happy Path、参数校验、鉴权/权限校验。适用于测试 API 端点的各种场景。
---

# API Test Generator Skill

## 🎯 角色定位

你是一名专注于 API 集成测试的测试工程师，为指定的 API 接口生成高质量、可维护的测试代码。

**核心原则**：
- 调用真实接口，**禁止使用任何 Mock**
- 每个接口 2-5 个测试用例，覆盖关键场景
- 测试必须稳定、可重复、执行快速

---

## 📥 触发条件

当用户请求以下内容时激活此 Skill：
- "为这个接口生成测试"
- "生成 API 测试"
- "测试这个 endpoint"
- 由 `testing-strategy` Skill 指派生成 API 测试

---

## 🔍 输入要求

在生成测试前，确认以下信息（如缺失则主动询问）：

| 必需信息 | 说明 | 示例 |
|----------|------|------|
| 接口定义 | 路由、方法、参数、响应 | `POST /api/orders` |
| 技术栈 | 语言和框架 | Python + FastAPI |
| 环境配置 | 测试环境地址或本地启动方式 | `http://localhost:8000` |
| 鉴权方式 | 如何获取测试用 Token | Bearer Token / API Key |

---

## 📋 每个接口必须覆盖的场景

生成测试时，**必须** 为每个接口覆盖以下场景：

### 1. 正常路径（Happy Path）
- 使用有效参数
- 验证正确的响应状态码
- 验证响应数据结构和关键字段

### 2. 参数校验错误
- 缺失必填参数
- 参数类型错误
- 参数边界值（过长、过短、超出范围）

### 3. 鉴权/权限校验
- 未携带 Token（401）
- Token 无效或过期（401）
- 无权限访问（403）

### 4. 业务边界条件（按需）
- 资源不存在（404）
- 幂等性验证（重复请求）
- 并发/竞态条件

---

## 🛠 各技术栈代码模板

### Python (pytest + httpx)

```python
"""
API Tests for {endpoint}
保护目标：{description}
"""
import pytest
import httpx
from typing import Generator

# ============ Fixtures ============

@pytest.fixture(scope="module")
def base_url() -> str:
    """测试环境 base URL"""
    return "http://localhost:8000"

@pytest.fixture(scope="module")
def auth_headers() -> dict:
    """获取认证 Token"""
    # TODO: 实现真实的登录流程获取 Token
    return {"Authorization": "Bearer test_token"}

@pytest.fixture(scope="module")
def client() -> Generator[httpx.Client, None, None]:
    """HTTP 客户端"""
    with httpx.Client(timeout=30.0) as client:
        yield client

# ============ Test Data ============

VALID_PAYLOAD = {
    # TODO: 填充有效的请求数据
}

INVALID_PAYLOADS = [
    ({}, "缺失必填字段"),
    ({"field": None}, "字段为 null"),
    ({"field": ""}, "字段为空字符串"),
]

# ============ Tests: Happy Path ============

def test_{endpoint_name}_success(client: httpx.Client, base_url: str, auth_headers: dict):
    """正常路径：有效参数应返回成功"""
    response = client.post(
        f"{base_url}/api/{endpoint}",
        json=VALID_PAYLOAD,
        headers=auth_headers,
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["field"] == VALID_PAYLOAD["field"]

# ============ Tests: Validation ============

@pytest.mark.parametrize("payload,description", INVALID_PAYLOADS)
def test_{endpoint_name}_validation_error(
    client: httpx.Client, 
    base_url: str, 
    auth_headers: dict,
    payload: dict,
    description: str,
):
    """参数校验：无效参数应返回 400/422"""
    response = client.post(
        f"{base_url}/api/{endpoint}",
        json=payload,
        headers=auth_headers,
    )
    
    assert response.status_code in (400, 422), f"场景：{description}"

# ============ Tests: Auth ============

def test_{endpoint_name}_unauthorized(client: httpx.Client, base_url: str):
    """鉴权：未携带 Token 应返回 401"""
    response = client.post(
        f"{base_url}/api/{endpoint}",
        json=VALID_PAYLOAD,
    )
    
    assert response.status_code == 401

def test_{endpoint_name}_forbidden(client: httpx.Client, base_url: str):
    """权限：无权限用户应返回 403"""
    no_permission_headers = {"Authorization": "Bearer limited_user_token"}
    
    response = client.post(
        f"{base_url}/api/{endpoint}",
        json=VALID_PAYLOAD,
        headers=no_permission_headers,
    )
    
    assert response.status_code == 403
```

### Node.js (Vitest + supertest)

```typescript
/**
 * API Tests for {endpoint}
 * 保护目标：{description}
 */
import { describe, it, expect, beforeAll } from 'vitest';
import request from 'supertest';

const BASE_URL = process.env.TEST_API_URL || 'http://localhost:3000';

// ============ Test Data ============

const VALID_PAYLOAD = {
  // TODO: 填充有效的请求数据
};

const INVALID_PAYLOADS = [
  { payload: {}, description: '缺失必填字段' },
  { payload: { field: null }, description: '字段为 null' },
  { payload: { field: '' }, description: '字段为空字符串' },
];

// ============ Auth Helper ============

let authToken: string;

beforeAll(async () => {
  // TODO: 实现真实的登录流程获取 Token
  authToken = 'test_token';
});

// ============ Tests ============

describe('{endpoint}', () => {
  describe('Happy Path', () => {
    it('有效参数应返回成功', async () => {
      const response = await request(BASE_URL)
        .post('/api/{endpoint}')
        .set('Authorization', `Bearer ${authToken}`)
        .send(VALID_PAYLOAD);

      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('id');
      expect(response.body.field).toBe(VALID_PAYLOAD.field);
    });
  });

  describe('Validation', () => {
    it.each(INVALID_PAYLOADS)(
      '无效参数应返回 400/422：$description',
      async ({ payload }) => {
        const response = await request(BASE_URL)
          .post('/api/{endpoint}')
          .set('Authorization', `Bearer ${authToken}`)
          .send(payload);

        expect([400, 422]).toContain(response.status);
      }
    );
  });

  describe('Auth', () => {
    it('未携带 Token 应返回 401', async () => {
      const response = await request(BASE_URL)
        .post('/api/{endpoint}')
        .send(VALID_PAYLOAD);

      expect(response.status).toBe(401);
    });

    it('无权限用户应返回 403', async () => {
      const response = await request(BASE_URL)
        .post('/api/{endpoint}')
        .set('Authorization', 'Bearer limited_user_token')
        .send(VALID_PAYLOAD);

      expect(response.status).toBe(403);
    });
  });
});
```

### Go (testing + testify)

```go
// {endpoint}_test.go
// API Tests for {endpoint}
// 保护目标：{description}

package api_test

import (
	"bytes"
	"encoding/json"
	"net/http"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

var baseURL = getEnv("TEST_API_URL", "http://localhost:8080")
var authToken string

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}

func TestMain(m *testing.M) {
	// TODO: 实现真实的登录流程获取 Token
	authToken = "test_token"
	os.Exit(m.Run())
}

// ============ Test Data ============

type Payload struct {
	Field string `json:"field"`
}

var validPayload = Payload{
	Field: "valid_value",
}

// ============ Tests: Happy Path ============

func Test{Endpoint}_Success(t *testing.T) {
	body, _ := json.Marshal(validPayload)
	req, _ := http.NewRequest("POST", baseURL+"/api/{endpoint}", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+authToken)

	client := &http.Client{}
	resp, err := client.Do(req)
	require.NoError(t, err)
	defer resp.Body.Close()

	assert.Equal(t, http.StatusCreated, resp.StatusCode)
}

// ============ Tests: Validation ============

func Test{Endpoint}_ValidationError(t *testing.T) {
	testCases := []struct {
		name    string
		payload interface{}
	}{
		{"缺失必填字段", map[string]interface{}{}},
		{"字段为空", Payload{Field: ""}},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			body, _ := json.Marshal(tc.payload)
			req, _ := http.NewRequest("POST", baseURL+"/api/{endpoint}", bytes.NewBuffer(body))
			req.Header.Set("Content-Type", "application/json")
			req.Header.Set("Authorization", "Bearer "+authToken)

			client := &http.Client{}
			resp, err := client.Do(req)
			require.NoError(t, err)
			defer resp.Body.Close()

			assert.Contains(t, []int{400, 422}, resp.StatusCode)
		})
	}
}

// ============ Tests: Auth ============

func Test{Endpoint}_Unauthorized(t *testing.T) {
	body, _ := json.Marshal(validPayload)
	req, _ := http.NewRequest("POST", baseURL+"/api/{endpoint}", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	// 不设置 Authorization header

	client := &http.Client{}
	resp, err := client.Do(req)
	require.NoError(t, err)
	defer resp.Body.Close()

	assert.Equal(t, http.StatusUnauthorized, resp.StatusCode)
}
```

### Java (JUnit 5 + REST Assured)

```java
/**
 * API Tests for {endpoint}
 * 保护目标：{description}
 */
package com.example.api;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.Map;
import java.util.stream.Stream;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

class {Endpoint}ApiTest {

    private static String authToken;

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = System.getenv().getOrDefault("TEST_API_URL", "http://localhost:8080");
        // TODO: 实现真实的登录流程获取 Token
        authToken = "test_token";
    }

    // ============ Test Data ============

    private static final Map<String, Object> VALID_PAYLOAD = Map.of(
        "field", "valid_value"
    );

    static Stream<Arguments> invalidPayloads() {
        return Stream.of(
            Arguments.of(Map.of(), "缺失必填字段"),
            Arguments.of(Map.of("field", ""), "字段为空字符串")
        );
    }

    // ============ Tests: Happy Path ============

    @Test
    @DisplayName("正常路径：有效参数应返回成功")
    void testSuccess() {
        given()
            .contentType(ContentType.JSON)
            .header("Authorization", "Bearer " + authToken)
            .body(VALID_PAYLOAD)
        .when()
            .post("/api/{endpoint}")
        .then()
            .statusCode(201)
            .body("id", notNullValue())
            .body("field", equalTo(VALID_PAYLOAD.get("field")));
    }

    // ============ Tests: Validation ============

    @ParameterizedTest(name = "参数校验：{1}")
    @MethodSource("invalidPayloads")
    void testValidationError(Map<String, Object> payload, String description) {
        given()
            .contentType(ContentType.JSON)
            .header("Authorization", "Bearer " + authToken)
            .body(payload)
        .when()
            .post("/api/{endpoint}")
        .then()
            .statusCode(anyOf(is(400), is(422)));
    }

    // ============ Tests: Auth ============

    @Test
    @DisplayName("鉴权：未携带 Token 应返回 401")
    void testUnauthorized() {
        given()
            .contentType(ContentType.JSON)
            .body(VALID_PAYLOAD)
        .when()
            .post("/api/{endpoint}")
        .then()
            .statusCode(401);
    }

    @Test
    @DisplayName("权限：无权限用户应返回 403")
    void testForbidden() {
        given()
            .contentType(ContentType.JSON)
            .header("Authorization", "Bearer limited_user_token")
            .body(VALID_PAYLOAD)
        .when()
            .post("/api/{endpoint}")
        .then()
            .statusCode(403);
    }
}
```

---

## 🗃 测试数据策略

### 数据准备原则

1. **隔离性**：每个测试用例负责自己的数据准备和清理
2. **唯一性**：使用 UUID 或时间戳生成唯一标识符，避免冲突
3. **独立性**：测试之间不能有数据依赖或执行顺序依赖

### 数据清理策略

```python
# Python 示例：使用 fixture 自动清理
@pytest.fixture
def created_order(client, base_url, auth_headers):
    """创建测试订单，测试后自动清理"""
    response = client.post(f"{base_url}/api/orders", json=VALID_PAYLOAD, headers=auth_headers)
    order_id = response.json()["id"]
    
    yield order_id
    
    # Teardown: 删除创建的订单
    client.delete(f"{base_url}/api/orders/{order_id}", headers=auth_headers)
```

```typescript
// TypeScript 示例：使用 afterEach 清理
let createdOrderId: string;

afterEach(async () => {
  if (createdOrderId) {
    await request(BASE_URL)
      .delete(`/api/orders/${createdOrderId}`)
      .set('Authorization', `Bearer ${authToken}`);
    createdOrderId = undefined;
  }
});
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

根据当前工作目录判断项目类型：

| 检测条件 | 项目类型 | 目录前缀 |
|----------|----------|----------|
| 路径包含 `backend/` 或 `api/` 或 `services/` | backend | `tests/backend/api` |
| 路径包含 `frontend/` 或 `web/` 或 `ui/` 或 `client/` | frontend | `tests/frontend/api` |
| 根目录下直接有 `src/` | 默认 | `tests/api` |

### 目录创建步骤

生成测试前，**必须先创建目录结构**：

```bash
# 1. 检测项目根目录（向上查找 package.json 等）
PROJECT_ROOT=$(find_project_root)

# 2. 检测项目类型（backend/frontend）
PROJECT_TYPE=$(detect_project_type)

# 3. 创建测试目录
mkdir -p "$PROJECT_ROOT/tests/$PROJECT_TYPE/api"

# 4. 创建测试报告目录
mkdir -p "$PROJECT_ROOT/test_reports/$PROJECT_TYPE/api_test_reports"
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
│   │   └── api/               # 后端 API 测试
│   │       └── test_orders_api.py
│   └── frontend/
│       └── api/               # 前端 API 调用测试
│           └── test_cart_api.test.ts
└── test_reports/               # 测试报告（按类型分类）
    ├── backend/
    │   └── api_test_reports/
    │       └── orders_api_test_report.md
    └── frontend/
        └── api_test_reports/
            └── cart_api_test_report.md
```

**关键规则**：
- 测试代码路径：`{项目根目录}/tests/{backend|frontend}/api/test_{resource}_api.py`
- 测试报告路径：`{项目根目录}/test_reports/{backend|frontend}/api_test_reports/{resource}_api_test_report.md`

---

## 📁 输出格式

生成测试后，必须输出：

### 1. 测试文件

根据项目类型按以下命名规范保存：

| 项目类型 | Python | Node.js | Go | Java |
|----------|--------|---------|-----|------|
| backend | `tests/backend/api/test_{resource}_api.py` | `tests/backend/api/{resource}.api.test.ts` | `tests/backend/api/{resource}_api_test.go` | `src/test/java/.../api/{Resource}ApiTest.java` |
| frontend | `tests/frontend/api/test_{resource}_api.py` | `tests/frontend/api/{resource}.api.test.ts` | - | - |
| 默认 | `tests/api/test_{resource}_api.py` | `tests/api/{resource}.api.test.ts` | `tests/api/{resource}_api_test.go` | `src/test/java/.../api/{Resource}ApiTest.java` |

### 2. 测试报告

根据项目类型生成测试报告：

```
test_reports/
├── backend/
│   └── api_test_reports/
│       └── {resource}_api_test_report.md
└── frontend/
    └── api_test_reports/
        └── {resource}_api_test_report.md
```

**报告命名规范**：`{resource}_api_test_report.md`

**测试报告模板**：

```markdown
# {资源名称} API 测试报告

## 概述

| 项目 | 内容 |
|------|------|
| API 端点 | {GET/POST/PUT/DELETE} /api/{resource} |
| 测试目标 | {保护目标说明} |
| 生成时间 | {YYYY-MM-DD HH:mm} |
| 测试框架 | {pytest/supertest/go test/rest assured} |

## 测试覆盖

### 测试文件
- `{test_file_path}`

### 测试用例统计

| 测试函数 | 场景 | 预期结果 |
|----------|------|----------|
| test_{resource}_success | 正常路径 | 201, 返回资源 ID |
| test_{resource}_validation_error | 参数校验 | 400/422 |
| test_{resource}_unauthorized | 未携带 Token | 401 |
| test_{resource}_forbidden | 无权限 | 403 |

## 运行方式

```bash
{运行命令}
```

## 成功标准

- [x] 覆盖 Happy Path
- [x] 覆盖参数校验错误
- [x] 覆盖鉴权/权限校验
- [x] 没有使用任何 Mock
```

### 3. 运行命令

```bash
# Python
pytest tests/api/test_orders_api.py -v

# Node.js
pnpm test tests/api/orders.api.test.ts

# Go
go test ./tests/api/... -v

# Java
mvn test -Dtest=OrdersApiTest
```

---

## 🚫 严格禁止

- ❌ 使用任何 Mock（数据库、HTTP、服务）
- ❌ 绕过鉴权进行测试
- ❌ 为同一接口生成超过 6 个测试用例
- ❌ 测试之间存在数据依赖
- ❌ 使用 sleep / 固定时间等待
- ❌ 硬编码敏感信息（Token、密码）

---

## ✅ 成功标准

生成测试后，自检以下各项：

- [ ] 覆盖了 Happy Path
- [ ] 覆盖了参数校验错误
- [ ] 覆盖了鉴权/权限校验
- [ ] 没有使用任何 Mock
- [ ] 测试数据有清理策略
- [ ] 可以独立运行，不依赖其他测试