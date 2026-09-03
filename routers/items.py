# routers/items.py —— 接口路由（router 层）：只收请求、调 service、包返回
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.receipt import ReceiptItem, ReceiptUpdate
from models.response import ApiResponse
from services.receipt_service import (
    create_receipt, get_receipt, list_receipts, update_receipt, delete_receipt, receipt_to_dict,
)
from database import get_db
from config import settings

router = APIRouter()


@router.get("/hello")
def hello():
    return ApiResponse(code=0, msg="ok", data={"app_name": settings.app_name, "debug": settings.debug})


@router.post("/echo")
def echo(item: dict):
    return ApiResponse(code=0, msg="ok", data={"you_sent": item})


# ① 新增一条收货单
@router.post("/items")
def create_item(item: ReceiptItem, db: Session = Depends(get_db)):
    db_item = create_receipt(db, item)
    return ApiResponse(code=0, msg="ok", data=receipt_to_dict(db_item))


# ② 查列表（分页 + 供应商筛选 + 日期筛选 + 排序）
@router.get("/items")
def list_items(
    page: int = 1, size: int = 10, supplier: str | None = None,
    date: str | None = None, order_by: str = "created_at", desc: bool = False,
    db: Session = Depends(get_db),
):
    rows, total = list_receipts(db, page, size, supplier, date, order_by, desc)
    return ApiResponse(code=0, msg="ok", data={
        "total": total, "page": page, "size": size,
        "items": [receipt_to_dict(r) for r in rows],
    })


# ③ 查一条（按 id）
@router.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    r = get_receipt(db, item_id)
    if not r:
        raise HTTPException(status_code=404, detail=f"id={item_id} 的收货单不存在")
    return ApiResponse(code=0, msg="ok", data=receipt_to_dict(r))


# ④ 改一条（按 id）
@router.put("/items/{item_id}")
def update_item(item_id: int, data: ReceiptUpdate, db: Session = Depends(get_db)):
    r = update_receipt(db, item_id, data)
    if not r:
        raise HTTPException(status_code=404, detail=f"id={item_id} 的收货单不存在")
    return ApiResponse(code=0, msg="ok", data=receipt_to_dict(r))


# ⑤ 删一条（按 id）
@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    ok = delete_receipt(db, item_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"id={item_id} 的收货单不存在")
    return ApiResponse(code=0, msg="ok", data={"deleted_id": item_id})


@router.get("/boom")
def boom():
    return 1 / 0   # 验证全局兜底网
