# Give and Take

Give and Take is a charity platform connecting givers (individuals and organizations) with takers (people or families in difficult situations).

Live site:
http://give.vfriends.info

## Current Architecture

This repository now uses a FastAPI backend and Vue 3 frontend.

- Frontend: Vue 3, Vite, Pinia, Bootstrap 5
- Backend: FastAPI, psycopg3, async connection pool
- Database: PostgreSQL 17
- Storage: Cloudinary (image upload variants)
- Runtime: Docker Compose (recommended)

## Repository Structure

Top-level:

- frontend: Vue frontend
- backend: FastAPI backend
- docker-compose.yml: local multi-service stack
- .env.example: environment template

Backend structure in backend:

- main.py: app bootstrap, lifespan, health, docs and schema routes
- config.py: settings and environment loading
- dependencies.py: FastAPI dependency injection for DB and auth context
- api: HTTP transport layer (route modules per domain)
- repositories: data-access layer (SQL per aggregate/domain)
- schemas: request and response models
- core: cross-domain helpers (security, storage, utilities)
- migrations: SQL bootstrap migrations
- scripts/bootstrap_db.py: migration + city fixture bootstrap
- entrypoint.sh: startup workflow (bootstrap then start server)

## Backend Layering Model

The backend follows a production-oriented layered design:

- API layer: endpoint declarations, status codes, route contracts
- Schema layer: request and response validation models
- Repository layer: SQL and persistence logic only
- Core layer: reusable business and infra helpers
- Dependency layer: DB connection and authenticated user resolution

This keeps routing concerns separate from SQL and shared logic.

## API Documentation

Docs URL:
http://localhost:8090/api/docs/

Schema URL:
http://localhost:8090/api/schema/

Endpoints are grouped by category in docs:

- System
- Auth
- Cities
- Takers
- Givers
- Donates
- Users
- Messages
- Images

## Runtime Ports

- Frontend: 8091
- Backend API: 8090
- PostgreSQL: 5432

## Environment Setup

1. Copy environment template:

   copy .env.example .env

2. Fill required values in .env:

- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD
- STORAGE_TYPE
- CLOUDINARY_CLOUD_NAME
- CLOUDINARY_API_KEY
- CLOUDINARY_API_SECRET

If needed, use setup-env.ps1 to generate starter files.

## Run with Docker (Recommended)

Start all services:

  docker compose up --build -d

Check status:

  docker compose ps

Follow logs:

  docker compose logs -f backend
  docker compose logs -f frontend

Stop services:

  docker compose down

## Startup Bootstrap Behavior

On backend container start, entrypoint.sh does:

1. Run SQL migrations from backend/migrations
2. Load city fixture from backend/cities.json when takers_city is empty
3. Start uvicorn on port 8090

## Run Without Docker

Backend:

  cd backend
  pip install -r requirements.txt
  uvicorn main:app --host 0.0.0.0 --port 8090 --reload

Frontend:

  cd frontend
  yarn install
  yarn dev

Frontend proxies /api to VITE_API_PROXY_TARGET (default in docker is http://backend:8090).

## Testing

Frontend unit tests:

  cd frontend
  npm test

Backend currently uses bootstrap SQL + runtime smoke verification in this branch.

## Notes

- Backend config is loaded from environment variables only. See `.env.example` for required variables.
- Never commit `.env` — use `setup-env.ps1` to generate starter files.
