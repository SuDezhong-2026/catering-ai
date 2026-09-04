# seed_data.py —— Day15：把真实收货单 JSON 批量导入数据库
import json
from database import SessionLocal
from services.receipt_service import create_receipt
from models.receipt import ReceiptItem

db = SessionLocal()
with open("data/receipts.json", encoding="utf-8") as f:
    records = json.load(f)

count = 0
for r in records:
    item = ReceiptItem(
        name=r["name"], qty=r["qty"], unit=r.get("unit", "份"),
        price=r["price"], supplier=r.get("supplier", ""),
    )
    create_receipt(db, item)   # 复用 service 层，total 自动算
    count += 1

print(f"✅ 导入完成，共 {count} 条")
db.close()
