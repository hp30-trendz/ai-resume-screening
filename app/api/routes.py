import uuid
from fastapi import APIRouter, UploadFile, File, Form, status

router = APIRouter()

@router.post("/upload-resume", status_code=status.HTTP_202_ACCEPTED)
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    evaluation_id = str(uuid.uuid4())

    # TEMP: we are not processing yet
    return {
        "evaluation_id": evaluation_id,
        "status": "processing"
    }