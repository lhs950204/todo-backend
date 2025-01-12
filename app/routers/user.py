from fastapi import APIRouter

router = APIRouter(prefix="/user")


@router.post("")
async def register_user(email: str, password: str, name: str):
    raise


@router.get("")
async def get_user(user_id: int):
    raise
