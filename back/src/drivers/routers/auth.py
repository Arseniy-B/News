from typing import Any

from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, EmailStr

from src.domain.exceptions import ValidationError
from src.drivers.dependencies.user import AuthRepoDep, UserRepoDep, EmailAuthRepoDep
from src.infrastructure.exceptions import TokenError
from src.infrastructure.repository.users.schemas import UserCreate
from src.use_cases.exceptions import (
    DublicateEntityError,
    InvalidCredentials,
    UserNotFound,
)
from src.use_cases.user_auth import login, registration
from src.infrastructure.adapters.auth.email_auth.schemas import UserLogin as EmailUserLogin
from src.infrastructure.adapters.auth.self_auth.schemas import UserLogin as UserLogin


class EmailAddress(BaseModel):
    email: EmailStr


router = APIRouter(prefix="/auth")


@router.post("/sign_up")
async def registration_endpoint(
    user_create: UserCreate, user_repo: UserRepoDep
):
    # try:
    #     user_create = UserCreate(**user_dict_create)
    # except ValidationError as e:
    #     return HTTPException(
    #         status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    #         detail=str(e),
    #     )
    try:
        await registration(user_create=user_create, user_repo=user_repo)
    except UserNotFound:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="something went wrong, try again later",
        )
    except DublicateEntityError as e:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return {"status_code": status.HTTP_200_OK, "detail": "you were registered"}


@router.post("/password_sign_in")
async def login_by_password_endpoint(
    user_login: UserLogin,
    user_repo: UserRepoDep,
    auth_repo: AuthRepoDep,
):
    # try:
    #     user_login = UserLogin(**user_dict_login)
    # except ValidationError as e:
    #     return HTTPException(
    #         status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    #         detail=str(e),
    #     )
    try:
        await login(user_login, auth_repo=auth_repo, user_repo=user_repo)
    except InvalidCredentials as e:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        )
    return {"status_code": status.HTTP_200_OK, "detail": "you were logged in"}


@router.post("/email/sign_in")
async def login_by_email_endpoint(
    user_repo: UserRepoDep,
    auth_repo: EmailAuthRepoDep,
    user_login: EmailUserLogin
): 
    await login(user_login, auth_repo, user_repo)

@router.post("/email/send_otp")
async def seend_top_endpoint(
    email: EmailStr,
    auth_repo: EmailAuthRepoDep,
):
    await auth_repo.send_code(email)


@router.post("/logout")
async def logoun_endpoint(auth_repo: AuthRepoDep):
    try:
        await auth_repo.logout()
    except TokenError:
        return {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "detail": "The token was not transferred. Most likely, you were not logged in",
        }
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "you have logged out of your account",
    }


@router.post("/token")
async def refresh_token(auth_repo: AuthRepoDep):
    try:
        auth_repo.refresh_token()
    except TokenError:
        return {"status_code": status.HTTP_401_UNAUTHORIZED, "detail": "wrong token"}
    return {"status_code": status.HTTP_200_OK, "detail": "you are authenticated"}
