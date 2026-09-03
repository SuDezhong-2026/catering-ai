# models/receipt_db.py —— 收货单的数据库表（ORM 模型）
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base


class ReceiptItemDB(Base):
    __tablename__ = "receipt_items"   # 表名

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)        # 品名
    qty = Column(Float, nullable=False)          # 数量
    unit = Column(String, default="份")           # 单位
    price = Column(Float, nullable=False)        # 单价
    total = Column(Float, nullable=False)        # 金额 = 数量 × 单价
    supplier = Column(String, default="")        # 供应商（Day12 新增）
    created_at = Column(DateTime, default=datetime.now)  # 入库时间（Day12 新增）
