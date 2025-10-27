#!/bin/sh

# Arguments (like uvicorn command)
CMD="$@"

# Database host and port
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Check every 2 seconds until DB is ready
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 2
done

echo "✅ PostgreSQL is ready! Starting the application..."
exec $CMD
