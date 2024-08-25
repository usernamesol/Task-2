from pydantic import BaseModel, EmailStr
from datetime import date


class BaseUser(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseUser):
    username: str
    birth_date: date
    phone: str
