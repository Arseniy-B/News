class BaseUseCasesError(Exception):
    pass


class UserNotFound(BaseUseCasesError):
    def __init__(self, user_id: int | None = None):
        super().__init__(f"User {user_id} not found")


class UserNotAuthorized(BaseUseCasesError):
    pass


class InvalidCredentials(BaseUseCasesError):
    def __str__(self):
        return "incorrect login or password"


class DublicateEntityError(BaseUseCasesError):
    def __init__(self, entity_name: str):
        self.entity_name = entity_name

    def __str__(self):
        return f"the {self.entity_name} already exists"


class ClienValidationError(BaseUseCasesError):
    """only for errors that are returned to the end user in their pure form"""

    def __init__(self, field: str, value: str | None = None):
        self.field = field
        self.value = value

        msg = f"Invalid {field}"
        if value is not None:
            msg += f": {value}"
        super().__init__(msg)

    def __str__(self):
        return f"{self.field}: {self.value}"
