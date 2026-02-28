---
name: bug-resolver
description: 'Automated bug fixing workflow that pulls bug tickets from Jira, analyzes root causes, fixes code, runs intelligent tests (unit/API/integration/E2E), commits changes, and updates Jira with full fix details. Use when: (1) User provides a Jira ticket ID to fix (e.g., "fix PROJ-123"), (2) User requests batch bug fixes with JQL query (e.g., "fix all high priority bugs"), (3) User mentions "fix bug", "resolve Jira ticket", "bug fixing", "修复bug", "处理bug工单" (4) After development completion when bugs need systematic fixing and testing.'
---

# Bug Resolver

Automated workflow for pulling, analyzing, fixing, testing, and tracking bug fixes through Jira integration.

## Workflow Decision Tree

```
User Request
│
├─ Single Bug Fix
│  Input: "Fix PROJ-123" or Jira ticket ID
│  → Go to Single Bug Fix Workflow
│
└─ Batch Bug Fix
   Input: "Fix all high priority bugs" or JQL query
   → Go to Batch Bug Fix Workflow
```

## Single Bug Fix Workflow

### Step 1: Fetch Bug from Jira

Use `scripts/jira_client.py` to fetch bug details:

```bash
python scripts/jira_client.py get TICKET-123
```

Extract key information:
- Summary and description
- Severity/priority
- Affected components
- Reproduction steps
- Reporter and assignee

**Required environment variables:**
- `JIRA_URL`: Your Jira instance URL (e.g., https://company.atlassian.net)
- `JIRA_EMAIL`: Your Jira email
- `JIRA_API_TOKEN`: Your Jira API token

### Step 2: Analyze the Bug

Follow the Bug Analysis Framework from `references/bug-analysis-guide.md`:

1. **Understand the bug report** - What/When/Where/Who/Impact
2. **Reproduce the bug** - Verify it occurs consistently
3. **Root cause analysis** - Use "5 Whys" technique
4. **Impact assessment** - User/business/technical/scope

**If cannot reproduce**: Comment on Jira ticket requesting more details, then stop.

### Step 3: Fix the Code

Apply appropriate fix pattern from `references/fix-patterns.md`:

Common patterns:
- **Defensive programming** - Add guard clauses, null safety
- **State management** - Fix race conditions, add transactions
- **Error handling** - Specific exceptions, graceful degradation
- **Performance** - Fix N+1 queries, memory leaks
- **Boundary conditions** - Array bounds, off-by-one errors

**Fix principles:**
- Minimal change targeting root cause
- Backward compatible
- Consider edge cases
- No performance degradation

### Step 4: Intelligent Test Selection

Use `scripts/test_selector.py` to determine which tests to run:

```bash
python scripts/test_selector.py '["src/api/users.py", "src/models/user.py"]' "API endpoint returns 500 error" "high"
```

**Returns JSON:**
```json
{
  "tests": ["unit", "api", "integration"]
}
```

**Test selection logic:**
- Analyzes modified file paths
- Parses bug description keywords
- Considers severity level
- Defaults to unit tests minimum

Consult `references/test-strategy.md` for detailed test selection criteria.

### Step 5: Run Selected Tests

Based on test selector output, invoke appropriate test generator skills:

**Unit Tests:**
```
Use unit-test-generator skill for modified modules
```

**API Tests:**
```
Use api-test-generator skill for affected endpoints
```

**Integration Tests:**
```
Use integration-test-generator skill for multi-service workflows
```

**E2E Tests:**
```
Use e2e-test-generator skill for user-facing changes
```

**If any test fails:**
- Stop immediately
- Analyze failure (new bug vs regression)
- Update Jira with failure details
- DO NOT proceed to commit

### Step 6: Commit Changes

Only after ALL tests pass, use the `commit` skill:

```
Use commit skill with message format:
"fix(module): Brief description of fix

Fixes TICKET-123

- Root cause: [explain]
- Solution: [explain]
- Tests: [list test types run]"
```

### Step 7: Update Jira Ticket

Use `scripts/jira_client.py` to update ticket with full fix details:

```bash
python scripts/jira_client.py update TICKET-123 "Bug fixed" "Done"
```

**Update content includes:**
1. **Problem analysis**
   - Root cause identified
   - Impact scope

2. **Fix description**
   - Changes made
   - Why this approach was chosen

3. **Code changes**
   - Files modified
   - Key code changes

4. **Test results**
   - Test types run
   - All tests passing
   - Coverage info if available

5. **Commit information**
   - Commit SHA
   - Branch name
   - Repository link

**Status transition**: Move ticket to "Done" or "Ready for QA" based on workflow.

**Add label**: `auto-fixed` to track automated fixes.

## Batch Bug Fix Workflow

### Step 1: Search Bugs with JQL

Use `scripts/jira_client.py` to search bugs:

```bash
python scripts/jira_client.py search "project=PROJ AND type=Bug AND priority=High AND status='To Do'"
```

**Common JQL queries:**
- High priority: `priority IN (High, Critical) AND status='To Do'`
- Specific component: `component='Backend' AND type=Bug`
- Recent bugs: `created >= -7d AND type=Bug`

### Step 2: Process Each Bug

For each bug in the search results:
1. Run Single Bug Fix Workflow (Steps 1-7)
2. If fix fails: Log failure and continue to next bug
3. Track success/failure counts

### Step 3: Generate Batch Report

After processing all bugs, generate summary:

```
Batch Fix Report
================
Total bugs: 10
Successfully fixed: 7
Failed: 2 (PROJ-101, PROJ-105)
Skipped (cannot reproduce): 1 (PROJ-110)

Commits created: 7
Tests run: unit (7), API (4), integration (3), E2E (1)
```

Post summary as comment on Epic or parent ticket if applicable.

## Failure Handling

When any step fails:

1. **Stop processing immediately**
2. **Document failure in Jira**:
   ```bash
   python scripts/jira_client.py update TICKET-123 "Auto-fix failed: [reason]"
   ```
3. **Add label**: `auto-fix-failed`
4. **NO automatic rollback** (requires manual review)
5. **Move to appropriate status**: "Blocked" or "Needs Investigation"

**Common failure reasons:**
- Cannot reproduce bug
- Tests fail after fix
- Multiple possible root causes
- Requires architectural change

## Integration with Other Skills

This skill coordinates with:

- **unit-test-generator** - Generate unit tests for fixed code
- **api-test-generator** - Generate API endpoint tests
- **integration-test-generator** - Generate integration tests
- **e2e-test-generator** - Generate E2E tests
- **commit** - Create conventional commits
- **dev-executor** - For complex fixes requiring new features

## Environment Setup

### Required Environment Variables

Create `.env` file or export variables:

```bash
export JIRA_URL="https://your-company.atlassian.net"
export JIRA_EMAIL="your-email@company.com"
export JIRA_API_TOKEN="your-api-token"
```

**Get Jira API Token:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Create API token
3. Copy token to `JIRA_API_TOKEN`

### Python Dependencies

Install required packages:

```bash
pip install requests
```

### Test Scripts

Verify setup by testing Jira connection:

```bash
python scripts/jira_client.py get YOUR-TICKET-ID
```

Should output ticket details if configured correctly.

## Example Usage

**Single bug fix:**
```
User: "Fix bug PROJ-123"
Claude: [Follows Single Bug Fix Workflow]
```

**Batch fix:**
```
User: "Fix all high priority API bugs"
Claude: [Constructs JQL, follows Batch Bug Fix Workflow]
```

**With specific test types:**
```
User: "Fix PROJ-456 and run full test suite"
Claude: [Runs all test types regardless of selector]
```

## Resources

### Scripts

- **jira_client.py** - Jira API wrapper for fetching and updating tickets
- **test_selector.py** - Intelligent test type selection based on bug context

### References

- **bug-analysis-guide.md** - Systematic bug analysis framework
- **fix-patterns.md** - Common bug fix patterns and examples
- **test-strategy.md** - Test selection decision trees and guidelines

No assets directory needed for this skill.
