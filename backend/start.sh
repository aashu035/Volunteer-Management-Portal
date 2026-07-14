#!/bin/sh
set -e

# Fix Render's DATABASE_URL for async driver
export DATABASE_URL=$(echo "$DATABASE_URL" | sed -e 's|^postgres://|postgresql+asyncpg://|' -e 's|^postgresql://|postgresql+asyncpg://|')

# Create DATABASE_URL_SYNC for Alembic (which uses psycopg2)
if [ -z "$DATABASE_URL_SYNC" ]; then
  export DATABASE_URL_SYNC=$(echo "$DATABASE_URL" | sed 's|postgresql+asyncpg://|postgresql://|')
fi

echo "Running Alembic migrations..."
python -m alembic upgrade head

echo "Seeding database..."
python -m app.db.seed || echo "Seeding skipped (already seeded)"

echo "Starting Gunicorn..."
exec gunicorn -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:${PORT:-8000} \
  --access-logfile - --error-logfile - app.main:app
