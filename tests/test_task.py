from fastapi import status
from tests.config import client


def test_add_task() -> None:
    task_data = {
        "task_name": "some text",
        "description": "some text",
    }
    response = client.post("task/add_task/", json=task_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_all_task() -> None:
    response = client.get("task/get_all_task/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_del_task() -> None:
    response = client.post("task/del_task/", json={'task_name': 'some name'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
