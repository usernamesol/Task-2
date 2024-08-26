from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from schemas.users import UserRegister


async def create_user(user: UserRegister, db: AsyncSession):
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
    return user
