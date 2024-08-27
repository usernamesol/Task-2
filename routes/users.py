from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserRegister, BaseUser
from dbase.db_conn import get_db
from dbase.db_operations.users import create_user, get_user_from_db
from jwt_auth import create_token


router = APIRouter(tags=["users"])


@router.post("/users/register", status_code=status.HTTP_201_CREATED)
async def users_register(
    user: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    user = await create_user(user, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username, email or phone already registered.",
        )

    response = {
        "Message": "Success",
        "username": user.username,
        "email": user.email,
    }

    return response


@router.post("/users/login", status_code=status.HTTP_200_OK)
async def users_login(
    user: BaseUser,
    db: AsyncSession = Depends(get_db),
):
    user_id = await get_user_from_db(user, db)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong email or password",
        )

    token = create_token({"sub": user.email})
    response = {
        "Message": "Success",
        "Your token": token,
        "Token type": "Bearer",
    }

    return response
