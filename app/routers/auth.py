from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login")
async def login():
    raise


@router.post("/tokens")
async def refresh_token(token: str = Depends(oauth2_scheme)):
    raise
