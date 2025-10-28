from src.domain.port.users import AuthPort


class GmailAdapter(AuthPort):
    def __init__(self):
        ...

    def login(self, user):
        ...

    async def logout(self):
        pass

    async def is_authenticated(self) -> bool:
        ...

    def get_user_id(self) -> int | None:
        pass
