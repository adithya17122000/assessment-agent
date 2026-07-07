User Flow

1. Team 3 sends completion data (Employee ID, Course ID, Course Name, Module Name, Topics, Difficulty, Completion Date) whenever an employee finishes learning content.
2. Employee lands on Team 4's assessment homepage → sees a dropdown of eligible courses/modules.
3. Employee selects a course, clicks Take Assessment.
4. System generates 10 questions (LLM, bulk, structured JSON) and presents them one per page.
5. Employee answers each question, clicks Next after each — no correctness shown to employee at this stage.
6. After the last question, employee clicks Submit.
7. Employee sees final score/pass-fail (feedback text explicitly out of Team 4's scope).
8. Separately, a dashboard team pulls Employee ID, Course ID, Score, Status via a Team 4-exposed read API — no push from Team 4.


Backend Flow

1. Team 3 → Team 4: POST/PATCH API call → insert row into AssessmentEligibility. Additive only, never mutated, one row per completion event.
2. Dropdown load: query all AssessmentEligibility rows for that Employee ID.
3. Take Assessment clicked: topics aggregated (union) across relevant AssessmentEligibility rows for that Employee+Course — aggregation boundary logic is yours to implement, not resolved in this design.
4. New AssessmentRequest row created from aggregated metadata.
5. New Assessment row created, Status = In Progress (unconfirmed enum — flagged, not settled), QuestionCount = 10 (hardcoded, Team 3's input ignored if sent).
6. LLM called once with course/difficulty/topics → returns structured JSON list of 10 questions → parsed directly into 10 Question rows. No raw-response storage, no partial-failure handling per your instruction.
7. Each Next click → one Response row inserted (raw answer only, no correctness computed).
8. Submit clicked → Assessment.Status → Completed → Evaluation triggered: joins all Response rows against Question.CorrectAnswer in one pass → single Evaluation row (Score, TotalQuestions, PassFailStatus).
9. Dashboard team calls Team 4's read API → data assembled from Assessment + Evaluation, no write happens on this path.


Database Flow — What Updates When
| Step                    | Table                   | Action                                                |
| ----------------------- | ----------------------- | ----------------------------------------------------- |
| Team 3 completion event | `AssessmentEligibility` | INSERT (new row, always)                              |
| Homepage load           | —                       | READ only (`AssessmentEligibility`)                   |
| Take Assessment clicked | `AssessmentRequest`     | INSERT                                                |
| Take Assessment clicked | `Assessment`            | INSERT (Status = In Progress)                         |
| LLM returns questions   | `Question`              | INSERT ×10                                            |
| Each Next click         | `Response`              | INSERT ×1                                             |
| Submit clicked          | `Assessment`            | UPDATE (Status → Completed, SubmittedAt set)          |
| Submit clicked          | `Evaluation`            | INSERT (1 row, computed from `Response` + `Question`) |
| Dashboard pull          | —                       | READ only (`Assessment` + `Evaluation`)               |
