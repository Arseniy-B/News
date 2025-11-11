from src.domain.exceptions import (
    DomainError,
)
from src.use_cases.exceptions import UserNotFound as UseCasesUserNotFound, FilterNotFound as UseCasesFilterNotFound


class BaseInfrastructureError(DomainError):
    """Base exceptions from infrastructure"""


class ValidationError(BaseInfrastructureError):
    pass




class UserNotFound(BaseInfrastructureError, UseCasesUserNotFound):
    pass

class FilterNotFound(BaseInfrastructureError, UseCasesFilterNotFound):
    pass

class BaseRepoError(DomainError):
    pass


class NewsRepoError(BaseRepoError):
    pass


class FilterSchemaNotFound(NewsRepoError):
    pass


class UserRepoError(BaseRepoError):
    pass


class AuthRepoError(BaseRepoError):
    pass


class TokenError(AuthRepoError):
    pass
