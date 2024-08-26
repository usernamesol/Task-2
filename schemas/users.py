from datetime import date
from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserRegister(BaseUser):
    username: str = Field(min_length=5)
    birth_date: date
    phone: str = Field(pattern=r"[0-9]{3,}")
