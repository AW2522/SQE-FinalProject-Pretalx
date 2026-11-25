#!/usr/bin/env bash
# Create the synthetic baseline data (event, CfP, four accounts). Idempotent.
set -euo pipefail
source "$(dirname "$0")/_env.sh"
require_redis
$MANAGE migrate --noinput
$MANAGE shell --unsafe-disable-scopes < "$ROOT/scripts/seed_data.py"
