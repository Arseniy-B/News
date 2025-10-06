from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsFilter:
    categories: list[str]


@dataclass
class News:
    title: str

