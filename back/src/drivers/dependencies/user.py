from fastapi import Depends, Request, Response

from src.infrastructure.adapters.auth.auth import AuthAdapter
from src.infrastructure.adapters.users.users import UserAdapter
from src.infrastructure.services.db.db import AsyncSession, db_helper


async def get_user_repo(session: AsyncSession = Depends(db_helper.get_session)):
    return UserAdapter(session)


async def get_auth_repo(request: Request, response: Response):
    return AuthAdapter(request, response)
