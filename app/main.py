from fastapi import FastAPI
from app.api.eligibility_routes import router as eligibility_router
from app.api.assessment_routes import router as assessment_router

app = FastAPI(title="Team 4 - Assessment Service")

app.include_router(eligibility_router)
app.include_router(assessment_router)