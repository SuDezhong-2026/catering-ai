# services/receipt_service.py —— 收货单业务逻辑（service 层）
# 这一层只算"业务"，不碰请求/响应/路由
from models.receipt import ReceiptItem


def calc_item_total(item: ReceiptItem) -> float:
    """一行收货单的金额 = 数量 × 单价"""
    return item.qty * item.price


def build_item_result(item: ReceiptItem) -> dict:
    """组装要返回的数据（不含 code/msg，那由 router 层包）"""
    return {"name": item.name, "total": calc_item_total(item)}
