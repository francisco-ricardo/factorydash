#!/bin/bash
set -e

# Run migrations if DATABASE_URL is set
if [ "$DATABASE_URL" ]; then
    
    # Assumes that DBMS is Postgres
    # Run pg_isready to check if the database is ready

    # Wait for database with timeout
    echo "DATABASE_URL set to: $DATABASE_URL"
    echo "Waiting for database to be ready (timeout: 30s)..."
    timeout 30s bash -c "until pg_isready -q; do echo 'Database not ready yet. Retrying in 1 second...'; sleep 1; done"
    if [ $? -ne 0 ]; then
        echo "Error: Database at $DATABASE_URL not ready after 30 seconds. Exiting."
        exit 1
    fi
    echo "Database is ready!"

    echo "Running migrations..."
    python app/factorydash/manage.py migrate --noinput
else
    echo "DATABASE_URL not set. Skipping database setup."
fi

exec "$@"
