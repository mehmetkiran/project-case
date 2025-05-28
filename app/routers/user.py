from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.libs.hash import hash_password, verify_password, create_access_token
from app.libs.services.auth import AuthService
from app.models.user import User
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