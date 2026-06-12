import sqlalchemy as sa
from sqlalchemy import String, func, Integer, create_engine, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from datetime import datetime
from typing import Dict
from app.core.constants import DATABASE_URL


def db_engine():
    connection_args = {}

    if DATABASE_URL.startswith("sqlite:"):
        connection_args = {"check_same_thread": False}

    return create_engine(
        DATABASE_URL,
        connect_args=connection_args
    )

engine = db_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


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
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )




    


    