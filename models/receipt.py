# models/receipt.py —— 收货单数据模型（model 层）
from pydantic import BaseModel


class ReceiptItem(BaseModel):
    name: str
    qty: float
    unit: str = "份"
    price: float
