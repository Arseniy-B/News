from src.domain.port.users import *
from src.domain.entities.user import User


async def registration(user_create: UserCreate, user_repo: UserRepo) -> UserAuthId:
    if user_create.password1 != user_create.password2:
        raise 
    await user_repo.check_password_strength(user_create.password1)

    user: User = await user_repo.create(user_create)
    return await user_repo.login(user)


async def login(user_login: UserLogin, user_repo: UserRepo) -> UserAuthId:
    user = await user_repo.get(user_login)
    return await user_repo.login(user)    

