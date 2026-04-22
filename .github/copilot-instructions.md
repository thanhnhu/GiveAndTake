# Copilot Instructions

## Project Overview

Give & Take is a Vietnamese charity web platform that connects **givers** (benefactors and charitable organizations) with **takers** (individuals/families in difficult circumstances). Users can register takers and givers, log monetary donations in VND, and manage their own records. The live site targets Vietnamese users and supports both Vietnamese and English.

## Tech Stack

**Frontend (`frontend/`)**
- Vue 3 with Composition API (`<script setup>`)
- Vite 6 (build tool), Vite dev proxy `/api` → `http://backend:8090`
- Pinia 2 + `pinia-plugin-persistedstate` (state management)
- Vue Router 4 (`createWebHistory`)
- Axios 1 with global interceptors (auto-unwraps `response.data`)
- Vee-Validate 4 + Yup (form validation)
- Bootstrap 5.3 + bootstrap-vue-next + Bootstrap Icons + FontAwesome 6 (UI)
- vue-i18n 11 (EN + VI translations in `src/lang/`)
- vue-toastification 2 (notifications)
- Moment.js (date formatting), js-cookie
- Jest 29 + `@vue/test-utils` 2 + jsdom (unit tests)

**Backend (`backend/`)**
- FastAPI + Uvicorn (ASGI)
- PostgreSQL 17 + psycopg3 async (`psycopg`, `psycopg_pool`)
- Raw SQL only — no ORM. All queries written by hand in Repository classes
- Token authentication (`Authorization: Token <key>`) stored in `authtoken_token` table
- Pydantic v2 (request/response schemas)
- Cloudinary / Azure / Google Drive / local (pluggable image storage via `StorageProvider` Protocol)
- Pillow (image processing), python-dotenv (config via env vars)

**Infrastructure**
- Docker + Docker Compose (frontend :8091, backend :8090, postgres :5432)
- Nginx in frontend container serves built Vue SPA and proxies `/api` to backend
- Database schema managed via plain SQL migrations in `backend/migrations/`

## Architecture

```
frontend/src/
  assets/styles/      # Global SCSS — global.css is the only custom stylesheet
  components/         # Vue SFCs — PascalCase filenames
    Givers/           # Giver list + detail (Givers.vue + givers.html, GiverInfo.vue + giverInfo.html)
    Main/             # Taker/donate views (Main.vue + main.html, TakerInfo, DonateInfo, Donates)
  helpers/            # Shared pure JS helpers (toastMessage, isMobile, array utils)
  lang/               # i18n JSON (en.json, vi.json)
  services/           # API call modules (one per domain, default export)
  stores/             # Pinia stores (one per domain, Options API)
  router.js           # All Vue Router routes
  validation.js       # Global vee-validate configuration + generateMessage
  utils.js            # $filters.formatDate (moment), registered as globalProperties

backend/
  api/                # FastAPI routers — one file per domain (takers, givers, donates, auth, users, images, messages, cities)
  core/               # security.py (auth helpers), storage.py (pluggable image upload), utils.py
  repositories/       # One Repository class per domain — all DB access lives here
  schemas/            # Pydantic models: *Create, *Update, *Out, Paginated* per domain
  dependencies.py     # FastAPI Depends: DBConn, CurrentUser, OptionalUser
  config.py           # Settings from env vars via python-dotenv
  migrations/         # Plain SQL files (001_init.sql, …)
  main.py             # FastAPI app, lifespan (connection pool), router registration
```

- FastAPI serves `/api/*`; Nginx serves the built Vue `index.html` at all other paths.
- DB connection pool is created at startup in `lifespan` and accessed via `request.app.state.pool`.
- `DBConn` / `CurrentUser` / `OptionalUser` are `Annotated` type aliases used directly in route signatures.
- Vue templates are split into external `.html` files (e.g. `main.html`, `givers.html`) and referenced via `<template src="./file.html">`.

## Coding Conventions

**Frontend**
- Vue SFCs: PascalCase filenames (`GiverInfo.vue`); external template files: camelCase (`giverInfo.html`)
- Pinia stores: Options API (`state/getters/actions`); exported as `fooStoreObj` (e.g. `userStoreObj`, `takersStoreObj`)
- All store state includes `fetchingData: false`, `error: null`, an entity array, and `total: 0`
- Use `storeToRefs` when destructuring reactive state from a store — never `computed(() => store.x)`
- Import alias `@` → `src/`; never use relative `../../` paths crossing module boundaries
- All UI text via `$t('key.subkey')`; never hardcode English strings in templates
- Service modules use `default export`; store constructors use named imports
- `useToast()` must be called inside a function, not at module level
- Validation schemas: `computed()` Yup object with `t()` inside, using `.typeError()` on number fields
- Pagination: use `$t('common.pagination_previous')` / `$t('common.pagination_next')`, never hardcode

**Backend**
- `snake_case` for variables, functions, file names; `PascalCase` for classes
- All domain tables use UUID primary keys; `auth_user` uses SERIAL (Django-compatible)
- One Repository class per domain in `repositories/`; all SQL lives inside Repository methods
- Pydantic schemas follow `*Create` / `*Update` / `*Out` / `Paginated*` naming
- `can_edit(owner_id, user)` → True for record owner or staff; `can_delete` → superuser only
- Never use an ORM — write raw async psycopg3 queries
- Config comes from environment variables only (never hardcode credentials)

## Testing

- Frontend tests live in `frontend/tests/unit/**/*.spec.js`
- Module alias `@` → `src/`, `~` → `tests/unit/factories/`
- Service layer always mocked via `jest.mock('@/services/fooService')`
- Pinia stores tested in isolation: `setActivePinia(createPinia())` in `beforeEach`
- Coverage thresholds: 80% branches/functions/lines; excluded: `main.js`, `router.js`, `stores/index.js`
- Run tests: `cd frontend && npm test`
- Backend: no automated test runner configured; validate via Swagger UI at `/api/docs` (dev only)

## Key Domain Concepts

| Term | Meaning |
|---|---|
| **Taker** | Person or family registered as needing charitable help |
| **Giver** | Charitable individual or organization offering help |
| **Donate** | A monetary contribution (VND integer) logged against a Taker |
| **stop_donate** | Boolean on Taker: no longer accepting new donations |
| **active** | Boolean on Giver: currently active/offering help |
| **can_edit** | Computed permission: true for record owner (`user_id`) or staff |
| **can_delete** | Computed permission: true for superuser only |
| **isMine** | Query param filter: returns only records owned by current user |
| **number** | Auto-incremented integer display ID on Taker/Giver (distinct from UUID PK) |
| **images** | JSONB column on Taker/Giver storing array of image objects (`{key, url, mob_url}`) |
| **city** | FK to `takers_city`; primary filter dimension for Takers and Givers |
| **isNewInline** | DonateInfo prop: renders icon gift button inline in taker row |
| **isNew** | DonateInfo prop: renders full "Add new" button (used in Donates page header) |
| **isEdit** | DonateInfo prop: renders pencil icon to edit an existing donate |
| **Pagination** | `{ count, results[] }` from backend; frontend uses `page` + `page_size` params |

## Project-Type Specifics

### Frontend

- **Component pattern**: Composition API only (`<script setup>`). Options API reserved for Pinia store definitions only.
- **Template split**: Large components have template in a separate `.html` file referenced with `<template src="./file.html">`. The Vite Babel plugin filter explicitly excludes `.html` and `?vue` virtual modules.
- **State management**: All async data fetching goes through a Pinia store action, never directly in a component. Set `fetchingData = true` before the call and `false` in `finally` (or catch).
- **Routing**: All routes in `src/router.js`. Route `/:pathMatch(.*)*` redirects to `/`. No auth guards currently — components check `user` ref from store.
- **Styling**: Bootstrap utility classes first; `.icon-action`, `.action-icons`, `table td { vertical-align: middle }` defined globally in `global.css`. Component-scoped styles only for layout/sizing (column widths, etc.).
- **Mobile layout**: `isMobile()` from `helpers/index.js` switches between table (desktop) and card (mobile) within the same component.
- **i18n**: Add new strings to both `en.json` and `vi.json` simultaneously. Validation messages use `computed()` Yup schemas with `t()` — never static Yup strings.
- **Persist**: Only `users` store has `persist: true`. `langs` store also persists locale preference — this is intentional.
- **Toast**: `toastMessage()` from `helpers/index.js` — calls `useToast()` lazily inside the function.

### Backend

- **API contracts**: All endpoints under `/api/`; routes defined directly in `api/*.py` files using `APIRouter`. Custom actions (e.g. `stop_donate`) are separate routes with action in path.
- **Auth**: Token authentication only. `Authorization: Token <key>` header. Tokens stored in `authtoken_token`, compatible with Django's DRF token table schema. Password verification uses Django PBKDF2 format via `verify_django_password`.
- **Database**: Raw psycopg3 async queries only. Schema managed via SQL migration files in `migrations/`. To alter schema: add a new numbered `.sql` file and run it manually (or via bootstrap script). Never edit existing migrations.
- **Connection pool**: `AsyncConnectionPool` created in `lifespan`, accessed as `request.app.state.pool` via `DBConn` dependency.
- **Required env vars**: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `STORAGE_TYPE`, and storage-specific vars (Cloudinary/Azure/Google). See `config.py` for defaults.
- **Image storage**: `get_storage_provider()` in `core/storage.py` returns correct provider based on `STORAGE_TYPE` env var. To add a backend: implement `StorageProvider` Protocol and register in the factory function.
- **Permissions**: `can_edit(owner_id, user)` used in route handlers before mutating. `can_delete` requires `user["is_superuser"]`. DELETE on users is not exposed.

## Dos and Don'ts

- **DO** use `storeToRefs` when reading reactive state from a Pinia store in a component.
- **DO** call `useToast()` inside the function body, not at module level.
- **DO** use `.typeError(msg)` on Yup `number()` fields to avoid raw "must be a number type" errors.
- **DO** use the server response (`newDonate`, `newTaker`, etc.) when pushing to local store arrays after a POST — never push the request payload.
- **DO** call `getTakers()` / `getGivers()` in `onMounted` when the component can be reached via direct URL (e.g. `Donates.vue` at `/donates/:id`).
- **DO** write raw SQL in Repository methods; use parameterized queries (`%s`) — never string interpolation.
- **DO** add new SQL schema changes as new numbered migration files.
- **DON'T** use an ORM on the backend — psycopg3 raw queries only.
- **DON'T** hardcode UI text in Vue templates — always use `$t()`.
- **DON'T** fetch data directly in components — go through a Pinia store action.
- **DON'T** use `computed(() => store.x)` to wrap store state — use `storeToRefs`.
- **DON'T** use named exports in service files — always `export default`.
- **DON'T** persist additional Pinia stores beyond `users` and `langs`.
- **DON'T** commit `.env` files or credentials — distribute changes through env var documentation in `config.py`.
- **DON'T** hardcode "Previous" / "Next" pagination text — use `$t('common.pagination_previous')` / `$t('common.pagination_next')`.


**Frontend (`frontend/`)**
- Vue 3 with Composition API (`<script setup>`)
- Vite 6 (build tool), Vite dev proxy for `/api`
- Pinia 2 + `pinia-plugin-persistedstate` (state management)
- Vue Router 4 (`createWebHistory`)
- Axios 1 with global interceptors (auto-unwraps `response.data`)
- Vee-Validate 4 + Yup (form validation)
- Bootstrap 5.3 + bootstrap-vue-next + FontAwesome 6 (UI)
- vue-i18n 11 (EN + VI translations in `src/lang/`)
- vue-toastification 2 (notifications)
- Moment.js (date formatting), js-cookie

**Backend (`backend/`)**
- Django + Django REST Framework
- PostgreSQL 15 (psycopg2)
- DRF Token Authentication
- WhiteNoise (static files), Gunicorn (WSGI)
- Cloudinary / Google Drive / Azure / local (pluggable image storage via factory)
- Pillow (image processing), python-dotenv + `credentials.json` (config)

**Infrastructure**
- Docker + Docker Compose (frontend :8091, backend :8090, postgres :5432)
- Vite dev server proxies `/api` → `http://localhost:8090`

**Testing**
- Jest 29 + `@vue/test-utils` 2 + jsdom (frontend only; backend tests in `tests.py` files)

## Architecture

```
frontend/src/
  assets/styles/      # Global SCSS
  components/         # Vue SFCs — PascalCase filenames
    Givers/           # Giver list + detail
    Main/             # Taker/donate views
  helpers/            # Shared pure JS helpers
  lang/               # i18n JSON (en.json, vi.json)
  services/           # API call modules (one per domain)
  stores/             # Pinia stores (one per domain)
  router.js           # All Vue Router routes
  validation.js       # Yup schemas
  utils.js            # isMobile(), misc utilities

backend/
  api/                # Django app: auth, users, messages
  takers/             # Django app: core domain (Taker, Giver, Donate, City, Image)
    models/           # One model class per file
    serializers/      # One serializer per file; factories/ for pluggable logic
    views/            # One ViewSet per file
  settings/           # dev.py / prod.py
  exception_handler.py
  urls.py
```

- Django serves `/api/` (DRF) and the built Vue `index.html` at all other paths.
- Two Django apps: `backend.api` (auth, users, messages) and `backend.takers` (core domain).
- `BaseModel → BaseSerializer → BaseViewSet` pattern for DRY abstraction across `takers/`.
- Router injected into every Pinia store via `pinia.use(({ store }) => { store.router = markRaw(router) })`.

## Coding Conventions

**Frontend**
- Vue SFCs: PascalCase filenames (`GiverInfo.vue`); JS utility files: camelCase (`takerService.js`, `givers.js`)
- Pinia stores exported as a callable `fooStoreObj` (e.g., `userStoreObj`, `takersStoreObj`)
- All store state includes `fetchingData: false`, `error: null`, an entity array, and `total` count
- Use `storeToRefs` when destructuring reactive state from a store in a component
- Import alias `@` → `src/`; never use relative `../../` paths that cross module boundaries
- All UI text via `$t('key.subkey')`; never hardcode English strings in templates
- Service modules use `default export`; use named imports for store constructors

**Backend**
- `snake_case` for variables, methods, and file names; `PascalCase` for class names
- `Base*` prefix for abstract base classes (`BaseModel`, `BaseSerializer`, `BaseViewSet`)
- One class per file in `models/`, `serializers/`, and `views/`
- All domain models use `UUIDField` primary key; never use integer PKs for domain entities
- Every domain model also has a `number` field (auto-incremented integer) as human-readable display ID
- Serializer `Meta.fields = '__all__'`; add computed permissions as `SerializerMethodField` (`can_edit`, `can_delete`)
- Filter querysets via `request.query_params.get(...)` in `get_queryset()`
- Permission classes composed with `&` (e.g., `IsOwnerOrIsAdmin & DeleteDenied`)

## Testing

- Test files live in `frontend/tests/unit/**/*.spec.js`
- Module alias `@` → `src/`, `~` → `tests/unit/factories/`
- Service layer is always mocked via `jest.mock('@/services/fooService')`
- Pinia stores are tested in isolation: `setActivePinia(createPinia())` in `beforeEach`
- Coverage thresholds: 80% branches/functions/lines; excluded from coverage: `main.js`, `router.js`, `stores/index.js`
- Run tests: `cd frontend && npm test`
- Backend tests live in `backend/api/tests.py` and `backend/takers/tests.py` (Django `TestCase`)

## Key Domain Concepts

| Term | Meaning |
|---|---|
| **Taker** | Person or family registered as needing charitable help |
| **Giver** | Charitable individual or organization offering help |
| **Donate** | A monetary contribution (VND integer) logged against a Taker |
| **stop_donate** | Boolean flag on Taker: no longer accepting new donations |
| **active** | Boolean flag on Giver: currently active/offering help |
| **can_edit** | Serializer-computed permission: true for record owner or admin |
| **can_delete** | Serializer-computed permission: true for superuser only |
| **isMine** | Query param filter: returns only records owned by the current user |
| **number** | Sequential integer display ID on Taker/Giver (distinct from UUID PK) |
| **images** | JSONField on Taker/Giver storing an array of image URL strings |
| **city** | FK to `City` model; primary filter dimension for both Takers and Givers |
| **BasePagination** | 30 results/page, `page_size` param, max 1000; response shape `{ count, results[] }` |

## Project-Type Specifics

### Frontend

- **Component pattern**: Composition API only (`<script setup>`). Do not use Options API in Vue components. Options API is reserved for Pinia store definitions.
- **State management**: All async data fetching goes through a Pinia store action, never directly in a component. Set `fetchingData = true` before the call and `false` in `finally`.
- **Routing**: All routes defined in `src/router.js`. Route guards check `userStore.isAuthenticated`.
- **Styling**: Use Bootstrap utility classes first; custom SCSS in `assets/styles/global.css` only for truly global overrides.
- **SSR vs CSR**: Pure CSR SPA. Django serves the built `index.html`; no SSR.
- **Mobile layout**: Use `isMobile()` from `utils.js` to switch between table (desktop) and card (mobile) layouts within the same component.
- **i18n**: Add new strings to both `en.json` and `vi.json` simultaneously.

### Backend

- **API contracts**: All endpoints under `/api/`; auto-generated by `DefaultRouter` from ViewSet registration. Custom actions use `@action(detail=True|False, methods=[...])`.
- **Auth pattern**: Token authentication only. Include `Authorization: Token <token>` on all authenticated requests. Tokens are auto-created via `post_save` signal on `User`.
- **Database & migrations**: Never edit existing migrations; always generate new ones via `python manage.py makemigrations`. Use `UUID` PKs for new domain models.
- **Required env vars / config**: Database credentials and storage config are read from `backend/credentials.json` (see `credentials.example.json` for schema). Never commit real credentials.
- **Image storage**: Determined by `STORAGE` setting; the `ImageSerializerFactory` returns the correct serializer. To add a new storage backend, add a new serializer in `serializers/factories/` and register it in the factory.
- **Service boundaries**: `backend.api` owns auth, user management, and messaging. `backend.takers` owns all charity-domain models (Taker, Giver, Donate, City, Image). Never import from `takers` inside `api` or vice versa.

## Dos and Don'ts

- **DO** use `storeToRefs` when reading reactive state from a Pinia store in a component.
- **DO** unwrap API responses in the Axios interceptor (`response.data`) — service methods receive the data directly, not the full Axios response.
- **DO** define new domain models as subclasses of `BaseModel` with a `UUID` primary key and a `number` field.
- **DO** add `can_edit` and `can_delete` as `SerializerMethodField` on any serializer that supports edit/delete in the UI.
- **DO** place all new API strings in both `en.json` and `vi.json`.
- **DON'T** use integer primary keys for new domain models in `backend.takers`.
- **DON'T** hardcode UI text in Vue templates — always use `$t()`.
- **DON'T** fetch data directly in components — go through a Pinia store action.
- **DON'T** persist additional Pinia stores beyond `users` unless there is an explicit requirement. User auth state is the only data that should survive page refresh.
- **DON'T** import backend `api` app models into `takers` or vice versa — keep the two Django apps independent.
- **DON'T** add a `DELETE` permission to the `users` endpoint — `DeleteDenied` is intentional.
- **DON'T** commit `credentials.json` — it is gitignored; distribute changes through `credentials.example.json`.
