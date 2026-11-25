# Proposed business-logic scope (draft for agreement with Member 2)

Based on a read of the source at the baseline commit and radon cyclomatic complexity. Agree the final list with
Member 2 and record it in `docs/business-rules.md`.

## Candidate files and functions
| Candidate | Where | What it decides | Radon CC |
|---|---|---|---|
| `set_submission_state` | `src/pretalx/submission/domain/submission.py:190` | state change, same-state no-op, initial-submit exception, clears `is_featured` on reject/cancel/withdraw, mail rule | 15 (C) |
| `can_be_reviewed` | `src/pretalx/submission/rules.py:135` | state is `submitted` AND active review phase allows review | 4 (A) |
| `can_be_withdrawn` | `rules.py:71` | state in submitted or accepted | 2 (A) |
| `can_be_confirmed` | `rules.py:76` | state is accepted | 2 (A) |
| `reviews_are_open` | `rules.py:99` | active review phase AND `can_review` | 2 (A) |
| `is_cfp_open` | `rules.py:51` | event AND public AND CfP open (3 conditions) | 3 (A) |
| `has_reviewer_access` | `rules.py:145` | reviewer permission, phase visibility, track limits | 9 (B) |
| `reviewer_can_change_submission_state` | `rules.py:168` | reviewer permission to change state | 3 (A) |
| `Submission.editable` | `submission/models/submission.py:353` | deadline, state, feature flag, review phase | 17 (C) |
| `ApiPermission._has_permission` | `src/pretalx/api/permissions.py:29` | token endpoint permissions and role | 19 (C) |

## Suggested mapping to the four business rules (to confirm with Member 2)
- **Boundary rule:** `Submission.title` max length 1000 (`models/submission.py:132`). Confirm where it is enforced
  (model validation or serializer) and test just below, at, just above.
- **Decision with two or more Boolean conditions:** `can_be_reviewed` (state AND phase) and/or `is_cfp_open` (3 conditions).
- **Change-of-state rule:** `can_be_withdrawn`, `can_be_confirmed`, `set_submission_state`.
- **Fourth rule:** `reviewer_can_change_submission_state` (permission) or the CfP open rule.

## Suggestions for the critical module (MCC and MC/DC)
- `is_cfp_open` has 3 conditions: 8 MCC rows, 4 MC/DC tests. Good size for a full truth table.
- `can_be_reviewed` has the guard `not obj` plus two conditions: small and easy to explain in the viva.
- Avoid `Submission.editable` (17) and `_has_permission` (19) for a full MCC table: too many conditions.

## Hand-calculated V(G) candidate (T1.2)
`has_reviewer_access` (rules.py:145): several `or` conditions, two early returns, a try/except. Radon gives 9;
Sonar may differ because of short-circuit and exception handling. Draw the CFG by hand and compare.

## Practical points to decide
1. **Coverage config:** upstream `pyproject.toml` has `fail_under = 100` over the whole run and its own omit list.
   Use a team config, for example `tests/team/coveragerc` with `branch = True`, `include` limited to the agreed files,
   `fail_under = 100`, and run `pytest -c tests/team/pytest.ini --cov-config=tests/team/coveragerc`.
2. **Test helpers:** upstream test factories live in `src/tests/factories`. Importing them blurs the "upstream tests
   earn no marks, do not mix" rule. Safer: write small own fixtures in `tests/team/unit/conftest.py`.
3. **Side effects:** `set_submission_state` sends signals, writes logs and queues mail. Cover the branches with
   real objects on SQLite rather than heavy mocking, and justify any line you cannot reach in
   `docs/uncovered-justification.md`.
4. **Keep the scope small:** the list must be short enough to reach 100% statement and branch coverage by Day 21 (brief: scope it tightly and write it down).
