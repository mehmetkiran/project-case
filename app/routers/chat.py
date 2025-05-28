import logging
from typing import Optional, List

from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session

from app.libs.hash import get_current_user
from app.libs.services.chat import ChatHistoryService
from app.libs.services.gemini import ChatService
from app.models.user import User
from app.routers.pdf import get_pdf_service
from app.schemas.chat import ChatRequest, ChatResponse
from db import get_session

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/pdf-chat/")
def pdf_chat(request: ChatRequest, session: Session = Depends(get_session),
             current_user: User = Depends(get_current_user)):
    chat_service = ChatService(session)
    selected_pdf = get_pdf_service().get_selected_pdf_for_user(int(current_user.id))

    response = chat_service.send_chat(
        user_id=current_user.id,
        current_user_message=request.message,
        pdf_id=selected_pdf["selected_pdf_id"],
    )
    return {"message": response}


@router.get("/chat-history/", response_model=List[ChatResponse])
def chat_history(
        session: Session = Depends(get_session),
        pdf_hash: Optional[str] = Query(None, description="Optional hash of the PDF to filter conversation"),
        limit: Optional[int] = Query(50, ge=1, le=1000, description="Number of latest messages to retrieve"),
        current_user: User = Depends(get_current_user)):
    try:
        chat_service = ChatHistoryService(session)
        history = chat_service.get_conversation(
            user_id=current_user.id,
            pdf_hash=pdf_hash,
            limit=limit
        )
        return history
    except Exception as e:
        logger.exception("Failed to retrieve chat history")
        raise HTTPException(status_code=500, detail="Could not retrieve chat history") from e
