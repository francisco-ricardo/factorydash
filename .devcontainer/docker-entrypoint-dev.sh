#!/bin/sh

set -e

# Ensure logs directory exists inside the container
mkdir -p /factorydash/app/factorydash/logs

exec "$@"

# EOF
