from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from models.users import User
from schemas.users import UserRegister, BaseUser


async def create_user(user: UserRegister, db: AsyncSession):
    stmt = select(User).where(
        or_(
            User.username == user.username,
            User.email == user.email,
            User.phone == user.phone,
        )
    )
    user_exist = await db.execute(stmt)
    if not user_exist.fetchone():
        user_db = User(
            username=user.username,
            password=user.password,
            email=user.email,
            birth_date=user.birth_date,
            phone=user.phone,
        )  # type: ignore
        db.add(user_db)
        await db.commit()
        await db.refresh(user_db)
    else:
        user_db = None

    return user_db


async def get_user_from_db(user: BaseUser, db: AsyncSession) -> int | None:
    stmt = select(User).where(
        User.email == user.email,
        User.password == user.password,
    )
    user_db = await db.execute(stmt)
    user_db = user_db.first()

    return user_db.tuple()[0].id if user_db else None
