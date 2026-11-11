"""Isolated business logic service for Task management.
No external dependencies – pure domain operations with in-memory storage for testability.
"""
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from app.models import Task, TaskCreate, TaskUpdate, TaskStatus


class TaskService:
    """Senior-level service: single responsibility, immutable where possible, explicit error handling."""

    def __init__(self) -> None:
        self._store: Dict[UUID, Task] = {}

    def create(self, data: TaskCreate) -> Task:
        task = Task(**data.model_dump())
        self._store[task.id] = task
        return task

    def get(self, task_id: UUID) -> Optional[Task]:
        return self._store.get(task_id)

    def list(self, status: Optional[TaskStatus] = None) -> List[Task]:
        tasks = list(self._store.values())
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    def update(self, task_id: UUID, data: TaskUpdate) -> Optional[Task]:
        task = self._store.get(task_id)
        if task is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return task

        updated = task.model_copy(update={**update_data, "updated_at": datetime.utcnow()})
        self._store[task_id] = updated
        return updated

    def delete(self, task_id: UUID) -> bool:
        if task_id in self._store:
            del self._store[task_id]
            return True
        return False

    def clear(self) -> None:
        """Utility for tests only."""
        self._store.clear()
