import os
from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.settings import settings
from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.user import User


class File(ModelBase):
    __tablename__ = "file"

    filename: Mapped[str]
    original_filename: Mapped[str]
    file_path: Mapped[str]
    mime_type: Mapped[str]
    size: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="files", lazy="selectin")

    def get_save_path(self) -> str:
        """
        파일의 전체 경로를 반환합니다.
        """
        return os.path.join(settings.MEDIA_ROOT, self.file_path)

    def get_media_url(self) -> str:
        return os.path.join(settings.MEDIA_URL, self.file_path)

    async def save_file(self, content: bytes) -> None:
        """
        파일을 media 폴더에 저장합니다.
        """
        full_path = Path(self.get_save_path())
        full_path.parent.mkdir(parents=True, exist_ok=True)

        full_path.write_bytes(content)

    async def delete_file(self) -> None:
        """
        media 폴더에서 파일을 삭제합니다.
        """
        try:
            full_path = Path(self.get_save_path())
            if full_path.exists():
                full_path.unlink()

            # 빈 디렉토리 정리
            directory = full_path.parent
            if directory.exists() and not any(directory.iterdir()):
                directory.rmdir()
        except Exception as e:
            print(f"파일 삭제 중 오류 발생: {e}")  # 로깅으로 대체하는 것이 좋습니다
