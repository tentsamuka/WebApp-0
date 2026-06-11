from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from app.core.constants import OrderStatus

class Product(BaseModel):
    """Defines Product"""

    id: int # Unique Identifier
    name: str # mod's name
    description: str # mod's description

    version: str # mod's version

    price: Decimal # mod's price

    image_url: str | None # an ilustrational image

    created_at: datetime # when the product was fistly uploaded
    updated_at: datetime # when the product was recently updated

    download_url: str
    slug: str

    active: bool # status

class Order(BaseModel):
    id: int

    user_id: int
    product_id: int

    product_price: Decimal

    status: OrderStatus

    created_at: datetime
    expires_at: datetime | None