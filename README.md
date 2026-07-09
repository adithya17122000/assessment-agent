# Team 4 — Assessment & Quiz Service

FastAPI microservice owning the complete Assessment & Quiz lifecycle: eligibility intake, assessment orchestration, AI-driven question generation, response capture, evaluation, and result exposure.

## Responsibilities

- **Assessment Eligibility** — receives course-completion events from Team 3, stores them, serves dropdown data (union/latest topic views) to the frontend.
- **Assessment Management** — creates AssessmentRequest and Assessment records when a user clicks "Take Assessment."
- **AI Question Generation** — builds prompts, calls the LLM, parses structured JSON output into stored questions.
- **Assessment Evaluation** — captures bulk submitted responses, scores them, produces pass/fail results.
- **Result Management** — read-only API exposing results (employee, course, score, status) to the downstream dashboard team.

## Tech Stack

- Python, FastAPI
- PostgreSQL, SQLAlchemy (2.x style)
- OpenAI-compatible LLM client

## Data Ownership

| Data | Owner | Notes |
|---|---|---|
| Employee identity | Team 1 | Referenced by ID only, never stored |
| Course/module metadata | Team 3 | Snapshotted at eligibility/request time |
| Questions, Responses, Scores | Team 4 | Full ownership |

## Repository Structure

See `app/` — 
organized by business capability (`eligibility/`, `assessment_management/`, `question_generation/`, `evaluation/`, `result_management/`),not technical layer. 
Each capability folder holds its own `models.py`, `schemas.py`, and service/helper logic. 
Routes live centrally under `app/api/`.

## Key Design Decisions

- No question bank — every assessment generates fresh questions via LLM.
- No AssessmentAttempt table — every "take" is an independent execution; retake history is queried via Employee ID + Course ID directly, not tracked as attempts.
- QuestionCount is fixed at 10, regardless of any count Team 3 sends.
- Correctness is computed only once, during Evaluation — never in real time as answers are submitted.
- Multi-select questions require an exact-set match — no partial credit.
- Pass/fail threshold is configurable via `PASS_THRESHOLD_PERCENT`, not hardcoded.
- Result Management is read-only — the dashboard team pulls via API; Team 4 never pushes data downstream.

## Known Gaps / Not Yet Built

- `Assessment.Status` only supports `In Progress` / `Completed` — no distinct failure state for generation errors.
- No ownership/auth check on result or assessment lookups by ID. as there is dependency
