from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from models.users import User
from schemas.users import UserRegister


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
        user = User(
            username=user.username,
            password=user.password,
            email=user.email,
            birth_date=user.birth_date,
            phone=user.phone,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        user = None

    return user
