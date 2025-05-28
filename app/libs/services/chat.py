from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional, Type

from app.models.chat import MessageDirection, ChatHistory


class ChatHistoryService:
    def __init__(self, db_session: Session):
        """
        Service for handling chat history operations in PostgreSQL.
        """
        self.db = db_session

    def save_message(
        self,
        user_id: int,
        message: str,
        direction: MessageDirection,
        pdf_hash: Optional[str] = None
    ) -> ChatHistory:
        """
        Saves a chat message to the database.

        Args:
            user_id (int): ID of the user.
            message (str): Message content.
            direction (MessageDirection): Direction of the message (user/assistant).
            pdf_hash (str, optional): Hash of the associated PDF.

        Returns:
            ChatHistory: The created chat history record.
        """
        chat_entry = ChatHistory(
            user_id=user_id,
            message=message,
            direction=direction,
            pdf_hash=pdf_hash,
            created_at=datetime.utcnow()
        )
        self.db.add(chat_entry)
        self.db.commit()
        self.db.refresh(chat_entry)
        return chat_entry


    def get_conversation(self, user_id: int, pdf_hash: Optional[str] = None, limit: int = 20) -> list[
        Type[ChatHistory]]:
        """
        Returns the last N chat messages for the user.

        Args:
            user_id (int): ID of the user.
            pdf_hash (str, optional): Filter by specific PDF.
            limit (int): Number of messages to return.

        Returns:
            List[ChatHistory]: List of recent chat history records.
        """
        query = self.db.query(ChatHistory).filter(ChatHistory.user_id == user_id)
        if pdf_hash:
            query = query.filter(ChatHistory.pdf_hash == pdf_hash)

        return query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
