---
name: self-review
description: >
  Perform automated pre-PR code review with clear verdict. Analyzes branch changes, generates a table-based report with severity-categorized issues, and provides a Ready/Not Ready decision for PR creation. Use this skill whenever the user mentions self-review, reviewing code, checking changes before PR, asking if code is ready for PR or merge, code quality check, pre-merge review, or any variation of "review my branch". Also trigger for phrases like "check my diff", "anything wrong with my changes", "am I ready to merge", or "scan my code for issues" — even casual requests like that.
---

# Self Review Skill

Review code changes on the current branch and provide a clear verdict with structured feedback.

**Speed matters.** Minimize tool calls — batch everything possible into parallel calls. The biggest cost is round-trip latency, not analysis time.

## Workflow

### Step 1: Gather Context (all parallel)

Run ALL of the following in a **single turn** as parallel tool calls:

**Tool call 1 — Config file:** Read `project.config.json` from the first path that exists: `.cursor/`, `.github/`, `.documents-design/`, `.agent/`, `.claude/`. Extract `baseBranch` (default to `main` if not found).

**Tool call 2 — Git context** (single shell command, chain everything):
```bash
BASE=<baseBranch> && echo "::BRANCH::" && git rev-parse --abbrev-ref HEAD && echo "::UNTRACKED::" && git ls-files --others --exclude-standard && echo "::FETCH::" && git fetch origin "$BASE" 2>/dev/null && echo "::DIVERGENCE::" && git log HEAD.."origin/$BASE" --oneline && echo "::FILES::" && git diff "origin/$BASE"...HEAD --name-only && echo "::DIFF::" && git diff "origin/$BASE"...HEAD --unified=3
```

**Tool call 3 (optional) — Review feedback:** If `review-feedback.md` exists in the repo, read it. Its rules (skip / elevate / rule) override all generic checklists. Skip this call if you already know it doesn't exist.

From the output, extract:
- **Untracked files** — If any, warn the user but proceed with tracked changes only
- **Divergence** — If target branch has new commits, note for the report header
- **Changed file list + extensions** — Determines which checklist to load (if any)
- **Full diff** — The primary input for analysis

### Step 2: Load Checklist (conditional — zero or one file)

Based on changed file extensions, load **only the single most relevant** reference file:

| Dominant extensions | Reference |
|---|---|
| `.tsx`, `.jsx`, `.css`, `.scss` | `references/frontend.md` |
| `.py`, `.go`, `.java`, `.rb`, `.cs`, `.sql` | `references/backend.md` |
| `.swift`, `.kt`, `Podfile` | `references/mobile.md` |
| `.test.ts`, `.spec.js`, `.spec.ts`, `_test.go` | `references/automation.md` |
| `*Test.swift`, `*Test.kt`, `*UITest.swift` | `references/automation-mobile.md` |

Pick the stack with the most changed files. **Skip this step entirely** if the diff is small (<100 changed lines) or doesn't match any stack — your built-in knowledge is sufficient.

Also apply any project-specific rules from auto-loaded context (cursor rules, CLAUDE.md, copilot instructions etc.) — these override generic checklists.

### Step 3: Analyze (single pass)

Review each changed file in a **single pass**, adjusting depth by risk:

| Risk level | File types | Review depth |
|---|---|---|
| Critical | Auth, security, payments, DB migrations, API endpoints, config/secrets | All severity levels |
| High | Core utilities, data models, business logic, state management | Critical + warnings |
| Medium | UI components, styling, layouts | Critical issues only |
| Low | Tests, docs, storybook, mocks, fixtures | Bugs and security only |

**Issue severity:**
- **❌ Critical** — Bugs, security vulnerabilities, breaking changes, data loss
- **⚠️ Warning** — Missing error handling, performance issues, incomplete implementation
- **💡 Suggestion** — Better patterns, optimizations, naming

**Filtering (apply during analysis, not as a second pass):**

The goal is to catch real mistakes — not demonstrate thoroughness. Every low-value issue buries the important ones.

- **Changed lines only:** Only flag lines with `+` in the diff. Pre-existing code is out of scope unless your change makes it newly broken.
- **Consolidate repeats:** Same pattern in multiple places → report once with the best example, note other locations.
- **Codebase consistency:** If the existing codebase does it the same way, don't flag it (unless security/correctness).
- **Confidence:** Only include issues you're genuinely confident about. If uncertain, check surrounding code first.
- **Large diffs (>500 lines):** Raise severity threshold — focus on critical and high-confidence warnings only.

**Always flag** (any file): new TODO/FIXME in diff (⚠️ Incomplete Implementation), debug artifacts like `console.log`/`debugger`/`print()` (⚠️ Debug Artifact), hardcoded dev values like `localhost`/test credentials in production code (⚠️ Hardcoded Dev Value).

**Never flag:** formatting, style preferences, import ordering, CI-caught issues (lint/types), test file hardcoded values, pre-existing TODOs, auto-generated/lock files, missing JSDoc on internal functions.

3 high-value findings > 15 nitpicks.

**Requirements coverage** (only if the user stated what the changes should accomplish):
- ✅ Met → no issue
- ⚠️ Partial → Warning (Requirements Gap)
- ❌ Missing → Critical (Acceptance Criteria Not Met)
- ❌ Contradiction → Critical (Constraint Violation)

Omit requirements section entirely if none were provided.

### Step 4: Report & Summary

Write `issues.md` at repo root. Omit any section that has no items.

```markdown
# Self Review Report

**Branch**: `BRANCH` → `TARGET`  **Reviewed**: DATE  **Tech Stack**: STACKS

## 🎯 Verdict: [✅ Ready | ⚠️ Ready with Warnings | ❌ Not Ready]

[VERDICT_MESSAGE]

> [Only if divergence > 0] ⚠️ Target branch has X new commit(s). Consider rebasing.
> [Only if large diff] ℹ️ Large diff (X files / Y lines). Review prioritized by risk.

## Summary

| Metric | Count |
|--------|-------|
| Files Reviewed | X |
| Critical Issues | X ❌ |
| Warnings | X ⚠️ |
| Suggestions | X 💡 |

## ✅ Requirements Coverage
<!-- Only if requirements were provided -->
| # | Requirement | Status | Notes |
|---|-------------|--------|-------|

## Files Reviewed
| File | Status | Lines Changed | Issues |
|------|--------|---------------|--------|

## ❌ Critical Issues (Must Fix)
| # | File | Line | Category | Issue | Recommendation |
|---|------|------|----------|-------|----------------|

## ⚠️ Warnings (Should Fix)
| # | File | Line | Category | Issue | Recommendation |
|---|------|------|----------|-------|----------------|

## 💡 Suggestions (Nice to Have)
| # | File | Line | Category | Issue | Recommendation |
|---|------|------|----------|-------|----------------|
```

No code snippets — keep compact; the developer has the diff.

Then show in chat:
```
✅ Self-review complete! Generated issues.md

📊 Summary:
- Files Reviewed: X (Y skipped)
- ❌ Critical: X | ⚠️ Warnings: X | 💡 Suggestions: X

Verdict: [✅ Ready | ⚠️ Ready with Warnings | ❌ Not Ready]
```

List any critical issues briefly in the chat summary for immediate feedback.

## Verdict Logic

| Verdict | Criteria |
|---------|----------|
| **✅ Ready** | Zero critical, zero warnings |
| **⚠️ Ready with Warnings** | Zero critical, some warnings/suggestions |
| **❌ Not Ready** | One or more critical issues |

## Configuration

Required in `project.config.json` (search: `.cursor/` → `.github/` → `.documents-design/` → `.agent/` → `.claude/`):
```json
{ "baseBranch": "main" }
```

## Reference Files

- `references/frontend.md` — Frontend checklist (React, Vue, Angular)
- `references/backend.md` — Backend checklist (API, DB, security)
- `references/mobile.md` — Mobile checklist (iOS/Android native)
- `references/automation.md` — Web test automation checklist
- `references/automation-mobile.md` — Mobile test automation checklist
