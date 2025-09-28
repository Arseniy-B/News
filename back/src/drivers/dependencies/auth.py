from fastapi import Request
from src.adapters.users.users import UserAdapter
from fastapi import Depends
from src.adapters.users.schemas import UserAuthId
from src.adapters.users.users import UserAdapter, AsyncSession
from src.adapters.db.db import db_helper


async def login_required(request: Request, session: AsyncSession = Depends(db_helper.get_session)):
    user_adapter = UserAdapter(session)

    user_auth_id = UserAuthId()
    if not await user_adapter.is_authenticated(user_auth_id):
        raise 
    return user_adapter

