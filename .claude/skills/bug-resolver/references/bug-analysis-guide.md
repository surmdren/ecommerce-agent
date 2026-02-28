# Bug Analysis Guide

Systematic approach to analyzing bugs before attempting fixes.

## Analysis Framework

### 1. Understand the Bug Report

Extract key information:
- **What**: Actual behavior vs expected behavior
- **When**: Conditions/triggers that cause the bug
- **Where**: Affected components/modules/files
- **Who**: User roles/permissions involved
- **Impact**: Severity and scope (single user vs all users)

### 2. Reproduce the Bug

Steps to confirm reproducibility:
1. Set up environment matching bug report
2. Follow exact steps described in ticket
3. Verify the bug occurs consistently
4. Document reproduction rate (always/intermittent/rare)

**If cannot reproduce**: Request more details from reporter before proceeding.

### 3. Root Cause Analysis

Use the "5 Whys" technique:

```
Bug: Login fails with 500 error
Why? → Server returns error
Why? → Database query fails
Why? → User table locked
Why? → Long-running migration in progress
Why? → Migration wasn't tested in staging

Root cause: Inadequate staging testing process
```

### 4. Impact Assessment

Evaluate:
- **User impact**: How many users affected?
- **Business impact**: Revenue/operations impacted?
- **Technical debt**: Does it expose larger architectural issues?
- **Scope**: Single module or cross-cutting concern?

## Common Bug Patterns

### Off-by-One Errors
```python
# Bug: Missing last element
for i in range(len(arr) - 1):  # Wrong
    process(arr[i])

# Fix
for i in range(len(arr)):  # Correct
    process(arr[i])
```

### Null/Undefined Handling
```javascript
// Bug: Crashes when user is null
const name = user.name;  // Throws error

// Fix: Safe access
const name = user?.name ?? 'Guest';
```

### Race Conditions
```python
# Bug: Check-then-act race condition
if balance >= amount:  # Thread 1 checks
    balance -= amount  # Thread 2 also passes check

# Fix: Atomic operation
with lock:
    if balance >= amount:
        balance -= amount
```

### Input Validation
```python
# Bug: No validation
def process_age(age):
    return age + 10  # Fails on invalid input

# Fix: Validate first
def process_age(age):
    if not isinstance(age, int) or age < 0 or age > 150:
        raise ValueError("Invalid age")
    return age + 10
```

## Investigation Checklist

Before coding a fix:

- [ ] Bug is reproducible
- [ ] Root cause identified (not just symptoms)
- [ ] Related code reviewed for similar issues
- [ ] Existing tests examined (do they cover this case?)
- [ ] Impact scope determined
- [ ] Fix approach validated (won't introduce new bugs)
