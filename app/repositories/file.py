from fastapi import UploadFile

from app.models.file import File
from app.repositories.base import BaseRepository
from app.schema.file import FileCreate


class FileRepository(BaseRepository[File, FileCreate, None]):
    async def create_from_upload(self, upload_file: UploadFile, user_id: int) -> "File":
        """
        UploadFile로부터 File 객체를 생성하고 파일을 저장합니다.
        """
        # 파일 정보 수집
        content = await upload_file.read()
        size = len(content)

        if not upload_file.filename:
            raise ValueError("파일 이름이 없습니다.")

        # 파일명 생성 (날짜_랜덤문자열.확장자)
        filename = f"{upload_file.filename}"

        # 저장 경로 생성 (user_id/filename)
        relative_path = f"{user_id}/{filename}"

        # File 객체 생성
        file_create = FileCreate(
            filename=filename,
            original_filename=upload_file.filename,
            file_path=relative_path,
            mime_type=upload_file.content_type or "application/octet-stream",
            size=size,
            user_id=user_id,
        )

        # 파일 저장
        file = await self.create(file_create)
        await file.save_file(content)
        return file
