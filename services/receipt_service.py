# services/receipt_service.py —— 收货单业务逻辑（service 层，操作数据库）
from sqlalchemy import func
from models.receipt import ReceiptItem, ReceiptUpdate
from models.receipt_db import ReceiptItemDB
from sqlalchemy.orm import Session


def calc_item_total(qty: float, price: float) -> float:
    """金额 = 数量 × 单价"""
    return qty * price


def receipt_to_dict(r: ReceiptItemDB) -> dict:
    """把数据库里的行转成字典（不含 code/msg，由 router 层包）"""
    return {
        "id": r.id, "name": r.name, "qty": r.qty, "unit": r.unit,
        "price": r.price, "total": r.total, "supplier": r.supplier,
        "created_at": str(r.created_at) if r.created_at else None,
    }


def create_receipt(db: Session, item: ReceiptItem) -> ReceiptItemDB:
    total = calc_item_total(item.qty, item.price)
    db_item = ReceiptItemDB(
        name=item.name, qty=item.qty, unit=item.unit,
        price=item.price, total=total, supplier=item.supplier,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_receipt(db: Session, item_id: int):
    return db.get(ReceiptItemDB, item_id)


def list_receipts(db: Session, page: int = 1, size: int = 10,
                  supplier: str | None = None, date: str | None = None,
                  order_by: str = "created_at", desc: bool = False):
    """查列表，支持分页 / 供应商筛选 / 日期筛选 / 排序"""
    query = db.query(ReceiptItemDB)
    if supplier:
        query = query.filter(ReceiptItemDB.supplier == supplier)
    if date:
        query = query.filter(func.date(ReceiptItemDB.created_at) == date)
    # 排序字段映射（防乱传字段名，默认按入库时间）
    col = {
        "price": ReceiptItemDB.price,
        "name": ReceiptItemDB.name,
        "qty": ReceiptItemDB.qty,
        "created_at": ReceiptItemDB.created_at,
    }.get(order_by, ReceiptItemDB.created_at)
    query = query.order_by(col.desc() if desc else col)
    total = query.count()                              # 总数（分页要用）
    rows = query.offset((page - 1) * size).limit(size).all()   # 分页
    return rows, total


def update_receipt(db: Session, item_id: int, data: ReceiptUpdate):
    db_item = db.get(ReceiptItemDB, item_id)
    if not db_item:
        return None
    changes = data.model_dump(exclude_unset=True)
    if "qty" in changes or "price" in changes:
        qty = changes.get("qty", db_item.qty)
        price = changes.get("price", db_item.price)
        changes["total"] = calc_item_total(qty, price)
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
