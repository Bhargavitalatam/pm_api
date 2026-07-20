from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: Optional[str], owner_id: str) -> Project:
        project = Project(name=name, description=description, owner_id=owner_id)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_all_by_owner(self, owner_id: str) -> List[Project]:
        return self.db.query(Project).filter(Project.owner_id == owner_id).all()

    def get_by_id(self, project_id: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def update(self, project: Project, name: Optional[str] = None, description: Optional[str] = None) -> Project:
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: Project) -> None:
        self.db.delete(project)
        self.db.commit()
