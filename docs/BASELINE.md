# Baseline (T1.1)

| Item | Value |
|---|---|
| System under test | pretalx (Python/Django conference management system) |
| Upstream URL | https://github.com/pretalx/pretalx |
| Baseline commit | `887525d8d3939172a4f3a52b3c8a48148608898a` ("Make serializer selection consistent", 20 Nov 2026) |
| Licence | **AGPL-3.0-only with additional terms (AGPL section 7)**, see `LICENSE`. Static files, locale files and some older contributions are Apache-2.0; docs are CC-BY-SA-4.0. |
| Python | 3.13 or newer (`requires-python >=3.13` in pyproject.toml) |
| Framework | Django 6.1.x, Django REST Framework |
| Database | SQLite (default, local file) |
| Required service | Redis (cache, API throttling, sessions) |
| Module under test | Submission and review management |
| Baseline tag | `baseline-v1` (create after the first clean reset) |

## Licence correction
The task briefs say "Apache-2.0 (confirm in LICENSE)". Checking `LICENSE` at the baseline commit shows the project is
licensed **AGPL-3.0-only** with extra terms (no SaaS use, keep the "powered by pretalx" attribution, do not imply an
authorised distribution). Older versions were Apache-2.0. Use AGPL-3.0-only in the registration sheet and the report.
Local testing and a public GitHub repository containing the unmodified source are consistent with these terms; keep
`LICENSE` and the attribution intact and do not host the app as a service.

## Pinning
After cloning run `git checkout 887525d8d3939172a4f3a52b3c8a48148608898a`. If the team chooses another commit,
update this file and the registration sheet together.

## Upstream tests
Upstream tests live in `src/tests/` and earn no marks. Team tests live only in `tests/team/`.
Note that upstream `pyproject.toml` sets `fail_under = 100` for coverage over the whole run, so team coverage runs
must use their own coverage config (see `docs/scope-proposal.md`).
