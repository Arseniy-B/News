from fastapi import APIRouter, Depends
from src.drivers.dependencies.auth import login_required
from src.adapters.users.schemas import *
from src.adapters.users.users import *
from src.use_cases.users import *


router = APIRouter(prefix="/user")


@router.post("/sign_up")
async def registration_endpoint(user_create: UserCreate):
    return await registration(
        user_create, 
        user_repo=UserAdapter()
    )


@router.post("/sign_in")
async def login_endpoint(user_login: UserLogin):
    return await login(user_login, UserAdapter())
