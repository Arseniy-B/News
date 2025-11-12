from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_serializer, model_validator, ConfigDict, Field

from src.domain.port.news_api import NewsFilter
from src.infrastructure.exceptions import ValidationError
from typing import get_args, Literal


class BaseFilter(BaseModel, NewsFilter):
    model_config = ConfigDict(use_enum_values=True)
    filter_type: str = ""

    def get_url_part(self) -> str:
        return ""

    def model_dump_url(self, *args, **kwargs) -> dict:
        return self.model_dump(*args, **kwargs)


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
    filter_type: str = "TopHeadlines"
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


class SearchIn(Enum):
    TITLE = "title"
    DESCRIPTION = "description"
    CONTENT = "content"


AllSearchIn = list(get_args(SearchIn))


class Domains(Enum):
    BBC = "bbc.co.uk"
    ECHCRUNCH = "echcrunch.com"
    ENGADGET = "engadget.com"


AllDomains = list(get_args(Domains))


class EverythingFilter(BaseFilter):
    filter_type: str = "Everything"
    from_: datetime | None = Field(alias="type", default=None)
    to: datetime | None = None
    sortBy: SortBy = SortBy.PUBLISHED_AT
    language: Language = Language.EN
    domains: list[Domains] = AllDomains
    q: str | None = None
    searchIn: list[SearchIn] = AllSearchIn
    pageSize: int = 20
    page: int = 1
    model_config = ConfigDict(use_enum_values=True)

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

    def model_dump_url(self, *args, **kwargs) -> dict:
        data = self.model_dump(*args, **kwargs)
        data["domains"] = ",".join(data["domains"])
        data["searchIn"] = ",".join(data["searchIn"])
        return data

