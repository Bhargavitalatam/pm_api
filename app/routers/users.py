from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserResponse
from app.middleware.auth import get_current_user
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_me(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.get_profile(user_id)
