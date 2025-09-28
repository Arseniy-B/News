from fastapi import APIRouter, Depends
from src.drivers.dependencies.auth import login_required
from src.adapters.users.schemas import *
from src.adapters.users.users import *
from src.use_cases.users import *
from src.adapters.db.db import db_helper
from typing import Annotated


router = APIRouter(prefix="/user")
SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]


@router.post("/sign_up")
async def registration_endpoint(user_create: UserCreate, user_adapter = Depends(login_required)):
    auth_id = await registration(
        user_create=user_create, 
        user_repo=user_adapter
    )
    return auth_id.__dict__


@router.post("/sign_in")
async def login_endpoint(user_login: UserLogin, user_adapter = Depends(login_required)):
    return await login(user_login, user_adapter)

