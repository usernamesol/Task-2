from fastapi import APIRouter
from schemas import users


router = APIRouter(tags=["users"])


@router.post("/users/register")
async def users_register(user: users.UserRegister):
    return user
