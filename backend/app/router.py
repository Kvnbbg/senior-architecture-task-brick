"""FastAPI router – thin presentation layer delegating to service."""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.models import Task, TaskCreate, TaskUpdate, TaskStatus
from app.service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_service() -> TaskService:
    # In a real app this would be a singleton or injected via DI container.
    # For this isolated brick we keep it simple and recreate per request (stateless demo).
    return TaskService()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, service: TaskService = Depends(get_service)) -> Task:
    return service.create(data)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: UUID, service: TaskService = Depends(get_service)) -> Task:
    task = service.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=List[Task])
def list_tasks(
    status_filter: Optional[TaskStatus] = None,
    service: TaskService = Depends(get_service),
) -> List[Task]:
    return service.list(status=status_filter)


@router.patch("/{task_id}", response_model=Task)
def update_task(
    task_id: UUID,
    data: TaskUpdate,
    service: TaskService = Depends(get_service),
) -> Task:
    task = service.update(task_id, data)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, service: TaskService = Depends(get_service)) -> None:
    if not service.delete(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
