from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        title: str,
        project_id: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.TODO,
        due_date=None,
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            status=status,
            due_date=due_date,
            project_id=project_id,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_all_by_project(self, project_id: str) -> List[Task]:
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def get_by_id(self, task_id: str) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def update(
        self,
        task: Task,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        due_date=None,
    ) -> Task:
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if due_date is not None:
            task.due_date = due_date
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
