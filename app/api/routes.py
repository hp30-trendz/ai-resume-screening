import uuid
import os
from fastapi import APIRouter, UploadFile, File, Form, status, HTTPException
from app.db.database import SessionLocal
from app.db.models import Evaluation

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

    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Save to DB
    db = SessionLocal()

    evaluation = Evaluation(
        id=evaluation_id,
        job_description=job_description,
        file_path=file_path,
        status="pending"
    )

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
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