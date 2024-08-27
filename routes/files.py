from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dbase.db_conn import get_db
from dbase.db_operations.users import get_files_from_db, get_user_from_db
from jwt_auth import get_user_from_token


router = APIRouter(tags=["files"])


@router.get("/files/all", status_code=status.HTTP_200_OK)
async def files_all(
    user: str = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    if not user:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bad token.",
            )
    user_id = await get_user_from_db(user, db)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user} doesn't registered",
        )
    
    files = await get_files_from_db(user_id, db)
    if not files:
        return {"Message": "You don't have any files."}

    return files
