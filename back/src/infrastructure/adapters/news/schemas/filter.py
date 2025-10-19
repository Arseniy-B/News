from enum import Enum

from pydantic import BaseModel, model_validator

from datetime import datetime
from src.domain.port.news_api import NewsFilter
from src.infrastructure.exceptions import ValidationError


class BaseFilter(BaseModel, NewsFilter):
    class Config:
        use_enum_values = True

    def get_url_part(self) -> str:
        return ""

class Language(Enum):
    AR = "ar"
    DE = "de"
    EN = "en"
    ES = "es"
    FR = "fr"
    HE = "he"
    IT = "it"
    NL = "nl"
    NO = "no"
    PT = "pt"
    RU = "ru"
    SV = "sv"
    UD = "ud"
    SH = "sh"

class CountryCode(Enum):
    US = "US"  # США
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


class TopHeadlinesFilter(BaseFilter):
    country: CountryCode = CountryCode.US
    category: Category | None = None
    q: str | None = None
    pageSize: int = 20
    page: int = 1

    @model_validator(mode="after")
    def vavlidate_all_fields(self):
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

    def get_url_part(self):
        return "top-headlines"

class SortBy(Enum):
    RELEVANCY = "relevancy"
    POPULARITY = "popularity"
    PUBLISHED_AT = "publishedAt"

class Everything(BaseFilter):
    from_: datetime | None = None
    to: datetime | None = None
    sortBy: SortBy = SortBy.PUBLISHED_AT
    language: Language = Language.EN
    q: str | None = None
    pageSize: int = 20
    page: int = 1
    
    def get_url_part(self):
        return "everything"
