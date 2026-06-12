from decimal import Decimal
from sqlalchemy import String, Boolean, Text, Numeric, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base, TimestampMixin, UniqueIdentifierMixin
from app.enums.product_enum import OrderStatus

class Product(Base, UniqueIdentifierMixin, TimestampMixin):
    __tablename__="products"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    version: Mapped[str] = mapped_column(String(20))

    price: Mapped[Decimal] = mapped_column(Numeric)

    image_url: Mapped[str] = mapped_column(String)

    download_url: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(
    String(100),
    unique=True,
    nullable=False
)

    

class Order(Base, UniqueIdentifierMixin, TimestampMixin):
    __tablename__="orders"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    user = relationship("User")
    product = relationship("Product")
    payments = relationship(
        "Payment",
        back_populates="order"
    )

    product_price: Mapped[Decimal] = mapped_column(Numeric)

    status: Mapped[OrderStatus] = mapped_column(SqlEnum(OrderStatus))
