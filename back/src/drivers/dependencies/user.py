from fastapi import Depends, Request, Response
from typing import Annotated

from src.infrastructure.adapters.auth.self_auth.auth import AuthAdapter
from src.infrastructure.adapters.auth.email_auth.auth import EmailAuthAdapter
from src.infrastructure.repository.users.users import UserRepository
from src.infrastructure.services.db.db import AsyncSession, db_helper


async def get_user_repo(
    session: AsyncSession = Depends(db_helper.get_session),
) -> UserRepository:
    user_adapter = UserRepository(session)
    return user_adapter


async def get_auth_repo(request: Request, response: Response) -> AuthAdapter:
    auth_adapter = AuthAdapter(request, response)
    return auth_adapter


async def get_email_auth_repo(request: Request, response: Response) -> EmailAuthAdapter:
    auth_adapter = EmailAuthAdapter(request, response)
    return auth_adapter

EmailAuthRepoDep = Annotated[EmailAuthAdapter, Depends(get_email_auth_repo)]
AuthRepoDep = Annotated[AuthAdapter, Depends(get_auth_repo)]
UserRepoDep = Annotated[UserRepository, Depends(get_user_repo)]
