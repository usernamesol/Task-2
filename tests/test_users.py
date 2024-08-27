from typing import AsyncGenerator
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from models.users import Base
from main import app
from dbase.db_conn import get_db
from dbase.db_conf import DBConfig


def create_drop_table(create: bool = True) -> None:
    db_url = DBConfig.PG_TEST_DB_URL.replace("asyncpg", "psycopg2")
    engine = create_engine(db_url)

    if not create:
        Base.metadata.create_all(engine)
    else:
        Base.metadata.drop_all(engine)


create_drop_table()

async_engine = create_async_engine(
    DBConfig.PG_TEST_DB_URL,
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(async_engine, autoflush=False)


async def override_get_db() -> AsyncGenerator:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        await db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_users_register(anyio_backend):
    base_url = "http://localhost"
    url = "/users/register"
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url=base_url,
    ) as ac:
        json = {
            "username": "test1234",
            "password": "test1234",
            "email": "test@test.com",
            "birth_date": "2000-01-01",
            "phone": "8 993 8123 231"
        }
        response_reg = await ac.post(url, json=json)
        response_rep = await ac.post(url, json=json)

    assert response_reg.status_code == 201
    assert response_reg.json() == {
        "Message": "Success",
        "username": json["username"],
        "email": json["email"],
    }
    assert response_rep.status_code == 400
    assert response_rep.json() == {
        "detail": "Username, email or phone already registered."
    }

    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url=base_url,
    ) as ac:
        json = {
            "username": "sash",  # Must be min 5 chars.
            "password": "test1234",
            "email": "sash@mail.ru",
            "birth_date": "2000-01-01",
            "phone": "777",
        }
        response_bad_username = await ac.post(url, json=json)

        json["username"] = "sasha"
        json["password"] = "11123z"  # Must be min 8 chars.
        response_bad_password = await ac.post(url, json=json)

        json["password"] = "test1234"
        json["email"] = "mailmail.ru"  # Must been separated by '@'.
        response_bad_email = await ac.post(url, json=json)

        json["email"] = "sasha@mail.ru"
        json["birth_date"] = "20000101"  # Must be in format 'Y-M-D'.
        response_bad_birth_date = await ac.post(url, json=json)

        json["birth_date"] = "2000-01-01"
        json["phone"] = "22"  # Must be min 2 digist.
        response_bad_phone = await ac.post(url, json=json)

        json["phone"] = "777"
        response = await ac.post(url, json=json)

    assert response_bad_username.status_code == 422
    assert response_bad_password.status_code == 422
    assert response_bad_email.status_code == 422
    assert response_bad_birth_date.status_code == 422
    assert response_bad_phone.status_code == 422
    assert response.status_code == 201


create_drop_table(create=False)
