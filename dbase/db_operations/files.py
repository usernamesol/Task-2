import os
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dbase.db_conf import DBConfig
from models.users import File, User


async def get_files_from_db(user_id: int, db: AsyncSession):
    stmt = select(File.name).where(File.user_id == user_id)
    files = await db.execute(stmt)
    files = files.fetchall()

    return files


async def get_file_from_db(
    user_id: int,
    file_name: str,
    db: AsyncSession,
):
    stmt = select(File).where(
        File.user_id == user_id,
        File.name == file_name,
    )
    file_db = await db.execute(stmt)
    file_db = file_db.first()

    return file_db


async def save_file_to_db(
    user_db: User,
    file_name: str,
    db: AsyncSession,
):
    file_db = await get_file_from_db(user_db.id, file_name, db)
    if not file_db:
        file_db = File(
            name=file_name,
            user=user_db,
        )
        db.add(file_db)
        await db.commit()
        await db.refresh(file_db)
    else:
        file_db = None

    return file_db


async def get_file_content(file: UploadFile):
    return await file.read()


async def save_file(
    file_name: str,
    file_content: bytes,
    username: str,
):
    path = DBConfig.USER_FILES_PATH + username
    os.makedirs(path, exist_ok=True)
    path = os.path.join(path, file_name)

    with open(path, "wb") as file:
        file.write(file_content)
