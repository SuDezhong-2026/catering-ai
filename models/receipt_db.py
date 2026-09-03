# models/receipt_db.py —— Day10：收货单的数据库表（ORM 模型）
# 注意：这是"数据库里的表"，和 models/receipt.py（接口收数据的 Pydantic 模型）是两码事
from sqlalchemy import Column, Integer, String, Float
from database import Base


class ReceiptItemDB(Base):
    __tablename__ = "receipt_items"   # 表名

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)   # 品名
    qty = Column(Float, nullable=False)     # 数量
    unit = Column(String, default="份")      # 单位
    price = Column(Float, nullable=False)   # 单价
    total = Column(Float, nullable=False)   # 金额 = 数量 × 单价
