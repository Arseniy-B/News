from datetime import datetime

from sqlalchemy import JSON, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


class UserModel(Base):
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)


class NewsFilterModel(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("usermodel.id"))
    filter_type: Mapped[str] = mapped_column(nullable=False)
    data: Mapped[dict | None] = mapped_column(JSON)
