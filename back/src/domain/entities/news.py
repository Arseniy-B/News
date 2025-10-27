from abc import ABC


class NewsFilters(ABC):
    pass


class News(ABC):
    pass

class NewsResponse(ABC):
    totalResults: int
