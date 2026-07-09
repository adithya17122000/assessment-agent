from fastapi import FastAPI
from app.api.eligibility_routes import router as eligibility_router
from app.api.assessment_routes import router as assessment_router
from app.api.question_generation_routes import router as question_generation_router
from app.api.orchestration_routes import router as orchestration_router
from app.api.result_routes import router as result_router


app = FastAPI(title="Team 4 - Assessment Service")

app.include_router(eligibility_router)
app.include_router(assessment_router)
app.include_router(question_generation_router)
app.include_router(orchestration_router)
app.include_router(result_router)