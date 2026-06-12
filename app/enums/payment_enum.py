from enum import Enum

class PaymentStatus(str, Enum):
    PENDING     = "pending"
    PAID        = "paid"
    FAILED      = "failed"
    REFUNDED    = "refunded"

class PaymentProvider(str, Enum):
    PIX = "pix"
    MERCADO_PAGO = "mercado_pago"
    STRIPE = "stripe"