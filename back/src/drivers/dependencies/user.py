from fastapi import Depends, Request, Response

from src.infrastructure.adapters.auth.auth import AuthAdapter
from src.infrastructure.adapters.users.users import UserAdapter
from src.infrastructure.services.db.db import AsyncSession, db_helper


async def get_user_repo(session: AsyncSession = Depends(db_helper.get_session)):
    user_adapter = UserAdapter(session)
    return user_adapter


async def get_auth_repo(request: Request, response: Response):
    auth_adapter = AuthAdapter(request, response)
    return auth_adapter
