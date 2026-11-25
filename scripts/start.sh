#!/usr/bin/env bash
# Start the development server on http://localhost:8000
set -euo pipefail
source "$(dirname "$0")/_env.sh"
require_redis
exec $MANAGE runserver 0.0.0.0:8000
