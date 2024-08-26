from sqlalchemy.orm import Session
from models.users import User
from schemas.users import UserRegister


def create_user(user: UserRegister, db: Session):
    user = User(
        username=user.username,
        password=user.password,
        email=user.email,
        birth_date=user.birth_date,
        phone=user.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
