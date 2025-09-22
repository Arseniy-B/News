from fastapi import APIRouter, Depends
from src.drivers.dependencies.auth import login_required

router = APIRouter(prefix="/user")


@router.post("/sign_up")
async def registration(user_login):
    ...
