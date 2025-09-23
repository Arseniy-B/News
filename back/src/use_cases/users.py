from src.domain.port.users import *
from src.domain.entities.user import User


async def registration(user_create: UserCreate, user_repo: UserRepo) -> UserAuthId:
    user: User = await user_repo.create(user_create)
    return await user_repo.login(user)


async def login(user_login: UserLogin, user_repo: UserRepo) -> UserAuthId:
    return await user_repo.login(user_login)    

