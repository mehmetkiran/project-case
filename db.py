import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

from app.models.chat import Base

load_dotenv()

db_name = os.environ.get("POSTGRES_DB", None)
db_user = os.environ.get("POSTGRES_USER", None)
db_password = os.environ.get("POSTGRES_PASSWORD", None)
db_host = os.environ.get("POSTGRES_HOST", None)

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    Base.metadata.create_all(engine)
