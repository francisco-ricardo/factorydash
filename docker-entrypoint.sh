#!/bin/bash

# This script is the entrypoint for the Docker container.
# It is responsible for running migrations and starting the application.

set -e


# Functions definitions

# Main function
main() {

    # Run migrations if DATABASE_URL is set
    if [ "$DATABASE_URL" ]; then
        echo "DATABASE_URL set to: $DATABASE_URL"
        parse_database_url

        # Assumes that DBMS is Postgres
        # Run pg_isready to check if the database is ready

        # Wait for database with timeout
        echo "Waiting for database to be ready (timeout: 30s)..."
        timeout 30s bash -c "until pg_isready -h \"$DB_HOST\" -p \"$DB_PORT\" -U \"$DB_USER\" -d \"$DB_NAME\" -q; do echo 'Database not ready yet. Retrying in 1 second...'; sleep 1; done"
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

    # Print environment variables (debbuging)
    echo "Environment variables:"
    env | sort

    # Collect static files
    echo "Collecting static files..."
    python app/factorydash/manage.py collectstatic --noinput

    # Create periodic tasks
    echo "Setting up periodic tasks..."
    python app/factorydash/manage.py setup_periodic_tasks

}


# Function to parse DATABASE_URL
# Assumes DATABASE_URL is set and in the format: postgres://user:password@host:port/dbname
parse_database_url() {

    # Extract components from DATABASE_URL (e.g., postgres://user:password@host:port/dbname)
    # Handle both postgres:// and postgresql://
    DB_USER=$(echo "$DATABASE_URL" | sed -E 's|^postgres(ql)?:\/\/([^:]+):.*$|\2|')
    DB_PASSWORD=$(echo "$DATABASE_URL" | sed -E 's|^postgres(ql)?:\/\/[^:]+:([^@]+)@.*$|\2|')
    DB_HOST=$(echo "$DATABASE_URL" | sed -E 's|^postgres(ql)?:\/\/[^@]+@([^:/]+).*|\2|')
    DB_PORT=$(echo "$DATABASE_URL" | sed -E 's|^postgres(ql)?:\/\/[^@]+@[^:]+:([0-9]+).*|\2|' || echo "5432")
    DB_NAME=$(echo "$DATABASE_URL" | sed -E 's|^postgres(ql)?:\/\/[^@]+@[^/]+/(.+)$|\2|')

    # Log for debugging
    echo "Parsed DATABASE_URL:"
    echo "  User: $DB_USER"
    echo "  Host: $DB_HOST"
    echo "  Port: $DB_PORT"
    echo "  Database: $DB_NAME"
}


# Run main function
main

# Run the command passed to the Docker container
exec "$@"

# EOF
