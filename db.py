import os

import gridfs
from dotenv import load_dotenv
from pymongo import MongoClient
from sqlmodel import SQLModel, create_engine, Session

from app.models.chat import Base

load_dotenv()

DB_NAME = os.environ.get("POSTGRES_DB", None)
DB_USER = os.environ.get("POSTGRES_USER", None)
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", None)
DB_HOST = os.environ.get("POSTGRES_HOST", None)

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
MONGO_DB_URL = os.environ.get("MONGO_URI", None)

engine = create_engine(DATABASE_URL, echo=True)
client = MongoClient(MONGO_DB_URL)


def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    Base.metadata.create_all(engine)
