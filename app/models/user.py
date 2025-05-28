from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Relationship, Mapped

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String)
    chat_histories: Mapped[List["ChatHistory"]]  = Relationship(back_populates="user")
