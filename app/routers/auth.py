from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    return auth_service.register(email=user.email, password=user.password)


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    return auth_service.login(email=user.email, password=user.password)
