from fastapi import Header, HTTPException


def get_token_from_header(authorization: str = Header(None)) -> str:
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
