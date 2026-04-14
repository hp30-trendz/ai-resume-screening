import uuid
import os
from fastapi import APIRouter, UploadFile, File, Form, status

router = APIRouter()

UPLOAD_DIR = "storage/resumes"

@router.post("/upload-resume", status_code=status.HTTP_202_ACCEPTED)
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    evaluation_id = str(uuid.uuid4())

    # Create file path
    file_path = os.path.join(UPLOAD_DIR, f"{evaluation_id}.pdf")

    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {
        "evaluation_id": evaluation_id,
        "status": "processing"
    }