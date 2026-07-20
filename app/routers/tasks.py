from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.middleware.auth import get_current_user
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.services.task_service import TaskService

router = APIRouter(tags=["tasks"])


@router.post("/api/projects/{project_id}/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    project_id: str,
    task: TaskCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    task_service = TaskService(task_repo, project_repo)
    return task_service.create(
        project_id=project_id,
        user_id=user_id,
        title=task.title,
        description=task.description,
        status=task.status,
        due_date=task.due_date,
    )


@router.get("/api/projects/{project_id}/tasks", response_model=List[TaskResponse])
def list_tasks(
    project_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    task_service = TaskService(task_repo, project_repo)
    return task_service.list_by_project(project_id, user_id)


@router.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    task_service = TaskService(task_repo, project_repo)
    return task_service.get_by_id(task_id, user_id)


@router.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task: TaskUpdate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    task_service = TaskService(task_repo, project_repo)
    return task_service.update(
        task_id,
        user_id,
        title=task.title,
        description=task.description,
        status=task.status,
        due_date=task.due_date,
    )


@router.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)
    task_service = TaskService(task_repo, project_repo)
    task_service.delete(task_id, user_id)
