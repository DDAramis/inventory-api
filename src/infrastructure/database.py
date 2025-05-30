from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_DOCKER = os.getenv("IS_DOCKER", "false").lower() == "true"

if ENVIRONMENT == "development":
    if IS_DOCKER:
        DATABASE_URL = "postgresql://postgres:postgres@db:5432/inventario"
    else:
        DATABASE_URL = os.getenv("DATABASE_URL_LOCAL")
else:
    DATABASE_URL = os.getenv("DATABASE_URL_SUPABASE")

if not DATABASE_URL:
    raise ValueError(
        f"DATABASE_URL for {ENVIRONMENT} not found in environment variables. "
        "Please set DATABASE_URL_LOCAL or DATABASE_URL_SUPABASE in the .env file."
    )
print(f"Using database URL: {DATABASE_URL}")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()