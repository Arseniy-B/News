from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from src.domain.entities.user import UserCreate, UserLogin
from src.domain.exceptions import ValidationError
from src.drivers.dependencies.user import get_auth_repo, get_user_repo
from src.use_cases.exceptions import UserNotFound, InvalidCredentials, DublicateEntityError
from src.use_cases.user_auth import login, registration

router = APIRouter(prefix="/user")


@router.post("/sign_up")
async def registration_endpoint(
    user_dict_create: dict[str, Any], user_repo=Depends(get_user_repo)
):
    try:
        user_create = UserCreate(**user_dict_create)
    except ValidationError as e:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        )
    try:
        await registration(user_create=user_create, user_repo=user_repo)
    except UserNotFound:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="something went wrong, try again later"
        )
    except DublicateEntityError as e:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return {"status_code": status.HTTP_200_OK, "detail": "you were registered"}


@router.post("/sign_in")
async def login_endpoint(
    user_dict_login: dict[str, Any],
    user_repo=Depends(get_user_repo),
    auth_repo=Depends(get_auth_repo),
):
    try:
        user_login = UserLogin(**user_dict_login)
    except ValidationError as e:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        )
    try:
        await login(user_login, auth_repo=auth_repo, user_repo=user_repo)
    except InvalidCredentials as e:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        )
    return {"status_code": status.HTTP_200_OK, "detail": "you were logged in"}
