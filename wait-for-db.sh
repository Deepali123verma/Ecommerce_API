#!/bin/sh

# Extract host and port safely from DATABASE_URL
DB_URL=$DATABASE_URL

# Example: postgresql://user:pass@dpg-abc123.oregon-postgres.render.com/dbname
DB_HOST=$(echo "$DB_URL" | sed -E 's|.*@([^:/]+)(:[0-9]+)?.*|\1|')
DB_PORT=$(echo "$DB_URL" | sed -nE 's|.*:([0-9]+)/.*|\1|p')

# Fallback defaults
[ -z "$DB_HOST" ] && DB_HOST="localhost"
[ -z "$DB_PORT" ] && DB_PORT="5432"

echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Wait for connection
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "✅ PostgreSQL is up - starting FastAPI"
exec "$@"
