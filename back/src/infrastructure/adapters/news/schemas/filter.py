from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_serializer, model_validator, ConfigDict

from src.domain.port.news_api import NewsFilters
from src.infrastructure.exceptions import ValidationError


class BaseFilter(BaseModel, NewsFilters):
    model_config = ConfigDict(use_enum_values=True)

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
    country: CountryCode | None = None 
    category: Category | None = None
    q: str | None = None
    pageSize: int = 20
    page: int = 1

    @model_validator(mode="after")
    def validate_all_fields(self):
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


class EverythingFilters(BaseFilter):
    from_: datetime | None = None
    to: datetime | None = None
    sortBy: SortBy | None = SortBy.PUBLISHED_AT
    language: Language | None = Language.EN
    domains: str
    q: str | None = None
    pageSize: int = 20
    page: int = 1
    model_config = ConfigDict(use_enum_values=True)

    @field_serializer("from_")
    def move_to_from_(self, data: dict[str, str] | None) -> datetime | None:
        if not data:
            return None
        field = None
        try:
            if "from" in data:
                field = datetime.fromtimestamp(int(data["from"]))
        except (KeyError, ValueError) as e:
            raise ValidationError(str(e))
        return field

    @model_validator(mode="after")
    def validate_all_fields(self):
        if self.from_:
            if not isinstance(self.from_, datetime):
                raise ValidationError("wrong type of field from")
        if self.q and len(self.q) > 1000:
            raise ValidationError("search phrase too long")
        if self.pageSize > 100 and self.pageSize < 1:
            raise ValidationError("page size out of range [1, 100]")
        if self.page < 0:
            raise ValidationError("the page number cannot be negative")
        return self

    def get_url_part(self):
        return "everything"
