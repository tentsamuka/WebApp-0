from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Boolean, Text, Numeric, ForeignKey, Integer, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base, TimestampMixin, UniqueIdentifierMixin
from app.core.constants import PaymentStatus, PaymentProvider

class Payment(Base, UniqueIdentifierMixin, TimestampMixin):
    __tablename__="payments"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        unique=True,
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    provider: Mapped[PaymentProvider] = mapped_column(
        SqlEnum(PaymentProvider)
    )

    transaction_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    status: Mapped[PaymentStatus] = mapped_column(
        SqlEnum(PaymentStatus)
    )

    confirmed_at: Mapped[datetime | None] = mapped_column(
        nullable=True
    )

    # Payment
    order = relationship(
        "Order",
        back_populates="payments"
    )