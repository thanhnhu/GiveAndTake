# Backend Code Review Checklist

Use this checklist when reviewing Backend, API, or Database code.

> **Severity guide**: Each item is tagged with a default severity. Adjust based on context — a missing index on a rarely-queried column is a suggestion, but on a high-traffic endpoint it's a warning.
> - ❌ = Critical
> - ⚠️ = Warning
> - 💡 = Suggestion

## 🔒 Security — OWASP (review first)
- ❌ **SQL Injection**: Are parameterized queries / prepared statements used? Raw SQL with string-concatenated user input is the most exploited web vulnerability.
- ❌ **Authentication**: Are endpoints requiring auth properly protected?
- ❌ **Authorization**: Does the user have permission to access this specific resource? (Check for IDOR — can user A access user B's data by changing an ID?)
- ❌ **No Hardcoded Secrets**: Are credentials, API keys, and tokens in env vars or secret managers (not committed in code)?
- ❌ **Password Hashing**: Are passwords hashed with bcrypt/Argon2? (MD5/SHA1 are broken for passwords)
- ⚠️ **JWT/Token Validation**: Are tokens verified, checked for expiry, and scoped correctly?
- ⚠️ **XSS Prevention**: Is user input sanitized before rendering in responses?
- ⚠️ **Safe Error Messages**: Do error responses hide internal details? (No stack traces, SQL errors, or file paths to the client)
- ⚠️ **Sensitive Data in Logs**: Is PII redacted from logs and error messages?
- ⚠️ **CORS Configuration**: Are CORS headers restrictive? (`Access-Control-Allow-Origin: *` in production is almost always wrong)
- ⚠️ **CSRF Protection**: Are state-changing endpoints protected from cross-site request forgery?
- ⚠️ **File Upload Security**: Are uploaded files validated for type, size, and content? Are they stored outside the web root?
- 💡 **Rate Limiting Headers**: Do rate-limited endpoints return `Retry-After` and `X-RateLimit-*` headers?

## ✅ Input Validation & Data
- ❌ **Input Validation**: Are all API inputs validated at the boundary? Unvalidated input is the root cause of injection attacks.
- ⚠️ **Type Checking**: Are input types validated (string, int, email format, UUID)?
- ⚠️ **Boundary Checks**: Are ranges validated (min/max length, value ranges, array sizes)?
- ⚠️ **Required Fields**: Are required fields enforced?
- 💡 **Business Rules**: Are domain-specific rules validated (e.g., quantity > 0, date in future)?

## 🌐 API Design & HTTP
- ⚠️ **HTTP Status Codes**: Are correct codes used? (200, 201, 400, 401, 403, 404, 409, 500)
- ⚠️ **REST Principles**: Do endpoints follow REST conventions (GET reads, POST creates, PUT/PATCH updates, DELETE removes)?
- ⚠️ **Response Format**: Is JSON structure consistent across endpoints (same envelope, error format)?
- 💡 **API Versioning**: Is the API versioned (e.g., `/v1/users`) for breaking changes?
- 💡 **Content-Type**: Are proper content-type headers set on requests and responses?

## 💾 Database & Queries
- ❌ **Transactions**: Are multi-step updates wrapped in transactions? Partial writes corrupt data.
- ⚠️ **N+1 Queries**: Are loops triggering individual DB calls? (Use `JOIN`, batch loading, or `IN` clause)
- ⚠️ **Connection Management**: Are DB connections properly closed/returned to pool?
- ⚠️ **Pagination**: Do list endpoints paginate large datasets? Unbounded queries can OOM.
- 💡 **Indexing**: Are foreign keys and frequently-queried/filtered columns indexed?
- 💡 **Query Optimization**: Are slow queries analyzed (EXPLAIN) for missing indexes or full scans?
- 💡 **Query Limits**: Are queries limited with a ceiling (e.g., `LIMIT 1000`) as a safety net?

## ⚡ Performance & Scalability
- ⚠️ **Timeouts**: Are external API calls wrapped with timeouts? A hanging dependency can cascade.
- ⚠️ **Rate Limiting**: Are public endpoints protected from abuse/DDoS?
- 💡 **Caching**: Are expensive or frequently-read queries/responses cached appropriately?
- 💡 **Lazy Loading**: Are large objects (files, blobs) loaded only when requested?
- 💡 **Async Processing**: Are long-running tasks offloaded to queues/workers instead of blocking the request?

## 🧱 Error Handling & Resilience
- ⚠️ **Error Handling**: Are errors caught, logged with context, and returned with appropriate HTTP status?
- ⚠️ **Idempotency**: Can create/update operations be safely retried without side effects? (Important for payment flows, webhooks)
- 💡 **Graceful Degradation**: Does the service handle dependency failures without cascading?
- 💡 **Circuit Breakers**: Are failing external services circuit-broken?
- 💡 **Retry Logic**: Are transient failures retried with exponential backoff and jitter?

## 📊 Observability & Monitoring
- ⚠️ **Logging**: Are errors logged with enough context (`request_id`, `user_id`, `timestamp`)?
- ⚠️ **Structured Logs**: Are logs in structured format (JSON) for parsing by log aggregators?
- 💡 **Tracing**: Can requests be traced across services (trace_id/span_id)?
- 💡 **Health Checks**: Does the service expose `/health` and `/ready` endpoints?
- 💡 **Metrics**: Are key metrics exposed (latency, error rate, throughput)?

## 🔄 Concurrency & State
- ❌ **Race Conditions**: Are concurrent updates handled? (e.g., optimistic locking, `SELECT ... FOR UPDATE`)
- ⚠️ **Concurrency Safety**: Is shared state protected (locks/mutex) in async or multi-threaded code?
- 💡 **Stateless Design**: Is the service stateless for horizontal scaling?

## 🧪 Testing
- ⚠️ **Unit Tests**: Are business logic and edge cases tested?
- ⚠️ **Error Scenarios**: Are error paths tested (not just happy path)?
- 💡 **Integration Tests**: Are database and API interactions tested end-to-end?
- 💡 **Test Isolation**: Do tests use isolated data and clean up after themselves?

## 🔄 Migrations & Deployments
- ❌ **Backward Compatible**: Can old code run with new schema during rolling deployment? Dropping a column that old code still reads causes outages.
- ⚠️ **Migration Rollback**: Can database migrations be safely rolled back?
- 💡 **Zero Downtime**: Does the change support rolling deployments?
- ⚠️ **Breaking API Changes**: Are breaking changes properly versioned with deprecation notices?

## 🏗️ Code Structure & Maintainability
- ⚠️ **Separation of Concerns**: Is business logic separated from routing/controllers?
- ⚠️ **DRY Principle**: Is duplicated code refactored?
- 💡 **Magic Numbers**: Are hardcoded values extracted to constants/config?
- 💡 **Naming Conventions**: Are variables, functions, and classes clearly named?

## 📦 Dependencies
- ⚠️ **Vulnerable Packages**: Are dependencies scanned for known CVEs?
- 💡 **Version Pinning**: Are dependency versions locked/pinned?
- 💡 **Unused Dependencies**: Are unused packages removed?
