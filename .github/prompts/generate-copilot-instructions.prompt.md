---
agent: agent
description: Analyze the project and generate a .github/copilot-instructions.md file tailored to this codebase.
---

Analyze this project and generate a `.github/copilot-instructions.md` file.

Explore the repository structure, key files (package.json, README, config files, source directories), and infer:

1. **Project type** — classify as one or more of: `frontend`, `backend`, `mobile`, `automation`. Look at frameworks, directory structure, and tooling to determine this.
2. **Stack** — language, framework, build tools, test runner
3. **Architecture** — directory layout, module boundaries, key patterns
4. **Coding conventions** — naming, formatting, import style, file organization
5. **Testing approach** — test framework, file naming, where tests live
6. **Domain vocabulary** — key terms, concepts, entity names specific to this project

Output the file using this structure:

---
# Copilot Instructions

## Project Overview
[1-3 sentence summary of what this project is and does]

## Tech Stack
[Bullet list: language, frameworks, key libraries, tools]

## Architecture
[Brief description of directory layout and module responsibilities]

## Coding Conventions
[Specific rules: naming conventions, file structure, import order, etc.]

## Testing
[How tests are organized and run, what to test, what not to mock]

## Key Domain Concepts
[Glossary of project-specific terms Copilot should understand]

## Project-Type Specifics
[Include only the subsections that apply to the detected project type(s):]
- **Frontend**: component patterns, state management, routing, styling approach, SSR vs CSR
- **Backend**: API contracts, auth patterns, database & migrations, required env vars, service boundaries
- **Mobile**: platform targets (iOS/Android/both), build & signing setup, emulator/simulator usage, native vs cross-platform distinctions
- **Automation**: test environment setup, selectors strategy, test data management, CI integration, credentials/secrets handling

## Dos and Don'ts
- DO: [project-specific best practices]
- DON'T: [common mistakes to avoid in this codebase]
---

Be specific and concrete — avoid generic advice. Every instruction should be grounded in what you actually observe in this codebase. Omit any Project-Type Specifics subsection that does not apply.
