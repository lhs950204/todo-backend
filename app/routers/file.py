from fastapi import APIRouter, UploadFile

from app.models.file import File

router = APIRouter(prefix="/files")


@router.post("")
async def upload_file(file: UploadFile, user_id: int):
    file_obj = await File.create_from_upload(file, user_id=user_id)
    return {"url": file_obj.get_media_url()}
