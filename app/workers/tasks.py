from app.workers.celery_app import celery
from app.db.database import SessionLocal
from app.db.models import Evaluation

@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def process_resume(self, evaluation_id: str):
    db = SessionLocal()

    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()

    if not evaluation:
        db.close()
        return

    # 🔴 TEMP: fake processing (we will replace with LLM later)
    evaluation.score = 75
    evaluation.verdict = "Moderate Fit"
    evaluation.missing_requirements = "Django experience"
    evaluation.justification = "Candidate has Python but lacks Django"
    evaluation.status = "completed"

    db.commit()
    db.close()