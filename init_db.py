# init_db.py —— Day12 重建：建表 + 插多条带供应商示例 + 查出来
from database import engine, Base, SessionLocal
from models.receipt_db import ReceiptItemDB

Base.metadata.create_all(bind=engine)
print("✅ 表已建好：", ReceiptItemDB.__tablename__)

db = SessionLocal()
if db.query(ReceiptItemDB).count() == 0:
    samples = [
        ReceiptItemDB(name="五花肉", qty=10, unit="斤", price=18.5, total=185.0, supplier="金源"),
        ReceiptItemDB(name="生菜",   qty=5,  unit="斤", price=3.0,  total=15.0,  supplier="金源"),
        ReceiptItemDB(name="基围虾", qty=2,  unit="斤", price=45.0, total=90.0,  supplier="锦绣大地"),
        ReceiptItemDB(name="三文鱼", qty=1,  unit="斤", price=88.0, total=88.0,  supplier="锦绣大地"),
        ReceiptItemDB(name="生抽",   qty=3,  unit="瓶", price=12.0, total=36.0,  supplier="快驴"),
        ReceiptItemDB(name="老抽",   qty=2,  unit="瓶", price=10.0, total=20.0,  supplier="快驴"),
    ]
    db.add_all(samples)
    db.commit()
    print(f"✅ 插入 {len(samples)} 条示例数据")
else:
    print("ℹ️ 已有数据，跳过插入")

rows = db.query(ReceiptItemDB).all()
print(f"✅ 当前表共有 {len(rows)} 条：")
for r in rows:
    print(f"   id={r.id} 品名={r.name} 供应商={r.supplier} 金额={r.total}")
db.close()
