from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
    UploadFile,
    File,
    BackgroundTasks
)
from sqlalchemy.ext.asyncio import AsyncSession
from dbase.db_conn import get_db
from dbase.db_operations.users import get_user_from_db
from dbase.db_operations.files import (
    get_files_from_db,
    get_file_content,
    save_file,
    save_file_to_db,
)
from jwt_auth import get_user_from_token


router = APIRouter(tags=["files"])


@router.get("/files/all", status_code=status.HTTP_200_OK)
async def files_all(
    user: str = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    user_db = await get_user_from_db(user, db)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user} doesn't registered",
        )

    files = await get_files_from_db(user_db._tuple()[0].id, db)
    if not files:
        return {"Message": "You don't have any files."}

    return {"Files": [row_file[0] for row_file in files]}


@router.post("/files/upload", status_code=201)
async def files_upload(
    background_tasks: BackgroundTasks,
    user: str = Depends(get_user_from_token),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    user_db = await get_user_from_db(user, db)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user} doesn't registered",
        )

    file_name = file.filename
    user_db = user_db._tuple()[0]
    username = user_db.username
    file_db = await save_file_to_db(user_db, file_name, db)

    if not file_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File: {file_name} exist."
        )

    file_content = await get_file_content(file)
    background_tasks.add_task(
        save_file,
        file_name,
        file_content,
        username,
    )

    return {"Message": f"File: {file_name} uploaded sucessfully."}
