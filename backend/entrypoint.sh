#!/bin/sh

set -e

# Wait until PostgreSQL accepts connections before proceeding
wait_for_db() {
  echo "${0}: waiting for database to be ready (host=${DB_HOST:-postgres}, port=${DB_PORT:-5432}, dbname=${DB_NAME:-giveandtake})..."
  MAX_RETRIES=30
  i=0
  while [ $i -lt $MAX_RETRIES ]; do
    if python -c "
import psycopg, sys
try:
    psycopg.connect('host=${DB_HOST:-postgres} port=${DB_PORT:-5432} dbname=${DB_NAME:-giveandtake} user=${DB_USER:-giveandtake} password=${DB_PASSWORD:-giveandtake}').close()
    sys.exit(0)
except Exception as e:
    print(f'Connection error: {e}', file=sys.stderr)
    sys.exit(1)
" 2>&1; then
      echo "${0}: database is ready."
      return 0
    fi
    i=$((i + 1))
    echo "${0}: attempt $i/$MAX_RETRIES â€” not ready, retrying in 2s..."
    sleep 2
  done
  echo "${0}: database did not become ready in time, aborting."
  exit 1
}

# Set RUN_MIGRATIONS=true to apply migrations (use k8s Job or first-replica only)
# Skipped by default to avoid concurrent migration runs on multi-replica deployments
if [ "${RUN_MIGRATIONS}" = "true" ]; then
  wait_for_db
  echo "${0}: running migrations."
  python scripts/bootstrap_db.py
else
  echo "${0}: skipping migrations (set RUN_MIGRATIONS=true to enable)."
fi

echo "${0}: starting API server."
exec uvicorn main:app --host 0.0.0.0 --port 8090
