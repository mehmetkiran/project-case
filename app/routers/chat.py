from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.libs.hash import hash_password, verify_password, create_access_token, get_current_user
from app.models.chat import ChatHistory
from app.models.user import User
from app.schemas.chat import ChatHistoryBase
from app.schemas.user import TokenResponse, LoginRequest, UserResponse
from db import get_session

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/pdf-chat/")
def pdf_chat(session: Session = Depends(get_session),
             current_user: str = Depends(get_current_user)):
    pass


@router.get("/chat-history/", response_model=ChatHistoryBase)
def chat_history(
        session: Session = Depends(get_session),
        current_user: str = Depends(get_current_user)):
    chat_data = session.query(ChatHistory).filter(ChatHistory.user_id == current_user).first()

    if not chat_data:
        return ChatHistoryBase(messages=[])

    return chat_data
