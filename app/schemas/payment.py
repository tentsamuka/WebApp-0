from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from app.enums.payment_enum import PaymentStatus
 
class Payment(BaseModel):
    id: int

    order_id: int

    amount: Decimal

    provider: str
    transaction_id: str

    status: PaymentStatus

    created_at: datetime
    confirmed_at: datetime | None