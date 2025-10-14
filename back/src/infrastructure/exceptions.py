from src.domain.exceptions import (
    DomainError,
)
from src.domain.exceptions import (
    ValidationError as DomainValidationError,
)
from src.use_cases.exceptions import UserNotFound as UseCasesUserNotFound


class BaseInfrastructureError(DomainError):
    """Base exceptions from infrastructure"""


class ValidationError(BaseInfrastructureError, DomainValidationError):
    pass


class UserNotFound(BaseInfrastructureError, UseCasesUserNotFound):
    pass

class BaseRepoError(Exception):
    pass

class NewsRepoError(BaseRepoError):
    pass

class UserRepoError(BaseRepoError):
    pass

class AuthRepoError(BaseRepoError):
    pass
