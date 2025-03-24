#!/bin/sh

set -e

# Ensure logs directory exists inside the container
mkdir -p /factorydash/app/factorydash/logs

# Print environment variables (debbuging)
echo "Environment variables:"
env | sort

# Run migrations if DATABASE_URL is set
if [ "$DATABASE_URL" ]; then
    echo "DATABASE_URL set to: $DATABASE_URL"
    echo "Running migrations..."
    python /factorydash/app/factorydash/manage.py migrate --noinput    
else
    echo "DATABASE_URL not set. Skipping database setup."
fi

# Check the integrity of the Django project
echo "Checking Django project integrity..."
python /factorydash/app/factorydash/manage.py check

# Create periodic tasks
echo "Setting up periodic tasks..."
python /factorydash/app/factorydash/manage.py setup_periodic_tasks

exec "$@"

# EOF
