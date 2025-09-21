from pydantic import BaseModel, model_validator, model_serializer
from enum import Enum

from src.domain.port.news_api import NewsFilter
from src.exceptions import ValidationError


class BaseFilter(BaseModel):
    pass


class CountryCode(Enum):
    US = "us"  # США
    RU = "RU"  # Россия
    CN = "CN"  # Китай
    GB = "GB"  # Великобритания
    DE = "DE"  # Германия
    FR = "FR"  # Франция
    JP = "JP"  # Япония
    IN = "IN"  # Индия
    BR = "BR"  # Бразилия
    CA = "CA"  # Канада
    AU = "AU"  # Австралия
    IT = "IT"  # Италия
    ES = "ES"  # Испания
    KR = "KR"  # Южная Корея
    MX = "MX"  # Мексика

    @classmethod
    def is_valid(cls, code: str) -> bool:
        return code in [item.value for item in cls]


class Category(Enum):
    BUSINESS = "business"
    ENTERTAINMENT = "entertainment"
    GENERAL = "general"
    HEALTH = "health"
    SCIENCE = "science"
    SPORTS = "sports"
    TECHNOLOGY = "technology"


class TopHeadlinesFilter(BaseFilter, NewsFilter):
    country: CountryCode | None = None
    category: Category | None = None
    q: str | None = None
    pageSize: int = 20
    page: int = 1

    class Config:
        use_enum_values = True


    @model_validator(mode='after')
    def validate(self):
        if self.country and not CountryCode.is_valid(str(self.country)):
            raise ValidationError("wrond country code")
        if self.q and len(self.q) > 1000:
            raise ValidationError("search phrase too long")
        if self.pageSize > 100 and self.pageSize < 1:
            raise ValidationError("page size out of range [1, 100]")
        if self.page < 0:
            raise ValidationError("the page number cannot be negative")
        if not any([self.country, self.category, self.q]):
            raise ValidationError(
                """Required parameters are missing, 
                Please set any of the following parameters:
                country, category, q"""
            )
        return self

