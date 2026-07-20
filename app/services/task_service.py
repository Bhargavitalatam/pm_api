from typing import Optional, List

from fastapi import HTTPException, status

from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.models.task import TaskStatus


class TaskService:
    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository):
        self.task_repository = task_repository
        self.project_repository = project_repository

    def _verify_project_ownership(self, project_id: str, user_id: str):
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if project.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        return project

    def _verify_task_ownership(self, task_id: str, user_id: str):
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        project = self.project_repository.get_by_id(task.project_id)
        if not project or project.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        return task

    def create(
        self,
        project_id: str,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.TODO,
        due_date=None,
    ):
        self._verify_project_ownership(project_id, user_id)
        return self.task_repository.create(
            title=title,
            project_id=project_id,
            description=description,
            status=status,
            due_date=due_date,
        )

    def list_by_project(self, project_id: str, user_id: str) -> List:
        self._verify_project_ownership(project_id, user_id)
        return self.task_repository.get_all_by_project(project_id)

    def get_by_id(self, task_id: str, user_id: str):
        return self._verify_task_ownership(task_id, user_id)

    def update(
        self,
        task_id: str,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        due_date=None,
    ):
        task = self._verify_task_ownership(task_id, user_id)
        return self.task_repository.update(task, title=title, description=description, status=status, due_date=due_date)

    def delete(self, task_id: str, user_id: str):
        task = self._verify_task_ownership(task_id, user_id)
        self.task_repository.delete(task)
