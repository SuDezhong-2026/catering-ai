# models/receipt.py —— 收货单的请求/响应模型（model 层，Pydantic）
from pydantic import BaseModel


class ReceiptItem(BaseModel):
    """新增收货单时收的数据"""
    name: str
    qty: float
    unit: str = "份"
    price: float
    supplier: str = ""     # 供应商（可选，默认空）


class ReceiptUpdate(BaseModel):
    """改收货单时收的数据（字段全可选：只传要改的）"""
    name: str | None = None
    qty: float | None = None
    unit: str | None = None
    price: float | None = None
    supplier: str | None = None
