from abc import ABC


class DomainError(Exception, ABC):
    """Base domain exception"""


class ValidationError(DomainError):
    """Domain validation exception"""
