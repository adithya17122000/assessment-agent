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
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=assessment_db

AI_API_URL=your_llm_endpoint
AI_API_KEY=your_llm_api_key
MODEL=your_model_name

PASS_THRESHOLD_PERCENT=60
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

## Notes

- Tables are created via `create_tables.py` (`Base.metadata.create_all`) — there is no migration tool in place. Any future schema change to an existing table with real data requires a manual `ALTER` or a drop-and-recreate; there is no automated migration path yet.
- If you change a model's column type on a table that already has data, `create_tables.py` will **not** apply that change automatically — it only creates tables that don't yet exist.
