import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_files_all(ac: AsyncClient):
    # Init user to test files.
    response = await ac.post("/users/register", json={
        "username": "usertestfile",
        "password": "usertpasswordfile",
        "email": "testfile@mail.ru",
        "birth_date": "2000-01-01",
        "phone": "38 542 5888 232",
    })
    assert response.status_code == 201

    # Get token.
    response = await ac.post("/users/login", json={
        "email": "testfile@mail.ru",
        "password": "usertpasswordfile",
    })
    assert response.status_code == 200
    token = "Bearer " + response.json()["Your token"]

    response = await ac.get("/files/all", headers={
        "Authorization": token,
    })
    assert response.status_code == 200
    assert response.json() == {"Message": "You don't have any files."}

    bad_token = "Bearer test"
    response = await ac.get("/files/all", headers={
        "Authorization": bad_token
    })
    assert response.status_code == 403
    assert response.json() == {"detail": "Bad token."}
