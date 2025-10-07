class BaseUseCasesError(Exception):
    pass

class UserNotFound(BaseUseCasesError):
    def __init__(self, user_id: int | None = None):
        super().__init__(f"User {user_id} not found")


class InvalidCredentials(BaseUseCasesError):
    def __str__(self):
        return "incorrect login or password"

class DublicateEntityError(BaseUseCasesError):
    def __init__(self, entity_name: str):
        self.entity_name = entity_name
    def __str__(self):
        return f"the {self.entity_name} already exists"
