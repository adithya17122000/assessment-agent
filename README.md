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
- organized by business capability (`eligibility/`, `assessment_management/`, `question_generation/`, `evaluation/`, `result_management/`),not technical layer. 
- Each capability folder holds its own `models.py`, `schemas.py`, and service/helper logic. 
- Routes live centrally under `app/api/`.

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

# Setup Instructions

## 1. Prerequisites

- Python 3.11+
- PostgreSQL installed and running(Only for prod , not for demo)
- An OpenAI-compatible LLM API endpoint and key

## 2. Clone and install dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## 3. Create the database(optional for demo as we are using supabase)

\`\`\`bash
psql -U your_username -h localhost -p 5432 -c "CREATE DATABASE assessment_db;"
\`\`\`

## 4. Configure environment variables

Create a `.env` file in the project root:

\`\`\`
- DB_HOST=localhost
- DB_PORT=5432
- DB_USER=your_username
- DB_PASSWORD=your_password
- DB_NAME=assessment_db

- AI_API_URL=your_llm_endpoint
- AI_API_KEY=your_llm_api_key
- MODEL=your_model_name

- PASS_THRESHOLD_PERCENT=60
\`\`\`

## 5. Create all tables

\`\`\`bash
python create_tables.py
\`\`\`

Expected output: a printed list of all six table names (`assessment_eligibility`, `assessment_request`, `assessment`, `question`, `response`, `evaluation`). Verify directly in Postgres if needed:

\`\`\`sql
\dt
\`\`\`

## 6. Run the service

\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

## 7. Verify

Open `http://localhost:8000/docs` — confirm all routers are listed (Eligibility, Assessment Management, Question Generation, Evaluation, Result Management, Take Assessment orchestration).

## Database Schema

### assessment_eligibility
Source of truth for course/module completions reported by Team 3. Insert-only — never updated or deleted.

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | string (PK) | No | |
| user_id | string | No | Indexed. References Team 1's employee identity — not a local FK. |
| employee_name | string | Yes | Optional, for display convenience only. |
| course_id | string | No | Indexed. |
| course_name | string | No | |
| module_id | string | Yes | Informational only — not used in grouping/aggregation. |
| module_name | string | Yes | Informational only. |
| topics | JSONB | No | List of topics covered in this completion event. |
| difficulty | string | No | Defaults to `"medium"` if not provided. |
| completion_date | date | No | |
| created_at | timestamptz | No | Auto-set on insert. |

---

### assessment_request
Created when a user clicks "Take Assessment." Snapshot of course/topic metadata at request time.

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | string (PK) | No | |
| user_id | string | No | Indexed. |
| course_id | string | No | Indexed. |
| course_name | string | No | |
| module_id | string | Yes | |
| module_name | string | Yes | |
| topics | JSONB | No | Aggregated topic set (union or latest, per user's choice at request time). |
| difficulty | string | No | |
| request_timestamp | timestamptz | No | Auto-set on insert. |

---

### assessment
One row per "take" — no retry/attempt tracking; every take is an independent execution.

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | string (PK) | No | |
| request_id | string (FK → assessment_request.id) | No | Indexed. |
| status | string | No | `"In Progress"` / `"Completed"`. Default `"In Progress"`. |
| question_count | integer | No | Always `10`, regardless of any value Team 3 sends. |
| started_at | timestamptz | No | Auto-set on insert. |
| submitted_at | timestamptz | Yes | Set when evaluation completes. |

---

### question
Generated once per assessment via LLM. Not reused across assessments — no question bank.

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | string (PK) | No | |
| assessment_id | string | No | Indexed. **No FK constraint** (known gap — see below). |
| sequence_number | integer | No | Question order, 1–10. |
| question_text | string | No | |
| question_type | string | No | Defaults to `"MCQ"` — not currently distinguished for boolean/multi-select. |
| topic | string | No | One of the topics from the originating request — used to compute weak_topics. |
| options | JSONB | No | Dict with keys `a`–`d` (or `a`/`b` for boolean). |
| correct_answer | JSONB | No | List of correct option keys — always a list, even for single-answer questions. |

---

### response
Bulk-inserted at submit time — all answers for an assessment arrive in one request.

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | string (PK) | No | |
| question_id | string (FK → question.id) | No | Indexed. |
| assessment_id | string (FK → assessment.id) | No | Indexed. Denormalized — also derivable via question_id → question.assessment_id. |
| submitted_answer | JSONB | No | List of selected option keys. |
| answered_at | timestamptz | No | Auto-set on insert. Redundant across all rows in one submission (kept intentionally). |

**Note:** `submitted_answer` correctness is never stored here — computed only once, at evaluation time.

---

### evaluation
One row per completed assessment. Computed once at submit time, never recalculated.

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | string (PK) | No | |
| assessment_id | string | No | Indexed. **No FK constraint** (known gap — see below). |
| score | integer | Yes | Count of correctly answered questions. |
| total_questions | integer | No | |
| pass_fail_status | string | Yes | `"Pass"` / `"Fail"`, based on `PASS_THRESHOLD_PERCENT` (configurable, default 60%). |
| weak_topics | JSONB | Yes | Topics behind incorrectly answered questions. Empty if all correct. |
| feedback | string | Yes | AI-generated, ~150 char max. Best-effort — `null` if generation fails. |
| evaluated_at | timestamptz | No | Auto-set on insert. |

---

### Known Schema Gaps

- **No foreign key constraints** on `question.assessment_id`, `response.assessment_id`, or `evaluation.assessment_id` — only indexed. Referential integrity is not enforced at the database level for these; queries and joins work correctly regardless, but orphaned rows are possible in theory. Left as-is deliberately.
- **No migration tool** — schema changes require manual `ALTER`/drop-recreate. `create_tables.py` only creates tables that don't yet exist; it does not apply changes to existing tables.

## Notes

- Tables are created via `create_tables.py` (`Base.metadata.create_all`) — there is no migration tool in place. Any future schema change to an existing table with real data requires a manual `ALTER` or a drop-and-recreate; there is no automated migration path yet.
- If you change a model's column type on a table that already has data, `create_tables.py` will **not** apply that change automatically — it only creates tables that don't yet exist.
