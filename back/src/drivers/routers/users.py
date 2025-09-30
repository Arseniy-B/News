from fastapi import APIRouter, Depends, Response
from src.drivers.dependencies.auth import login_required, set_user_jwt
from src.adapters.users.schemas import UserAuthId
from src.adapters.users.users import *
from src.use_cases.users import registration, login
from src.adapters.db.db import db_helper
from typing import Annotated


router = APIRouter(prefix="/user")
SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]


@router.post("/sign_up")
async def registration_endpoint(user_create: UserCreate, session: SessionDep):
    await registration(
        user_create=user_create, 
        user_repo=UserAdapter(session)
    )
    return {"success", True}


@router.post("/sign_in")
async def login_endpoint(user_login: UserLogin, response: Response, session: SessionDep):
    auth_id = await login(user_login, UserAdapter(session))
    if not isinstance(auth_id, UserAuthId):
        raise 

    await set_user_jwt(response, auth_id)
    return {"success": "True"} 

