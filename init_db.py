# init_db.py —— Day10 验收：建表 + 插一条示例 + 查出来
from database import engine, Base, SessionLocal
from models.receipt_db import ReceiptItemDB

# 1. 建表（表已存在就跳过，不会报错）
Base.metadata.create_all(bind=engine)
print("✅ 表已建好：", ReceiptItemDB.__tablename__)

# 2. 开会话，插一条（重复跑不会重复插同名示例）
db = SessionLocal()
existing = db.query(ReceiptItemDB).filter(ReceiptItemDB.name == "五花肉").first()
if not existing:
    item = ReceiptItemDB(name="五花肉", qty=10, unit="斤", price=18.5, total=185.0)
    db.add(item)
    db.commit()
    db.refresh(item)
    print(f"✅ 插入成功，新记录 id={item.id}")
else:
    print("ℹ️ 示例数据已存在，跳过插入")

# 3. 查出来
rows = db.query(ReceiptItemDB).all()
print(f"✅ 当前表共有 {len(rows)} 条：")
for r in rows:
    print(f"   id={r.id} 品名={r.name} 数量={r.qty}{r.unit} 单价={r.price} 金额={r.total}")
db.close()
