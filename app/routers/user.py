from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.libs.services.auth import AuthService
from app.schemas.user import TokenResponse, LoginRequest, UserResponse
from db import get_session

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

auth_service = AuthService()

@router.post("/register/", response_model=UserResponse)
def create_user(user: LoginRequest, session: Session = Depends(get_session)):
    return auth_service.register_user(user, session)

@router.post("/login/", response_model=TokenResponse)
def login(request: LoginRequest, session: Session = Depends(get_session)):
    return auth_service.login_user(request, session)