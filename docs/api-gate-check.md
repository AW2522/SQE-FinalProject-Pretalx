# API gate check (brief section 1)

Question: does the pretalx version expose an API operation that changes or creates a submission, and is an organiser
token allowed while a reviewer token is denied?

Method: baseline commit `887525d`, SQLite, Redis running, seeded data, one submission in state `submitted`
(created through the ORM for the check), API tokens created for the organiser, reviewer and speaker accounts with
submissions endpoint permissions. Requests sent with `curl` to `/api/events/sqe-conf/submissions/<code>/<action>/`.
Source: `src/pretalx/api/views/submission.py` defines POST actions accept, reject, confirm, cancel, make-submitted.

| # | Request | Token | Observed |
|---|---|---|---|
| 1 | POST accept | reviewer | 403 "You do not have permission to perform this action." |
| 2 | POST accept | speaker | 401 "Invalid token." (speaker tokens are not accepted for this endpoint) |
| 3 | POST accept | none | 404 "No Submission matches the given query." |
| 4 | POST accept (submitted to accepted) | organiser | 200 |
| 5 | POST accept again (same state) | organiser | 200 (no-op, state unchanged) |
| 6 | POST reject (accepted to rejected) | organiser | 200 |
| 7 | POST confirm (rejected to confirmed) | organiser | 200 |

Result: **gate passes.** Organiser allowed, reviewer denied.

Observation for the team (verify before logging as a defect): request 7 changed `rejected` to `confirmed` through the
API. In the source, `set_submission_state` (`submission/domain/submission.py`) has no allowed-transition table; the
UI-side guards are the predicates in `submission/rules.py` (for example `can_be_confirmed` requires `accepted`).
This is a candidate API weakness for Member 2 and a candidate disallowed-transition test for unit level.
Request 3 returns 404 rather than 401 for an unauthenticated caller; check whether this is intended hiding.

Repeat the table on your own machine and attach the raw output before using it as evidence.
