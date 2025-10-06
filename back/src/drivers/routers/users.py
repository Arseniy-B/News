from fastapi import APIRouter, Depends
from src.domain.entities.user import UserCreate, UserLogin
from src.use_cases.users import login, registration
from src.drivers.dependencies.user import get_user_repo, get_auth_repo

router = APIRouter(prefix="/user")


@router.post("/sign_up")
async def registration_endpoint(
    user_create: UserCreate,
    user_repo = Depends(get_user_repo)
):
    await registration(user_create=user_create, user_repo=user_repo)
    return {"success", True}


@router.post("/sign_in")
async def login_endpoint(
    user_login: UserLogin,
    user_repo = Depends(get_user_repo),
    auth_repo = Depends(get_auth_repo)
):
    await login(user_login, auth_repo=auth_repo, user_repo=user_repo)
    return {"success": "True"}
