#!/usr/bin/env bash
# Install pretalx + dev tools into a local virtual environment (needs Python >= 3.13, uv).
set -euo pipefail
cd "$(dirname "$0")/.."
command -v uv >/dev/null || { echo "Install uv first: pip install uv"; exit 1; }
uv python install 3.13
uv sync --extra dev --inexact
uv pip install mutmut pip-audit radon
echo "Install done. Next: scripts/reset.sh"
