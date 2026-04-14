# AI Resume Screening Service

## 🚀 Overview

This project is a production-ready backend service that automatically evaluates resumes against a job description using Large Language Models (LLMs).

It follows an asynchronous architecture using a worker queue and ensures reliable, structured evaluation output.

---

## 🧠 Architecture

FastAPI (API Layer)
→ Redis (Message Broker)
→ Celery Worker (Background Processing)
→ PostgreSQL (Persistent Storage)

---

## ⚙️ Tech Stack

* FastAPI
* Celery
* Redis
* PostgreSQL (Dockerized)
* LLM (Groq API - LLaMA 3.1)
* Docker & Docker Compose

---

## 🔄 Workflow

1. User uploads resume (PDF) + Job Description
2. API returns `evaluation_id` immediately (202 Accepted)
3. Background worker processes resume
4. LLM evaluates and returns structured JSON
5. Results stored in PostgreSQL
6. User fetches results via `/result/{evaluation_id}`

---

## 📦 Features

* Asynchronous processing with Celery
* External prompt management (`prompts/evaluation_prompt.md`)
* Robust JSON parsing and validation
* Dockerized multi-service architecture
* Fault-tolerant LLM handling

---

## 🐳 Setup Instructions

### 1. Clone repository

```bash
git clone <your-repo-link>
cd ai-resume-screening-service
```

---

### 2. Create `.env` file

```env
GROQ_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@db:5432/resume_db
```

---

### 3. Run application

```bash
docker-compose up --build
```

---

### 4. Access API

http://localhost:8000/docs

---

## 🧪 Testing the Flow

1. Upload resume via `/upload-resume`
2. Receive `evaluation_id`
3. Wait a few seconds
4. Fetch result via `/result/{evaluation_id}`

---
---
 ## API Example Response
 {
  "evaluation_id": "066d5ebd-5883-4a86-b2d4-e4a73867d086",
  "status": "completed",
  "score": 82,
  "verdict": "Strong Fit",
  "missing_requirements": "['Oracle Cloud Infrastructure (OCI) experience', 'Ansible or Terraform experience', 'Oracle Database Administration Professional (OCP) certification']",
  "justification": "Candidate has extensive experience in Oracle DBA, strong analytical skills, and good problem-solving skills. However, lacks experience in Oracle Cloud Infrastructure and automation tools like Ansible or Terraform."
}
---
---
## Run Tests

pytest tests/test_integration.py
---

## 🧠 Prompt Engineering

Prompts are stored externally in:

```
prompts/evaluation_prompt.md
```

Key techniques used:

* Strict JSON schema enforcement
* Clear output constraints
* No extra text instructions
* Realistic scoring rules

---

## ⚠️ Error Handling & Resilience

* Handles invalid JSON from LLM
* Retries on transient failures
* Validates output schema before saving
* Prevents system crashes

---

## 🔐 Security

* API keys stored in `.env`
* `.env` excluded via `.gitignore`
* `.env.example` provided

---

## 📈 Future Improvements

* Add authentication
* Improve resume parsing (NER-based)
* Add scoring explainability UI
* Support multiple job roles

---

## 👨‍💻 Author

Harshvardhan Patil
