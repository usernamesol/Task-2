import os
from datetime import datetime
from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
    UploadFile,
    File,
    BackgroundTasks
)
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from dbase.db_conf import DBConfig
from dbase.db_conn import get_db
from dbase.db_operations.users import get_user_from_db
from dbase.db_operations.files import (
    get_files_from_db,
    get_file_from_db,
    delete_file_from_db,
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
    user_db = user_db._tuple()[0]
    files = await get_files_from_db(user_db.id, db)
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
    user_db = user_db._tuple()[0]
    file_name = file.filename
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


@router.get("/files/{file_name}", status_code=status.HTTP_200_OK)
async def files_get_info(
    file_name: str,
    user: str = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    user_db = await get_user_from_db(user, db)
    user_db = user_db._tuple()[0]
    file_db = await get_file_from_db(user_db.id, file_name, db)
    if not file_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File: {file_name} not found.",
        )

    file_path = DBConfig.USER_FILES_PATH + user_db.username
    file_path = os.path.join(file_path, file_name)
    mtime = os.path.getmtime(file_path)
    mtime_readable = datetime.fromtimestamp(mtime)
    file_size_mb = round(os.path.getsize(file_path) / 1024 ** 2, 2)
    response = {
        "file": file_name,
        "last modified": mtime_readable,
        "size": file_size_mb,
    }

    return response


@router.delete("/files/{file_name}", status_code=status.HTTP_200_OK)
async def files_delete(
    file_name: str,
    user: str = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    user_db = await get_user_from_db(user, db)
    user_db = user_db._tuple()[0]
    username = user_db.username
    file_db = await get_file_from_db(user_db.id, file_name, db)
    if not file_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File: {file_name} not found.",
        )

    await delete_file_from_db(file_db._tuple()[0], db)
    file_path = DBConfig.USER_FILES_PATH + username
    file_path = os.path.join(file_path, file_name)
    os.remove(file_path)

    return {"Message": f"File {file_name} has been deleted."}


@router.get("/files/get/{file_name}", status_code=status.HTTP_200_OK)
async def files_upload_to_user(
    file_name: str,
    user: str = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_db),
):
    user_db = await get_user_from_db(user, db)
    user_db = user_db._tuple()[0]
    file_db = await get_file_from_db(user_db.id, file_name, db)
    if not file_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File: {file_name} not found.",
        )

    file_path = DBConfig.USER_FILES_PATH + user_db.username
    file_path = os.path.join(file_path, file_name)

    return FileResponse(file_path)
