import sqlalchemy as sa
from sqlalchemy import String, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app.core.config import database_connection

class Base(DeclarativeBase):
    pass

class UniqueIdentifierMixin:
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )
engine = sa.create_engine(database_connection)
con = engine.connect()

