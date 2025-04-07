from fastapi import HTTPException


class NotFoundHTTPException(HTTPException):
    def __init__(self, detail: str = "자원을 찾을 수 없습니다"):
        super().__init__(status_code=404, detail=detail)


class ConflictHTTPException(HTTPException):
    def __init__(self, detail: str = "리소스 충돌이 발생했습니다"):
        super().__init__(status_code=409, detail=detail)


class ForbiddenHTTPException(HTTPException):
    def __init__(self, detail: str = "접근 권한이 없습니다"):
        super().__init__(status_code=403, detail=detail)


class UnauthorizedHTTPException(HTTPException):
    def __init__(self, detail: str = "인증이 필요합니다"):
        super().__init__(status_code=401, detail=detail)


class BadRequestHTTPException(HTTPException):
    def __init__(self, detail: str = "잘못된 요청입니다"):
        super().__init__(status_code=400, detail=detail)
