from fastapi import FastAPI
from app.api.eligibility_routes import router as eligibility_router
from app.api.question_generation_routes import router as question_generation_router

app = FastAPI(title="Team 4 - Assessment Service")

app.include_router(eligibility_router)
app.include_router(question_generation_router)