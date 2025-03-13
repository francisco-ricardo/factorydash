#!/bin/sh

set -e

# Ensure logs directory exists inside the container
mkdir -p /factorydash/app/factorydash/logs

# Run database migrations
python /factorydash/app/factorydash/manage.py migrate

# Check the integrity of the Django project
python /factorydash/app/factorydash/manage.py check --settings=factorydash.settings_test

exec "$@"

# EOF
