#!/usr/bin/env bash
# Drop the database, media and cache, then migrate and reseed to the known baseline state.
set -euo pipefail
source "$(dirname "$0")/_env.sh"
require_redis
rm -rf "$PRETALX_DATA_DIR"
mkdir -p "$PRETALX_DATA_DIR"
flush_redis
"$ROOT/scripts/seed.sh"
