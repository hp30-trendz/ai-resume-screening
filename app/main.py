from fastapi import FastAPI
from app.api.routes import router
from app.db.database import Base, engine

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "AI Resume Screening Service is running"}