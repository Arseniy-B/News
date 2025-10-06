from src.domain.exceptions import (
    DomainError,
)
from src.domain.exceptions import (
    UserNotFound as DomainUserNotFound,
)
from src.domain.exceptions import (
    ValidationError as DomainValidationError,
)


class BaseInfrastructureError(DomainError):
    """Base exceptions from infrastructure"""


class ValidationError(BaseInfrastructureError, DomainValidationError):
    pass


class UserNotFound(BaseInfrastructureError, DomainUserNotFound):
    pass
