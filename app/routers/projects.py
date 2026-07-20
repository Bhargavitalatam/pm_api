from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.middleware.auth import get_current_user
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    project: ProjectCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project_repo = ProjectRepository(db)
    project_service = ProjectService(project_repo)
    return project_service.create(name=project.name, description=project.description, owner_id=user_id)


@router.get("", response_model=List[ProjectResponse])
def list_projects(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project_repo = ProjectRepository(db)
    project_service = ProjectService(project_repo)
    return project_service.list_by_owner(user_id)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project_repo = ProjectRepository(db)
    project_service = ProjectService(project_repo)
    return project_service.get_by_id(project_id, user_id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str,
    project: ProjectUpdate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project_repo = ProjectRepository(db)
    project_service = ProjectService(project_repo)
    return project_service.update(
        project_id,
        user_id,
        name=project.name,
        description=project.description,
    )


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project_repo = ProjectRepository(db)
    project_service = ProjectService(project_repo)
    project_service.delete(project_id, user_id)
