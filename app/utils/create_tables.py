# create_tables.py  (place at repo root, outside app/)
from app.config.database import Base, engine

# Import every model so Base.metadata knows about all six tables.
# create_all only creates tables it's seen registered on Base — an unimported model is invisible to it.
from app.eligibility.models import AssessmentEligibility
from app.assessment_management.models import AssessmentRequest, Assessment
from app.question_generation.models import Question
from app.evaluation.models import Response, Evaluation

if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done. Tables created:", list(Base.metadata.tables.keys()))