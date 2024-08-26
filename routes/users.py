from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import users
from dbase.db_conn import get_db
from dbase.db_operations.users import create_user


router = APIRouter(tags=["users"])


@router.post("/users/register", status_code=status.HTTP_201_CREATED)
async def users_register(
    user: users.UserRegister,
    db: AsyncSession = Depends(get_db),
):
    user = await create_user(user, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username, email or phone already registered."
        )

    response = {
        "Message": "Success",
        "username": user.username,
        "email": user.email,
    }

    return response
