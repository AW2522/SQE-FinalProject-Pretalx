# Setup, start, seed and reset (T1.1)

Works on Linux, macOS and Windows via WSL2 (the scripts are bash). Tested on Ubuntu 24.04.

## Prerequisites
- Git, Python 3.13 (installed automatically by `uv`), `uv` (`pip install uv`)
- Redis on `127.0.0.1:6379`. Easiest: `docker run -d --name sqe-redis -p 6379:6379 redis:7`
- Docker is also needed later for SonarQube (about 4 GB free RAM)

## Commands
```bash
git clone https://github.com/pretalx/pretalx.git      # or the team repository
cd pretalx && git checkout 887525d8d3939172a4f3a52b3c8a48148608898a
./scripts/install.sh      # installs Python 3.13, dependencies, dev tools (pytest, coverage, mutmut, pip-audit, radon)
./scripts/reset.sh        # drops .data/, flushes Redis, migrates, seeds baseline data
./scripts/start.sh        # http://localhost:8000
```
- `./scripts/seed.sh` creates the baseline data (idempotent).
- `./scripts/reset.sh` returns to the known state: use it before every test run.
- `./scripts/start.sh` stops with a clear message if Redis is not running.

## Baseline data (synthetic)
Event `sqe-conf` ("SQE Test Conference"), CfP open for one year, password for all accounts `SqeTest-2026!`

| Role | Email | Rights |
|---|---|---|
| Admin | admin@sqe.test | administrator |
| Organiser | organiser@sqe.test | team "Organisers": can change submissions, settings, teams |
| Reviewer | reviewer@sqe.test | team "Reviewers": reviewer, cannot change submissions |
| Speaker | speaker@sqe.test | normal account, submits proposals |

Event URL: http://localhost:8000/sqe-conf/ (CfP at `/sqe-conf/cfp`), organiser area: http://localhost:8000/orga/
Mail uses the console backend; nothing is sent.

## Known setup facts
- Without Redis the API returns HTTP 500 (throttling uses the cache) and sessions fail. Scripts check for it.
- Do not run bare `uv run` after install: it re-syncs and removes dev tools. The scripts use `uv run --no-sync`.
- Configuration is in `scripts/pretalx.sqe.cfg`; data lives in `.data/` (git-ignored).
