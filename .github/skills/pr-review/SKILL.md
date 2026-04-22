---
name: pr-review
description: >
  Review pull request code changes, analyze for bugs/security/quality issues, and post inline comments to Git platforms. Use this skill whenever the user mentions reviewing a PR, checking code changes, doing a code review, looking at a pull request or merge request, or giving feedback on submitted code — for any request like "Review PR #42", "Check the changes in PR 123", "Can you review my pull request?", "Look at this MR", "What do you think about this PR?", or any variation involving PR/MR numbers or code review requests.
---

# PR Review Skill

Reviews PR diffs and posts structured inline comments to Git platforms.

Speed matters — minimize tool calls. Combine shell commands, avoid unnecessary file reads, and use the inline checklist below instead of loading reference files.

## Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prNumber` | number | Yes | The pull request number to review |

## Execution Steps

### Step 1: Load Configuration

Search for `project.config.json` in this order:
1. `.documents-design/project.config.json`
2. `.cursor/project.config.json`
3. `.github/project.config.json`
4. `.agent/project.config.json`
5. `.claude/project.config.json`

Extract: `baseBranch`, `platform`, `platformConfig`, `enableCommentPosting`, `enableNotification`. If not found, ask user to create it.

**Example config** (minimal, single-repo):
```json
{
  "baseBranch": "develop",
  "platform": "gitea",
  "platformConfig": {
    "gitea": {
      "apiUrl": "https://gitea.example.com/api/v1",
      "owner": "my-org",
      "repo": "my-repo"
    }
  },
  "enableCommentPosting": true,
  "enableNotification": true
}
```

### Step 2: Fetch and Prepare Diff

```bash
# Platform-specific fetch
# GitHub/Gitea: git fetch origin pull/${PR_NUMBER}/head:pr-${PR_NUMBER}
# GitLab: git fetch origin merge-requests/${PR_NUMBER}/head:mr-${PR_NUMBER}
# Bitbucket: git fetch origin pull-requests/${PR_NUMBER}/from:pr-${PR_NUMBER}

git checkout pr-${PR_NUMBER}
git fetch origin ${BASE_BRANCH}
git diff origin/${BASE_BRANCH}...HEAD --unified=3 > pr-${PR_NUMBER}.diff
git diff origin/${BASE_BRANCH}...HEAD --name-only > pr-${PR_NUMBER}-files.txt

# Add explicit line numbers to diff for accurate parsing
python {PR_REVIEW_SKILL_PATH}/scripts/add-line-numbers.py \
  pr-${PR_NUMBER}.diff pr-${PR_NUMBER}.diff
```

Inform the user: `✅ Diff saved to pr-${PR_NUMBER}.diff with line numbers (will be cleaned up after review)`

**Skip these files entirely** (don't read or analyze them):
- Lock files: `*.lock`, `package-lock.json`, `yarn.lock`, `Gemfile.lock`, `go.sum`
- Generated files: `*.generated.*`, `*.pb.go`, `*.pb.ts`, or files starting with `// @generated`
- Node modules, dist, build, .git directories

**Diff format with line numbers:**
```
@@ -10,5 +10,7 @@
 10 | function login(user) {
 11 | -  const token = secret_key;
 11 | +  const token = process.env.SECRET_KEY;
 12 | +  if (!token) throw new Error();
 13 |  return token;
```

### Step 3: Detect Tech Stack, Load Checklists, and Analyze

#### 3a. Load relevant checklists

From file extensions in the diff, load **only** the matching checklist(s):
- **Frontend**: `.tsx`, `.jsx`, `.css`, `.scss` → `references/frontend.md`
- **Backend**: `.py`, `.go`, `.java`, `.rb`, `.cs`, `.sql` → `references/backend.md`
- **Mobile**: `.swift`, `.kt`, `Podfile` → `references/mobile.md`
- **Web Tests**: `.test.ts`, `.spec.js`, `_test.go` → `references/automation.md`
- **Mobile Tests**: `*Test.swift`, `*Test.kt`, `*UITest.swift` → `references/automation-mobile.md`

Also load project-specific guidelines (glob search, exclude `node_modules`, `dist`, `build`, `.git`):
- `**/*-project-blueprint.md`, `**/*-instructions.md`, `**/*-best-practices.md`
- `**/review-feedback.md` — **highest precedence**, use first match found

Project-specific rules override generic checklists. Within checklists, focus on ❌ Critical and ⚠️ Warning items. Only raise 💡 Suggestion items on critical-risk files (auth, security, payments, database).

#### 3b. Apply review-feedback.md rules (if found)

Before analyzing, apply every row:
- `skip` rows — discard any matching comment silently
- `elevate:*` rows — override severity of matching comments
- `rule` rows — treat as additional checklist items at `critical` severity

#### 3c. Single-pass analysis

Read the full diff **once**. For each file, assess risk inline and adjust review depth:

| Risk Level | File Types | Depth |
|------------|-----------|-------|
| 🔴 Critical | Auth, security, secrets, payments, DB migrations, API endpoints | Deep — apply all checklist items |
| ⚠️ High | Core utils, data models, service handlers, business logic | Careful — critical + warnings |
| 💡 Medium | UI components, views, styling | Standard — critical issues only, skip minor |
| ✅ Low | Tests, docs, README | Light — only flag logical errors |

While reading, simultaneously assess:
- **Intent**: What's the purpose? Is the approach sound? Missing pieces?
- **Details**: Apply checklist items at the appropriate depth per file risk

**Severity definitions:**
- **critical** — Bugs (null access, race conditions, logic flaws), security (injection, broken auth, hardcoded secrets), breaking changes, data loss
- **warning** — Performance (N+1 queries, unbounded loops), missing error handling, maintainability
- **suggestion** — Better patterns, minor optimizations, readability

**Categories:** `Bug`, `Security`, `BreakingChange`, `Performance`, `Pattern`, `Type`, `Readability`, `Naming`, `Project Convention`

#### 3d. Noise filtering

The goal is to help the author ship better code — not demonstrate thoroughness. Every unhelpful comment buries the important ones.

**Core rules:**
1. **Changed-lines only** — Only comment on `+` lines. Pre-existing code is not up for review unless the author's change breaks it.
2. **Consolidate repeats** — Same issue in multiple places? ONE comment on the best example, note "Same pattern in [file:line, ...]".
3. **Consistency wins** — If the codebase already does it this way, don't flag the author for following the pattern (unless it's a security/correctness issue).
4. **Confidence required** — Only comment when genuinely confident something is wrong. Uncertain? Read surrounding code to confirm, or skip it.
5. **Respect scope** — Don't ask for scope expansion. Review what's in the PR, not what you wish were in it.
6. **Large PR threshold** — For PRs >500 lines changed, raise the bar: critical + high-confidence warnings only.

**Never comment on:** formatting, style preferences, linter-catchable issues, import ordering, blank lines, test hardcoded values/verbose setup, auto-generated files, TODO/FIXME comments, missing docstrings on private functions, variable naming that follows the file's existing conventions.

**Principle: 3 high-value comments > 15 nitpicks.**

### Step 4: Generate review.json

Create `review.json` in the workspace root. See `references/output-schema.md` for the full schema.

Each comment should have:
- A clear **title** summarizing the issue
- A **body** explaining the problem and why it matters
- A **recommendation** with the suggested fix
- A **codeSnippet** showing corrected code (when applicable)

### Step 5: Show Preview and Get Confirmation

```
PR #${PR_NUMBER} Review Summary
Found: X Critical | X Warnings | X Suggestions
Platform: ${PLATFORM} | Files: X | Comments: X

Post to ${PLATFORM}? (yes/no)
```

If no: review is saved. Post later with:
```bash
python {PR_REVIEW_SKILL_PATH}/scripts/post-review.py
```

### Step 6: Post Review

> ⚠️ **Never modify `project.config.json`** to enable posting.

```bash
python {PR_REVIEW_SKILL_PATH}/scripts/post-review.py
```

The script reads `review.json` and `project.config.json`, then:
- Posts inline comments to the platform if `enableCommentPosting: true`
- Sends a Google Chat notification if `enableNotification: true`
- Does both if both are `true` (notification is compact stats-only when comments are posted)
- Sends full rich notification when `enableCommentPosting: false`

### Step 7: Cleanup

```bash
rm -f pr-${PR_NUMBER}.diff
rm -f pr-${PR_NUMBER}-files.txt
git checkout -
git branch -D pr-${PR_NUMBER}
```

> ℹ️ `review.json` is automatically deleted by `post-review.py` during posting. Do not add it to this cleanup block.

## Reference Files

- `references/output-schema.md` — review.json schema and status rules
- `references/frontend.md` — Frontend code review checklist
- `references/backend.md` — Backend code review checklist
- `references/mobile.md` — Mobile (iOS/Android) app code review checklist
- `references/automation.md` — Web test automation checklist
- `references/automation-mobile.md` — Mobile test automation checklist
