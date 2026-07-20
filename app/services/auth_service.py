from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.middleware.auth import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, email: str, password: str) -> dict:
        existing = self.user_repository.get_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use",
            )
        password_hash = hash_password(password)
        user = self.user_repository.create(email=email, password_hash=password_hash)
        return {"id": user.id, "email": user.email}

    def login(self, email: str, password: str) -> dict:
        user = self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        token = create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}
