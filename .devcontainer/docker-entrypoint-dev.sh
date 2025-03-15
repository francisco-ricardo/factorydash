#!/bin/sh

set -e

# Ensure logs directory exists inside the container
mkdir -p /factorydash/app/factorydash/logs


# Run migrations if DATABASE_URL is set
if [ "$DATABASE_URL" ]; then
    echo "DATABASE_URL set to: $DATABASE_URL"
    echo "Running migrations..."
    python /factorydash/app/factorydash/manage.py migrate --noinput    
else
    echo "DATABASE_URL not set. Skipping database setup."
fi


# Check the integrity of the Django project
python /factorydash/app/factorydash/manage.py check

exec "$@"

# EOF
