from abc import ABC


class NewsFilter(ABC):
    filter_type: str


class News(ABC):
    pass


class NewsResponse(ABC):
    totalResults: int
