#!/bin/sh

set -e

# Ensure logs directory exists inside the container
mkdir -p /workspace/factorydash/logs

exec "$@"

# EOF
