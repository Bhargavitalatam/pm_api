from typing import Optional, List

from fastapi import HTTPException, status

from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def create(self, name: str, description: Optional[str], owner_id: str):
        return self.project_repository.create(name=name, description=description, owner_id=owner_id)

    def list_by_owner(self, owner_id: str) -> List:
        return self.project_repository.get_all_by_owner(owner_id)

    def get_by_id(self, project_id: str, user_id: str):
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if project.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        return project

    def update(self, project_id: str, user_id: str, name: Optional[str] = None, description: Optional[str] = None):
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if project.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        return self.project_repository.update(project, name=name, description=description)

    def delete(self, project_id: str, user_id: str):
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if project.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        self.project_repository.delete(project)
