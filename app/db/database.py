from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL= "postgresql://neondb_owner:npg_eBFb4S3Aokap@ep-curly-art-a9g7pvm7-pooler.gwc.azure.neon.tech/neondb?sslmode=require&channel_binding=require"

# 🔥 Fail fast if missing
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()