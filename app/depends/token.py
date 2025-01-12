from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader


def get_token_from_header(authorization: str = Security(APIKeyHeader(name="Authorization"))) -> str:
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is missing",
        )
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format. Use 'Bearer <token>'",
        )
    return parts[1]
