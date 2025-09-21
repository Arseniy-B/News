class DomainError(Exception):
    pass


class ValidationError(Exception):
    def __init__(self, detail):
        self.detail = detail


class NewsClientError(Exception):
    pass


class NewsFetchingError(Exception):
    def __init__(self, detail):
        self.detail = detail
