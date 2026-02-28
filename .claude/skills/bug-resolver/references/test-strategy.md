# Test Strategy for Bug Fixes

Decision framework for selecting appropriate test types after bug fixes.

## Test Selection Decision Tree

```
Start: Bug Fixed
│
├─ Does fix change business logic?
│  ├─ Yes → Run UNIT tests
│  └─ No → Skip unit tests
│
├─ Does fix affect API endpoints?
│  ├─ Yes → Run API tests
│  └─ No → Skip API tests
│
├─ Does fix involve multiple services/modules?
│  ├─ Yes → Run INTEGRATION tests
│  └─ No → Skip integration tests
│
├─ Does fix affect user-facing UI?
│  ├─ Yes → Run E2E tests
│  └─ No → Skip E2E tests
│
└─ Severity = Critical?
   ├─ Yes → Run ALL test types
   └─ No → Run only selected tests
```

## Test Type Guidelines

### Unit Tests

**When to run:**
- Changed business logic (calculations, validations)
- Modified utility functions
- Fixed algorithm bugs
- Updated state management

**Example scenarios:**
- "Fixed discount calculation rounding error" → Unit test
- "Corrected date parsing logic" → Unit test
- "Fixed null pointer in validator" → Unit test

**Test focus:**
- Verify fix resolves the specific bug
- Test edge cases that caused the bug
- Ensure no regression in related logic

### API Tests

**When to run:**
- Changed API endpoint behavior
- Modified request/response handling
- Fixed authentication/authorization bugs
- Updated API error responses

**Example scenarios:**
- "Fixed 500 error on /api/users endpoint" → API test
- "Corrected authentication token validation" → API test
- "Fixed wrong status code on error" → API test

**Test focus:**
- Verify correct HTTP status codes
- Check request/response payload structure
- Test error handling for invalid inputs
- Validate authentication/authorization flows

### Integration Tests

**When to run:**
- Fixed bugs involving multiple services
- Changed database interaction patterns
- Modified external API integrations
- Fixed workflow/orchestration bugs

**Example scenarios:**
- "Fixed payment processing workflow" → Integration test
- "Corrected user registration email flow" → Integration test
- "Fixed data sync between services" → Integration test

**Test focus:**
- Verify end-to-end workflow completes
- Check data consistency across services
- Test transaction rollback behavior
- Validate message queue processing

### E2E Tests

**When to run:**
- Fixed UI bugs affecting user interactions
- Changed user-facing workflows
- Modified critical business flows
- Fixed security vulnerabilities in UI

**Example scenarios:**
- "Fixed checkout button not working" → E2E test
- "Corrected form submission error" → E2E test
- "Fixed login redirect loop" → E2E test

**Test focus:**
- Verify user can complete critical flows
- Test across different browsers (if UI change)
- Validate user experience improvements
- Check accessibility issues resolved

## Severity-Based Test Requirements

### Critical Severity
**Impact**: System down, data loss, security vulnerability

**Required tests**: ALL types
- Unit tests for the fix
- API tests if backend involved
- Integration tests for affected workflows
- E2E tests for critical user paths

### High Severity
**Impact**: Major feature broken, many users affected

**Required tests**: Depends on bug type + integration tests
- Tests specific to the bug type
- Integration tests to verify system stability
- Consider E2E for critical paths

### Medium/Low Severity
**Impact**: Minor issue, few users affected

**Required tests**: Specific to bug type only
- Run only tests directly related to the fix
- Skip comprehensive test suites

## Test Execution Strategy

### Parallel Execution
When tests are independent, run in parallel:
```bash
# Run unit and API tests simultaneously
pytest tests/unit & pytest tests/api & wait
```

### Sequential Execution
When tests have dependencies:
```bash
# Run integration tests after unit tests pass
pytest tests/unit && pytest tests/integration
```

### Smoke Tests First
Always run a quick smoke test before full suite:
```bash
# Quick smoke test (< 1 min)
pytest tests/smoke/

# If smoke tests pass, run full suite
if [ $? -eq 0 ]; then
  pytest tests/
fi
```

## Test Coverage Targets

### For Bug Fixes

**Minimum coverage**: Test the bug scenario
- Add test that reproduces the bug (should fail before fix)
- Verify test passes after fix

**Recommended coverage**: Test related edge cases
- Add tests for similar scenarios
- Test boundary conditions
- Test error handling paths

**Ideal coverage**: Comprehensive module testing
- Achieve 80%+ coverage for modified modules
- Add regression tests for related functionality

## Quick Reference

| Bug Type | Unit | API | Integration | E2E |
|----------|------|-----|-------------|-----|
| Logic error | ✅ | ❌ | ❌ | ❌ |
| API endpoint bug | ✅ | ✅ | ❌ | ❌ |
| Multi-service issue | ✅ | ✅ | ✅ | ❌ |
| UI bug | ❌ | ❌ | ❌ | ✅ |
| Workflow bug | ✅ | ✅ | ✅ | ✅ |
| Security bug | ✅ | ✅ | ✅ | ✅ |
| Data corruption | ✅ | ✅ | ✅ | ❌ |
| Performance issue | ✅ | ✅ | ✅ | ❌ |
