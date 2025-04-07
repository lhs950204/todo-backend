from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def handle_db_exception(exc: Exception) -> HTTPException:
    """데이터베이스 예외를 HTTPException으로 변환합니다."""
    # 고유성 제약 조건 위반 (Unique constraint violation)
    if isinstance(exc, HTTPException):
        return exc
    if isinstance(exc, IntegrityError):
        error_message = str(exc)
        if "unique constraint" in error_message.lower():
            # 구체적인 충돌 유형 파악 (todo_id 등)
            return HTTPException(status_code=409, detail="중복된 데이터가 존재합니다.")
        # 외래 키 제약 조건 위반 (Foreign key constraint violation)
        elif "foreign key constraint" in error_message.lower():
            return HTTPException(status_code=400, detail="관련 데이터가 존재하지 않습니다.")
        return HTTPException(status_code=400, detail=f"데이터 무결성 오류: {error_message}")
    # 일반적인 SQLAlchemy 예외
    elif isinstance(exc, SQLAlchemyError):
        return HTTPException(status_code=500, detail=f"데이터베이스 오류: {str(exc)}")
    # 기타 예외
    else:
        return HTTPException(status_code=500, detail=f"서버 오류: {str(exc)}")
