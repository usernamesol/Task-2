from fastapi import Depends
import jwt
from fastapi.security import OAuth2PasswordBearer
from dbase.db_conf import DBConfig


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_token(data: dict):
    token = jwt.encode(
        payload=data,
        key=DBConfig.SECRET_KEY,
        algorithm=DBConfig.ALGORITHM,
    )

    return token


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            jwt=token,
            key=DBConfig.SECRET_KEY,
            algorithms=[DBConfig.ALGORITHM],
        )
        return payload.get("sub")
    except jwt.InvalidTokenError:
        return None
