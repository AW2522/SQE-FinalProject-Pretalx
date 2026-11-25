# Shared environment for all scripts. Source, do not execute.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PRETALX_DATA_DIR="${PRETALX_DATA_DIR:-$ROOT/.data}"
export PRETALX_CONFIG_FILE="${PRETALX_CONFIG_FILE:-$ROOT/scripts/pretalx.sqe.cfg}"
PY="uv run --no-sync --project $ROOT python"
MANAGE="$PY $ROOT/src/manage.py"

# pretalx needs Redis for its cache (API throttling) and sessions. Fail loudly if it is missing.
require_redis() {
  $PY - <<'PYEOF' || { echo "Redis is not reachable on 127.0.0.1:6379. Start it first, e.g.: docker run -d --name sqe-redis -p 6379:6379 redis:7"; exit 1; }
import redis
redis.Redis.from_url("redis://127.0.0.1:6379/1").ping()
PYEOF
}
flush_redis() {
  $PY -c 'import redis; redis.Redis.from_url("redis://127.0.0.1:6379/1").flushdb()'
}
