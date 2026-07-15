from fastapi import FastAPI
from app.api.eligibility_routes import router as eligibility_router
from app.api.assessment_routes import router as assessment_router
from app.api.question_generation_routes import router as question_generation_router
from app.api.orchestration_routes import router as orchestration_router
from app.api.result_routes import router as result_router
from app.api.evaluation_routes import router as evaluation_router


app = FastAPI(title="Team 4 - Assessment Service", debug=True)

@app.get("/")
def root():
    return {
        "service": "Team 4 - AI Assessment & Quiz Service",
        "description": "Handles assessment eligibility, AI-driven question generation, evaluation, and results for the learning platform.",
        "docs": "/docs",
    }

app.include_router(eligibility_router, prefix="/assessment")
app.include_router(assessment_router, prefix="/assessment")
app.include_router(question_generation_router, prefix="/assessment")
app.include_router(orchestration_router, prefix="/assessment")
app.include_router(result_router, prefix="/assessment")
app.include_router(evaluation_router, prefix="/assessment")
