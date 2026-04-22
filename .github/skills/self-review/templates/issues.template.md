# Self Review Report

**Branch**: `[CURRENT_BRANCH]` → `[TARGET_BRANCH]`  
**Reviewed**: [DATE]  
**Tech Stack**: [DETECTED_STACKS]

## 🎯 Verdict: [VERDICT_STATUS]

[VERDICT_MESSAGE]

> [DIVERGENCE_WARNING — include only if target branch has new commits since this branch diverged]
> ⚠️ Target branch has X new commit(s) since this branch diverged. This review covers your branch's changes only and cannot detect conflicts with new code on [TARGET_BRANCH]. Consider rebasing before PR.

> [PRIORITIZED_REVIEW_NOTE — include only if diff exceeded 30 files or 2000 lines]
> ℹ️ Large diff (X files / Y lines). Review was prioritized: security-sensitive and high-change files reviewed in depth. Generated/config/lock files received lighter review.

## Summary

| Metric | Count |
|--------|-------|
| Files Reviewed | [FILES_COUNT] |
| Critical Issues | [CRITICAL_COUNT] ❌ |
| Warnings | [WARNING_COUNT] ⚠️ |
| Suggestions | [SUGGESTION_COUNT] 💡 |
| Guidelines Loaded | [GUIDELINES_LIST or "Domain checklists only"] |

<!-- Include only if requirements were provided by the user -->
## ✅ Requirements Coverage

| # | Requirement | Status | Notes |
|---|-------------|--------|-------|
| 1 | [REQUIREMENT_TEXT] | ✅ Met / ⚠️ Partial / ❌ Missing | [EVIDENCE_OR_GAP] |

_No requirements provided._ <!-- Remove this section entirely if no requirements were given -->

## Files Reviewed

| File | Status | Lines Changed | Issues |
|------|--------|---------------|--------|
| `[FILE_PATH]` | [STATUS_ICON] | +[ADDED] / -[REMOVED] | [ISSUE_COUNT] |

## ❌ Critical Issues (Must Fix)

> Bugs, security vulnerabilities, breaking changes, data loss risks.

| # | File | Line | Category | Issue | Recommendation |
|---|------|------|----------|-------|----------------|
| [ISSUE_ID] | `[FILE_PATH]` | [LINE_NUMBER] | [CATEGORY] | [ISSUE_DESCRIPTION] | [FIX_RECOMMENDATION] |

_No critical issues found._ <!-- Remove this line if issues exist -->

## ⚠️ Warnings (Should Fix)

> Code quality, readability, maintainability, missing error handling.

| # | File | Line | Category | Issue | Recommendation |
|---|------|------|----------|-------|----------------|
| [ISSUE_ID] | `[FILE_PATH]` | [LINE_NUMBER] | [CATEGORY] | [ISSUE_DESCRIPTION] | [FIX_RECOMMENDATION] |

_No warnings found._ <!-- Remove this line if issues exist -->

## 💡 Suggestions (Nice to Have)

> Patterns, optimizations, naming improvements.

| # | File | Line | Category | Issue | Recommendation |
|---|------|------|----------|-------|----------------|
| [ISSUE_ID] | `[FILE_PATH]` | [LINE_NUMBER] | [CATEGORY] | [ISSUE_DESCRIPTION] | [FIX_RECOMMENDATION] |

_No suggestions found._ <!-- Remove this line if issues exist -->

<!-- Include only if project-specific guidelines were loaded -->
## 📐 Project Convention Issues

> Violations of project blueprint, instructions, or best practices. Category shows which document the rule comes from.

| # | File | Line | Source | Issue | Recommendation |
|---|------|------|--------|-------|----------------|
| [ISSUE_ID] | `[FILE_PATH]` | [LINE_NUMBER] | [Blueprint / Instructions / Best Practices] | [ISSUE_DESCRIPTION] | [FIX_RECOMMENDATION] |

_No project convention issues found._ <!-- Remove this line if issues exist -->
