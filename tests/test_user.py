from fastapi import status

from tests.config import client


def test_registration() -> None:
    register_data = {
        "username": "orneys",
        "email": "qwerty1234@gmail.com",
        "password": "qwerty@12",
        "repeat_password": "qwerty@12",
    }
    response = client.post("/user/registration/", json=register_data)
    assert response.status_code == status.HTTP_200_OK


def test_login() -> None:
    login_data = {
        "email": "qwerty1234@gmail.com",
        "password": "qwerty@12",
    }
    response = client.post("/user/login/", json=login_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('access_token') is not None
