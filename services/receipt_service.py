# services/receipt_service.py —— 收货单业务逻辑（service 层，操作数据库）
from models.receipt import ReceiptItem, ReceiptUpdate
from models.receipt_db import ReceiptItemDB
from sqlalchemy.orm import Session


def calc_item_total(qty: float, price: float) -> float:
    """金额 = 数量 × 单价"""
    return qty * price


def receipt_to_dict(r: ReceiptItemDB) -> dict:
    """把数据库里的行转成字典（不含 code/msg，由 router 层包）"""
    return {"id": r.id, "name": r.name, "qty": r.qty, "unit": r.unit, "price": r.price, "total": r.total}


def create_receipt(db: Session, item: ReceiptItem) -> ReceiptItemDB:
    total = calc_item_total(item.qty, item.price)
    db_item = ReceiptItemDB(name=item.name, qty=item.qty, unit=item.unit, price=item.price, total=total)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_receipt(db: Session, item_id: int):
    return db.get(ReceiptItemDB, item_id)


def list_receipts(db: Session):
    return db.query(ReceiptItemDB).all()


def update_receipt(db: Session, item_id: int, data: ReceiptUpdate):
    db_item = db.get(ReceiptItemDB, item_id)
    if not db_item:
        return None
    changes = data.model_dump(exclude_unset=True)   # 只取"用户传了的"字段
    if "qty" in changes or "price" in changes:
        qty = changes.get("qty", db_item.qty)
        price = changes.get("price", db_item.price)
        changes["total"] = calc_item_total(qty, price)   # 改了数量/单价就重算金额
    for key, value in changes.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_receipt(db: Session, item_id: int) -> bool:
    db_item = db.get(ReceiptItemDB, item_id)
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True
