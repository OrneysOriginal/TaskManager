from typing import AsyncIterator

from fastapi import status
import pytest_asyncio
import httpx


@pytest_asyncio.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000/") as client:
        yield client


async def test_registration(client: httpx.AsyncClient) -> None:
    register_data = {
        "username": "orneys",
        "email": "qwerty1234@gmail.com",
        "password": "qwerty@12",
        "repeat_password": "qwerty@12",
    }
    response = await client.post("/user/registration/", json=register_data)
    assert response.status_code == status.HTTP_200_OK


async def test_login(client: httpx.AsyncClient) -> None:
    login_data = {
        "email": "qwerty1234@gmail.com",
        "password": "qwerty@12",
    }
    response = await client.post("/user/login/", json=login_data)
    assert response.status_code == status.HTTP_200_OK
