"""Minimal unit tests covering the TaskService logic.
100% pass required before any commit.
"""
from uuid import uuid4

import pytest

from app.models import TaskCreate, TaskUpdate, TaskStatus
from app.service import TaskService


@pytest.fixture
def service() -> TaskService:
    s = TaskService()
    s.clear()
    return s


def test_create_and_get(service: TaskService) -> None:
    data = TaskCreate(title="Write senior architecture", description="Demonstrate rigor")
    created = service.create(data)

    assert created.title == "Write senior architecture"
    assert created.status == TaskStatus.TODO
    assert created.id is not None

    fetched = service.get(created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.title == created.title


def test_list_with_filter(service: TaskService) -> None:
    service.create(TaskCreate(title="Todo task", status=TaskStatus.TODO))
    service.create(TaskCreate(title="Done task", status=TaskStatus.DONE))
    service.create(TaskCreate(title="Another todo", status=TaskStatus.TODO))

    all_tasks = service.list()
    assert len(all_tasks) == 3

    todos = service.list(status=TaskStatus.TODO)
    assert len(todos) == 2
    assert all(t.status == TaskStatus.TODO for t in todos)


def test_update(service: TaskService) -> None:
    created = service.create(TaskCreate(title="Original"))
    update = TaskUpdate(title="Updated title", status=TaskStatus.IN_PROGRESS)

    updated = service.update(created.id, update)
    assert updated is not None
    assert updated.title == "Updated title"
    assert updated.status == TaskStatus.IN_PROGRESS
    assert updated.updated_at > created.updated_at


def test_update_not_found(service: TaskService) -> None:
    result = service.update(uuid4(), TaskUpdate(title="Nope"))
    assert result is None


def test_delete(service: TaskService) -> None:
    created = service.create(TaskCreate(title="To delete"))
    assert service.delete(created.id) is True
    assert service.get(created.id) is None
    assert service.delete(created.id) is False


def test_invalid_create_rejected_by_model() -> None:
    with pytest.raises(Exception):  # Pydantic ValidationError
        TaskCreate(title="   ")  # empty after strip
