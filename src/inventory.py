"""收货单小工具：对一行行物品做聚合汇总（练习类型注解与异常处理）。

后续会接入真实映射表与数据库，这里先用纯函数打底。
"""

from dataclasses import dataclass


@dataclass
class ReceiptItem:
    name: str
    qty: float
    unit: str
    price: float


def summarize_items(items: list[ReceiptItem]) -> dict:
    """汇总收货单明细，返回总金额与各品类数量。

    Args:
        items: 收货单条目列表。

    Returns:
        含 total_amount 与 total_qty 的字典。

    Raises:
        ValueError: 当列表为空或任一价格/数量为负。
    """
    if not items:
        raise ValueError("收货单不能为空")

    total_amount = 0.0
    total_qty = 0.0
    for item in items:
        if item.price < 0 or item.qty < 0:
            raise ValueError(f"条目 {item.name} 的价格或数量不能为负")
        total_amount += item.qty * item.price
        total_qty += item.qty

    return {
        "total_amount": round(total_amount, 2),
        "total_qty": round(total_qty, 2),
        "item_count": len(items),
    }


if __name__ == "__main__":
    sample = [
        ReceiptItem("五花肉", 10.0, "斤", 18.5),
        ReceiptItem("香葱", 2.0, "斤", 6.0),
    ]
    print(summarize_items(sample))
