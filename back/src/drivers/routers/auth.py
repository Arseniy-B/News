from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, EmailStr

from src.drivers.dependencies.user import AuthRepoDep, UserRepoDep, EmailAuthRepoDep
from src.infrastructure.exceptions import TokenError
from src.infrastructure.repository.users.schemas import UserCreate
from src.use_cases.exceptions import (
    DublicateEntityError,
    InvalidCredentials,
    UserNotFound,
)
from src.use_cases.user_auth import login, registration
from src.infrastructure.adapters.auth.email_auth.schemas import (
    UserLogin as EmailUserLogin,
)
from src.infrastructure.adapters.auth.self_auth.schemas import UserLogin as UserLogin


class EmailAddress(BaseModel):
    email: EmailStr


router = APIRouter(prefix="/auth")


@router.post("/sign_up")
async def registration_endpoint(user_create: UserCreate, user_repo: UserRepoDep):
    try:
        await registration(user_create=user_create, user_repo=user_repo)
    except (UserNotFound, DublicateEntityError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="something went wrong",
        )
    return {"detail": "you were registered"} 


@router.post("/sign_in")
async def login_by_password_endpoint(
    user_login: UserLogin,
    user_repo: UserRepoDep,
    auth_repo: AuthRepoDep,
):
    try:
        await login(user_login, auth_repo=auth_repo, user_repo=user_repo)
    except InvalidCredentials as e:
        return JSONResponse(
            {"detail": str(e)},
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )
    return {"detail": "you were logged in"}


@router.post("/email/sign_in")
async def login_by_email_endpoint(
    user_repo: UserRepoDep, auth_repo: EmailAuthRepoDep, user_login: EmailUserLogin
):
    await login(user_login, auth_repo, user_repo)
    return {"detail": "you were logged in"}


@router.post("/email/send_otp")
async def seend_top_endpoint(
    email: EmailStr,
    auth_repo: EmailAuthRepoDep,
):
    await auth_repo.send_code(email)
    return {"detail": "a one-time password has been sent"}


@router.post("/logout")
async def logoun_endpoint(auth_repo: AuthRepoDep):
    try:
        await auth_repo.logout()
    except TokenError:
        return JSONResponse(
            {
                "detail": "The token was not transferred. Most likely, you were not logged in"
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return {"detail": "you have logged out of your account"}


@router.post("/token")
async def refresh_token(auth_repo: AuthRepoDep):
    try:
        auth_repo.refresh_token()
    except TokenError:
        return JSONResponse(
            {"detail": "wrong token"}, status_code=status.HTTP_401_UNAUTHORIZED
        )
    return {"detail": "you are authenticated"}
