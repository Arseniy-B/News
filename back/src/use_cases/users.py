from src.domain.port.users import UserRepo 


async def registration(user_login, user_repo: UserRepo):
    user = await user_repo.create(user_login)
    return user_repo.login(user)

