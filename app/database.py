from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get DATABASE_URL from .env or fallback
DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://postgres:Admin123@localhost:5432/ecommerce_db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI (optional)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
