import requests
import time

BASE_URL = "http://localhost:8000"

def test_full_flow():
    files = {
        "file": open("sample_resume.pdf", "rb")
    }

    data = {
        "job_description": "Python developer with FastAPI and Docker"
    }

    # Upload
    response = requests.post(f"{BASE_URL}/upload-resume", files=files, data=data)
    assert response.status_code == 202

    evaluation_id = response.json()["evaluation_id"]

    # Wait for processing
    time.sleep(10)

    # Fetch result
    result = requests.get(f"{BASE_URL}/result/{evaluation_id}")
    assert result.status_code == 200

    data = result.json()

    assert data["status"] == "completed"
    assert data["score"] is not None