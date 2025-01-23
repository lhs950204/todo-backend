import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import UploadFile
from sqlmodel import Field, Relationship

from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.user import User

# 프로젝트 루트 디렉토리의 상위에 media 폴더 생성
MEDIA_ROOT = Path(__file__).parent.parent.parent.parent / "media"
MEDIA_ROOT.mkdir(exist_ok=True)


class File(ModelBase, table=True):
    filename: str = Field(nullable=False)
    original_filename: str = Field(nullable=False)
    file_path: str = Field(nullable=False)  # media 폴더 내의 상대 경로
    mime_type: str = Field(nullable=False)
    size: int = Field(nullable=False)  # 파일 크기 (bytes)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    user: "User" = Relationship(back_populates="files", sa_relationship_kwargs={"lazy": "selectin"})

    def get_full_path(self) -> str:
        """
        파일의 전체 경로를 반환합니다.
        """
        return str(MEDIA_ROOT / self.file_path)

    @classmethod
    async def create_from_upload(cls, upload_file: UploadFile, user_id: int) -> "File":
        """
        UploadFile로부터 File 객체를 생성하고 파일을 저장합니다.
        """
        # 파일 정보 수집
        content = await upload_file.read()
        size = len(content)

        if not upload_file.filename:
            raise ValueError("파일 이름이 없습니다.")

        # 파일명 생성 (날짜_랜덤문자열.확장자)
        ext = os.path.splitext(upload_file.filename)[1]
        filename = f"{datetime.utcnow().strftime('%Y%m%d')}_{os.urandom(8).hex()}{ext}"

        # 저장 경로 생성 (user_id/filename)
        relative_path = f"user_{user_id}/{filename}"

        # File 객체 생성
        file_obj = cls(
            filename=filename,
            original_filename=upload_file.filename,
            file_path=relative_path,
            mime_type=upload_file.content_type or "application/octet-stream",
            size=size,
            user_id=user_id,
        )

        # 파일 저장
        await file_obj.save_file(content)
        return file_obj

    async def save_file(self, content: bytes) -> None:
        """
        파일을 media 폴더에 저장합니다.
        """
        full_path = Path(self.get_full_path())
        full_path.parent.mkdir(parents=True, exist_ok=True)

        full_path.write_bytes(content)

    async def delete_file(self) -> None:
        """
        media 폴더에서 파일을 삭제합니다.
        """
        try:
            full_path = Path(self.get_full_path())
            if full_path.exists():
                full_path.unlink()

            # 빈 디렉토리 정리
            directory = full_path.parent
            if directory.exists() and not any(directory.iterdir()):
                directory.rmdir()
        except Exception as e:
            print(f"파일 삭제 중 오류 발생: {e}")  # 로깅으로 대체하는 것이 좋습니다
