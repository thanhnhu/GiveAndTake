# Mobile Test Automation Review Checklist

Use this checklist when reviewing iOS (XCUITest, Detox) or Android (Espresso, UI Automator, Appium) test automation code.

> **Severity guide**: Each item is tagged with a default severity. Adjust based on context — a missing wait in a smoke test is a suggestion, but in a CI-gating test suite it's a warning.
> - ❌ = Critical
> - ⚠️ = Warning
> - 💡 = Suggestion

## ⏱️ Stability & Waits (review first — #1 cause of flaky mobile tests)

- ❌ **No Hard Waits**: Avoid `sleep()`, `Thread.sleep()`, or fixed delays. Use framework waits (`waitForElement`, `waitForElementWithMatcher`, `wait(for:timeout:)`, `waitForExistence`). Hard waits cause flakiness — too short (test fails) or too long (suite is slow).
- ⚠️ **Element Presence Verification**: Are tests verifying element existence before interacting? Missing checks cause "element not found" failures.
- ⚠️ **Timeout Configuration**: Are explicit timeouts set on waits? Framework defaults (10s-30s) may mask slow tests.
- ⚠️ **Animation/Transition Handling**: Are waits accounting for animations and screen transitions? (e.g., `waitForElementToDisappear` for modal closes)
- 💡 **Retry Logic**: Are auto-retry mechanisms used for flaky actions (network, animations)?

## 🎯 Locators & Identifiers (critical for maintainability)

- ❌ **Stable Identifiers**: Are locators resilient to UI refactoring? Avoid position-based selectors (`element(at: 0)` / `getChildAt(0)`).
- ⚠️ **Identifier Priority**: Follow:
  - **iOS**: `accessibilityIdentifier` > `accessibilityLabel` > NSPredicate with text/type (last resort)
  - **Android**: `contentDescription` > `resource-id` / `android:id` > XPath (last resort)
- ⚠️ **Unique Identifiers**: Are locators specific enough to match exactly one element? Ambiguous selectors interact with wrong elements.
- ⚠️ **Label Fragility**: Avoid text-based matching if labels are dynamic or translated — use accessibility IDs instead.
- 💡 **Accessibility IDs**: Do app developers set `accessibilityIdentifier` (iOS) / `contentDescription` (Android) for testable elements?

## 🧱 Test Structure & Organization

- ⚠️ **Page Object Pattern**: Is test logic separated from locators? POM keeps tests readable and locators maintainable.
- ⚠️ **Descriptive Names**: Does the test name describe the behavior being verified? (`test_login_with_expired_token_shows_error` — not `testLogin` or `test1`)
- ⚠️ **Given-When-Then / AAA**: Is test structure clear? (Arrange → Act → Assert)
- ⚠️ **Single Assertion Focus**: Does each test verify one user behavior? Multiple assertions per test make failures ambiguous.
- 💡 **Helper Methods**: Are repeated setup sequences (login, navigate, permissions) extracted to reusable helpers?
- 💡 **Positive & Negative Tests**: Does the test verify both success and error scenarios?

## 🧹 Isolation & Cleanup

- ❌ **Test Independence**: Can each test run in isolation, in any order? Tests that depend on prior state are fragile.
- ⚠️ **App State Reset**: Is app state reset between tests? (Clear cache, reset login, reset permissions)
- ⚠️ **Data Cleanup**: Does `tearDown`/`afterEach` clean up created data (even on failure)?
- ⚠️ **Permission Reset**: Are permissions reset to known state between tests? (Especially location, camera, contacts)
- ⚠️ **UI State Recovery**: Does the test handle unexpected dialogs (system alerts, crashes) and recover?
- 💡 **Parallel Safe**: Can tests run in parallel without device/simulator conflicts?

## 🔒 Security & Data

- ❌ **No Hardcoded Secrets**: Are credentials, tokens, API keys in environment variables or config — not hardcoded in test code?
- ⚠️ **Test Data Privacy**: Is PII/sensitive data anonymized or mocked?
- ⚠️ **Separate Test Accounts**: Are test API keys/accounts separate from production?
- 💡 **Mock External Services**: Are external APIs mocked to avoid flakiness from third-party outages?

## 📱 Device-Specific Handling

- ⚠️ **Device Orientation**: Are tests accounting for landscape/portrait orientation changes?
- ⚠️ **Screen Size Variance**: Do tests work on different device sizes (phones, tablets, foldables)?
- ⚠️ **OS Version Compatibility**: Is code handling API level differences (Android) and iOS version differences?
- ⚠️ **Safe Area / Notches**: Do tests account for notches, dynamic islands, safe areas affecting UI layout?
- 💡 **Simulator vs Device**: Can tests run on both simulators/emulators and real devices?
- 💡 **Background/Foreground**: Are app lifecycle transitions (background/foreground) handled?

## 🌐 Network & API Integration

- ⚠️ **Network Isolation**: Are API calls mocked or intercepted? (Mock Server, Appium Proxy, OkHttp Interceptor)
- ⚠️ **Request/Response Validation**: Are API responses validated before assertions on UI?
- ⚠️ **Offline Mode**: Are tests validating offline behavior and error handling?
- 💡 **Timeout Handling**: Are network timeouts tested (slow network, connection loss)?
- 💡 **Request Ordering**: Are requests properly sequenced (avoid race conditions in API calls)?

## 🐛 Error Handling & Debugging

- ⚠️ **Screenshots on Failure**: Are screenshots captured automatically on test failure? (Helps debugging)
- ⚠️ **Video Recording**: Are test videos recorded for debugging? (especially for flaky tests)
- ⚠️ **Logs Capture**: Are app logs and system logs captured for debugging? (Logcat for Android, Console for iOS)
- ⚠️ **Meaningful Assertions**: Do assertion messages explain WHAT failed and WHY?
- ⚠️ **Error Recovery**: Are expected transient failures (network hiccups, slow UI) handled gracefully?
- 💡 **Accessibility Tree Dump**: Can the test framework dump accessibility tree for debugging?

## 🧩 Framework-Specific Patterns

### iOS (XCUITest)

- ⚠️ **Predicate Matching**: Are predicates well-formed and efficient? (Avoid overly complex NSPredicate)
- ⚠️ **Tap/Swipe Accuracy**: Are taps using center of element coordinates (not hardcoded offsets)?
- ⚠️ **Keyboard Handling**: Are keyboard interactions tested (type, return key, autocorrect)?
- 💡 **Launch Arguments**: Are launch arguments used to configure test mode (bypass login, enable debug logs)?
- 💡 **Custom Activities**: Are XCUIActivity used to group related actions for better logging?

### Android (Espresso / UI Automator)

- ⚠️ **Idling Resources**: Are custom IdlingResources registered for async work? (Prevents "root cause was: "Test infrastructure error" failures)
- ⚠️ **ViewMatcher Efficiency**: Are view matchers efficient? Overly complex matchers slow tests.
- ⚠️ **System UI**: Are system UI interactions (back button, navigation) properly handled with `Uiautomator`?
- ⚠️ **Input Method Editor**: Is IME behavior handled (keyboard show/hide, text input)?
- 💡 **Device Interactions**: Are device-level actions (rotation, permissions) using `UiDevice` correctly?

### Cross-Platform (Appium / Detox)

- ⚠️ **Platform Abstraction**: Is platform-specific code abstracted away? (Separate page objects for iOS/Android if needed)
- ⚠️ **Capability Configuration**: Are capabilities properly configured for target device/OS?
- ⚠️ **Driver Initialization**: Is driver properly initialized and cleaned up between tests?
- 💡 **Native Context Switching**: When testing webviews, is context switching handled correctly?

## ♿ Accessibility (a11y)

- ⚠️ **Accessibility IDs Set**: Do developers set `accessibilityIdentifier` (iOS) / `contentDescription` (Android) for all interactive elements?
- ⚠️ **Screen Reader Testing**: Can critical flows be completed with screen reader enabled?
- 💡 **a11y Validation**: Are accessibility rules checked during tests (e.g., axe-core mobile)?
- 💡 **Dynamic Type / Font Scaling**: Are tests verifying UI with scaled fonts?

## 🌍 Localization (if applicable)

- ⚠️ **Locale-Agnostic Tests**: Do tests work across locales? Avoid hardcoding UI text.
- 💡 **RTL Support**: Are tests verifying right-to-left layout?
- 💡 **Date/Number Formatting**: Are date/number assertions locale-aware?

## 📊 Test Data Management

- ⚠️ **API Setup**: Are test preconditions set up via API calls rather than through UI? API setup is faster and more reliable.
- ⚠️ **Test Server**: Does the test point to a test server or staging environment (not production)?
- 💡 **Fixtures / Factories**: Are reusable data factories used for test data generation?
- 💡 **Database Seeding**: For complex scenarios, is the test environment database seeded directly?

## 🌐 Environment & CI

- ❌ **CI Ready**: Will the test run in headless/unattended mode? (No interactive prompts, no display dependencies)
- ⚠️ **Environment Agnostic**: Do tests work across environments (dev/staging/QA) using config — not hardcoded URLs/endpoints?
- ⚠️ **Test Duration**: Does each test complete in reasonable time? (< 3 min per test, < 30 min total suite for CI gating)
- ⚠️ **Flakiness Tracking**: Are flaky tests tracked and root-caused? (Avoid ignoring failures)
- 💡 **Reporting Format**: Are results reported in CI-parseable format (JUnit XML, HTML report, xcodebuild format)?
- 💡 **Artifact Capture**: Are logs, videos, screenshots saved as CI artifacts for post-mortem analysis?

## 🏗️ Code Quality & Patterns

- ⚠️ **DRY Principle**: Is duplicated test logic refactored into helpers?
- ⚠️ **Magic Values**: Are hardcoded delays, coordinates, or strings extracted to constants?
- ⚠️ **Naming Conventions**: Are variables, functions, and test classes clearly named per platform conventions?
- 💡 **Code Comments**: Are complex locators or workarounds documented?
- 💡 **Deprecated APIs**: Are deprecated framework methods replaced with current APIs?

## 🔄 Performance & Load

- 💡 **Test Suite Duration**: Is the total suite duration optimized? (Parallel execution, fast setup/teardown)
- 💡 **Device Resource Usage**: Are tests monitoring device CPU, memory, battery during runs?
- 💡 **App Launch Time**: Is app launch time from test optimized? (Use app lifecycle hooks, avoid full restarts)

## 📦 Dependencies & Configuration

- ⚠️ **Framework Version**: Are test framework versions pinned? (Avoid version drift breaking tests)
- ⚠️ **Device/OS Version Support**: Are targeted device/OS versions documented and tested?
- 💡 **CI Agent Capabilities**: Are CI agents configured with required SDKs and tools?
- 💡 **Dependency Updates**: Are test dependencies regularly updated for security and bug fixes?
