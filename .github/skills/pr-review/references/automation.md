# Automation Test Review Checklist

Use this checklist when reviewing E2E or integration tests (Playwright, Cypress, Selenium, WebdriverIO, etc.).

> **Severity guide**: Each item is tagged with a default severity. Adjust based on context — a hard-coded wait in a quick smoke test is a suggestion, but in a CI-gating test suite it's a warning.
> - ❌ = Critical
> - ⚠️ = Warning
> - 💡 = Suggestion

## ⏱️ Stability & Waits (review first — #1 cause of flaky tests)
- ❌ **No Hard Waits**: Avoid `sleep()`, `page.waitForTimeout()`, or fixed delays. Use dynamic waits (`waitForSelector`, `waitForResponse`, `expect().toBeVisible()`). Hard waits are the leading cause of flaky tests — they're either too short (test fails) or too long (suite is slow).
- ⚠️ **Race Conditions**: Are async operations properly awaited? Missing `await` before Playwright/Cypress commands causes non-deterministic failures.
- ⚠️ **Timeout Configuration**: Are explicit timeouts set on actions and assertions? Relying on framework defaults (30s/60s) masks slow tests.
- ⚠️ **Network Waits**: Are tests waiting for API responses to complete before asserting on rendered data? (`waitForResponse`, `cy.intercept`)
- 💡 **Retry on Assertion**: Are auto-retrying assertions used (`expect(locator).toHaveText()` in Playwright, `.should()` in Cypress) instead of manual retry loops?

## 🎯 Selectors & Locators
- ❌ **Stable Selectors**: Are selectors resilient to UI changes? Using CSS classes tied to styling (`.btn-primary`) or fragile XPath (`/div[3]/span[2]`) breaks when the UI is refactored.
- ⚠️ **Selector Priority**: Follow: `data-testid` > `role` / ARIA > `id` > CSS > XPath (last resort)
- ⚠️ **Unique Selectors**: Are selectors specific enough to match exactly one element? Ambiguous selectors cause tests to interact with the wrong element.
- 💡 **Playwright Locators**: Prefer Playwright's built-in locators (`getByRole`, `getByText`, `getByTestId`) over raw CSS selectors — they auto-wait and provide better error messages.

## 🧹 Isolation & Cleanup
- ❌ **Test Independence**: Can each test run in isolation, in any order? Tests that depend on prior test state are fragile and impossible to parallelize.
- ⚠️ **Teardown**: Does `afterEach`/`afterAll` clean up created data (even on failure)? Leaked test data poisons later runs.
- ⚠️ **Own Test Data**: Does each test create its own seed data via API or fixtures? Shared data causes inter-test interference.
- 💡 **Parallel Safe**: Can tests run in parallel without conflicts? (No shared mutable state, no port collisions)

## 🔒 Security & Data
- ❌ **No Hardcoded Secrets**: Are credentials, tokens, and API keys in environment variables or config, not in test code?
- ⚠️ **Test Data Privacy**: Is PII/sensitive data anonymized or mocked?
- 💡 **API Keys Separation**: Are test API keys separate from production?

## 🐛 Error Handling & Debugging
- ⚠️ **Screenshots on Failure**: Are screenshots/videos/traces captured automatically on test failure?
- ⚠️ **Meaningful Assertions**: Do assertion messages explain WHAT failed and WHY? (`expect(count).toBe(5, 'Cart should have 5 items after adding')` not just `expect(count).toBe(5)`)
- ⚠️ **Trace / Debug Logs**: Are critical user actions logged for troubleshooting? (`console.log('Clicked checkout button')`)
- 💡 **Error Recovery**: Are expected transient failures (e.g., toast auto-dismiss) handled gracefully with retry or conditional logic?

## 🧱 Code Quality & Patterns
- ⚠️ **Page Object Pattern**: Is test logic separated from locators/selectors? Page Object Model (or equivalent abstraction) keeps tests readable and locators maintainable.
- ⚠️ **Explicit Assertions**: Does every test action have a corresponding assertion? Actions without assertions pass even when the feature is broken.
- ⚠️ **Descriptive Names**: Does the test name describe the behavior being verified? (`should show error when login with expired token` — not `test1` or `loginTest`)
- ⚠️ **Given-When-Then / AAA**: Is test structure clear? (Arrange preconditions → Act on the system → Assert expected outcome)
- 💡 **Positive & Negative Tests**: Does the test verify both success and error scenarios?
- 💡 **DRY Helpers**: Are repeated setup sequences (login, navigate, seed data) extracted to reusable helpers?

## 🌐 Environment & CI
- ❌ **CI Ready**: Will the test run in headless mode without display dependencies? (No `headless: false` left in CI config)
- ⚠️ **Environment Agnostic**: Does the test work across environments (dev/staging/prod) using config — not hardcoded URLs or ports?
- ⚠️ **Test Duration**: Does each test complete in a reasonable time? (< 2 min per E2E test, < 10 min total suite for CI gating)
- 💡 **External Dependencies**: Are external APIs/services mocked or stubbed to avoid flakiness from third-party outages?
- 💡 **Test Reporting**: Are results reported in a format CI can parse (JUnit XML, HTML report)?

## 📊 Test Data Management
- ⚠️ **Data Setup via API**: Are test preconditions set up via API calls rather than through the UI? API setup is faster and more reliable.
- 💡 **Fixtures / Factories**: Are reusable data factories or fixture files used for test data generation?
- 💡 **Database Seeding**: For complex scenarios, is the database seeded directly rather than clicking through UI flows?

## ♿ Accessibility (Optional)
- 💡 **A11y Validation**: Are basic accessibility rules checked during E2E flows (e.g., axe-core integration)?
- 💡 **Keyboard Navigation**: Can critical flows complete using keyboard only?
