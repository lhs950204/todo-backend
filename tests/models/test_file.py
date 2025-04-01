import os
import pytest
from pathlib import Path
from unittest.mock import Mock

from fastapi import UploadFile

from app.core.settings import settings
from app.models.file import File
from app.models.user import User


@pytest.fixture
def test_user():
    return User(email="test@example.com", hashed_password="hashed", name="Test User")


@pytest.fixture
def test_file(test_user):
    return File(
        filename="test.txt",
        original_filename="original.txt",
        file_path=f"user_{test_user.id}/test.txt",
        mime_type="text/plain",
        size=100,
        user_id=test_user.id,
    )


@pytest.fixture
def temp_upload_file(tmp_path):
    content = b"test content"
    file_path = tmp_path / "test_upload.txt"
    file_path.write_bytes(content)

    async def mock_read(size: int = -1) -> bytes:
        return content

    upload_file = Mock(spec=UploadFile)
    upload_file.filename = "test_upload.txt"
    upload_file.content_type = "text/plain"
    upload_file.read = mock_read
    return upload_file


class TestFile:
    def test_get_full_path(self, test_file):
        full_path = test_file.get_full_path()
        expected_path = str(settings.MEDIA_ROOT / f"user_{test_file.user_id}/test.txt")
        assert full_path == expected_path

    @pytest.mark.asyncio
    async def test_create_from_upload(self, test_user, temp_upload_file):
        # 파일 생성 테스트
        file_obj = await File.create_from_upload(upload_file=temp_upload_file, user_id=test_user.id)

        # 기본 속성 검증
        assert file_obj.original_filename == "test_upload.txt"
        assert file_obj.mime_type == "text/plain"
        assert file_obj.size == len(b"test content")
        assert file_obj.user_id == test_user.id

        # 파일 저장 검증
        saved_path = Path(file_obj.get_save_path())
        assert saved_path.exists()
        assert saved_path.read_bytes() == b"test content"

        # 테스트 후 정리
        if saved_path.exists():
            saved_path.unlink()
            if saved_path.parent.exists():
                saved_path.parent.rmdir()

    @pytest.mark.asyncio
    async def test_save_and_delete_file(self, test_file):
        content = b"test content"

        # 파일 저장 테스트
        await test_file.save_file(content)
        saved_path = Path(test_file.get_full_path())
        assert saved_path.exists()
        assert saved_path.read_bytes() == content

        # 파일 삭제 테스트
        await test_file.delete_file()
        assert not saved_path.exists()
        assert not saved_path.parent.exists()  # 부모 디렉토리도 삭제되었는지 확인
