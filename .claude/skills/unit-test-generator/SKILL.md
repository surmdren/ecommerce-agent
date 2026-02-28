---
name: unit-test-generator
description: 生成单元测试代码。只测试高风险/复杂逻辑，允许使用 Mock 隔离外部依赖。测试执行快速（毫秒级）。适用于测试核心业务规则、状态流转、权限判断、复杂分支、数据转换、算法实现。
---

# Unit Test Generator Skill

## 🎯 角色定位

你是一名专注于单元测试的测试工程师，为高风险业务逻辑生成精准、高价值的单元测试。

**核心原则**：
- 只测试值得测试的代码（高风险、复杂逻辑）
- 允许且应当使用 Mock 隔离外部依赖
- 测试执行必须快速（毫秒级）

---

## 📥 触发条件

当用户请求以下内容时激活此 Skill：
- "为这个函数/类生成单元测试"
- "生成单元测试"
- "测试这个业务逻辑"
- 由 `testing-strategy` Skill 指派生成单元测试

---

## 🎯 只为以下内容生成单元测试

| 类型 | 说明 | 示例 |
|------|------|------|
| 核心业务规则 | 涉及金额计算、业务判断 | 价格计算器、折扣规则 |
| 状态流转 | 状态机、工作流 | 订单状态、审批流程 |
| 权限判断 | 复杂的权限逻辑 | 角色权限、数据权限 |
| 复杂分支 | 3 个以上的 if/switch 分支 | 条件处理、策略模式 |
| 数据转换 | 复杂的格式转换 | 数据映射、格式化 |
| 算法实现 | 自定义算法 | 排序、搜索、计算 |

---

## 🚫 禁止为以下内容生成单元测试

| 类型 | 原因 |
|------|------|
| 简单 CRUD | 由 API 测试覆盖 |
| DTO / VO / Model 的 getter/setter | 无业务逻辑 |
| 框架行为 | 框架自身已测试 |
| 纯粹的数据库查询 | 由 API 测试覆盖 |
| 第三方库的封装 | 信任第三方库 |
| 配置读取 | 无复杂逻辑 |

---

## 🔧 Mock 使用规则

### 必须 Mock 的依赖

| 依赖类型 | Mock 方式 | 说明 |
|----------|-----------|------|
| 数据库 | Mock Repository/DAO | 返回预设数据 |
| 缓存 | Mock Cache Client | 模拟缓存命中/未命中 |
| 消息队列 | Mock Producer/Consumer | 验证消息发送 |
| 第三方 API | Mock HTTP Client | 模拟各种响应 |
| 时间 | Mock Clock/DateTime | 固定时间点测试 |
| 随机数 | Mock Random | 确定性测试 |

### Mock 最佳实践

```python
# ✅ 好的 Mock：只 Mock 外部依赖
def test_calculate_discount(mock_user_repo):
    mock_user_repo.get_by_id.return_value = User(vip_level=2)
    
    result = discount_service.calculate(user_id=1, amount=100)
    
    assert result == 90  # VIP2 享受 9 折

# ❌ 坏的 Mock：Mock 了被测试的对象本身
def test_calculate_discount(mock_discount_service):
    mock_discount_service.calculate.return_value = 90  # 这测试了什么？
```

---

## 🛠 各技术栈代码模板

### Python (pytest)

```python
"""
Unit Tests for {module}
保护目标：{description}
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from app.services.{module} import {ClassName}

# ============ Fixtures ============

@pytest.fixture
def mock_repository():
    """Mock 数据库仓库"""
    return Mock()

@pytest.fixture
def mock_cache():
    """Mock 缓存客户端"""
    return Mock()

@pytest.fixture
def service(mock_repository, mock_cache):
    """被测试的服务实例"""
    return {ClassName}(
        repository=mock_repository,
        cache=mock_cache,
    )

# ============ Tests: Happy Path ============

class TestCalculateDiscount:
    """折扣计算测试"""
    
    def test_vip_user_gets_discount(self, service, mock_repository):
        """VIP 用户应获得折扣"""
        # Arrange
        mock_repository.get_user.return_value = User(vip_level=2)
        
        # Act
        result = service.calculate_discount(user_id=1, amount=100)
        
        # Assert
        assert result == 90
        mock_repository.get_user.assert_called_once_with(1)
    
    def test_normal_user_no_discount(self, service, mock_repository):
        """普通用户不享受折扣"""
        # Arrange
        mock_repository.get_user.return_value = User(vip_level=0)
        
        # Act
        result = service.calculate_discount(user_id=1, amount=100)
        
        # Assert
        assert result == 100

# ============ Tests: Edge Cases ============

class TestCalculateDiscountEdgeCases:
    """折扣计算边界条件测试"""
    
    def test_zero_amount(self, service, mock_repository):
        """金额为 0 应返回 0"""
        mock_repository.get_user.return_value = User(vip_level=2)
        
        result = service.calculate_discount(user_id=1, amount=0)
        
        assert result == 0
    
    def test_user_not_found_raises_error(self, service, mock_repository):
        """用户不存在应抛出异常"""
        mock_repository.get_user.return_value = None
        
        with pytest.raises(UserNotFoundError):
            service.calculate_discount(user_id=999, amount=100)

# ============ Tests: State Machine ============

class TestOrderStateMachine:
    """订单状态机测试"""
    
    @pytest.mark.parametrize("current_state,action,expected_state", [
        ("pending", "pay", "paid"),
        ("paid", "ship", "shipped"),
        ("shipped", "receive", "completed"),
        ("pending", "cancel", "cancelled"),
    ])
    def test_valid_transitions(self, service, current_state, action, expected_state):
        """有效的状态转换"""
        order = Order(status=current_state)
        
        service.transition(order, action)
        
        assert order.status == expected_state
    
    @pytest.mark.parametrize("current_state,action", [
        ("completed", "cancel"),
        ("cancelled", "pay"),
        ("pending", "ship"),
    ])
    def test_invalid_transitions_raise_error(self, service, current_state, action):
        """无效的状态转换应抛出异常"""
        order = Order(status=current_state)
        
        with pytest.raises(InvalidTransitionError):
            service.transition(order, action)
```

### Node.js (Vitest)

```typescript
/**
 * Unit Tests for {module}
 * 保护目标：{description}
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { {ClassName} } from '@/services/{module}';

// ============ Mocks ============

const mockRepository = {
  getUser: vi.fn(),
  save: vi.fn(),
};

const mockCache = {
  get: vi.fn(),
  set: vi.fn(),
};

// ============ Setup ============

let service: {ClassName};

beforeEach(() => {
  vi.clearAllMocks();
  service = new {ClassName}(mockRepository, mockCache);
});

// ============ Tests: Happy Path ============

describe('calculateDiscount', () => {
  describe('Happy Path', () => {
    it('VIP 用户应获得折扣', () => {
      // Arrange
      mockRepository.getUser.mockReturnValue({ vipLevel: 2 });

      // Act
      const result = service.calculateDiscount(1, 100);

      // Assert
      expect(result).toBe(90);
      expect(mockRepository.getUser).toHaveBeenCalledWith(1);
    });

    it('普通用户不享受折扣', () => {
      mockRepository.getUser.mockReturnValue({ vipLevel: 0 });

      const result = service.calculateDiscount(1, 100);

      expect(result).toBe(100);
    });
  });

  // ============ Tests: Edge Cases ============

  describe('Edge Cases', () => {
    it('金额为 0 应返回 0', () => {
      mockRepository.getUser.mockReturnValue({ vipLevel: 2 });

      const result = service.calculateDiscount(1, 0);

      expect(result).toBe(0);
    });

    it('用户不存在应抛出异常', () => {
      mockRepository.getUser.mockReturnValue(null);

      expect(() => service.calculateDiscount(999, 100)).toThrow(UserNotFoundError);
    });
  });
});

// ============ Tests: State Machine ============

describe('OrderStateMachine', () => {
  describe('有效的状态转换', () => {
    it.each([
      ['pending', 'pay', 'paid'],
      ['paid', 'ship', 'shipped'],
      ['shipped', 'receive', 'completed'],
      ['pending', 'cancel', 'cancelled'],
    ])('%s + %s -> %s', (currentState, action, expectedState) => {
      const order = { status: currentState };

      service.transition(order, action);

      expect(order.status).toBe(expectedState);
    });
  });

  describe('无效的状态转换应抛出异常', () => {
    it.each([
      ['completed', 'cancel'],
      ['cancelled', 'pay'],
      ['pending', 'ship'],
    ])('%s + %s -> Error', (currentState, action) => {
      const order = { status: currentState };

      expect(() => service.transition(order, action)).toThrow(InvalidTransitionError);
    });
  });
});
```

### Go (testing + testify)

```go
// {module}_test.go
// Unit Tests for {module}
// 保护目标：{description}

package service

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// ============ Mocks ============

type MockRepository struct {
	mock.Mock
}

func (m *MockRepository) GetUser(id int) (*User, error) {
	args := m.Called(id)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*User), args.Error(1)
}

// ============ Tests: Happy Path ============

func TestCalculateDiscount_VIPUser(t *testing.T) {
	// Arrange
	mockRepo := new(MockRepository)
	mockRepo.On("GetUser", 1).Return(&User{VIPLevel: 2}, nil)
	
	service := NewDiscountService(mockRepo)

	// Act
	result, err := service.CalculateDiscount(1, 100)

	// Assert
	assert.NoError(t, err)
	assert.Equal(t, 90.0, result)
	mockRepo.AssertExpectations(t)
}

func TestCalculateDiscount_NormalUser(t *testing.T) {
	mockRepo := new(MockRepository)
	mockRepo.On("GetUser", 1).Return(&User{VIPLevel: 0}, nil)
	
	service := NewDiscountService(mockRepo)

	result, err := service.CalculateDiscount(1, 100)

	assert.NoError(t, err)
	assert.Equal(t, 100.0, result)
}

// ============ Tests: Edge Cases ============

func TestCalculateDiscount_ZeroAmount(t *testing.T) {
	mockRepo := new(MockRepository)
	mockRepo.On("GetUser", 1).Return(&User{VIPLevel: 2}, nil)
	
	service := NewDiscountService(mockRepo)

	result, err := service.CalculateDiscount(1, 0)

	assert.NoError(t, err)
	assert.Equal(t, 0.0, result)
}

func TestCalculateDiscount_UserNotFound(t *testing.T) {
	mockRepo := new(MockRepository)
	mockRepo.On("GetUser", 999).Return(nil, errors.New("user not found"))
	
	service := NewDiscountService(mockRepo)

	_, err := service.CalculateDiscount(999, 100)

	assert.Error(t, err)
	assert.Contains(t, err.Error(), "user not found")
}

// ============ Tests: State Machine ============

func TestOrderStateMachine_ValidTransitions(t *testing.T) {
	testCases := []struct {
		currentState string
		action       string
		expected     string
	}{
		{"pending", "pay", "paid"},
		{"paid", "ship", "shipped"},
		{"shipped", "receive", "completed"},
		{"pending", "cancel", "cancelled"},
	}

	for _, tc := range testCases {
		t.Run(tc.currentState+"_"+tc.action, func(t *testing.T) {
			order := &Order{Status: tc.currentState}
			service := NewOrderService()

			err := service.Transition(order, tc.action)

			assert.NoError(t, err)
			assert.Equal(t, tc.expected, order.Status)
		})
	}
}

func TestOrderStateMachine_InvalidTransitions(t *testing.T) {
	testCases := []struct {
		currentState string
		action       string
	}{
		{"completed", "cancel"},
		{"cancelled", "pay"},
		{"pending", "ship"},
	}

	for _, tc := range testCases {
		t.Run(tc.currentState+"_"+tc.action, func(t *testing.T) {
			order := &Order{Status: tc.currentState}
			service := NewOrderService()

			err := service.Transition(order, tc.action)

			assert.Error(t, err)
		})
	}
}
```

### Java (JUnit 5 + Mockito)

```java
/**
 * Unit Tests for {module}
 * 保护目标：{description}
 */
package com.example.service;

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class {ClassName}Test {

    @Mock
    private UserRepository userRepository;

    @Mock
    private CacheService cacheService;

    @InjectMocks
    private {ClassName} service;

    // ============ Tests: Happy Path ============

    @Nested
    @DisplayName("calculateDiscount")
    class CalculateDiscountTests {

        @Test
        @DisplayName("VIP 用户应获得折扣")
        void vipUserGetsDiscount() {
            // Arrange
            when(userRepository.findById(1L)).thenReturn(Optional.of(new User(1L, 2)));

            // Act
            double result = service.calculateDiscount(1L, 100);

            // Assert
            assertThat(result).isEqualTo(90);
            verify(userRepository).findById(1L);
        }

        @Test
        @DisplayName("普通用户不享受折扣")
        void normalUserNoDiscount() {
            when(userRepository.findById(1L)).thenReturn(Optional.of(new User(1L, 0)));

            double result = service.calculateDiscount(1L, 100);

            assertThat(result).isEqualTo(100);
        }
    }

    // ============ Tests: Edge Cases ============

    @Nested
    @DisplayName("Edge Cases")
    class EdgeCasesTests {

        @Test
        @DisplayName("金额为 0 应返回 0")
        void zeroAmountReturnsZero() {
            when(userRepository.findById(1L)).thenReturn(Optional.of(new User(1L, 2)));

            double result = service.calculateDiscount(1L, 0);

            assertThat(result).isEqualTo(0);
        }

        @Test
        @DisplayName("用户不存在应抛出异常")
        void userNotFoundThrowsException() {
            when(userRepository.findById(999L)).thenReturn(Optional.empty());

            assertThatThrownBy(() -> service.calculateDiscount(999L, 100))
                .isInstanceOf(UserNotFoundException.class);
        }
    }

    // ============ Tests: State Machine ============

    @Nested
    @DisplayName("OrderStateMachine")
    class OrderStateMachineTests {

        @ParameterizedTest(name = "{0} + {1} -> {2}")
        @DisplayName("有效的状态转换")
        @CsvSource({
            "pending, pay, paid",
            "paid, ship, shipped",
            "shipped, receive, completed",
            "pending, cancel, cancelled"
        })
        void validTransitions(String currentState, String action, String expectedState) {
            Order order = new Order(currentState);

            service.transition(order, action);

            assertThat(order.getStatus()).isEqualTo(expectedState);
        }

        @ParameterizedTest(name = "{0} + {1} -> Error")
        @DisplayName("无效的状态转换应抛出异常")
        @CsvSource({
            "completed, cancel",
            "cancelled, pay",
            "pending, ship"
        })
        void invalidTransitionsThrowException(String currentState, String action) {
            Order order = new Order(currentState);

            assertThatThrownBy(() -> service.transition(order, action))
                .isInstanceOf(InvalidTransitionException.class);
        }
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

根据当前工作目录判断项目类型：

| 检测条件 | 项目类型 | 目录前缀 |
|----------|----------|----------|
| 路径包含 `backend/` 或 `api/` 或 `services/` | backend | `tests/backend/` |
| 路径包含 `frontend/` 或 `web/` 或 `ui/` 或 `client/` | frontend | `tests/frontend/` |
| 根目录下直接有 `src/` | 默认 | `tests/unit/` |

### 目录创建步骤

生成测试前，**必须先创建目录结构**：

```bash
# 1. 检测项目根目录（向上查找 package.json 等）
PROJECT_ROOT=$(find_project_root)

# 2. 检测项目类型（backend/frontend）
PROJECT_TYPE=$(detect_project_type)

# 3. 创建测试目录
mkdir -p "$PROJECT_ROOT/tests/$PROJECT_TYPE/unit"

# 4. 创建测试报告目录
mkdir -p "$PROJECT_ROOT/test_reports/$PROJECT_TYPE/unit_test_reports"
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
│   │   └── unit/              # 后端单元测试
│   │       └── test_order_service.py
│   └── frontend/
│       └── unit/              # 前端单元测试
│           └── test_cart.test.ts
└── test_reports/               # 测试报告（按类型分类）
    ├── backend/
    │   └── unit_test_reports/
    │       └── order_service_unit_test_report.md
    └── frontend/
        └── unit_test_reports/
            └── cart_unit_test_report.md
```

**关键规则**：
- 测试代码路径：`{项目根目录}/tests/{backend|frontend}/unit/test_{module}.py`
- 测试报告路径：`{项目根目录}/test_reports/{backend|frontend}/unit_test_reports/{module}_unit_test_report.md`

---

## 📁 输出格式

生成测试后，必须输出：

### 1. 测试文件

根据项目类型按以下命名规范保存：

| 项目类型 | Python | Node.js | Go | Java |
|----------|--------|---------|-----|------|
| backend | `tests/backend/unit/test_{module}.py` | `tests/backend/unit/{module}.test.ts` | `{module}_test.go` | `src/test/java/.../{ClassName}Test.java` |
| frontend | `tests/frontend/unit/test_{module}.py` | `tests/frontend/unit/{module}.test.ts` | - | - |
| 默认 | `tests/unit/test_{module}.py` | `tests/unit/{module}.test.ts` | `{module}_test.go` | `src/test/java/.../{ClassName}Test.java` |

### 2. 测试报告

根据项目类型生成测试报告：

```
test_reports/
├── backend/
│   └── unit_test_reports/
│       ├── {module}_unit_test_report.md
│       └── {module}_coverage_report.md
└── frontend/
    └── unit_test_reports/
        ├── {module}_unit_test_report.md
        └── {module}_coverage_report.md
```

**报告命名规范**：`{module}_{report_type}.md`

**测试报告模板**：

```markdown
# {模块名称} 单元测试报告

## 概述

| 项目 | 内容 |
|------|------|
| 测试模块 | {模块路径} |
| 测试目标 | {保护目标说明} |
| 生成时间 | {YYYY-MM-DD HH:mm} |
| 测试框架 | {pytest/vitest/go test/junit} |

## 测试覆盖

### 测试文件
- `{test_file_path}`

### 测试用例统计

| 测试类/函数 | 场景 | Mock 依赖 | 预期结果 |
|-------------|------|-----------|----------|
| test_vip_user_gets_discount | VIP 用户折扣 | UserRepository | 返回 90 |
| test_invalid_transitions | 无效状态转换 | 无 | 抛出异常 |

## 运行方式

```bash
{运行命令}
```

## 成功标准

- [x] 只测试高风险/复杂逻辑
- [x] 正确使用 Mock 隔离外部依赖
- [x] 覆盖正常路径和关键边界条件
```

### 3. 运行命令

```bash
# Python
pytest tests/unit/test_{module}.py -v

# Node.js
pnpm test tests/unit/{module}.test.ts

# Go
go test ./{module}_test.go -v

# Java
mvn test -Dtest={ClassName}Test
```

---

## 🚫 严格禁止

- ❌ 为简单 CRUD 生成单元测试
- ❌ 为 getter/setter 生成测试
- ❌ 测试框架或第三方库的行为
- ❌ 在单元测试中调用真实数据库/API
- ❌ 测试执行时间超过 100ms
- ❌ 测试之间存在状态共享

---

## ✅ 成功标准

生成测试后，自检以下各项：

- [ ] 只测试了高风险/复杂逻辑
- [ ] 正确使用 Mock 隔离外部依赖
- [ ] 覆盖了正常路径和关键边界条件
- [ ] 状态机覆盖了所有有效/无效转换
- [ ] 单个测试执行时间 < 100ms
- [ ] 测试命名清晰，能看出测试目的