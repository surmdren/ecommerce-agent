---
name: api-docs
description: 根据后端代码和API设计自动生成API文档。支持Swagger/OpenAPI 3.0格式，生成交互式文档、SDK客户端代码、Postman Collection。适用于API文档生成、接口对接、前后端协作。当用户提到"API文档"、"接口文档"、"Swagger"、"OpenAPI"、"api docs"时触发。
---

# API 文档生成器

## Overview

根据后端代码和 API 设计规范自动生成专业的 API 文档，包含：

```
1. 解析后端代码（Controller/Router）
2. 提取 API 端点信息
3. 生成 OpenAPI/Swagger 规范
4. 生成交互式文档页面
5. 生成 SDK 客户端代码（可选）
6. 生成 Postman Collection（可选）
```

## 支持的框架

| 后端框架 | 支持情况 |
|---------|---------|
| Fastify (Node.js) | ✅ 原生支持 |
| Express (Node.js) | ✅ 通过注解 |
| NestJS (Node.js) | ✅ 原生支持 |
| Spring Boot (Java) | ✅ SpringDoc |
| Gin (Go) | ✅ Swaggo |
| FastAPI (Python) | ✅ 原生支持 |

## Parameters

| 参数 | 必填 | 描述 |
|------|------|------|
| `格式` | ❌ | 输出格式：swagger/openapi/html(默认) |
| `输出` | ❌ | 输出目录，默认 `api-docs/` |

## Instructions

你是一名【技术文档工程师 + API 专家】，拥有 8 年 API 设计和文档化经验。

### 工作流程

#### Step 1: 分析 API 设计

**1.1 读取 API 设计文档**
```bash
# 读取 API 设计规范
read TechSolution/backend/api-design.md

# 读取后端代码结构
read backend/src/modules/
```

**1.2 扫描后端代码**

扫描以下文件：
- Controller 文件（`*.controller.ts`, `*.routes.ts`）
- DTO 定义（`*.dto.ts`, `*.schema.ts`）
- API 装饰器/注解

**1.3 提取 API 信息**

提取以下信息：
| 信息 | 说明 |
|------|------|
| 端点路径 | `/api/users`, `/api/sessions/:id` |
| HTTP 方法 | GET, POST, PUT, DELETE, PATCH |
| 请求参数 | Query, Path, Body, Header |
| 响应格式 | 200, 400, 401, 403, 404, 500 |
| 数据模型 | Request/Response DTO |
| 认证方式 | Bearer Token, API Key |
| 描述说明 | API 功能描述 |

#### Step 2: 生成 OpenAPI 规范

**2.1 OpenAPI 3.0 规范结构**

```yaml
openapi: 3.0.0
info:
  title: 智能客服系统 API
  version: 1.0.0
  description: |
    智能客服系统的 RESTful API 文档

    ## 认证方式
    所有 API 需要使用 Bearer Token 认证

  contact:
    name: API Support
    email: support@example.com

servers:
  - url: https://api.example.com/v1
    description: 生产环境
  - url: https://staging-api.example.com/v1
    description: 预发布环境
  - url: http://localhost:3000/v1
    description: 开发环境

security:
  - BearerAuth: []

tags:
  - name: Auth
    description: 认证授权
  - name: Sessions
    description: 会话管理
  - name: Messages
    description: 消息处理
  - name: Agents
    description: 客服管理

paths:
  /auth/login:
    post:
      tags: [Auth]
      summary: 用户登录
      description: 使用邮箱和密码登录系统
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
            example:
              email: "user@example.com"
              password: "password123"
      responses:
        '200':
          description: 登录成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoginResponse'
        '400':
          description: 请求参数错误
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '401':
          description: 认证失败
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

  /sessions:
    post:
      tags: [Sessions]
      summary: 创建会话
      description: 创建新的客服会话
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateSessionRequest'
      responses:
        '201':
          description: 会话创建成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SessionResponse'
        '401':
          description: 未认证
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

    get:
      tags: [Sessions]
      summary: 获取会话列表
      description: 获取当前用户的会话列表
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/SessionResponse'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

  /sessions/{sessionId}:
    get:
      tags: [Sessions]
      summary: 获取会话详情
      parameters:
        - name: sessionId
          in: path
          required: true
          schema:
            type: string
          description: 会话 ID
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SessionDetailResponse'
        '404':
          description: 会话不存在
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    LoginRequest:
      type: object
      required:
        - email
        - password
      properties:
        email:
          type: string
          format: email
          description: 用户邮箱
        password:
          type: string
          format: password
          minLength: 8
          description: 用户密码

    LoginResponse:
      type: object
      properties:
        accessToken:
          type: string
          description: JWT 访问令牌
        refreshToken:
          type: string
          description: 刷新令牌
        user:
          $ref: '#/components/schemas/User'

    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string

    ErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 错误代码
        message:
          type: string
          description: 错误信息
        details:
          type: object
          description: 错误详情

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer
```

**2.2 数据模型定义**

基于 Prisma Schema 和 DTO 定义：

```typescript
// Prisma Schema → OpenAPI Schema
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

// 转换为 OpenAPI
User:
  type: object
  properties:
    id:
      type: string
      format: uuid
      description: 用户 ID
    email:
      type: string
      format: email
      description: 用户邮箱
    name:
      type: string
      nullable: true
      description: 用户名称
    role:
      type: string
      enum: [USER, AGENT, ADMIN]
      description: 用户角色
    createdAt:
      type: string
      format: date-time
    updatedAt:
      type: string
      format: date-time
  required: [id, email, role, createdAt, updatedAt]
```

#### Step 3: 生成交互式文档

**3.1 使用 Swagger UI**

创建 `api-docs/index.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>API 文档 - 智能客服系统</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
  <style>
    body { margin: 0; padding: 0; }
    .swagger-ui .topbar { background-color: #1c2833; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: './openapi.yaml',
      dom_id: '#swagger-ui',
      deepLinking: true,
      presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
      ],
      layout: "BaseLayout",
      defaultModelsExpandDepth: 1,
      defaultModelExpandDepth: 1,
      docExpansion: "list",
      filter: true,
      tryItOutEnabled: true,
      persistAuthorization: true,
      syntaxHighlight: {
        activate: true,
        theme: "monokai"
      }
    });
  </script>
</body>
</html>
```

**3.2 使用 Redoc**

创建 `api-docs/redoc.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>API 文档 - 智能客服系统</title>
  <link href="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.css" rel="stylesheet">
</head>
<body>
  <redoc spec-url='./openapi.yaml'></redoc>
  <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
  <style>
    body { margin: 0; padding: 0; }
  </style>
</body>
</html>
```

#### Step 4: 生成 Postman Collection

```json
{
  "info": {
    "name": "智能客服系统 API",
    "description": "智能客服系统的 RESTful API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "baseUrl",
      "value": "http://localhost:3000/v1",
      "type": "string"
    },
    {
      "key": "token",
      "value": "",
      "type": "string"
    }
  ],
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{token}}",
        "type": "string"
      }
    ]
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"user@example.com\",\n  \"password\": \"password123\"\n}"
            },
            "url": {
              "raw": "{{baseUrl}}/auth/login",
              "host": ["{{baseUrl}}"],
              "path": ["auth", "login"]
            }
          },
          "response": []
        }
      ]
    },
    {
      "name": "Sessions",
      "item": [
        {
          "name": "Create Session",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"userId\": \"user-123\"\n}"
            },
            "url": {
              "raw": "{{baseUrl}}/sessions",
              "host": ["{{baseUrl}}"],
              "path": ["sessions"]
            }
          }
        },
        {
          "name": "Get Sessions",
          "request": {
            "method": "GET",
            "url": {
              "raw": "{{baseUrl}}/sessions?page=1&limit=20",
              "host": ["{{baseUrl}}"],
              "path": ["sessions"],
              "query": [
                {
                  "key": "page",
                  "value": "1"
                },
                {
                  "key": "limit",
                  "value": "20"
                }
              ]
            }
          }
        }
      ]
    }
  ]
}
```

#### Step 5: 生成 SDK 客户端代码（可选）

**5.1 TypeScript SDK**

```typescript
// api-docs/sdk/typescript/src/client.ts
export class ApiClient {
  private baseUrl: string;
  private token?: string;

  constructor(baseUrl: string, token?: string) {
    this.baseUrl = baseUrl;
    this.token = token;
  }

  setToken(token: string) {
    this.token = token;
  }

  private async request<T>(
    method: string,
    path: string,
    body?: any,
    params?: Record<string, string>
  ): Promise<T> {
    const url = new URL(path, this.baseUrl);
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        url.searchParams.set(key, value);
      });
    }

    const response = await fetch(url.toString(), {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { Authorization: `Bearer ${this.token}` }),
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      throw new ApiError(response.status, await response.json());
    }

    return response.json();
  }

  // Auth APIs
  async login(data: LoginRequest): Promise<LoginResponse> {
    return this.request<LoginResponse>('POST', '/auth/login', data);
  }

  // Session APIs
  async createSession(data: CreateSessionRequest): Promise<SessionResponse> {
    return this.request<SessionResponse>('POST', '/sessions', data);
  }

  async getSessions(params: GetSessionsParams): Promise<SessionsListResponse> {
    return this.request<SessionsListResponse>('GET', '/sessions', undefined, params);
  }

  async getSession(sessionId: string): Promise<SessionDetailResponse> {
    return this.request<SessionDetailResponse>('GET', `/sessions/${sessionId}`);
  }
}

export class ApiError extends Error {
  constructor(
    public status: number,
    public data: ErrorResponse
  ) {
    super(data.message);
  }
}
```

**5.2 Python SDK**

```python
# api-docs/sdk/python/api_client.py
from typing import Optional, Dict, Any
import requests
from dataclasses import dataclass

@dataclass
class LoginRequest:
    email: str
    password: str

class ApiClient:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()

    def set_token(self, token: str):
        self.token = token

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = {
            "Content-Type": "application/json",
            **({"Authorization": f"Bearer {self.token}"} if self.token else {})
        }

        response = self.session.request(
            method,
            url,
            json=data,
            params=params,
            headers=headers
        )
        response.raise_for_status()
        return response.json()

    def login(self, email: str, password: str) -> Dict[str, Any]:
        return self._request("POST", "/auth/login", {
            "email": email,
            "password": password
        })

    def create_session(self, user_id: str) -> Dict[str, Any]:
        return self._request("POST", "/sessions", {"userId": user_id})
```

#### Step 6: 生成文档概览

创建 `api-docs/README.md`:

```markdown
# API 文档

## 目录

- [概览](#概览)
- [认证方式](#认证方式)
- [快速开始](#快速开始)
- [API端点](#api端点)
- [错误处理](#错误处理)
- [SDK使用](#sdk使用)
- [在线文档](#在线文档)
- [Postman Collection](#postman-collection)
- [变更日志](#变更日志)

---

## 概览

本文档描述了智能客服系统的 RESTful API。

**Base URL**: `https://api.example.com/v1`

## 认证方式

所有 API 请求需要使用 Bearer Token 认证：

```
Authorization: Bearer <your-jwt-token>
```

## 快速开始

### 1. 获取 Token

```bash
curl -X POST https://api.example.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

响应：
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "name": "张三"
  }
}
```

### 2. 使用 Token

```bash
curl -X GET https://api.example.com/v1/sessions \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

## API 端点

| 模块 | 端点 | 方法 | 描述 |
|------|------|------|------|
| Auth | `/auth/login` | POST | 用户登录 |
| Auth | `/auth/refresh` | POST | 刷新 Token |
| Sessions | `/sessions` | GET | 获取会话列表 |
| Sessions | `/sessions` | POST | 创建会话 |
| Sessions | `/sessions/:id` | GET | 获取会话详情 |
| Messages | `/sessions/:id/messages` | GET | 获取消息列表 |
| Messages | `/sessions/:id/messages` | POST | 发送消息 |

## 错误处理

所有错误响应遵循统一格式：

```json
{
  "code": "ERROR_CODE",
  "message": "错误描述",
  "details": {}
}
```

常见 HTTP 状态码：
- `200` - 成功
- `201` - 创建成功
- `400` - 请求参数错误
- `401` - 未认证
- `403` - 权限不足
- `404` - 资源不存在
- `500` - 服务器错误

## SDK 使用

### TypeScript

```typescript
import { ApiClient } from '@myapp/api-client';

const client = new ApiClient('https://api.example.com/v1');

// 登录
const { accessToken } = await client.login({
  email: 'user@example.com',
  password: 'password123'
});

client.setToken(accessToken);

// 创建会话
const session = await client.createSession({ userId: 'user-123' });
```

### Python

```python
from api_client import ApiClient

client = ApiClient('https://api.example.com/v1')

# 登录
result = client.login('user@example.com', 'password123')
client.set_token(result['accessToken'])

# 创建会话
session = client.create_session('user-123')
```

## 在线文档

- [Swagger UI](./index.html) - 交互式 API 文档
- [ReDoc](./redoc.html) - 美观的只读文档

## Postman Collection

下载 [postman_collection.json](./postman_collection.json) 导入到 Postman。

## 变更日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2024-01-15 | 初始版本 |
```

## Output

### 目录结构

```
api-docs/
├── README.md                    # 文档概览
├── openapi.yaml                 # OpenAPI 规范
├── openapi.json                 # OpenAPI JSON 格式
├── index.html                   # Swagger UI
├── redoc.html                   # ReDoc
├── postman_collection.json      # Postman Collection
└── sdk/
    ├── typescript/              # TypeScript SDK
    │   ├── src/
    │   ├── package.json
    │   └── README.md
    └── python/                  # Python SDK
        ├── api_client.py
        ├── setup.py
        └── README.md
```

## 代码注解规范

### Fastify Schema

```typescript
app.post('/sessions', {
  schema: {
    tags: ['Sessions'],
    summary: '创建会话',
    description: '创建新的客服会话',
    security: [{ bearerAuth: [] }],
    body: {
      type: 'object',
      required: ['userId'],
      properties: {
        userId: { type: 'string', format: 'uuid' }
      }
    },
    response: {
      201: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          userId: { type: 'string' },
          status: { type: 'string' },
          createdAt: { type: 'string', format: 'date-time' }
        }
      }
    }
  }
}, async (request, reply) => {
  // 处理逻辑
});
```

### NestJS DTO

```typescript
import { ApiProperty, ApiTags } from '@nestjs/swagger';

@ApiTags('Sessions')
export class CreateSessionDto {
  @ApiProperty({
    description: '用户 ID',
    format: 'uuid'
  })
  @IsUUID()
  userId: string;
}

export class SessionResponse {
  @ApiProperty({ description: '会话 ID' })
  id: string;

  @ApiProperty({ description: '用户 ID' })
  userId: string;

  @ApiProperty({ description: '会话状态', enum: SessionStatus })
  status: SessionStatus;
}
```

## Examples

### 示例 1: 生成完整文档
```bash
# 用户请求
请生成 API 文档

# Claude 执行流程
1. 扫描后端代码
2. 提取 API 端点
3. 生成 OpenAPI 规范
4. 生成交互式文档
5. 生成 Postman Collection
6. 生成 SDK
```

### 示例 2: 更新文档
```bash
# 用户请求
API 有更新，请刷新文档

# Claude 执行流程
1. 检测代码变更
2. 更新 OpenAPI 规范
3. 重新生成文档
```

## 最佳实践

1. **版本管理**: 使用语义化版本号
2. **变更日志**: 记录所有 API 变更
3. **示例代码**: 每个端点提供示例
4. **错误文档**: 详细说明所有错误类型
5. **更新及时**: 代码变更后及时更新文档

## 适用场景

- API 文档生成
- 前后端协作
- 第三方接入
- API 测试
- SDK 生成
