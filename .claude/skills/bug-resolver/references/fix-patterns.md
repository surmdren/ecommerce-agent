# Common Bug Fix Patterns

Proven approaches for fixing common bug types.

## Pattern Categories

### 1. Defensive Programming

**Add Guard Clauses**
```python
# Before: Crashes on invalid input
def calculate_discount(price, percentage):
    return price * (percentage / 100)

# After: Validates input
def calculate_discount(price, percentage):
    if price <= 0:
        raise ValueError("Price must be positive")
    if not 0 <= percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100")
    return price * (percentage / 100)
```

**Null Safety**
```typescript
// Before: May crash
function getUsername(user) {
  return user.profile.name;
}

// After: Safe access
function getUsername(user) {
  return user?.profile?.name || 'Anonymous';
}
```

### 2. State Management

**Race Condition Fix**
```python
# Before: Race condition
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        temp = self.count
        time.sleep(0.001)  # Simulates processing
        self.count = temp + 1

# After: Thread-safe
import threading

class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1
```

**Transaction Rollback**
```python
# Before: Partial updates on error
def transfer_money(from_account, to_account, amount):
    from_account.balance -= amount
    to_account.balance += amount  # May fail

# After: Atomic transaction
def transfer_money(from_account, to_account, amount):
    with transaction.atomic():
        from_account.balance -= amount
        from_account.save()
        to_account.balance += amount
        to_account.save()
```

### 3. Error Handling

**Specific Exception Handling**
```python
# Before: Catches too much
try:
    data = fetch_data()
    process_data(data)
except Exception:
    return None  # Hides real errors

# After: Specific handling
try:
    data = fetch_data()
    process_data(data)
except NetworkError as e:
    logger.error(f"Network error: {e}")
    return cached_data()
except ValidationError as e:
    logger.warning(f"Invalid data: {e}")
    return default_data()
```

**Graceful Degradation**
```javascript
// Before: Hard failure
async function loadUserProfile() {
  const profile = await api.getProfile();
  const stats = await api.getStats();  // Blocks on failure
  return { profile, stats };
}

// After: Partial success
async function loadUserProfile() {
  const profile = await api.getProfile();
  let stats = null;
  try {
    stats = await api.getStats();
  } catch (e) {
    console.warn('Failed to load stats:', e);
    stats = { views: 0, likes: 0 };  // Default values
  }
  return { profile, stats };
}
```

### 4. Performance Fixes

**N+1 Query Problem**
```python
# Before: N+1 queries
def get_users_with_posts():
    users = User.objects.all()
    for user in users:
        user.posts = Post.objects.filter(user=user)  # N queries
    return users

# After: Single query with join
def get_users_with_posts():
    return User.objects.prefetch_related('posts').all()
```

**Memory Leak Fix**
```javascript
// Before: Event listeners never removed
function setupListener() {
  document.addEventListener('click', handleClick);
}

// After: Cleanup on unmount
function setupListener() {
  document.addEventListener('click', handleClick);
  return () => {
    document.removeEventListener('click', handleClick);
  };
}
```

### 5. Boundary Conditions

**Array Bounds Check**
```python
# Before: May access out of bounds
def get_next_item(arr, index):
    return arr[index + 1]

# After: Boundary check
def get_next_item(arr, index):
    if index + 1 < len(arr):
        return arr[index + 1]
    return None
```

**Off-by-One Fix**
```python
# Before: Skips last element
for i in range(len(items) - 1):
    process(items[i])

# After: Includes all elements
for i in range(len(items)):
    process(items[i])
# Or simply:
for item in items:
    process(item)
```

## Fix Implementation Checklist

For each bug fix:

1. **Minimal change**: Fix root cause, not symptoms
2. **Backward compatible**: Don't break existing functionality
3. **Add tests**: Prevent regression
4. **Update documentation**: If API/behavior changes
5. **Consider edge cases**: What else could break?
6. **Performance impact**: Will fix slow down operations?
