from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import File


async def get_files_from_db(user_id: int, db: AsyncSession):
    stmt = select(File.name).where(File.user_id == user_id)
    files = await db.execute(stmt)
    files = files.fetchall()

    return files
