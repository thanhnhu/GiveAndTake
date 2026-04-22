# Frontend Code Review Checklist

Use this checklist when reviewing Web Frontend code. **Primary focus: React.** Vue, Angular, and Svelte developers should adapt checks for framework-specific patterns (Vue composition API, Angular decorators/DI, Svelte reactivity).

> **Severity guide**: Each item is tagged with a default severity. Adjust based on context — a missing error boundary in a settings page is a warning, but in a payment flow it's critical.
> - ❌ = Critical
> - ⚠️ = Warning
> - 💡 = Suggestion

## 🛡️ Security (review first)
- ❌ **XSS Prevention**: Is `dangerouslySetInnerHTML` avoided or input sanitized? Unsanitized user content renders directly into the DOM.
- ❌ **Sensitive Data Exposure**: Are tokens/passwords stored securely? (not in localStorage for auth tokens — use httpOnly cookies or secure session management)
- ⚠️ **CSRF Protection**: Are CSRF tokens included in state-changing forms?
- ⚠️ **Cookie Flags**: Are cookies set with `Secure`, `HttpOnly`, and `SameSite` flags?
- ⚠️ **Third-Party Scripts**: Are CDN scripts verified with Subresource Integrity (SRI)?
- 💡 **Content Security Policy**: Is CSP configured to limit script sources?

## 🚨 Error Handling
- ❌ **Error Boundaries**: Are error boundaries in place to catch component crashes? An uncaught error in a child component can take down the entire app.
- ⚠️ **Fallback UI**: Is there graceful fallback for error states?
- ⚠️ **Network Errors**: Are API failures handled with user-facing feedback and retry/fallback?
- ⚠️ **Form Validation**: Are validation errors clearly displayed near the relevant fields?
- 💡 **Error Messages**: Are messages user-friendly (not raw error objects or stack traces)?

## 🧩 Component Architecture
- ⚠️ **Component Size**: Are components too large (>200 lines)? Should they be split?
- ⚠️ **Single Responsibility**: Does each component do one thing well?
- ⚠️ **Prop Drilling**: Are props passed through many levels? (Consider context/state management)
- 💡 **Reusability**: Are common patterns extracted to shared components?

## 🗄️ State Management
- ❌ **Effect Cleanups**: Do `useEffect` hooks clean up listeners/timers/subscriptions? Missing cleanups cause memory leaks and stale state bugs.
- ⚠️ **State Location**: Is state at the right level (not too high, not too low)?
- ⚠️ **Derived State**: Is redundant state avoided (computed from existing state)?
- ⚠️ **State Updates**: Are state updates immutable?
- 💡 **Global State**: Is global state (Redux/Zustand/Context) used only when needed?

## ⚡ Performance & Rendering
- ⚠️ **Re-renders**: Are components re-rendering unnecessarily? (Check `useCallback`/`useMemo` in React, `computed` in Vue)
- ⚠️ **Bundle Size**: Are large libraries imported efficiently? (`import map from 'lodash/map'` vs `import _ from 'lodash'`)
- ⚠️ **Race Conditions**: Are stale requests cancelled (AbortController) to prevent rendering outdated data?
- 💡 **Image Optimization**: Are images lazy-loaded with explicit dimensions (prevent CLS)?
- 💡 **List Virtualization**: Are long lists (>100 items) virtualized?
- 💡 **Code Splitting**: Are routes and large components code-split?
- 💡 **Memoization**: Are expensive computations memoized?

## ⏳ Loading & Async States
- ⚠️ **Loading Indicators**: Are loading states shown for async operations?
- ⚠️ **Optimistic Updates**: Are UI updates optimistic where appropriate?
- 💡 **Skeleton Screens**: Are skeleton loaders used instead of spinners for better UX?
- 💡 **Suspense / Streaming**: Is React Suspense, Vue async components, or framework streaming used appropriately?

## 📝 Forms & User Input
- ⚠️ **Controlled Components**: Are form inputs properly controlled?
- ⚠️ **Validation**: Is client-side validation implemented for required fields and formats?
- ⚠️ **Submit Protection**: Are submit buttons disabled during API calls to prevent double submission?
- 💡 **Debouncing**: Are expensive operations (search, API calls) debounced/throttled?
- 💡 **Success Feedback**: Is user notified of successful actions?

## 🔄 Data & API Integration
- ⚠️ **Error States**: Are API errors caught and displayed to user?
- ⚠️ **Request Cancellation**: Are pending requests cancelled on unmount?
- 💡 **Caching**: Are API responses cached (React Query, SWR, Apollo) to avoid redundant requests?
- 💡 **Retry Logic**: Are failed requests retried with backoff?

## 📱 Responsiveness & CSS
- ⚠️ **Mobile Support**: Does the layout work on small screens (320px+)?
- ⚠️ **Design Tokens**: Are CSS variables/design tokens used instead of hardcoded values?
- 💡 **Touch Targets**: Are interactive elements at least 44x44px?
- 💡 **Animations**: Are animations performant (use `transform`/`opacity`, avoid layout thrashing)?
- 💡 **Dark Mode**: Is dark mode support considered?

## ♿ Accessibility (a11y)
- ⚠️ **Semantic HTML**: Are proper elements used (`<button>`, `<nav>`, `<main>`, not `<div>` for everything)?
- ⚠️ **Alt Text**: Do all images have meaningful `alt` attributes?
- ⚠️ **Keyboard Navigation**: Are interactive elements reachable via Tab?
- ⚠️ **Focus Indicators**: Are focus styles visible (not `outline: none` without replacement)?
- 💡 **Color Contrast**: Does text meet WCAG contrast ratios (4.5:1 for normal text)?
- 💡 **ARIA Labels**: Are ARIA labels used where native semantics are insufficient?
- 💡 **Heading Hierarchy**: Are headings (h1-h6) used in logical order?

## 🔒 Type Safety
- ⚠️ **TypeScript**: Are types defined for props, state, and functions?
- ⚠️ **Any Types**: Is `any` avoided? (use `unknown` or proper types)
- ⚠️ **Null Checks**: Are nullable values properly handled?
- 💡 **Type Inference**: Are types inferred where possible (avoid redundant annotations)?

## 🧪 Testing & Quality
- ⚠️ **Unit Tests**: Are components tested for key behaviors?
- ⚠️ **Test IDs**: Are `data-testid` attributes added for E2E testing?
- 💡 **Accessibility Tests**: Are a11y rules tested (jest-axe, testing-library)?
- 💡 **Edge Cases**: Are loading/error states tested?

## 🏗️ Code Quality
- ⚠️ **Console Logs**: Are debug `console.log` statements removed?
- ⚠️ **DRY Principle**: Is duplicated code refactored?
- 💡 **Magic Numbers**: Are hardcoded values extracted to constants?
- 💡 **Naming Conventions**: Are variables, functions, and components clearly named?

## 🔍 SEO & Meta (if applicable)
- 💡 **Meta Tags**: Are title, description, and Open Graph tags set?
- 💡 **Semantic HTML**: Are heading tags used hierarchically?
- 💡 **Canonical URLs**: Are canonical tags set for duplicate content?
