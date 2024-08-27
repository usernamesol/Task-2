import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_users_register(ac: AsyncClient):
    # Correct data.
    response = await ac.post("/users/register", json={
        "username": "usertest",
        "password": "usertpassword",
        "email": "test@mail.ru",
        "birth_date": "2000-01-01",
        "phone": "777"
    })
    assert response.status_code == 201
    assert response.json() == {
        "Message": "Success",
        "username": "usertest",
        "email": "test@mail.ru",
    }

    # The same data.
    response = await ac.post("/users/register", json={
        "username": "usertest",
        "password": "usertpassword",
        "email": "test@mail.ru",
        "birth_date": "2000-01-01",
        "phone": "777"
    })
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Username, email or phone already registered."
    }


@pytest.mark.asyncio
async def test_users_login(ac: AsyncClient):
    response = await ac.post("/users/login", json={
        "email": "test@mail.ru",
        "password": "usertpassword",
    })
    assert response.status_code == 200

    response = await ac.post("/users/login", json={
        "email": "bad@mail.ru",
        "password": "fakepassword",
    })
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Wrong email or password"
    }
