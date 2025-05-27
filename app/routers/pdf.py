from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.libs.hash import get_current_user
from db import get_session

router = APIRouter(
    prefix="/pdf",
    tags=["pdf"]
)


@router.post("/pdf-upload/")
def pdf_upload(session: Session = Depends(get_session),
               current_user: str = Depends(get_current_user)):
    pass


@router.get("/pdf-list/")
def pdf_list(session: Session = Depends(get_session),
             current_user: str = Depends(get_current_user)):
    pass


@router.post("/pdf-parse/")
def pdf_parse(session: Session = Depends(get_session),
              current_user: str = Depends(get_current_user)):
    pass


@router.post("/pdf-select/")
def pdf_select(session: Session = Depends(get_session),
               current_user: str = Depends(get_current_user)):
    pass
