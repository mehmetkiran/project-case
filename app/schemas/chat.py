from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class MessageDirection(str, Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"


class ChatHistoryBase(BaseModel):
    created_at: Optional[datetime] = None
    pdf_hash: Optional[str] = None
    message: Optional[str] = None
    direction: MessageDirection

    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    id: int
    message: str
    direction: MessageDirection
    created_at: datetime
    pdf_hash: Optional[str] = None