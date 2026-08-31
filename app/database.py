import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# na fase 2 irei trocar p postgres
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./f1.db")

# sqlite, precisa por causa dos testes/fastapi usando thread
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # os models (Team, Driver, Race, Result) vao herdar daqui


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
