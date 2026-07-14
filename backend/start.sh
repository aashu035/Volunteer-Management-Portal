#!/bin/sh
set -e

# Fix Render's postgres:// → postgresql+asyncpg:// for async driver
if echo "$DATABASE_URL" | grep -q "^postgres://"; then
  export DATABASE_URL=$(echo "$DATABASE_URL" | sed 's|^postgres://|postgresql+asyncpg://|')
fi

if echo "$DATABASE_URL_SYNC" | grep -q "^postgres://"; then
  export DATABASE_URL_SYNC=$(echo "$DATABASE_URL_SYNC" | sed 's|^postgres://|postgresql://|')
elif [ -z "$DATABASE_URL_SYNC" ]; then
  export DATABASE_URL_SYNC=$(echo "$DATABASE_URL" | sed 's|postgresql+asyncpg://|postgresql://|')
fi

echo "Running Alembic migrations..."
alembic upgrade head

echo "Seeding database..."
python -m app.db.seed || echo "Seeding skipped (already seeded)"

echo "Starting Gunicorn..."
exec gunicorn -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:${PORT:-8000} \
  --access-logfile - --error-logfile - app.main:app
