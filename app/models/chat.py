from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEEnum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy.orm import relationship

from app.models.user import User, Base


class MessageDirection(Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    pdf_hash = Column(String)
    message = Column(String)
    direction = Column(SQLEEnum(MessageDirection), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship(User, back_populates="chat_histories")