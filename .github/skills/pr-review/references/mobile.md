# Mobile Code Review Checklist

Use this checklist when reviewing **native** iOS (Swift/SwiftUI) or Android (Kotlin/Jetpack Compose) code. For cross-platform frameworks (Flutter, React Native), adapt these checks to framework-specific patterns.

> **Severity guide**: Each item is tagged with a default severity. Adjust based on context — a missing loading indicator on a debug screen is a suggestion, but on a checkout flow it's a warning.
> - ❌ = Critical
> - ⚠️ = Warning
> - 💡 = Suggestion

## 🔒 Security (review first)
- ❌ **No Hardcoded Secrets**: Are API keys, tokens, and credentials stored in config/env — not committed in source code?
- ❌ **Secure Storage**: Are sensitive credentials stored in Keychain (iOS) or Android Keystore — not SharedPreferences/UserDefaults?
- ❌ **Deep Link Validation**: Are deep link parameters validated and sanitized to prevent injection attacks?
- ⚠️ **Certificate Pinning**: Is SSL pinning implemented for sensitive API calls?
- ⚠️ **Biometric Auth**: Is biometric authentication implemented with proper fallback (passcode)?
- 💡 **Root/Jailbreak Detection**: Is rooted/jailbroken device detection implemented for sensitive flows?
- 💡 **Screenshot Protection**: Is sensitive data hidden when app enters background (recent apps view)?
- 💡 **Code Obfuscation**: Is ProGuard/R8 (Android) enabled for release builds?

## 📱 Threading & Lifecycle
- ❌ **Main Thread Safety**: Is heavy work (DB, network, computation, image processing) off the UI thread? Main-thread blocking causes ANRs (Android) and UI freezes (iOS).
- ❌ **Lifecycle Cleanup**: Are observers, listeners, and subscriptions removed in `onDestroy`/`onDisappear`/`deinit`? Leaking these causes crashes and ghost updates.
- ⚠️ **Memory Management**: Are strong reference cycles avoided in closures/listeners? (Use `[weak self]` in Swift, `WeakReference` in Kotlin)
- ⚠️ **Configuration Changes**: Are configuration changes (rotation, dark mode, locale) handled without data loss?
- ⚠️ **State Restoration**: Is state saved/restored correctly on process death?
- 💡 **Permissions**: Are runtime permissions requested at appropriate times with clear explanation?

## 🌐 Networking
- ⚠️ **Timeout Configuration**: Are network requests configured with explicit timeouts?
- ⚠️ **Error Handling**: Are network errors handled gracefully with user-friendly messages?
- ⚠️ **Offline Mode**: Does the app handle "No Internet" states without crashing?
- ⚠️ **Request Cancellation**: Are pending requests cancelled when leaving the screen?
- 💡 **Retry Logic**: Are failed requests retried with exponential backoff?
- 💡 **Response Validation**: Are API responses validated before use (null checks, type validation)?
- 💡 **Network Reachability**: Is network status checked before making API calls?

## 💾 Memory & Resources
- ❌ **Memory Leaks**: Are retain cycles (iOS closures) and context leaks (Android activities in singletons) avoided?
- ⚠️ **Image Handling**: Are bitmaps scaled/compressed before loading into memory? Full-resolution images in lists cause OOM.
- ⚠️ **Image Caching**: Are images cached appropriately (Glide/Coil for Android, SDWebImage/Kingfisher for iOS)?
- 💡 **Resource Files**: Are strings, colors, and dimensions in resource files (not hardcoded)?
- 💡 **Memory Warnings**: Are memory warnings handled (iOS `didReceiveMemoryWarning`)?

## ⚡ Performance
- ⚠️ **List Recycling**: Are RecyclerView (Android) / LazyColumn (Compose) / List (SwiftUI) used for scrollable lists?
- ⚠️ **Lazy Loading**: Are heavy resources loaded only when needed?
- 💡 **App Launch Time**: Is cold start optimized? (Defer non-essential initialization)
- 💡 **Smooth Animations**: Are animations smooth (avoid layout passes during animation)?
- 💡 **Background Work**: Is WorkManager (Android) or BGTaskScheduler (iOS) used for background tasks?
- 💡 **App Size**: Are unused resources and large assets optimized?

## 🧭 Navigation & Architecture
- ⚠️ **Navigation Patterns**: Is navigation consistent? (Navigation Component / Compose Navigation on Android, NavigationStack / Coordinator on iOS)
- ⚠️ **Back Stack**: Is back navigation handled properly without stack corruption?
- ⚠️ **Architecture Pattern**: Is MVVM / MVI followed consistently? Business logic should not live in Views.
- 💡 **Dependency Injection**: Are dependencies injected (Hilt/Koin for Android, manual DI or Swinject for iOS)?
- 💡 **Deep Linking**: Do deep links route to the correct screens?

## 📱 UI/UX
- ⚠️ **Safe Areas**: Does content respect notches, dynamic islands, and status bars?
- ⚠️ **Loading States**: Are loading indicators shown for async operations?
- ⚠️ **Error States**: Are error messages user-friendly with retry options?
- ⚠️ **Keyboard Handling**: Does the keyboard not cover input fields? (Insets, scroll adjustment)
- 💡 **Touch Feedback**: Do interactive elements show visual feedback when pressed?
- 💡 **Empty States**: Are empty states designed with helpful messages?
- 💡 **Pull to Refresh**: Is pull-to-refresh implemented where appropriate?

## ♿ Accessibility
- ⚠️ **Screen Reader**: Is content accessible to VoiceOver (iOS) / TalkBack (Android)?
- ⚠️ **Content Descriptions**: Do images/icons have content descriptions?
- ⚠️ **Touch Targets**: Are touch targets at least 44x44 points?
- 💡 **Font Scaling**: Does UI support dynamic font sizes?
- 💡 **Color Contrast**: Does text meet WCAG contrast requirements?

## 🌍 Localization
- ⚠️ **Hardcoded Strings**: Are all user-facing strings in resource files (Localizable.strings / strings.xml)?
- 💡 **RTL Support**: Does layout support right-to-left languages?
- 💡 **Date/Number Formatting**: Are dates/numbers formatted for locale?
- 💡 **Plurals**: Are plural strings handled correctly?

## 💾 Data Persistence
- ⚠️ **Database**: Is Room (Android) or Core Data / SwiftData (iOS) used correctly?
- ⚠️ **Migrations**: Are database migrations handled safely without data loss?
- 💡 **Cache Management**: Is cached data invalidated when stale?
- 💡 **Preferences**: Are SharedPreferences/UserDefaults used only for simple key-value data?

## 🧪 Testing
- ⚠️ **Unit Tests**: Are business logic and ViewModels tested?
- 💡 **UI Tests**: Are critical user flows tested (Espresso/Compose Testing / XCUITest)?
- 💡 **Mock Data**: Are network calls mocked for testing?
- 💡 **Edge Cases**: Are error states and edge cases tested?

## 📊 Analytics & Monitoring
- ⚠️ **Crash Reporting**: Is crash reporting configured (Firebase Crashlytics / Sentry)?
- 💡 **Analytics Events**: Are key user actions tracked?
- 💡 **Performance Monitoring**: Is app performance monitored (launch time, screen load)?
- 💡 **ANR Detection**: Are ANRs monitored (Android)?

## 🏗️ Code Quality
- ⚠️ **Naming Conventions**: Are classes, functions, and variables clearly named per platform conventions?
- ⚠️ **DRY Principle**: Is duplicated code refactored?
- ⚠️ **Deprecated APIs**: Are deprecated APIs replaced with modern alternatives?
- 💡 **Magic Numbers**: Are hardcoded values extracted to constants?

## 🛠️ Build & CI/CD
- ⚠️ **Signing**: Are signing configs secure (not committed to repo)?
- 💡 **Build Variants**: Are debug/release builds configured properly?
- 💡 **Version Code/Number**: Are version codes incremented?
