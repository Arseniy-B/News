from sqlalchemy.orm import Mapped, mapped_column, declared_attr, DeclarativeBase
from src.config import config
from src.adapters.db.db import db_helper


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


class Users(Base):
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str]
    password: Mapped[str] = mapped_column(nullable=False)

