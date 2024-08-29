import sys
import pytest
from httpx import AsyncClient
from dbase.db_conf import DBConfig


@pytest.mark.asyncio
async def test_files_upload(ac: AsyncClient):
    global token, file_name

    if sys.platform == "win32":
        file_name = DBConfig.TEST_FILE.split("\\")[-1]
    else:
        file_name = DBConfig.TEST_FILE.split("/")[-1]
    # Init user to test files.
    response = await ac.post(
        url="/users/register",
        json={
            "username": "usertestfile",
            "password": "usertpasswordfile",
            "email": "testfile@mail.ru",
            "birth_date": "2000-01-01",
            "phone": "38 542 5888 232",
        }
    )
    assert response.status_code == 201

    # Get token.
    response = await ac.post("/users/login", json={
        "email": "testfile@mail.ru",
        "password": "usertpasswordfile",
    })
    assert response.status_code == 200
    token = "Bearer " + response.json()["Your token"]

    with open(DBConfig.TEST_FILE, "rb") as file:
        response = await ac.post(
            url="/files/upload",
            headers={"Authorization": token},
            files={"file": file},
        )
    assert response.status_code == 201
    assert response.json() == {
        "Message": f"File: {file_name} uploaded sucessfully."
    }

    # Repeat upload the same file
    with open(DBConfig.TEST_FILE, "rb") as file:
        response = await ac.post(
            url="/files/upload",
            headers={"Authorization": token},
            files={"file": file},
        )
    assert response.status_code == 400
    assert response.json() == {
        "detail": f"File: {file_name} exist."
    }
