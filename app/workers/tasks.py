import json
import re

from app.workers.celery_app import celery
from app.db.database import SessionLocal
from app.db.models import Evaluation
from app.services.resume_parser import extract_text_from_pdf
from app.services.llm_service import evaluate_resume


def load_prompt():
    with open("prompts/evaluation_prompt.md", "r") as f:
        return f.read()


def clean_llm_output(output: str):
    """
    Extract valid JSON from LLM response
    """
    output = output.strip()

    # Extract JSON block using regex
    match = re.search(r"\{.*\}", output, re.DOTALL)

    if match:
        return match.group(0)

    return output


@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def process_resume(self, evaluation_id: str):

    db = SessionLocal()

    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()

    if not evaluation:
        db.close()
        return

    try:
        # 1. Extract resume text
        resume_text = extract_text_from_pdf(evaluation.file_path)

        # 2. Load prompt
        prompt_template = load_prompt()

        prompt = prompt_template.replace("{{job_description}}", evaluation.job_description)
        prompt = prompt.replace("{{resume_text}}", resume_text[:3000])  # limit size

        # 3. Call LLM
        llm_output = evaluate_resume(prompt)

        print("\n=== RAW LLM OUTPUT ===")
        print(llm_output)

        # 4. Clean output
        cleaned_output = clean_llm_output(llm_output)

        print("\n=== CLEANED OUTPUT ===")
        print(cleaned_output)

        # 5. Parse JSON safely
        try:
            result = json.loads(cleaned_output)
        except Exception as e:
            print("JSON PARSE ERROR:", str(e))
            evaluation.status = "failed"
            db.commit()
            db.close()
            return

        # 6. Validate score
        score = result.get("score")

        if not isinstance(score, int) or not (0 <= score <= 100):
            print("INVALID SCORE FROM LLM:", score)
            evaluation.status = "failed"
            db.commit()
            db.close()
            return

        # 7. Save results
        evaluation.score = score
        evaluation.verdict = result.get("verdict")
        evaluation.missing_requirements = str(result.get("missing_requirements"))
        evaluation.justification = result.get("justification")
        evaluation.status = "completed"

        print("\n=== SAVED SUCCESSFULLY ===")

    except Exception as e:
        print("TASK ERROR:", str(e))
        evaluation.status = "failed"

    db.commit()
    db.close()