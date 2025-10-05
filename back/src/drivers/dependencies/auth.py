from fastapi import Request, Cookie, Response
from src.adapters.users.users import UserAdapter
from fastapi import Depends
from src.adapters.users.schemas import UserAuthId
from src.adapters.users.users import UserAdapter, AsyncSession
from src.adapters.db.db import db_helper
from src.config import config


async def set_user_jwt(response: Response, auth_id: UserAuthId):
    conf = {
        "httponly": True,
        "secure": True,  # только по HTTPS
        "samesite": "none",  # защита от CSRF
        "max_age": config.auth_jwt.refresh_token_expire_minutes,
    }

    response.set_cookie(key="refresh_token", value=auth_id.refresh_token, **conf)
    response.headers["Authorization"] = f"Bearer {auth_id.access_token}"


async def login_required(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(db_helper.get_session),
):
    user_adapter = UserAdapter(session)
    access_token = request.headers["Authorization"]
    refresh_token = request.cookies.get("refresh_token")

    access_token = access_token.split(" ")
    if access_token[0] != "Bearer":
        raise
    access_token = access_token[1]

    if not access_token or not refresh_token:
        raise

    user_auth_id = UserAuthId(access_token=access_token, refresh_token=refresh_token)

    if not await user_adapter.is_authenticated(user_auth_id):
        auth_id = await user_adapter.refresh_token(refresh_token)
        await set_user_jwt(response, auth_id)

    return user_adapter
