from enum import Enum

class OrderStatus(str, Enum):
    PENDING     = "pending"
    PAID        = "paid"
    CANCELLED   = "cancelled"
    EXPIRED     = "expired"

class PaymentStatus(str, Enum):
    PENDING     = "pending"
    PAID        = "paid"
    FAILED      = "failed"
    REFUNDED    = "refunded"

class PaymentProvider(str, Enum):
    PIX = "pix"
    MERCADO_PAGO = "mercado_pago"
    STRIPE = "stripe"