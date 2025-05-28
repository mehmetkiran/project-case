from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.libs.hash import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import LoginRequest, TokenResponse


class AuthService:
    """
    Authentication service to handle user registration and login.

    Methods
    -------
    register_user(user: LoginRequest, session: Session) -> User
        Registers a new user with hashed password, raises HTTPException if email exists.

    login_user(request: LoginRequest, session: Session) -> TokenResponse
        Authenticates user and returns JWT token, raises HTTPException if credentials invalid.
    """

    def register_user(self, user: LoginRequest, session: Session) -> User:
        """
        Register a new user with the provided credentials.

        Parameters
        ----------
        user : LoginRequest
            User credentials including email and password.
        session : Session
            SQLAlchemy database session.

        Returns
        -------
        User
            The created user model instance.

        Raises
        ------
        HTTPException
            If the email is already registered (status code 400).
        """
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

    def login_user(self, request: LoginRequest, session: Session) -> TokenResponse:
        """
        Authenticate a user and create a JWT token if credentials are valid.

        Parameters
        ----------
        request : LoginRequest
            User login request containing email and password.
        session : Session
            SQLAlchemy database session.

        Returns
        -------
        TokenResponse
            Access token to be used for authenticated requests.

        Raises
        ------
        HTTPException
            If email or password is incorrect (status code 401).
        """
        user = session.query(User).filter(User.email == request.email).first()
        if not user or not verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="E-Mail or Password is incorrect.")

        token = create_access_token({"user": str(user.email)})
        return TokenResponse(access_token=token)
