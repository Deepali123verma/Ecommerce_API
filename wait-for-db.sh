#!/bin/sh
# Extract DB host and port from DATABASE_URL (fallback to default 5432)
DB_URL=$DATABASE_URL

# Use parameter expansion to extract hostname safely
DB_HOST=$(echo "$DB_URL" | sed -E 's/.*@([^:/]+).*/\1/')
DB_PORT=$(echo "$DB_URL" | grep -oE ':[0-9]+' | head -1 | tr -d ':')

# Default port if not found
if [ -z "$DB_PORT" ]; then
  DB_PORT=5432
fi

echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Keep checking until connection is successful
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "✅ PostgreSQL is up - starting FastAPI"
exec "$@"
