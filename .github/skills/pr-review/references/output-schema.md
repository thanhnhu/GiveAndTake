# Review Output Schema

## Standard Review Output (review.json)

Create a JSON file following this schema and save it to the project root as `review.json`.

### Full Example

```json
{
  "prNumber": 42,
  "status": "REQUEST_CHANGES",
  "summary": "The userId parameter is passed directly into a raw SQL query, exposing this endpoint to SQL injection. There is also an unhandled promise rejection in the error path that will silently swallow failures in production.",
  "statistics": {
    "filesReviewed": 5,
    "totalComments": 3,
    "criticalCount": 2,
    "warningCount": 1,
    "suggestionCount": 0
  },
  "comments": [
    {
      "path": "src/utils/api.ts",
      "line": 15,
      "category": "Security",
      "severity": "critical",
      "title": "Hardcoded API Key",
      "body": "API keys should never be committed to the repository.",
      "recommendation": "Use environment variables instead",
      "codeSnippet": "const API_KEY = process.env.API_KEY;"
    },
    {
      "path": "src/components/LoginForm.tsx",
      "line": 42,
      "category": "Bug",
      "severity": "critical",
      "title": "Unhandled Promise Rejection",
      "body": "The login handler does not catch errors from the authentication service, which will cause unhandled promise rejections in production.",
      "recommendation": "Add a \"try-catch\" block around the authentication call and handle errors gracefully.",
      "codeSnippet": "try {\n  await authService.login(userId, password);\n} catch (error) {\n  // Handle error\n}"
    }
  ],
  "metadata": {
    "reviewedAt": "2026-02-03T15:30:00Z",
    "baseBranch": "main",
    "sourceBranch": "feature/new-feature",
    "commitSha": "abc123def456"
  }
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prNumber` | integer | Yes | PR/MR number |
| `status` | string | Yes | `APPROVE`, `REQUEST_CHANGES`, or `COMMENT` |
| `summary` | string | Yes | Human-readable narrative describing what was found |
| `statistics` | object | No | Review statistics |
| `comments` | array | Yes | List of inline comments |
| `metadata` | object | No | Additional metadata |

### Comment Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | string | Yes | File path from repo root |
| `line` | integer | Yes | Line number in new file |
| `category` | string | Yes | `Security`, `Bug`, `BreakingChange`, `Performance`, `Pattern`, `Type`, `Readability`, `Naming`, `Project Convention` |
| `severity` | string | Yes | `critical`, `warning`, `suggestion` |
| `title` | string | Yes | Short issue title |
| `body` | string | Yes | Detailed description |
| `recommendation` | string | No | Suggested fix |
| `codeSnippet` | string | No | Recommended code |

### Status Rules

- **`APPROVE`** — Zero critical issues. Warnings and suggestions may exist but are non-blocking.
- **`COMMENT`** — Zero critical issues, but has warnings or suggestions that should be reviewed.
- **`REQUEST_CHANGES`** — One or more critical issues found. The PR should not be merged as-is.
