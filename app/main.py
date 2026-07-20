from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.database import engine, Base, SessionLocal
from app.routers import auth, users, projects, tasks
from app.repositories.user_repository import UserRepository
from app.middleware.auth import hash_password


def seed_data():
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        existing = user_repo.get_by_email("test@example.com")
        if not existing:
            password_hash = hash_password("testpassword123")
            user_repo.create(email="test@example.com", password_hash=password_hash)
            print("Seed user created: test@example.com / testpassword123")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_data()
    yield


app = FastAPI(title="Project Management API", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"detail": "A database integrity error occurred. The resource may already exist."},
    )


@app.get("/health")
def health_check():
    return {"status": "healthy"}
