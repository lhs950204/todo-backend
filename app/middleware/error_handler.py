from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.exceptions.db_exception import handle_db_exception


class SQLAlchemyExceptionMiddleware(BaseHTTPMiddleware):
    """SQLAlchemy 예외를 처리하는 미들웨어"""

    async def dispatch(self, request: Request, call_next):
        try:
            # 정상적인 요청 처리
            response = await call_next(request)
            return response
        except Exception as exc:
            http_exc = handle_db_exception(exc)
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"detail": http_exc.detail},
            )
