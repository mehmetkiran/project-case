from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.libs.hash import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import TokenResponse, LoginRequest, UserResponse
from db import get_session

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register/", response_model=UserResponse)
def create_user(user: LoginRequest, session: Session = Depends(get_session)):
    try:
        hashed_password = hash_password(user.password)
        new_user = User(email=user.email, password=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")


@router.post("/login/", response_model=TokenResponse)
def login(request: LoginRequest, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="E-Mail or Password is incorrect.")

    token = create_access_token({"user": str(user.email)})
    return TokenResponse(access_token=token)
