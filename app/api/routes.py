import uuid
import os
from fastapi import APIRouter, UploadFile, File, Form, status, HTTPException
from app.db.database import SessionLocal
from app.db.models import Evaluation
from app.workers.tasks import process_resume

router = APIRouter()

UPLOAD_DIR = "storage/resumes"

@router.post("/upload-resume", status_code=status.HTTP_202_ACCEPTED)
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    evaluation_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{evaluation_id}.pdf")

    # 1. Save file to storage
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 2. Prepare Database Record
    db = SessionLocal()
    try:
        evaluation = Evaluation(
            id=evaluation_id,
            job_description=job_description,
            file_path=file_path,
            status="pending"
        )
        db.add(evaluation)
        db.commit() # Commit first to ensure data exists for the worker
        
        # 3. Trigger Task AFTER successful commit
        process_resume.delay(evaluation_id)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()

    return {
        "evaluation_id": evaluation_id,
        "status": "processing"
    }

@router.get("/result/{evaluation_id}")
def get_result(evaluation_id: str):
    db = SessionLocal()
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    db.close()

    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    return {
        "evaluation_id": evaluation.id,
        "status": evaluation.status,
        "score": evaluation.score,
        "verdict": evaluation.verdict,
        "missing_requirements": evaluation.missing_requirements,
        "justification": evaluation.justification
    }