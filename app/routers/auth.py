from fastapi import APIRouter

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login():
    raise


# @router.post("/tokens")
# async def refresh_token(token: str = Depends(oauth2_scheme)):
#     raise
